from unittest.mock import patch

import pytest
from aiohttp import ClientSession

from judobase.base import BASE_URL, _Base


@pytest.mark.asyncio
async def test_aenter_aexit():
    """Test that the context manager properly creates and closes the session."""

    async with _Base() as client:
        assert isinstance(client._session, ClientSession)
        assert not client._session.closed
    assert client._session.closed

    client = _Base()
    assert not client._session.closed
    await client.close_session()

    async with client:
        assert not client._session.closed
    assert client._session.closed


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "mock_api_response",
    [
        ({"key": "value"}, 200, {"data": "test_response"}),
    ],
    indirect=True
)
async def test_get_json_success(mock_session, mock_api_response):
    """Test _get_json with a successful API response."""

    params, status, mock_response = mock_api_response

    with patch("judobase.base.ClientSession", return_value=mock_session):
        async with _Base() as client:
            result = await client._get_json(params)

            assert result == mock_response
            mock_session.get.assert_called_once_with(
                f"{BASE_URL}get_json",
                timeout=10,
                params=params,
            )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "mock_api_response",
    [
        ({"key": "value"}, 500, {"data": "test_response"}),
    ],
    indirect=True
)
async def test_get_json_failure(mock_session, mock_api_response):
    """Test _get_json with a successful API response."""

    params, status, mock_response = mock_api_response

    with patch("judobase.base.ClientSession", return_value=mock_session):
        async with _Base() as client:
            with pytest.raises(ConnectionError):
                await client._get_json(params)
