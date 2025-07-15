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

ARCPAC = pd.read_csv("dataset/ARCPAC_data.csv")
ARCTAS = pd.read_csv("dataset/ARCTAS_data.csv")
ATom_1 = pd.read_csv("dataset/ATom-1_data.csv")
ATom_2 = pd.read_csv("dataset/ATom-2_data.csv")
ATom_3 = pd.read_csv("dataset/ATom-3_data.csv")
ATom_4 = pd.read_csv("dataset/ATom-4_data.csv")
CalNex = pd.read_csv("dataset/CalNex_data.csv")
DC3 = pd.read_csv("dataset/DC3_data.csv")
GOAMAZON = pd.read_csv("dataset/GOAMAZON_data.csv")
KORUSAQ = pd.read_csv("dataset/KORUS-AQ_data.csv")
ORACLES = pd.read_csv("dataset/ORACLES_data.csv")
SEAC4RS = pd.read_csv("dataset/SEAC4RS_data.csv")
SENEX = pd.read_csv("dataset/SENEX_data.csv")

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

path = r"D:\Others(English)\Database\FDUROP\wind2016.nc"
Wind_data = xr.open_dataset(path)
Wind_data = Wind_data.sel(time="2016-01-01T14:00:00.000000000")

lon = Wind_data.longitude.values
lat = Wind_data.latitude.values
u10 = Wind_data.u10.values
v10 = Wind_data.v10.values
fsr = Wind_data.fsr.values

# 降低分辨率
lon_resolution = 2.5
lat_resolution = 2

# 计算新的经纬度网格
new_lon = np.arange(
    lon.min() + lon_resolution / 2, lon.max() + lon_resolution / 2, lon_resolution
)
new_lat = np.arange(
    lat.min() + lat_resolution / 2, lat.max() + lat_resolution / 2, lat_resolution
)

# 创建新的经纬度网格
new_lon_mesh, new_lat_mesh = np.meshgrid(new_lon, new_lat)

# 初始化新的风数据
new_u10 = np.zeros_like(new_lon_mesh)
new_v10 = np.zeros_like(new_lat_mesh)
new_fsr = np.zeros_like(new_lat_mesh)
f = np.zeros_like(new_lat_mesh)
Omega = 7.2921159e-5  # 地球自转速率

# 对每个新的网格点进行采样
for i in range(len(new_lat)):
    for j in range(len(new_lon)):
        lat_mask = (lat >= new_lat[i] - lat_resolution / 2) & (
            lat < new_lat[i] + lat_resolution / 2
        )
        lon_mask = (lon >= new_lon[j] - lon_resolution / 2) & (
            lon < new_lon[j] + lon_resolution / 2
        )
        masked_u10 = u10[lat_mask][:, lon_mask]
        masked_v10 = v10[lat_mask][:, lon_mask]
        masked_fsr = fsr[lat_mask][:, lon_mask]
        if masked_u10.size > 0 and masked_v10.size > 0 and masked_fsr.size > 0:
            new_u10[i, j] = masked_u10[0, 0]
            new_v10[i, j] = masked_v10[0, 0]
            new_fsr[i, j] = masked_fsr[0, 0]
        f[i, j] = 2 * Omega * np.sin(np.deg2rad(new_lat[i]))  # 科氏参数

# 绘制风矢量图
fig = plt.figure(figsize=(20, 16))
ax = plt.axes(projection=ccrs.PlateCarree())

# 添加地图特征
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=":")
ax.add_feature(cfeature.LAKES, alpha=0.5)
ax.add_feature(cfeature.RIVERS)

# 绘制风矢量
q = ax.quiver(
    new_lon_mesh,
    new_lat_mesh,
    new_u10,
    new_v10,
    transform=ccrs.PlateCarree(),
    scale=1800,
)


plt.title("Wind Vectors with Reduced Resolution")
plt.show()

U_10 = np.sqrt(new_u10**2 + new_v10**2)  # 风速
kappa = 0.4  # 冯卡门常数
u_f = kappa * U_10 / (np.log(10 / new_fsr))  # 摩擦速度
h = np.zeros_like(new_lat_mesh)
for i in range(len(new_lat)):
    for j in range(len(new_lon)):
        if np.abs(new_lat_mesh[i][j]) > 22.5:
            h[i, j] = np.abs(u_f[i, j] / f[i, j])
        else:
            h[i, j] = None


# 绘制风矢量图
fig = plt.figure(figsize=(20, 16))
ax = plt.axes(projection=ccrs.PlateCarree())

# 添加地图特征
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=":")
ax.add_feature(cfeature.LAKES, alpha=0.5)
ax.add_feature(cfeature.RIVERS)

contour = ax.contourf(
    new_lon_mesh,
    new_lat_mesh,
    h,
    levels=10,
    cmap="viridis",
    transform=ccrs.PlateCarree(),
)
cbar = plt.colorbar(contour, ax=ax, orientation="horizontal", pad=0.05)
cbar.set_label("Height")
ax.set_title("Contour Plot of 2D Array on Map")
plt.show()
