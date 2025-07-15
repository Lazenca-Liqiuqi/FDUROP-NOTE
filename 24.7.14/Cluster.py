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
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN

# region 网格化二维聚类
grouped = pd.read_csv("dataset/Meshed_data.csv")

lon_resolution = 2.5
lat_resolution = 2
height_resolution = 500
# 生成参数列表
lon_list = [
    lon_resolution * (i) + lon_resolution / 2
    for i in range(int(-180 // lon_resolution), int(180 // lon_resolution))
]
lat_list = [
    lat_resolution * i + lat_resolution / 2
    for i in range(int(-90 // lat_resolution), int(90 // lat_resolution))
]
height_list = [height_resolution * i for i in range(0, 35)]

mass_array_2d = np.zeros(
    (
        len(lon_list),
        len(lat_list),
    )
)

for idx, row in grouped.iterrows():
    lon_idx = np.where(np.array(lon_list) == row["lon_bin"])[0][0]
    lat_idx = np.where(np.array(lat_list) == row["lat_bin"])[0][0]
    height_idx = np.where(height_list == row["height_bin"])
    mass_array_2d[lon_idx, lat_idx] = max(mass_array_2d[lon_idx, lat_idx], row["mass"])

_25_percent = np.percentile(grouped["mass"], 99)

for i in range(len(lon_list)):
    for j in range(len(lat_list)):
        if mass_array_2d[i, j] > _25_percent:
            mass_array_2d[i, j] = 1
        else:
            mass_array_2d[i, j] = 0

# 聚类

X = np.argwhere(mass_array_2d == 1)

# 使用K-means聚类
for i in range(2, 11):
    kmeans = KMeans(n_clusters=i, random_state=0).fit(X)
    labels = kmeans.labels_

    # 将聚类结果可视化
    fig, ax = plt.subplots(
        subplot_kw={"projection": ccrs.PlateCarree()}, figsize=(10, 10)
    )
    ax.set_extent([-180, 180, -90, 90], ccrs.PlateCarree())
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=":")
    ax.add_feature(cfeature.LAKES, alpha=0.5)
    ax.add_feature(cfeature.RIVERS)

    # 将索引转换为经纬度
    lon_indices, lat_indices = X[:, 0], X[:, 1]
    lons = [lon_list[i] for i in lon_indices]
    lats = [lat_list[i] for i in lat_indices]

    # 绘制聚类结果
    scatter = ax.scatter(
        lons, lats, c=labels, cmap="viridis", transform=ccrs.PlateCarree()
    )
    legend = plt.legend(
        *scatter.legend_elements(),
        loc="center left",
        bbox_to_anchor=(1, 0.5),
        title="Cluster",
    )
    plt.title("K-Means Clustering on Map")
    plt.show()

# endregion

# region 所有数据点聚类
# region 读取数据集
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
# endregion

data = data[data["mass"] > data["mass"].quantile(0.99)]
latitudes = []
longitudes = []
for name, df in dataset.items():
    latitudes.extend(df["lat"].tolist())
    longitudes.extend(df["lon"].tolist())

# 创建一个包含所有经纬度信息的数据框
data = pd.DataFrame({"Latitude": latitudes, "Longitude": longitudes})

for i in range(2, 11):
    # 使用K-means进行聚类分析
    kmeans = KMeans(n_clusters=i, random_state=0).fit(data)
    data["Cluster"] = kmeans.labels_

    # 创建地图
    fig, ax = plt.subplots(
        figsize=(10, 5), subplot_kw={"projection": ccrs.PlateCarree()}
    )
    ax.set_global()
    ax.coastlines()

    # 绘制聚类结果
    for cluster in range(i):
        cluster_data = data[data["Cluster"] == cluster]
        ax.scatter(
            cluster_data["Longitude"],
            cluster_data["Latitude"],
            label=f"Cluster {cluster}",
            transform=ccrs.PlateCarree(),
        )

    # 添加图例
    ax.legend()

    # 显示地图
    plt.show()
# endregion
