from matplotlib.axes import Axes
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta


FILE_NAME = "file_size.csv"

# Read data from CSV.
data = pd.read_csv(FILE_NAME).values

# Preprocess: split data and parse dates.
dates = []
count = []
sizes = []
for row in data:
    dates.append(datetime.strptime(row[0], "%Y-%m-%d"))
    count.append(row[1])
    sizes.append(row[2] / 10**9)  # Convert to GiB

# Add forecasting.
dates_forecast = [dates[-1]]
count_forecast = [count[-1]]
sizes_forecast = [sizes[-1]]

forecat_months = 5 * 12  # 5 years
history_months = 6
month_grow_percent = 1.06  # 6% per months


def predict(real_values: list, forecast_values: list):
    history_sum = 0
    if forecast_len := min(history_months, len(forecast_values)):
        history_sum += sum(forecast_values[-forecast_len:])
    if real_len := max(0, history_months - forecast_len):
        history_sum += sum(real_values[-real_len:])
    return (history_sum / history_months) * month_grow_percent


for month in range(forecat_months):
    dates_forecast.append(dates_forecast[-1] + timedelta(days=30))
    count_forecast.append(int(predict(count, count_forecast)))
    sizes_forecast.append(predict(sizes, sizes_forecast))

# Plotting: common.
fig, (plt_count, plt_sizes) = plt.subplots(2, 1, sharex=True)

plt_count.set_title("Count of files")
plt_count.set_ylabel("Count")

plt_sizes.set_title("Total files size")
plt_sizes.set_ylabel("Size (GiB)")

# Plotting: real data.
plt_count.plot(dates, count, label="Read data")
plt_sizes.plot(dates, sizes, label="Read data")

# Plotting: forecast.
plt_count.plot(dates_forecast, count_forecast, "--m", label="Forecasted data")
plt_sizes.plot(dates_forecast, sizes_forecast, "--m", label="Forecasted data")


def print_comment(axe: Axes, real_val: str, forecast_val: str, total_val: str) -> None:
    axe.text(
        0.01,
        0.7,
        f"Real data: {real_val}",
        fontsize=12,
        transform=axe.transAxes,
    )
    axe.text(
        0.01,
        0.6,
        f"Forecast (5 years): {forecast_val}",
        fontsize=12,
        transform=axe.transAxes,
    )
    axe.text(
        0.01,
        0.5,
        f"Real + forecast: {total_val}",
        fontsize=12,
        transform=axe.transAxes,
    )


print_comment(
    plt_count,
    sum(count),
    sum(count_forecast),
    sum(count) + sum(count_forecast),
)

format_sum_result = lambda lst: f"{round((sum(lst)) / 1024.0, 2)} TiB"
print_comment(
    plt_sizes,
    format_sum_result(sizes),
    format_sum_result(sizes_forecast),
    format_sum_result([*sizes, *sizes_forecast]),
)

plt_sizes.legend()
plt_count.legend()

plt.show()
