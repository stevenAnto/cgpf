#!/usr/bin/env python3
import os
import pandas as pd
import argparse

def procesar_datos(ruta_csv_entrada):
    """
    Procesa y combina los datos de dorsales con tiempos y información adicional.
    
    Args:
        ruta_csv_entrada (str): Ruta al archivo CSV con datos de participantes
    """
    
    # 1. Definir rutas
    dir_output_paddle = "outputPaddle"
    dir_output_csv = "outputCSV"
    archivo_tiempos = "dorsales_y_tiempos.csv"
    
    # 2. Crear directorio de salida si no existe
    os.makedirs(dir_output_csv, exist_ok=True)
    
    try:
        # 3. Cargar ambos archivos
        df_tiempos = pd.read_csv(os.path.join(dir_output_paddle, archivo_tiempos))
        df_datos = pd.read_csv(ruta_csv_entrada)
        
    except FileNotFoundError as e:
        print(f"❌ Error al leer archivos: {e}")
        return

    # 4. Convertir tiempo a segundos para ordenar
    df_tiempos['Segundos'] = df_tiempos['Tiempo'].str.split(':').apply(
        lambda x: int(x[0])*60 + int(x[1])
    )
    
    # 5. Ordenar por tiempo (ascendente)
    df_tiempos = df_tiempos.sort_values('Segundos')
    
    # 6. Combinar datos manteniendo el orden
    df_final = pd.merge(
        df_tiempos,
        df_datos,
        on='Dorsal',
        how='left'
    ).drop(columns=['Segundos'])  # Eliminar columna temporal
    
    # 7. Guardar resultado
    ruta_resultado = os.path.join(dir_output_csv, "resultado_final.csv")
    df_final.to_csv(ruta_resultado, index=False)
    
    print(f"✅ Resultado guardado en: {ruta_resultado}")
    print("\nResultado:")
    print(df_final.to_string(index=False))

def main():
    parser = argparse.ArgumentParser(description='Procesa datos de dorsales y tiempos')
    parser.add_argument('--rutacsv', required=True, help='Ruta al CSV con datos de participantes')
    args = parser.parse_args()
    
    procesar_datos(args.rutacsv)

if __name__ == "__main__":
    main()
