import pytest
from fastapi.testclient import TestClient
from datetime import datetime

# Mock app and client
class MockPortfolioItem:
    def __init__(self, symbol, quantity, purchase_price, current_price):
        self.symbol = symbol
        self.quantity = quantity
        self.purchase_price = purchase_price
        self.current_price = current_price

class MockPortfolio:
    def __init__(self, user_id, items):
        self.user_id = user_id
        self.items = items
        self.created_at = datetime.now()

@pytest.fixture
def sample_portfolio():
    items = [
        MockPortfolioItem("AAPL", 10, 150.0, 155.0),
        MockPortfolioItem("GOOGL", 5, 2800.0, 2850.0),
        MockPortfolioItem("MSFT", 8, 300.0, 310.0),
    ]
    return MockPortfolio("user-001", items)

def test_portfolio_creation(sample_portfolio):
    assert sample_portfolio.user_id == "user-001"
    assert len(sample_portfolio.items) == 3
    assert sample_portfolio.items[0].symbol == "AAPL"

def test_portfolio_total_value(sample_portfolio):
    total = sum(item.quantity * item.current_price for item in sample_portfolio.items)
    expected = (10 * 155.0) + (5 * 2850.0) + (8 * 310.0)
    assert total == expected
    assert total == 19280.0

def test_portfolio_gain_loss():
    item = MockPortfolioItem("AAPL", 10, 150.0, 155.0)
    gain = (item.current_price - item.purchase_price) * item.quantity
    assert gain == 50.0

def test_portfolio_gain_loss_negative():
    item = MockPortfolioItem("GOOGL", 5, 2900.0, 2850.0)
    loss = (item.current_price - item.purchase_price) * item.quantity
    assert loss == -250.0

def test_portfolio_item_count(sample_portfolio):
    assert len(sample_portfolio.items) == 3

def test_portfolio_user_id_validation(sample_portfolio):
    assert sample_portfolio.user_id != ""
    assert len(sample_portfolio.user_id) > 0

def test_portfolio_price_validation(sample_portfolio):
    for item in sample_portfolio.items:
        assert item.current_price > 0
        assert item.purchase_price > 0
        assert item.quantity > 0

def test_portfolio_empty():
    empty_portfolio = MockPortfolio("user-002", [])
    assert len(empty_portfolio.items) == 0
    total = sum(item.quantity * item.current_price for item in empty_portfolio.items)
    assert total == 0

def test_portfolio_diversity():
    items = [
        MockPortfolioItem("AAPL", 10, 150.0, 155.0),
        MockPortfolioItem("GOOGL", 5, 2800.0, 2850.0),
        MockPortfolioItem("MSFT", 8, 300.0, 310.0),
    ]
    symbols = [item.symbol for item in items]
    assert len(set(symbols)) == len(symbols)  # All unique
