import pytest
from unittest.mock import AsyncMock
from aiohttp import ClientSession

@pytest.fixture
def mock_session():
    """Mocks aiohttp.ClientSession."""
    session_mock = AsyncMock(spec=ClientSession)
    session_mock.get = AsyncMock()
    return session_mock

@pytest.fixture
def mock_api_response(mock_session, request):
    """Mocks API response."""

    params, status, mock_response = request.param

    # Mocks .get()
    mock_response_obj = AsyncMock()
    mock_response_obj.status = status
    mock_response_obj.json.return_value = mock_response
    mock_session.get.return_value = mock_response_obj

    return params, status, mock_response
