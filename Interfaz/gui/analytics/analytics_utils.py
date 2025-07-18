# tabs/statistics/statistics_utils.py
import os
import pandas as pd
import numpy as np
from glob import glob

def listar_proyectos_csv(ruta="resultados"):
    files = glob(os.path.join(ruta, "*.csv"))
    files.sort(key=os.path.getmtime, reverse=True)
    return [os.path.basename(f) for f in files]

def convertir_a_segundos(tiempo_str):
    partes = tiempo_str.strip().split("-")
    try:
        nums = [int(p) for p in partes][::-1]
        ms = nums[0] if len(nums) > 0 else 0
        s  = nums[1] if len(nums) > 1 else 0
        m  = nums[2] if len(nums) > 2 else 0
        h  = nums[3] if len(nums) > 3 else 0
        return h*3600 + m*60 + s + ms/1000
    except:
        return 0

def cargar_estadisticas_csv(path):
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]
    df['Tiempo_s'] = df['Tiempo'].astype(str).apply(convertir_a_segundos)

    total = len(df)
    prom  = df['Tiempo_s'].mean()
    mins  = df['Tiempo_s'].min()
    maxs  = df['Tiempo_s'].max()
    cats  = df['Categoria'].value_counts().sort_index()
    return df, total, prom, mins, maxs, cats

def generar_cdf(df):
    times = np.sort(df['Tiempo_s'])
    cdf = np.arange(1, len(times)+1) / len(times)

    xs = np.linspace(times.min(), times.max(), 300)
    coefs = np.polyfit(times, cdf, deg=3)
    poly = np.poly1d(coefs)
    ys = np.clip(poly(xs), 0, 1)
    return times, cdf, xs, ys
