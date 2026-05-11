import pytest
from unittest.mock import AsyncMock, patch
from services.currency_maudan import convert_currency


# Mock rates — we don't want real API calls during tests
MOCK_RATES = {"SAR": 3.75, "EUR": 0.92, "GBP": 0.79}


@pytest.mark.asyncio
async def test_basic_conversion():
    """USD to SAR should multiply by the rate."""
    with patch("services.currency_maudan.get_exchange_rates", new=AsyncMock(return_value=MOCK_RATES)):
        result = await convert_currency("USD", "SAR", 100)
        assert result["converted_amount"] == 375.0
        assert result["rate"] == 3.75


@pytest.mark.asyncio
async def test_same_currency():
    """Converting a currency to itself should return the same amount."""
    result = await convert_currency("USD", "USD", 50)
    assert result["converted_amount"] == 50
    assert result["rate"] == 1.0


@pytest.mark.asyncio
async def test_unsupported_currency():
    """An unsupported currency should raise a ValueError."""
    with patch("services.currency_maudan.get_exchange_rates", new=AsyncMock(return_value=MOCK_RATES)):
        with pytest.raises(ValueError):
            await convert_currency("USD", "XYZ", 100)