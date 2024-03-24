from typing import List, Literal, Any, Dict


class StrategyError(Exception):
    """Raised when a strategy cannot be executed."""


class DynamicGradientEntry:
    def __init__(self, total_risk: float = 0.5, order_sizes: List[float] = None):
        """Initializes the Dynamic Gradient Entry Strategy.
        :param total_risk: The total risk percentage.
        :param order_sizes: A list of order sizes as percentages of total risk.
        """
        self.total_risk: float = total_risk
        self.order_sizes: List[float] = order_sizes or [0.5, 0.25, 0.15, 0.10]

    @property
    def num_orders(self) -> int:
        """Calculates the number of orders based on the order sizes.
        :return: The number of orders.
        """
        return len(self.order_sizes)

    def _calculate_entry_points(self, entry_range: List[float]) -> List[float]:
        """Calculates equally spaced entry points within the given entry price range.
        :param entry_range: A list containing two floats, defining the low and high prices of the entry range.
        :return: A list of entry points (floats) equally spaced within the range.
        """
        low, high = sorted(
            entry_range
        )  # Ensure low is the lowest and high is the highest
        step = (high - low) / (self.num_orders + 1)
        return sorted([low + i * step for i in range(1, self.num_orders + 1)])

    def _prepare_buy_below(
        self,
        entries: List[float],
        take_profit_prices: List[float],
        balance: float,
        precision: int,
    ):
        """Prepares the strategy orders for a buy signal below the entry range."""
        entries_info = [
            {"price": round(price, precision), "size": self.total_risk * size * balance}
            for price, size in zip(entries, self.order_sizes)
        ]
        take_profits_info = [
            {"price": round(tp, precision), "size": self.total_risk * size * balance}
            for tp, size in zip(take_profit_prices, self.order_sizes)
        ]
        return entries_info, take_profits_info

    def _prepare_buy_above(
        self,
        entries: List[float],
        take_profit_prices: List[float],
        balance: float,
        precision: int,
    ):
        """Prepares the strategy orders for a buy signal above the entry range."""
        entries_info = [
            {"price": round(price, precision), "size": self.total_risk * size * balance}
            for price, size in zip(reversed(entries), self.order_sizes)
        ]
        take_profits_info = [
            {"price": round(tp, precision), "size": self.total_risk * size * balance}
            for tp, size in zip(take_profit_prices, self.order_sizes)
        ]
        return entries_info, take_profits_info

    def _prepare_sell_below(
        self,
        entries: List[float],
        take_profit_prices: List[float],
        balance: float,
        precision: int,
    ):
        """Prepares the strategy orders for a sell signal below the entry range."""
        entries_info = [
            {"price": round(price, precision), "size": self.total_risk * size * balance}
            for price, size in zip(entries, self.order_sizes)
        ]
        take_profits_info = [
            {"price": round(tp, precision), "size": self.total_risk * size * balance}
            for tp, size in zip(reversed(take_profit_prices), self.order_sizes)
        ]
        return entries_info, take_profits_info

    def _prepare_sell_above(
        self,
        entries: List[float],
        take_profit_prices: List[float],
        balance: float,
        precision: int,
    ):
        """Prepares the strategy orders for a sell signal above the entry range."""
        entries_info = [
            {"price": round(price, precision), "size": self.total_risk * size * balance}
            for price, size in zip(reversed(entries), self.order_sizes)
        ]
        take_profits_info = [
            {"price": round(tp, precision), "size": self.total_risk * size * balance}
            for tp, size in zip(reversed(take_profit_prices), self.order_sizes)
        ]
        return entries_info, take_profits_info

    def prepare_orders(
        self,
        signal_direction: Literal["buy", "sell"],
        entry_range: List[float],
        take_profit_prices: List[float],
        stop_loss_price: float,
        current_price: float,
        balance: float,
        precision: int,
    ) -> Dict[str, Any]:
        """Prepares the strategy orders based on the given parameters.
        :param signal_direction: 'buy' or 'sell'.
        :param entry_range: A list of two floats defining the entry price range.
        :param take_profit_prices: A list of take profit prices as floats.
        :param stop_loss_price: The stop loss price as a float.
        :param current_price: The current market price.
        :param balance: The amount against which to calculate the order sizes. Could be the account balance, or lot size.
        :param precision: The precision to round the order prices to. Hint: int(-math.log10(0.001)) -> 3
        :return: A dictionary containing 'entries', 'take_profits', and 'stop_loss' information.
        :raises StrategyError: If the current price is within the entry range.
        """
        # Calculate entry points within the range
        entries = self._calculate_entry_points(entry_range)

        buy = signal_direction == "buy"
        sell = signal_direction == "sell"

        below = current_price < entry_range[0]
        above = current_price > entry_range[1]

        if buy and below:
            entries_info, take_profits_info = self._prepare_buy_below(
                entries, take_profit_prices, balance, precision
            )
        elif buy and above:
            entries_info, take_profits_info = self._prepare_buy_above(
                entries, take_profit_prices, balance, precision
            )
        elif sell and below:
            entries_info, take_profits_info = self._prepare_sell_below(
                entries, take_profit_prices, balance, precision
            )
        elif sell and above:
            entries_info, take_profits_info = self._prepare_sell_above(
                entries, take_profit_prices, balance, precision
            )
        else:
            msg = (
                "Current price is within the entry range.\nCurrent price: %s\nEntry range: %s"
                % (
                    current_price,
                    entry_range,
                )
            )
            raise StrategyError(msg)

        stop_loss_info = {
            "price": round(stop_loss_price, precision),
            "size": sum(self.order_sizes) * self.total_risk * balance,
        }
        return {
            "entries": entries_info,
            "take_profits": take_profits_info,
            "stop_loss": stop_loss_info,
        }
