import pytest

from entry import DynamicGradientEntry, StrategyError
from .conftest import display_strategy

DISPLAY = False


def test_below_lowest_entry_buy():
    # Test Case 1: Current price is below the lowest entry and signal_direction is buy
    strategy = DynamicGradientEntry(total_risk=0.5, order_sizes=[0.5, 0.25, 0.15, 0.10])
    orders = strategy.prepare_orders(
        signal_direction="buy",
        entry_range=[1.0, 1.5],
        take_profit_prices=[1.6, 1.7, 1.8, 1.9],
        stop_loss_price=0.9,
        current_price=0.8,
        balance=100,
        precision=2,
    )
    expected_orders = {
        "entries": [
            {"price": 1.1, "size": 25.0},
            {"price": 1.2, "size": 12.5},
            {"price": 1.3, "size": 7.5},
            {"price": 1.4, "size": 5.0},
        ],
        "take_profits": [
            {"price": 1.6, "size": 25.0},
            {"price": 1.7, "size": 12.5},
            {"price": 1.8, "size": 7.5},
            {"price": 1.9, "size": 5.0},
        ],
        "stop_loss": {"price": 0.9, "size": 50.0},
    }
    if DISPLAY:
        display_strategy(expected_orders, "below")
    assert orders == expected_orders


def test_above_highest_entry_buy():
    # Test Case 2: Current price is above the highest entry and signal_direction is buy
    strategy = DynamicGradientEntry(total_risk=0.5, order_sizes=[0.5, 0.25, 0.15, 0.10])
    orders = strategy.prepare_orders(
        signal_direction="buy",
        entry_range=[1.0, 1.5],
        take_profit_prices=[1.6, 1.7, 1.8, 1.9],
        stop_loss_price=0.9,
        current_price=1.6,
        balance=100,
        precision=2,
    )

    expected_orders = {
        "entries": [
            {"price": 1.4, "size": 25.0},
            {"price": 1.3, "size": 12.5},
            {"price": 1.2, "size": 7.5},
            {"price": 1.1, "size": 5.0},
        ],
        "take_profits": [
            {"price": 1.6, "size": 25.0},
            {"price": 1.7, "size": 12.5},
            {"price": 1.8, "size": 7.5},
            {"price": 1.9, "size": 5.0},
        ],
        "stop_loss": {"price": 0.9, "size": 50.0},
    }
    if DISPLAY:
        display_strategy(expected_orders, "above")
    assert orders == expected_orders


def test_below_lowest_entry_sell():
    # Test Case 3: Current price is below the lowest entry and signal_direction is sell
    strategy = DynamicGradientEntry(total_risk=0.5, order_sizes=[0.5, 0.25, 0.15, 0.10])
    orders = strategy.prepare_orders(
        signal_direction="sell",
        entry_range=[1.0, 1.5],
        take_profit_prices=[0.5, 0.6, 0.7, 0.8],
        stop_loss_price=1.6,
        current_price=0.8,
        balance=100,
        precision=2,
    )

    expected_orders = {
        "entries": [
            {"price": 1.1, "size": 25.0},
            {"price": 1.2, "size": 12.5},
            {"price": 1.3, "size": 7.5},
            {"price": 1.4, "size": 5.0},
        ],
        "take_profits": [
            {"price": 0.8, "size": 25.0},
            {"price": 0.7, "size": 12.5},
            {"price": 0.6, "size": 7.5},
            {"price": 0.5, "size": 5.0},
        ],
        "stop_loss": {"price": 1.6, "size": 50.0},
    }
    if DISPLAY:
        display_strategy(expected_orders, "below")
    assert orders == expected_orders


def test_above_highest_entry_sell():
    # Test Case 4: Current price is above the highest entry and signal_direction is sell
    strategy = DynamicGradientEntry(total_risk=0.5, order_sizes=[0.5, 0.25, 0.15, 0.10])
    orders = strategy.prepare_orders(
        signal_direction="sell",
        entry_range=[1.0, 1.5],
        take_profit_prices=[0.5, 0.6, 0.7, 0.8],
        stop_loss_price=1.6,
        current_price=1.6,
        balance=100,
        precision=2,
    )

    expected_orders = {
        "entries": [
            {"price": 1.4, "size": 25.0},
            {"price": 1.3, "size": 12.5},
            {"price": 1.2, "size": 7.5},
            {"price": 1.1, "size": 5.0},
        ],
        "take_profits": [
            {"price": 0.8, "size": 25.0},
            {"price": 0.7, "size": 12.5},
            {"price": 0.6, "size": 7.5},
            {"price": 0.5, "size": 5.0},
        ],
        "stop_loss": {"price": 1.6, "size": 50.0},
    }
    if DISPLAY:
        display_strategy(expected_orders, "above")
    assert orders == expected_orders


def test_within_entry():
    # Test Case 5: Current price is within the entry range
    strategy = DynamicGradientEntry(total_risk=0.5, order_sizes=[0.5, 0.25, 0.15, 0.10])
    with pytest.raises(StrategyError, match="Current price is within the entry range"):
        strategy.prepare_orders(
            signal_direction="buy",
            entry_range=[1.0, 1.5],
            take_profit_prices=[1.6, 1.7, 1.8, 1.9],
            stop_loss_price=0.9,
            current_price=1.3,
            balance=100,
            precision=2,
        )
