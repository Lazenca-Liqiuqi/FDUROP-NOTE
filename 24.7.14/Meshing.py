import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import gsw
import xarray as xr
import netCDF4 as nc
from matplotlib.colorbar import ColorbarBase
from matplotlib.colors import Normalize

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
ORACLES = pd.read_csv("ORACLES_data.csv")
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
        ORACLES,
        SEAC4RS,
        SENEX,
    ],
    ignore_index=True,
)
data.loc[data["lon"] < -180, "lon"] = 180 + (180 + data.loc[data["lon"] < -180, "lon"])
data.loc[data["lon"] > 180, "lon"] = data.loc[data["lon"] > 180, "lon"] - 360
data = data[data["mass"] <= data["mass"].quantile(0.95)]

lon_resolution = 2.5
lat_resolution = 2
height_resolution = 500
# 生成经度列表
lon_list = [
    lon_resolution * (i) + lon_resolution / 2
    for i in range(int(-180 // lon_resolution), int(180 // lon_resolution))
]
# 生成纬度列表
lat_list = [
    lat_resolution * i + lat_resolution / 2
    for i in range(int(-90 // lat_resolution), int(90 // lat_resolution))
]
# 生成高度列表
height_list = [height_resolution * i for i in range(0, 35)]

data["lon_bin"] = data["lon"].apply(
    lambda x: lon_list[np.argmin(np.abs(np.array(lon_list) - x))]
)
data["lat_bin"] = data["lat"].apply(
    lambda x: lat_list[np.argmin(np.abs(np.array(lat_list) - x))]
)
data["height_bin"] = (data["alt"] // height_resolution) * height_resolution
grouped = (
    data.groupby(["date", "lon_bin", "lat_bin", "height_bin"])["mass"]
    .mean()
    .reset_index()
)
grouped.to_csv("Meshed_data.csv", index=False)

dates = grouped["date"].unique()

mass_array = np.zeros(
    (
        len(dates),
        len(lon_list),
        len(lat_list),
        len(height_list),
    )
)


for idx, row in grouped.iterrows():
    date_idx = np.where(dates == row["date"])[0][0]
    lon_idx = np.where(np.array(lon_list) == row["lon_bin"])[0][0]
    lat_idx = np.where(np.array(lat_list) == row["lat_bin"])[0][0]
    height_idx = np.where(np.array(height_list) == row["height_bin"])[0]
    height_idx
    mass_array[date_idx, lon_idx, lat_idx, height_idx] = row["mass"]

mass_array_2d = np.zeros(
    (
        len(lon_list),
        len(lat_list),
    )
)

selected_date = dates[0]
for idx, row in grouped.iterrows():
    if row["date"] == selected_date:
        lon_idx = np.where(np.array(lon_list) == row["lon_bin"])[0][0]
        lat_idx = np.where(np.array(lat_list) == row["lat_bin"])[0][0]
        height_idx = np.where(height_list == row["height_bin"])
        mass_array_2d[lon_idx, lat_idx] = max(
            row["mass"], mass_array_2d[lon_idx, lat_idx]
        )


# 绘制格子图
fig, ax = plt.subplots(subplot_kw={"projection": ccrs.PlateCarree()})
ax.add_feature(cfeature.COASTLINE, edgecolor="black", linewidth=0.2)
ax.set_extent([-180, 180, -90, 90], ccrs.PlateCarree())
ax.add_feature(cfeature.LAND, facecolor="white")
ax.add_feature(cfeature.OCEAN, facecolor="aqua")

lon_mesh, lat_mesh = np.meshgrid(lon_list, lat_list)
# 使用 pcolormesh 绘制网格图
c = ax.pcolormesh(
    lon_mesh, lat_mesh, mass_array_2d.T, transform=ccrs.PlateCarree(), cmap="binary"
)
cbar = plt.colorbar(c, fraction=0.046, pad=0.04)
plt.show()
