import pytest
from pymongo import MongoClient
from src.server import Server
from unittest.mock import patch, MagicMock

"""Unit Tests for server.py and DB actions"""

""" Format for average Unit Test 

def test_view_menu(mock_db):
    mock_menu_collection = MagicMock()
    mock_db.__viewmenu__.return_value = mock_menu_collection

                             #This is the test data that the function will be run on
    mock_menu_collection.find.return_value = [

    ]

    menu = Menu(mock_db)
    result = menu.viewMenu() #function call of the function being tested

                             #this is what the function return based on the test data defined above
    assert result == [

    ]


"""

@patch("server.MongoClient")
def test_init_success(mock_mongo):
    """Unit test to simulate the DB connection"""
    # Mock client instance
    mock_client = MagicMock()
    mock_mongo.return_value = mock_client

    # Mock database
    mock_db = MagicMock()
    mock_client.get_database.return_value = mock_db

    # Simulate successful ping
    mock_db.command.return_value = {"ok": 1}

    # Instantiate class (uses mock instead of real MongoClient)
    obj = FoodDeliveryDB("user123", "pass123")

    # Assertions
    mock_mongo.assert_called_once()  # MongoClient was called
    mock_client.get_database.assert_called_with("user123_project")
    mock_db.command.assert_called_with("ping")

    # Collections assigned correctly
    assert obj._FoodDeliveryDB__user == mock_db["user"]
    assert obj._FoodDeliveryDB__menu == mock_db["menu"]
    assert obj._FoodDeliveryDB__order == mock_db["order"]
  
