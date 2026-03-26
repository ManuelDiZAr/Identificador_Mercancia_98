import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Verificador de 98's")
        self.geometry("800x500")
        #Comenzamos a crear los Frames
        self.grid_rowconfigure(0, weight=1) #Creo la fila en la que vivirán los 2 frames
        self.grid_columnconfigure((0, 1), weight=1) #Creo las 2 columnas en las que vivirán los frames
        #Creo los 2 Frames, y hago que cada uno tome cada columna en su totalidad
        self.frame1=ctk.CTkFrame(self)
        self.frame1.grid(row=0,column=0,padx=10, pady=(10, 0), sticky="nsew")
        self.frame2=ctk.CTkFrame(self)
        self.frame2.grid(row=0,column=1,padx=10, pady=(10, 0), sticky="nsew")

        #Comienzo a darle forma al Frame 1. Contendrá 4 ROWS ---------------------------------
        self.frame1.grid_columnconfigure(0, weight=1)
        self.frame1.grid_rowconfigure((0,1,2,3), weight=1)
        #ROW 1
        self.titulo_frame1 = ctk.CTkLabel(self.frame1, text="Verifica la Mercancia"
                                          , fg_color="transparent",
                                          font=("Roboto", 28, "bold"),       # Tamaño grande y negrita
                                          text_color="#5dade2",              # Un azul claro tipo "Tech" (o el que te guste)
                                          anchor="center")
        self.titulo_frame1.grid(row=0)
        #ROW 2
        self.frame_row1=ctk.CTkFrame(self.frame1,fg_color="transparent")
        self.frame_row1.grid(row=1)
        
        self.label_sku=(ctk.CTkLabel(self.frame_row1,text="SKU:  "))
        self.label_sku.grid(row=0,column=0)
        self.entrada_sku=ctk.CTkEntry(self.frame_row1)
        self.entrada_sku.grid(row=0,column=1)
        self.btn_verificar=ctk.CTkButton(self.frame_row1,text="Verificar")
        self.btn_verificar.grid(row=0,column=2,padx=10)
        #ROW 3
        self.label_sino=ctk.CTkLabel(self.frame1,text="Este label debe de cambiar a Sí es 98 o No Es 98 ")
        self.label_sino.grid(row=2)
        #ROW 4
        self.btn_generar=ctk.CTkButton(self.frame1,text="Generar Reporte de 98's")
        self.btn_generar.grid(row=3)

        #Comienzo a darle forma al frame 2, contendrá 2 ROWS --------------------------------------------
        #ROW 0
        self.frame2.grid_columnconfigure(0, weight=1)
        self.frame2.grid_rowconfigure((0,1), weight=1)
        self.titulo_frame2 = ctk.CTkLabel(self.frame2, text="98s Encontrados"
                                          , fg_color="transparent",
                                          font=("Roboto", 28, "bold"),       # Tamaño grande y negrita
                                          text_color="#5dade2",              # Un azul claro tipo "Tech" (o el que te guste)
                                          anchor="center")
        self.titulo_frame2.grid(row=0)

        #ROW 1
        
        self.frame2_row1=ctk.CTkFrame(self.frame2)
        self.frame2_row1.grid_columnconfigure((0,1,2), weight=1)
        self.frame2_row1.grid(row=1,sticky="ew",padx=10,pady=10)
        self.label_sku=ctk.CTkLabel(self.frame2_row1,text="SKU")
        self.label_sku.grid(row=0,column=0)
        self.label_desc=ctk.CTkLabel(self.frame2_row1,text="Descripcion")
        self.label_desc.grid(row=0,column=1)
        self.label_eliminar=ctk.CTkLabel(self.frame2_row1,text="¿Eliminar?")
        self.label_eliminar.grid(row=0,column=2)



        

app = App()

app.mainloop()

