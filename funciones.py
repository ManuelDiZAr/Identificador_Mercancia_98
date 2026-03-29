import pandas as pd
import os
import openpyxl
import time
import json

#Creo el DF que será el reporte final
def CrearDF_Final():
    
    df_reporte = pd.DataFrame(columns=['ID','SKU','Descripcion'])
    print("Reporte inicial Creado")
    return df_reporte

def cargar_json():
    with open("columnas.json","r",encoding="utf-8") as f:
        return json.load(f)

def encontrar_columnas(columnas,lista_sinonimos):
    for col in columnas:
        if col in lista_sinonimos:
            return col
    return None

def CargarDF_98():
    try:
        config = cargar_json()
        print("JSON CARGADO CON EXITO!!")
        ruta=os.path.join("archivos",'98s.xlsx')
        df_98=pd.read_excel(ruta)
        #Busco las columnas en el JSON
        col_sku_real= encontrar_columnas(df_98, config["columnas"]["sku"])
        col_desc_real= encontrar_columnas(df_98, config["columnas"]["descripcion"])

        #Valido que ambas columnas existan en el archivo
        if col_desc_real and col_sku_real:
            print("Columnas Encontradas!!")
            df_98=df_98.rename(columns={col_sku_real: "SKU", col_desc_real: "DESCRIPCION"})
            print("Columnas Renombradas")
        
            df_98['SKU'] = df_98['SKU'].fillna(0).astype(int).astype(str).str.strip() #Convierto todos los datos de SKU a STRing
            print("Datos de SKU Corregidos")
            print(df_98)
            print("Termino de imprimir el DF98-----------")
            return df_98, False
        else:
            return None, True
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


