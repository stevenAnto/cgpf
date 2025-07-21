import os
import csv

def obtener_csvs_ordenados(folder="resultados"):
    if not os.path.exists(folder):
        os.makedirs(folder)
    archivos = [f for f in os.listdir(folder) if f.lower().endswith(".csv")]
    archivos.sort(key=lambda f: os.path.getmtime(os.path.join(folder, f)), reverse=True)
    return [(os.path.splitext(f)[0], os.path.join(folder, f)) for f in archivos]

def leer_datos_csv(path):
    datos = []
    categorias = set()
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            datos.append(row)
            cat = row.get("Categoria", "")
            if cat:
                categorias.add(cat)
    return datos, sorted(categorias)

def filtrar_por_categoria(data, categoria):
    if categoria == "Todos":
        return data
    return [r for r in data if r.get("Categoria") == categoria]
