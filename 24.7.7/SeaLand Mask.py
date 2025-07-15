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
from matplotlib.colors import ListedColormap, BoundaryNorm

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

path = r"D:\Others(English)\Database\FDUROP\woa23_B5C2_t00_04.nc"
ocean_data = xr.open_dataset(path, decode_times=False)
ocean_data = ocean_data.sel(depth=0, method="nearest")
ocean_data = ocean_data.t_an.sel(time=294.0)
lat = ocean_data.lat.values
lon = ocean_data.lon.values
mask = ocean_data.values
mask = np.where(mask > -100, 1, mask)
mask = np.nan_to_num(mask, nan=0.0)
# 陆地0，海洋1
np.savetxt("masks/OceanLand/ocean_land_mask_array.csv", mask, delimiter=",")
np.savetxt("masks/OceanLand/ocean_land_mask_lat.csv", lat, delimiter=",")
np.savetxt("masks/OceanLand/ocean_land_mask_lon.csv", lon, delimiter=",")

# region 判断数据集中的点位是否在海洋中
for i in range(len(ARCPAC)):
    lat_val = ARCPAC.loc[i, "lat"]
    lon_val = ARCPAC.loc[i, "lon"]

    # 找到最近的lat和lon索引
    lat_idx = np.argmin(np.abs(lat - lat_val))
    lon_idx = np.argmin(np.abs(lon - lon_val))

    # 获取mask中的值
    mask_val = mask[lat_idx, lon_idx]
    ARCPAC.loc[i, "location"] = mask_val
ARCPAC.to_csv("ARCPAC_data.csv", index=False)

for i in range(len(ARCTAS)):
    lat_val = ARCTAS.loc[i, "lat"]
    lon_val = ARCTAS.loc[i, "lon"]

    # 找到最近的lat和lon索引
    lat_idx = np.argmin(np.abs(lat - lat_val))
    lon_idx = np.argmin(np.abs(lon - lon_val))

    # 获取mask中的值
    mask_val = mask[lat_idx, lon_idx]
    ARCTAS.loc[i, "location"] = mask_val
ARCTAS.to_csv("ARCTAS_data.csv", index=False)


for i in range(len(ATom_1)):
    lat_val = ATom_1.loc[i, "lat"]
    lon_val = ATom_1.loc[i, "lon"]

    # 找到最近的lat和lon索引
    lat_idx = np.argmin(np.abs(lat - lat_val))
    lon_idx = np.argmin(np.abs(lon - lon_val))

    # 获取mask中的值
    mask_val = mask[lat_idx, lon_idx]
    ATom_1.loc[i, "location"] = mask_val
ATom_1.to_csv("ATom-1_data.csv", index=False)


for i in range(len(ATom_2)):
    lat_val = ATom_2.loc[i, "lat"]
    lon_val = ATom_2.loc[i, "lon"]

    # 找到最近的lat和lon索引
    lat_idx = np.argmin(np.abs(lat - lat_val))
    lon_idx = np.argmin(np.abs(lon - lon_val))

    # 获取mask中的值
    mask_val = mask[lat_idx, lon_idx]
    ATom_2.loc[i, "location"] = mask_val
ATom_2.to_csv("ATom-2_data.csv", index=False)


for i in range(len(ATom_3)):
    lat_val = ATom_3.loc[i, "lat"]
    lon_val = ATom_3.loc[i, "lon"]

    # 找到最近的lat和lon索引
    lat_idx = np.argmin(np.abs(lat - lat_val))
    lon_idx = np.argmin(np.abs(lon - lon_val))

    # 获取mask中的值
    mask_val = mask[lat_idx, lon_idx]
    ATom_3.loc[i, "location"] = mask_val
ATom_3.to_csv("ATom-3_data.csv", index=False)


for i in range(len(ATom_4)):
    lat_val = ATom_4.loc[i, "lat"]
    lon_val = ATom_4.loc[i, "lon"]

    # 找到最近的lat和lon索引
    lat_idx = np.argmin(np.abs(lat - lat_val))
    lon_idx = np.argmin(np.abs(lon - lon_val))

    # 获取mask中的值
    mask_val = mask[lat_idx, lon_idx]
    ATom_4.loc[i, "location"] = mask_val
ATom_4.to_csv("ATom-4_data.csv", index=False)


for i in range(len(CalNex)):
    lat_val = CalNex.loc[i, "lat"]
    lon_val = CalNex.loc[i, "lon"]

    # 找到最近的lat和lon索引
    lat_idx = np.argmin(np.abs(lat - lat_val))
    lon_idx = np.argmin(np.abs(lon - lon_val))

    # 获取mask中的值
    mask_val = mask[lat_idx, lon_idx]
    CalNex.loc[i, "location"] = mask_val
