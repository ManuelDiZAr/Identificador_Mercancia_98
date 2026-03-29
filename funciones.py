import pandas as pd
import os
import openpyxl
import time

#Creo el DF que será el reporte final
def CrearDF_Final():
    
    df_reporte = pd.DataFrame(columns=['ID','SKU','Descripcion'])
    print("Reporte inicial Creado")
    return df_reporte

def CargarDF_98():
    try:
        ruta=os.path.join("archivos",'98s.xlsx')
        df_98=pd.read_excel(ruta)
        df_98['SKU'] = df_98['SKU'].fillna(0).astype(int).astype(str).str.strip() #Convierto todos los datos de SKU a STRing
        print(df_98)
        print("Termino de imprimir el DF98-----------")
        return df_98, False
    except:
        return None, True

def RevisarSKU(sku_escaneado,df_reporte,df_referencia):
    """
    Busca el SKU, extrae su descripción y lo añade al reporte.
    """
    # Convertimos a string para asegurar que la comparación sea exacta
    try:
        sku_buscado = str(sku_escaneado)
        df_referencia["SKU"] = df_referencia["SKU"].astype(str)

        # 1. Buscamos si existe en la referencia
        if sku_buscado in df_referencia["SKU"].values:
            #Generamos un ID con timestamp
            id=int(time.time()*1000)
            # 2. "VLOOKUP": Extraemos la descripción de esa fila específica
            # .loc[filas, columnas]
            descripcion = df_referencia.loc[df_referencia["SKU"] == sku_buscado, "DESCRIPCION"].values[0]
            
            # 3. Creamos el DF temporal incluyendo la descripción
            df_temporal = pd.DataFrame({
                'ID':[id],
                'SKU': [sku_buscado], 
                'Descripcion': [descripcion]
            })
            
            # 4. Unimos al reporte
            df_reporte = pd.concat([df_reporte, df_temporal], ignore_index=True)
            
            # Retornamos el DF, el estatus de éxito y la descripción encontrada
            return df_reporte, descripcion , True, id, False
        else:
            # Si no existe, retornamos el DF sin cambios y None en la descripción
            return df_reporte, None, False, None, False
    except:
            return None, None, None, None, True
    
    

def Eliminar_Elemento(df_reporte,id_a_eliminar):
    
    df_final=df_reporte[df_reporte['ID']!=id_a_eliminar].copy()
    return df_final

def Generar_Reporte(DF):
    try:
        ruta_destino=os.path.join("archivos","Reporte.csv")
        DF.to_csv(ruta_destino, index=False)
        return True
    except:
        return False


