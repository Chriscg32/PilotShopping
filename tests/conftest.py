import pytest
import asyncio
import os
import tempfile
import pandas as pd
from unittest.mock import Mock, AsyncMock

@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def sample_data():
    """Sample data for testing"""
    return {
        "customers": [
            {"id": 1, "name": "John Doe", "age": 30, "purchase_amount": 100.0},
            {"id": 2, "name": "Jane Smith", "age": 25, "purchase_amount": 150.0},
            {"id": 3, "name": "Bob Johnson", "age": 35, "purchase_amount": 200.0}
        ]
    }

@pytest.fixture
def sample_csv_file(sample_data):
    """Create a temporary CSV file for testing"""
    df = pd.DataFrame(sample_data["customers"])
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        df.to_csv(f.name, index=False)
        yield f.name
    os.unlink(f.name)

@pytest.fixture
def mock_mqtt_client():
    """Mock MQTT client for testing"""
    mock = Mock()
    mock.publish = AsyncMock()
    mock.subscribe = AsyncMock()
    return mock