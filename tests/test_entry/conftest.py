from typing import Literal

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from datetime import datetime, timedelta


def display_strategy(orders, price_movement_option: Literal["below", "above"]):
    # Create a datetime range for the x-axis
    start_time = datetime.strptime("08:00", "%H:%M")
    end_time = datetime.strptime("18:00", "%H:%M")
    line_start_time = datetime.strptime("12:00", "%H:%M")
    line_end_time = end_time
    highest_entry = max(order["price"] for order in orders["entries"])
    lowest_entry = min(order["price"] for order in orders["entries"])
    vertical_range = highest_entry - lowest_entry

    fig, ax = plt.subplots(figsize=(10, 6))

    # Define datetime objects for plotting
    hours = mdates.HourLocator(interval=1)
    h_fmt = mdates.DateFormatter("%H:%M")

    # Set x-axis to represent time from 08:00 to 18:00
    ax.xaxis.set_major_locator(hours)
    ax.xaxis.set_major_formatter(h_fmt)
    plt.xticks(rotation=45)
    ax.set_xlim(start_time, end_time)

    # Simulate price movement from 08:00 to 12:00 with three large movements
    times = [
        start_time + timedelta(hours=i) for i in range(5)
    ]  # Every hour from 08:00 to 12:00
    vertical_movement = vertical_range * 0.8  # 80% of the vertical range
    mid_point = (highest_entry + lowest_entry) / 2

    if price_movement_option == "below":
        starting_point = lowest_entry - 0.1
        prices = [
            starting_point,
            mid_point + vertical_movement / 2,
            mid_point - vertical_movement / 2,
            mid_point + vertical_movement / 2,
            starting_point,
        ]
    elif price_movement_option == "above":
        starting_point = highest_entry + 0.1
        prices = [
            starting_point,
            mid_point - vertical_movement / 2,
            mid_point + vertical_movement / 2,
            mid_point - vertical_movement / 2,
            starting_point,
        ]
    else:
        raise ValueError("Invalid price_movement_option")

    ax.plot(times, prices, label="Price Movement", color="black", marker="o")

    # Define a vertical offset for label placement above the lines
    vertical_offset = (ax.get_ylim()[1] - ax.get_ylim()[0]) * 0.005

    # Set y-axis to have 0.1 increments
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.1))

    # Plot test_entry, take profit, and stop loss lines
    for entry in orders["entries"]:
        ax.hlines(
            entry["price"],
            xmin=line_start_time,
            xmax=line_end_time,
            colors="blue",
            linestyles="dashed",
            label="Entry" if entry == orders["entries"][0] else "",
        )
        ax.text(
            line_start_time,
            entry["price"] + vertical_offset,
            f'test_entry size: {entry["size"]}',
            va="bottom",
            color="blue",
            fontsize=9,
            horizontalalignment="left",
        )

    for tp in orders["take_profits"]:
        ax.hlines(
            tp["price"],
            xmin=line_start_time,
            xmax=line_end_time,
            colors="green",
            linestyles="dashed",
            label="Take Profit" if tp == orders["take_profits"][0] else "",
        )
        ax.text(
            line_start_time,
            tp["price"] + vertical_offset,
            f'tp size: {tp["size"]}',
            va="bottom",
            color="green",
            fontsize=9,
            horizontalalignment="left",
        )

    ax.hlines(
        orders["stop_loss"]["price"],
        xmin=line_start_time,
        xmax=line_end_time,
        colors="red",
        linestyles="dashed",
        label="Stop Loss",
    )
    ax.text(
        line_start_time,
        orders["stop_loss"]["price"] + vertical_offset,
        f'sl size: {orders["stop_loss"]["size"]}',
        va="bottom",
        color="red",
        fontsize=9,
        horizontalalignment="left",
    )

    ax.set_ylim(
        [
            min(
                prices
                + [
                    order["price"]
                    for order in orders["entries"]
                    + orders["take_profits"]
                    + [orders["stop_loss"]]
                ]
            )
            - 0.1,
            max(
                prices
                + [
                    order["price"]
                    for order in orders["entries"]
                    + orders["take_profits"]
                    + [orders["stop_loss"]]
                ]
            )
            + 0.1,
        ]
    )

    ax.set_xlabel("Time (HH:MM)")
    ax.set_ylabel("Price")
    ax.yaxis.tick_right()
    ax.yaxis.set_label_position("right")
    ax.set_title("Strategy Entry, Take Profit, and Stop Loss Points")
    ax.legend()
    ax.grid(True)

    plt.tight_layout()
    plt.show()
