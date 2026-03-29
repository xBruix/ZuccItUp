import sys
from pathlib import Path
import pytest
from unittest.mock import MagicMock, patch

# Add parent directory to Python path so tests can import from 'src'
sys.path.insert(0, str(Path(__file__).parent.parent))

"""Creates a param that can be placed in each unit test function as the mock db"""
@pytest.fixture
def mock_db():
    with patch("server.MongoClient") as mock_mongo:
        mock_client = MagicMock()
        mock_mongo.return_value = mock_client

        mock_db = MagicMock()
        mock_client.get_database.return_value = mock_db

        # Default ping success
        mock_db.command.return_value = {"ok": 1}

        yield mock_db