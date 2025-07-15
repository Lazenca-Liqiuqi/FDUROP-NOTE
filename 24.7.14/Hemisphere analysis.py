import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import gsw
import xarray as xr
import netCDF4 as nc
import matplotlib.animation as animation
from matplotlib.colorbar import ColorbarBase
from matplotlib.colors import Normalize

# region read
ARCPAC = pd.read_csv("ARCPAC_data.csv")
ARCTAS = pd.read_csv("ARCTAS_data.csv")
ATom_1 = pd.read_csv("ATom-1_data.csv")
ATom_2 = pd.read_csv("ATom-2_data.csv")
ATom_3 = pd.read_csv("ATom-3_data.csv")
ATom_4 = pd.read_csv("ATom-4_data.csv")
CalNex = pd.read_csv("CalNex_data.csv")
DC3 = pd.read_csv("DC3_data.csv")
GOAMAZON = pd.read_csv("GOAMAZON_data.csv")
KORUSAQ = pd.read_csv("KORUS-AQ_data.csv")
SEAC4RS = pd.read_csv("SEAC4RS_data.csv")
SENEX = pd.read_csv("SENEX_data.csv")

data = pd.concat(
    [
        ARCPAC,
        ARCTAS,
        ATom_1,
        ATom_2,
        ATom_3,
        ATom_4,
        CalNex,
        DC3,
        GOAMAZON,
        KORUSAQ,
        SEAC4RS,
        SENEX,
    ],
    ignore_index=True,
)
dataset = {
    "ARCPAC": ARCPAC,
    "ARCTAS": ARCTAS,
    "ATom-1": ATom_1,
    "ATom-2": ATom_2,
    "ATom-3": ATom_3,
    "ATom-4": ATom_4,
    "CalNex": CalNex,
    "DC3": DC3,
    "GOAMAZON": GOAMAZON,
    "KORUSAQ": KORUSAQ,
    "SEAC4RS": SEAC4RS,
    "SENEX": SENEX,
}
# endregion

data = data[data["mass"] <= data["mass"].quantile(0.95)]
south_hemisphere = data[data["lat"] < 0]
north_hemisphere = data[data["lat"] >= 0]

south_hemisphere_daily_avg = south_hemisphere.groupby("date")["mass"].mean()
north_hemisphere_daily_avg = north_hemisphere.groupby("date")["mass"].mean()
south_hemisphere_daily_avg.index = pd.to_datetime(south_hemisphere_daily_avg.index)
north_hemisphere_daily_avg.index = pd.to_datetime(north_hemisphere_daily_avg.index)

# 创建一个完整的日期范围
date_range = pd.date_range(
    start=min(
        south_hemisphere_daily_avg.index.min(), north_hemisphere_daily_avg.index.min()
    ),
    end=max(
        south_hemisphere_daily_avg.index.max(), north_hemisphere_daily_avg.index.max()
    ),
    freq="D",
)

# 将数据重新索引到完整的日期范围，并在缺失的日期插入NaN值
south_hemisphere_daily_avg = south_hemisphere_daily_avg.reindex(date_range).fillna(
    np.nan
)
north_hemisphere_daily_avg = north_hemisphere_daily_avg.reindex(date_range).fillna(
    np.nan
)


plt.figure(figsize=(24, 6), dpi=200)

plt.plot(
    south_hemisphere_daily_avg.index,
    south_hemisphere_daily_avg.values,
    label="South Hemisphere",
    color="blue",
    drawstyle="default",
)
plt.plot(
    north_hemisphere_daily_avg.index,
    north_hemisphere_daily_avg.values,
    label="North Hemisphere",
    color="red",
    drawstyle="default",
)

# 添加四季的半透明色块和注释
seasons = [
    ("Spring", "green", 3, 5),
    ("Summer", "red", 6, 8),
    ("Autumn", "orange", 9, 11),
    ("Winter", "blue", 12, 2),
]

# 创建一个空的图例句柄列表
legend_handles = []

for year in date_range.year.unique():
    year_dates = date_range[date_range.year == year]
    for season, color, start_month, end_month in seasons:
        if start_month <= end_month:
            patch = plt.axvspan(
                year_dates[year_dates.month == start_month].min(),
                year_dates[year_dates.month == end_month].max(),
                color=color,
                alpha=0.2,
            )
        else:
            patch = plt.axvspan(
                year_dates[year_dates.month == start_month].min(),
                year_dates[year_dates.month == 12].max(),
                color=color,
                alpha=0.2,
            )
            plt.axvspan(
                year_dates[year_dates.month == 1].min(),
                year_dates[year_dates.month == end_month].max(),
                color=color,
                alpha=0.2,
            )

        # 添加图例句柄
        if season not in [h.get_label() for h in legend_handles]:
            patch.set_label(season)
            legend_handles.append(patch)

# 添加图例
plt.legend(
    handles=legend_handles, loc="lower center", bbox_to_anchor=(0.5, -0.15), ncol=4
)
plt.xlabel("Date")
plt.ylabel("Average BC Concentration(ng/m3)")
plt.title("Daily Average Pollution Concentration in South and North Hemispheres")
plt.legend()
plt.grid(True)
plt.show()
