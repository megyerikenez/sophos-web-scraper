import pytest
from unittest.mock import patch, MagicMock
from pymongo.errors import ConnectionFailure
from app.mongo_connector import MongoConnector
from app.constants import MONGO_URI_ENV_VAR, DEFAULT_MONGO_URI, DATABASE_NAME, MONGO_TIMEOUT_MS
import os

@patch.dict(os.environ, { "MONGO_URI": "mongodb://localhost:27017/" })
@patch("app.mongo_connector.MongoClient")
def test_connect_success(mock_mongo_client):
    mock_client_instance = MagicMock()
    mock_mongo_client.return_value = mock_client_instance
    mock_client_instance.admin.command.return_value = {"ok": 1}

    connector = MongoConnector()
    connector.connect()

    mock_mongo_client.assert_called_once_with(
        "mongodb://localhost:27017/", serverSelectionTimeoutMS=MONGO_TIMEOUT_MS
    )
    mock_client_instance.admin.command.assert_called_once_with("ping")
    assert connector.db is not None
    assert connector.db == mock_client_instance[DATABASE_NAME]

@patch("app.mongo_connector.MongoClient")
def test_connect_failure(mock_mongo_client):
    mock_client_instance = MagicMock()
    mock_client_instance.admin.command.side_effect = ConnectionFailure("Failed ping")
    mock_mongo_client.return_value = mock_client_instance

    connector = MongoConnector()
    with pytest.raises(ConnectionFailure):
        connector.connect()

@patch("app.mongo_connector.MongoClient")
def test_get_collection_success(mock_mongo_client):
    mock_client_instance = MagicMock()
    mock_db = MagicMock()
    mock_client_instance.__getitem__.return_value = mock_db
    mock_mongo_client.return_value = mock_client_instance
    mock_client_instance.admin.command.return_value = {"ok": 1}

    connector = MongoConnector()
    connector.connect()

    collection_name = "test_collection"
    collection = connector.get_collection(collection_name)
    mock_db.__getitem__.assert_called_once_with(collection_name)
    assert collection == mock_db[collection_name]

def test_get_collection_not_connected():
    connector = MongoConnector()
    with pytest.raises(Exception) as exc_info:
        connector.get_collection("any_collection")
    assert "Database not connected" in str(exc_info.value)
