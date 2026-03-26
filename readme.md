# 📦 Verificador de 98's - Liverpool

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-6A5ACD?style=for-the-badge&logo=python&logoColor=white)

Una herramienta de escritorio diseñada para optimizar la auditoría de mercancía en almacén, identificando automáticamente artículos con terminación **"98"** mediante el cruce de datos de inventario.

---

## 🚀 Características
* **Interfaz Moderna:** Construida con `CustomTkinter` para una experiencia de usuario oscura y limpia.
* **Cruce de Datos en Tiempo Real:** Utiliza `Pandas` para buscar SKUs en bases de datos de Excel de forma instantánea.
* **Lista Dinámica:** Visualización de artículos encontrados con opción de eliminación individual (sincronizada con el reporte).
* **Generación de Reportes:** Exporta los resultados finales a un archivo `.xlsx` listo para su uso administrativo.

## 🛠️ Cómo funciona
1.  **Carga:** El sistema lee el archivo maestro de inventario al iniciar.
2.  **Escaneo:** El usuario ingresa o escanea el SKU en el panel izquierdo.
3.  **Validación:** * Si el artículo es tipo **98**, se añade visualmente a la lista derecha y al DataFrame de reporte.
    * Si no lo es, el sistema arroja una alerta visual inmediata.
4.  **Exportación:** Con un clic, se genera el reporte de todos los artículos auditados con éxito.

## 📦 Requisitos
Para correr este proyecto necesitas instalar las siguientes librerías:
```bash
pip install customtkinter pandas openpyxl