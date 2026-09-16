import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# 1. Cargar los archivos locales
# ---------------------------------------------------------
barrio = gpd.read_file("barrio.geojson")
predios = gpd.read_file("predios.geojson")

print(barrio.head())
print(barrio.crs)
print(predios.head())
print(predios.crs)
print("Cantidad de predios descargados:", len(predios))

# ---------------------------------------------------------
# 2. Quedarnos solo con los predios que están dentro del barrio
# ---------------------------------------------------------
predios = predios.to_crs(barrio.crs)

predios_amparo = gpd.sjoin(
    predios,
    barrio[["geometry"]],
    predicate="within",
    how="inner"
)

print("Cantidad de predios dentro de Amparo:", len(predios_amparo))

# ---------------------------------------------------------
# 3. Reproyectar a metros (EPSG 3116, Colombia) y calcular el área
# ---------------------------------------------------------
predios_amparo = predios_amparo.to_crs("EPSG:3116")
predios_amparo["area_m2"] = predios_amparo.geometry.area

print(predios_amparo["area_m2"].describe())

# ---------------------------------------------------------
# 4. Clasificar cada predio en un rango de área (estilo CCRP)
# ---------------------------------------------------------
predios_amparo["grupo_area"] = pd.cut(
    predios_amparo["area_m2"],
    bins=[0, 100, 200, 300, 400, 500, float("inf")],
    labels=[
        "< 100 m2",
        "100 - 200 m2",
        "200 - 300 m2",
        "300 - 400 m2",
        "400 - 500 m2",
        "> 500 m2"
    ]
)

print(predios_amparo["grupo_area"].value_counts().sort_index())

# ---------------------------------------------------------
# 5. Graficar
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 10))

predios_amparo.plot(
    column="grupo_area",
    categorical=True,
    legend=True,
    ax=ax,
    edgecolor="black",
    linewidth=0.2
)

barrio.to_crs("EPSG:3116").boundary.plot(
    ax=ax,
    edgecolor="black",
    linewidth=2
)

plt.title("Predios del barrio Amparo según rango de área")
plt.axis("off")
plt.show()
