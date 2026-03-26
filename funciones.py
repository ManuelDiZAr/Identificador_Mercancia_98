import pandas as pd
import os
import openpyxl

ruta=os.path.join("pruebas",'98s.xlsx')
ruta_destino=os.path.join("pruebas","Reporte.csv")
df_98=pd.read_excel(ruta)
print(df_98)

#Creo el DF que será el reporte final
df_reporte = pd.DataFrame(columns=['SKU'])
print("Reporte inicial")
print(df_reporte)

df_98['SKU'] = df_98['SKU'].astype(str).str.strip() #Convierto todos los datos de SKU a columna

def revisar(sku_escaneado,df_reporte,df_referencia):
    """
    Revisa si el sku escaneado está en la tabla de referencia
    """
    if sku_escaneado in df_referencia["SKU"].values: #Busca el SKU en los valores de SKU
        df_temporal=pd.DataFrame({'SKU': [sku_escaneado]}) #Creo un DF temporal para poder agregarlo al DF del reporte
        df_reporte=pd.concat([df_reporte,df_temporal],ignore_index=True) #Agrego el DF
        return df_reporte #Regreso el DF unido
    else: #Si no se econtró el SKU escaneado, regreso el DF inicial
        return df_reporte

df_reporte=revisar("1",df_reporte,df_98)
df_reporte=revisar("5",df_reporte,df_98)
df_reporte=revisar("7",df_reporte,df_98)
df_reporte=revisar("21",df_reporte,df_98)

print("\nReporte Final")
df_reporte=pd.merge(df_reporte, df_98, on='SKU', how='left') #Hago el left Join para generar el reporte final
print(df_reporte)
df_reporte.to_csv(ruta_destino, index=False, encoding='utf-8-sig')
