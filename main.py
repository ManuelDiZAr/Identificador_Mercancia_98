import customtkinter as ctk
import os
from funciones import CrearDF_Final, CargarDF_98, RevisarSKU, Generar_Reporte, Eliminar_Elemento

class SkuListado(ctk.CTkFrame):
    def __init__(self, master,id,sku, descripcion,funcion_borrar, **kwargs):
        super().__init__(master,**kwargs)
        #Le asigno el ID al elemento. No se vera en la interfaz, pero servira de referencia
        self.id_elemento=id
        self.eliminar=funcion_borrar
        # Se distribuyen pesos de las columnas
        self.grid_columnconfigure(0, weight=1) # SKU
        self.grid_columnconfigure(1, weight=3) # Descripcion (más larga)
        self.grid_columnconfigure(2, weight=0) # El botón no necesita crecer
        
        self.label_sku = ctk.CTkLabel(self, text=sku)
        self.label_sku.grid(row=0, column=0, padx=10, sticky="w") # "w" para alinear texto a la izquierda
        
        self.label_desc = ctk.CTkLabel(self, text=descripcion)
        self.label_desc.grid(row=0, column=1, padx=10, sticky="w")
        
        # Agregamos un ancho pequeño (width) para que no sea un botón gigante
        self.btn_delete = ctk.CTkButton(self, text="❌", width=40, fg_color="#333333", hover_color="red",command=self.BTN_eliminar_listado)
        self.btn_delete.grid(row=0, column=2, padx=5, pady=2)
    
    def BTN_eliminar_listado(self):
        self.eliminar(self.id_elemento)
        self.destroy()
        print(f"{self.id_elemento} Eliminado con exito")
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        #Cargamos los dos archivos con los que vamos a trabajar
        self.df_final=CrearDF_Final()
        print("Archivo de referencia cargado con exito")
        self.df_referencia=CargarDF_98()
        print("Archivo de reporte final creado con exito")

        
        self.title("Verificador de 98's")
        self.geometry("800x500")
        self.resizable(False, False)
        #Comenzamos a crear los Frames
        self.grid_rowconfigure((1), weight=1) #Creo la fila en la que vivirán los 2 frames
        self.grid_columnconfigure((0, 1), weight=1) #Creo las 2 columnas en las que vivirán los frames
        
        self.titulo_1 = ctk.CTkLabel(self, text="Verifica la Mercancia"
                                          , fg_color="transparent",
                                          font=("Roboto", 28, "bold"),       # Tamaño grande y negrita
                                          text_color="#5dade2",              # Un azul claro tipo "Tech" (o el que te guste)
                                          anchor="center")
        self.titulo_1.grid(row=0,column=0, sticky="ew",pady=10)

        self.titulo_2 = ctk.CTkLabel(self, text="98's Encontrados"
                                          , fg_color="transparent",
                                          font=("Roboto", 28, "bold"),       # Tamaño grande y negrita
                                          text_color="#5dade2",              # Un azul claro tipo "Tech" (o el que te guste)
                                          anchor="center")
        self.titulo_2.grid(row=0,column=1, sticky="ew",pady=10)


        #Creo los 2 Frames, y hago que cada uno tome cada columna en su totalidad
        self.frame1=ctk.CTkFrame(self)
        self.frame1.grid(row=1,column=0,padx=10, pady=(10, 10), sticky="nsew")
        self.frame2=ctk.CTkFrame(self)
        self.frame2.grid(row=1,column=1,padx=10, pady=(10, 10), sticky="nsew")

        #Comienzo a darle forma al Frame 1. Contendrá 4 ROWS ---------------------------------
        self.frame1.grid_columnconfigure(0, weight=1)
        self.frame1.grid_rowconfigure((1,2), weight=1)
        #ROW 0
        self.frame_row1=ctk.CTkFrame(self.frame1,fg_color="transparent")
        self.frame_row1.grid(row=0,pady=10)
        
        self.label_sku=(ctk.CTkLabel(self.frame_row1,text="SKU:  "))
        self.label_sku.grid(row=0,column=0)
        self.entrada_sku=ctk.CTkEntry(self.frame_row1)
        self.entrada_sku.grid(row=0,column=1)
        self.entrada_sku.bind('<Return>', lambda event: self.BTN_Verificar())
        self.btn_verificar=ctk.CTkButton(self.frame_row1,text="Verificar",command=self.BTN_Verificar)
        self.btn_verificar.grid(row=0,column=2,padx=10)
        #ROW 1
        self.label_sino=ctk.CTkLabel(self.frame1,text="Este label debe de cambiar a Sí es 98 o No Es 98 ")
        self.label_sino.grid(row=1)
        #ROW 2
        self.btn_generar=ctk.CTkButton(self.frame1,text="Generar Reporte de 98's",command=self.BTN_Generar)
        self.btn_generar.grid(row=2)

        #Comienzo a darle forma al frame 2, contendrá 2 ROWS --------------------------------------------
        #ROW 0
        self.frame2.grid_columnconfigure(0, weight=1)
        self.frame2.grid_rowconfigure((1), weight=1)
        
        #Se crea el encabezado de SKU | DESCRIPCION | ¿ELIMINAR?
        self.frame2_row1=ctk.CTkFrame(self.frame2)
        self.frame2_row1.grid_columnconfigure((0,1,2), weight=1)
        self.frame2_row1.grid(row=0,sticky="ew",padx=10,pady=10)
        self.label_sku=ctk.CTkLabel(self.frame2_row1,text="SKU")
        self.label_sku.grid(row=0,column=0)
        self.label_desc=ctk.CTkLabel(self.frame2_row1,text="Descripcion")
        self.label_desc.grid(row=0,column=1)
        self.label_eliminar=ctk.CTkLabel(self.frame2_row1,text="¿Eliminar?")
        self.label_eliminar.grid(row=0,column=2)

        #ROW 1
        self.scrollF_skus=ctk.CTkScrollableFrame(self.frame2)
        self.scrollF_skus.grid(row=1,sticky="nsew",padx=10,pady=1)
        self.scrollF_skus.grid_columnconfigure(0, weight=1)
       
        # for i in range(0,21):
        #     sku1=SkuListado(scrollF_skus,f"{i}",f"SKU de prueba {i}")
        #     sku1.pack(fill="x",pady=1)
    
    def BTN_Verificar(self):
        sku=self.entrada_sku.get()
        self.df_final, descripcion, lista, id=RevisarSKU(sku,self.df_final,self.df_referencia)
        print(f"SKU {sku} Revisado!!!!!!!")
        print(self.df_final)
        print(lista)
        if lista==True:
            objeto_listado=SkuListado(self.scrollF_skus,id,sku,descripcion,self.BTN_eliminar_listado)
            objeto_listado.pack(fill='x',pady=1)
        self.entrada_sku.delete(0,'end')
        self.entrada_sku.focus()
        
    def BTN_Generar(self):
        Generar_Reporte(self.df_final)
        print("Archivo Generado!!!!")
    
    def BTN_eliminar_listado(self,id_a_borrar):
        self.df_final=Eliminar_Elemento(self.df_final,id_a_borrar)
        
        print(self.df_final)
app = App()

app.mainloop()