CalNex.to_csv("CalNex_data.csv", index=False)


for i in range(len(DC3)):
    lat_val = DC3.loc[i, "lat"]
    lon_val = DC3.loc[i, "lon"]

    # 找到最近的lat和lon索引
    lat_idx = np.argmin(np.abs(lat - lat_val))
    lon_idx = np.argmin(np.abs(lon - lon_val))

    # 获取mask中的值
    mask_val = mask[lat_idx, lon_idx]
    DC3.loc[i, "location"] = mask_val
DC3.to_csv("DC3_data.csv", index=False)


for i in range(len(GOAMAZON)):
    lat_val = GOAMAZON.loc[i, "lat"]
    lon_val = GOAMAZON.loc[i, "lon"]

    # 找到最近的lat和lon索引
    lat_idx = np.argmin(np.abs(lat - lat_val))
    lon_idx = np.argmin(np.abs(lon - lon_val))

    # 获取mask中的值
    mask_val = mask[lat_idx, lon_idx]
    GOAMAZON.loc[i, "location"] = mask_val
GOAMAZON.to_csv("GOAMAZON_data.csv", index=False)


for i in range(len(KORUSAQ)):
    lat_val = KORUSAQ.loc[i, "lat"]
    lon_val = KORUSAQ.loc[i, "lon"]

    # 找到最近的lat和lon索引
    lat_idx = np.argmin(np.abs(lat - lat_val))
    lon_idx = np.argmin(np.abs(lon - lon_val))

    # 获取mask中的值
    mask_val = mask[lat_idx, lon_idx]
    KORUSAQ.loc[i, "location"] = mask_val
KORUSAQ.to_csv("KORUS-AQ_data.csv", index=False)


for i in range(len(ORACLES)):
    lat_val = ORACLES.loc[i, "lat"]
    lon_val = ORACLES.loc[i, "lon"]

    # 找到最近的lat和lon索引
    lat_idx = np.argmin(np.abs(lat - lat_val))
    lon_idx = np.argmin(np.abs(lon - lon_val))

    # 获取mask中的值
    mask_val = mask[lat_idx, lon_idx]
    ORACLES.loc[i, "location"] = mask_val
ORACLES.to_csv("ORACLES_data.csv", index=False)


for i in range(len(SEAC4RS)):
    lat_val = SEAC4RS.loc[i, "lat"]
    lon_val = SEAC4RS.loc[i, "lon"]

    # 找到最近的lat和lon索引
    lat_idx = np.argmin(np.abs(lat - lat_val))
    lon_idx = np.argmin(np.abs(lon - lon_val))

    # 获取mask中的值
    mask_val = mask[lat_idx, lon_idx]
    SEAC4RS.loc[i, "location"] = mask_val
SEAC4RS.to_csv("SEAC4RS_data.csv", index=False)


for i in range(len(SENEX)):
    lat_val = SENEX.loc[i, "lat"]
    lon_val = SENEX.loc[i, "lon"]

    # 找到最近的lat和lon索引
    lat_idx = np.argmin(np.abs(lat - lat_val))
    lon_idx = np.argmin(np.abs(lon - lon_val))

    # 获取mask中的值
    mask_val = mask[lat_idx, lon_idx]
    SENEX.loc[i, "location"] = mask_val
SENEX.to_csv("SENEX_data.csv", index=False)

# endregion


# 绘制所有点的海陆位置
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
    "ORACLES": ORACLES,
    "SEAC4RS": SEAC4RS,
    "SENEX": SENEX,
}
fig = plt.figure(figsize=(16, 9), dpi=200)
ax = plt.axes(projection=ccrs.PlateCarree())
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.LAKES, alpha=0.5)
ax.add_feature(cfeature.RIVERS)

cmap = ListedColormap(["green", "blue"])
bounds = [0, 1, 2]
norm = BoundaryNorm(bounds, cmap.N)

for name, data in dataset.items():
    x = data["lon"]
    y = data["lat"]
    type = data["location"]
    sc = ax.scatter(
        x,
        y,
        c=type,
        s=1,
        alpha=0.5,
        transform=ccrs.PlateCarree(),
        label=name,
        cmap=cmap,
        norm=norm,
    )
cbar = plt.colorbar(sc, ticks=[0.5, 1.5], orientation="horizontal", shrink=0.5, pad=0.1)
cbar.ax.set_xticklabels(["Land", "Ocean"])

plt.title("Ocean and Land Mask")
plt.show()
