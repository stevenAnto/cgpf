#!/usr/bin/env python3
import sys
import os
import pandas as pd
import argparse

def procesar_datos(ruta_csv_entrada, ruta_salida=None):
    """
    Procesa y combina los datos de dorsales con tiempos y información adicional.
    
    Args:
        ruta_csv_entrada (str): Ruta al archivo CSV con datos de participantes
        ruta_salida (str, optional): Ruta personalizada para el archivo de salida
    """
    # 1. Definir rutas
    dir_output_paddle = "outputPaddle"
    archivo_tiempos = "dorsales_y_tiempos.csv"
    
    try:
        # 2. Cargar ambos archivos
        df_tiempos = pd.read_csv(os.path.join(dir_output_paddle, archivo_tiempos))
        df_datos = pd.read_csv(ruta_csv_entrada)
        
    except FileNotFoundError as e:
        print(f"❌ Error al leer archivos: {e}", file=sys.stderr)
        sys.exit(1)

    # 3. Procesamiento de datos
    df_tiempos['Segundos'] = df_tiempos['Tiempo'].str.split(':').apply(
        lambda x: int(x[0])*60 + int(x[1])
    )
    df_tiempos = df_tiempos.sort_values('Segundos')
    
    df_final = pd.merge(
        df_tiempos,
        df_datos,
        on='Dorsal',
        how='left'
    ).drop(columns=['Segundos'])

    # 4. Determinar ruta de salida
    ruta_resultado = ruta_salida if ruta_salida else "resultado_final.csv"
    
    # 5. Guardar resultado
    df_final.to_csv(ruta_resultado, index=False)
    
    # 6. Mostrar información por stderr (no afecta al CSV)
    print(f"✅ Resultado guardado en: {os.path.abspath(ruta_resultado)}", file=sys.stderr)
    print("\nVista previa del resultado:", file=sys.stderr)
    print(df_final.head().to_string(index=False), file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description='Procesa datos de dorsales y tiempos')
    parser.add_argument('--rutacsv', required=True, help='Ruta al CSV con datos de participantes')
    parser.add_argument('--output', help='Ruta personalizada para el archivo de salida CSV')
    args = parser.parse_args()
    
    procesar_datos(args.rutacsv, args.output)

if __name__ == "__main__":
    main()
