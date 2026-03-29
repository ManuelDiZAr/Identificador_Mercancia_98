import customtkinter as ctk
from tkinter import messagebox
import sys
from funciones import CrearDF_Final, CargarDF_98, RevisarSKU, Generar_Reporte, Eliminar_Elemento

class SkuListado(ctk.CTkFrame):
    def __init__(self, master,id,sku, descripcion,funcion_borrar, **kwargs):
        super().__init__(master,**kwargs)
        #Le asigno el ID al elemento. No se vera en la interfaz, pero servira de referencia
        self.id_elemento=id
        self.eliminar=funcion_borrar
        # Se distribuyen pesos de las columnas
        self.grid_columnconfigure(0, weight=0) # SKU
        self.grid_columnconfigure(1, weight=2) # Descripcion (más larga)
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
        self.df_referencia,self.error=CargarDF_98()
        if self.error:
            messagebox.showerror("Archivo no Encontrado",
            "Archivo 98s.xlsx No ha sido encontrado, o no se encuentran las columas \n SKU | DESCRIPCION") # DE TIENDA | TIENDA | SKU | VENTAS | OH
            self.destroy()
            sys.exit() #Si se cumple la condición, el programa se cierra.
        print("Archivo de reporte final creado con exito")

        
        self.title("Verificador de 98's")
        self.geometry("550x700")
        self.resizable(False, False)
        
        #Comenzamos a crear los Frames
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=0)
        self.grid_rowconfigure(1,weight=1)

        
        self.frame1=ctk.CTkFrame(self)
        self.frame1.grid(row=0,column=0,padx=10, pady=(10, 10), sticky="nsew")
        self.frame2=ctk.CTkFrame(self)
        self.frame2.grid(row=1,column=0,padx=10, pady=(10, 10), sticky="nsew")

        self.titulo_1 = ctk.CTkLabel(self.frame1, text="Verifica la Mercancia"
                                          , fg_color="transparent",
                                          font=("Roboto", 28, "bold"),       # Tamaño grande y negrita
                                          text_color="#5dade2",              # Un azul claro tipo "Tech" (o el que te guste)
                                          anchor="center")
        self.titulo_1.grid(row=0,column=0, sticky="ew",pady=10)

        

        #Comienzo a darle forma al Frame 1. Contendrá 4 ROWS ---------------------------------
        self.frame1.grid_columnconfigure(0, weight=1)
        self.frame1.grid_rowconfigure((0,1,2,3), weight=1)
        #ROW 0
        self.frame_row1=ctk.CTkFrame(self.frame1,fg_color="transparent")
        self.frame_row1.grid(row=1,pady=10)
        
        self.label_sku=(ctk.CTkLabel(self.frame_row1,text="SKU:  "))
        self.label_sku.grid(row=0,column=0)
        self.entrada_sku=ctk.CTkEntry(self.frame_row1)
        self.entrada_sku.grid(row=0,column=1)
        self.entrada_sku.bind('<Return>', lambda event: self.BTN_Verificar())
        self.btn_verificar=ctk.CTkButton(self.frame_row1,text="Verificar",command=self.BTN_Verificar)
        self.btn_verificar.grid(row=0,column=3,padx=10)
        #ROW 1
        self.label_sino=ctk.CTkLabel(self.frame1,
                                     text="Escanea un Artículo para Comenzar...",
                                     font=("Roboto", 16, "bold"),       # Fuente moderna y legible
                                     fg_color="#2B2B2B",                # Fondo oscuro tipo pantalla
                                     text_color="#FFEE00",              # Verde neón (da sensación de "Online/Listo")
                                     height=45,                         # Un poco más de presencia física
                                     corner_radius=8,                   # Bordes suavizados
                                     padx=20
                                     )
        self.label_sino.grid(row=2)
        #ROW 2
        self.btn_generar=ctk.CTkButton(self.frame1,text="Generar Reporte de 98's",command=self.BTN_Generar)
        self.btn_generar.grid(row=4)

        #FRAME 2 DE ABAJO -------------------------------------------------------------
        
        self.frame2.grid_columnconfigure(0, weight=1)
        # Le damos peso real a la fila 2 (donde está el scroll) para que crezca
        self.frame2.grid_rowconfigure(0, weight=0) # Titulo (fijo)
        self.frame2.grid_rowconfigure(1, weight=0) # Encabezados (fijo)
        self.frame2.grid_rowconfigure(2, weight=1) # Scroll (expandible)

        # FILA 0: EL TÍTULO
        self.titulo_2 = ctk.CTkLabel(self.frame2, text="98's Encontrados",
                                    font=("Roboto", 28, "bold"),
                                    text_color="#5dade2")
        self.titulo_2.grid(row=0, column=0, sticky="new", pady=10)

        # FILA 1: ENCABEZADOS (SKU | DESCRIPCION | ¿ELIMINAR?)
        self.frame2_row1 = ctk.CTkFrame(self.frame2)
        self.frame2_row1.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 5))

        self.frame2_row1.grid_columnconfigure((0), weight=0)
        self.frame2_row1.grid_columnconfigure((1), weight=1)
        self.frame2_row1.grid_columnconfigure((2), weight=0)
        self.label_sku = ctk.CTkLabel(self.frame2_row1, text="    SKU                       Descripción")
        self.label_sku.grid(row=0, column=0)
        self.label_desc = ctk.CTkLabel(self.frame2_row1, text="")
        self.label_desc.grid(row=0, column=1)
        self.label_eliminar = ctk.CTkLabel(self.frame2_row1, text="¿Eliminar?    ")
        self.label_eliminar.grid(row=0, column=2)

        # FILA 2: EL SCROLLABLE FRAME
        self.scrollF_skus = ctk.CTkScrollableFrame(self.frame2)
        self.scrollF_skus.grid(row=2, column=0, sticky="nsew", padx=10, pady=5) # row 2
        self.scrollF_skus.grid_columnconfigure(0, weight=1)
        self.entrada_sku.focus()


    def BTN_Verificar(self):
        sku=self.entrada_sku.get()
        self.df_final, descripcion, lista, id,self.error=RevisarSKU(sku,self.df_final,self.df_referencia)
        if self.error:
            messagebox.showerror("Error en Columnas",
            "No se ha encontrado la(s) columna(s): SKU | DESCRIPCION") # DE TIENDA | TIENDA | SKU | VENTAS | OH
            sys.exit() #Si se cumple la condición, el programa se cierra.
        print(f"SKU {sku} Revisado!!!!!!!")
        print(self.df_final)
        print(lista)
        if lista==True:
            objeto_listado=SkuListado(self.scrollF_skus,id,sku,descripcion,self.BTN_eliminar_listado)
            objeto_listado.pack(fill='x',pady=1)
            self.update_idletasks()
            self.Cambiar_label_Sino(True)
        else:
            self.Cambiar_label_Sino(False)
        self.scrollF_skus._parent_canvas.yview_moveto(1.0)
        self.entrada_sku.delete(0,'end')
        self.entrada_sku.focus()
        
    def BTN_Generar(self):
        self.error=Generar_Reporte(self.df_final)
        if self.error:
            print("Archivo Generado!!!!")
            messagebox.showinfo("Reporte creado",
            "Se ha generado el reporte correctamente en la carpeta archivos") # DE TIENDA | TIENDA | SKU | VENTAS | OH
            
        else:
            messagebox.showerror("Error en Carpeta",
            "No se ha encontrado la carpeta Archivos") # DE TIENDA | TIENDA | SKU | VENTAS | OH
            self.destroy()
            sys.exit() #Si se cumple la condición, el programa se cierra.
    
    def BTN_eliminar_listado(self,id_a_borrar):
        self.df_final=Eliminar_Elemento(self.df_final,id_a_borrar)
        
        print(self.df_final)

    def Cambiar_label_Sino(self,si_no):
        if si_no:
            mensaje = "✅ Sí es 98"
            color = "#18CF04"
        else:
            mensaje = "❌ No es 98"
            color = "#DA0000"
        self.label_sino.configure(text=mensaje, text_color=color)

        self.after(1500, lambda: self.label_sino.configure(text="Esperando escaneo...", text_color="#FFEE00"))

app = App()

app.mainloop()

