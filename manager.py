#
#--> Importamos la libreria tkinter, y las clases Login, Registro y Container de ventanas.py
#
from tkinter import *
from tkinter import messagebox
from ventanas import Login,Registro,Container
from dataDB import Datos

#--> Definimos la ventana principal desde donde el usuario hará el login, 
#    pudiendo existir ya en la BD o bien darse de alta como nuevo.
#--> Creamos un container donde vamos a alojar LOGIN  
class Manager(Tk):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.title("ACARMAS")
        self.geometry("1200x900")  
        self.menu()       
        container=Frame(self)
        container.pack(side=TOP,fill=BOTH,expand=True)
        container.configure(bg="green")               
        self.frames={}
        for i in (Login,Registro,Container):
            frame=i(container,self)
            self.frames[i]=frame
        self.show_frame(Login)

#--> Funcion asociado al menu de creacion de DB.
    def crearDB(self):
        db=Datos()
        try:
            db.crear()
        except:
            messagebox.showinfo(title="Informacion",message="La BASE DE DATOS ya esta CREADA")        

#--> Creamos una pequeña barra de menu para crear la BD y tablas
    def menu(self):
        menubar=Menu()
        menudata=Menu(menubar,tearoff=0)
        menudata.add_command(label="Crear/conectar BASE DE DATOS",command=self.crearDB)
        menubar.add_cascade(label="Inicio",menu=menudata)
        self.config(menu=menubar)

    def show_frame(self,container):
        frame=self.frames[container]
        frame.tkraise()        

        