#--> Importamos las librerias necesariass
from tkinter import *
from tkinter import ttk,messagebox
from dataDB import Datos
#from PIL import Image, ImageTk
#import cv2
#import imutils
import sqlite3
#-------------------- clase Login
#--> Empezamos definiendo la clase login y el metodo init con sus caracteristicas, donde el usuario
#    se loga y se identifica, con sus controles.
class Login(Frame):
#    image=None
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.pack
        self.place(x=0,y=0,width=1200,height=900)
        self.controlador=controlador
        self.widgets()
#        self.imagen()

#--> Definimos la funcion para representar una imagen en la pantalla de logon
#    def imagen(self):
#        global image
#        image=cv2.imread("IMAG\acarmas.png")
#        image_show=imutils.resize(image,width=240,height=240)
#        image_show=cv2.cvtColor(image_show,cv2.COLOR_BGR2RGB)
#        im=Image.fromarray(image_show)
#        img=ImageTk.PhotoImage(image=im)

#--> Le damos cierta estetica a los botones de la pantalla login
    def botones(self,x,y,text,bcolor,fcolor,cmd):
        def on_enter(e):
            btn["background"]=bcolor
            btn["foreground"]=fcolor
        def on_leave(e):
            btn["background"]=fcolor
            btn["foreground"]=bcolor
        btn=Button(self,text=text,
        fg=bcolor,
        bg=fcolor,
        border=1,
        activeforeground=fcolor,
        activebackground=bcolor,
        command=cmd)
        btn.bind("<Enter>",on_enter)
        btn.bind("<Leave>",on_leave)
        btn.place(x=x,y=y,width=120)

    def validacion(self,user,pas):
        return len(user)>0 and len(pas)>0    

#--> Hacemos una select contra la BD usuarios para comprobas si existe el usuario y su contraseña, y 
#    validamos que rellene los campos.
    def login(self):
        with sqlite3.connect("database.db") as conn:
            cursor=conn.cursor()
            user=self.username.get()
            pas=self.password.get()
            if self.validacion(user,pas):                
                consulta="SELECT*FROM usuarios WHERE name=? and password=?"
                parametros=(user,pas)
                try:
                    cursor.execute(consulta,parametros)
                    if cursor.fetchall():
                       self.control1()
                    else:
                       self.username.delete(0,END)
                       self.password.delete(0,END)
                       messagebox.showerror(title="Error",message="Usuario y/o contraseña INCORRECTA")
                except:
                    messagebox.showerror(title="Error",message="No se conecto a la BASE DE DATOS")
            else:
                messagebox.showerror(title="Error",message="Rellene Usuario y/o contraseña")               
            cursor.close()        

#--> Creamos la funcion control1, para ser llamada en el btn1, en command
    def control1(self):
        self.controlador.show_frame(Container)    

#--> Creamos una funcion para ser llamada en el btn2, en command
    def control2(self):
        self.controlador.show_frame(Registro)           

#--> Definimos la funcion widgest, que contendrá el frame de usuario/contraseña con sus entry's
#    y botones de registrarse o conectarse.        
    def widgets(self):
        fondo=Frame(self,bg="cyan")
        fondo.pack
        fondo.place(x=0,y=0,width=1200,height=900)
#        self.perfil=Label(fondo)
#        self.place(x=540,y=150)
        self.username=Entry(fondo,font="Arial 16")
        self.username.place(x=540,y=400,width=240,height=40)
        self.password=Entry(fondo,show="*",font="16")
        self.password.place(x=540,y=460,width=240,height=40)
        btn=self.botones(540,520,"INICIAR SESION","blue","white",cmd=self.login)
#        btn1=Button(fondo,bg="blue",fg="white",text="INICIAR SESION",command=self.login)
#        btn1.place(x=580,y=520)
        btn1=self.botones(700,520,"REGISTRAR USUARIO","blue","white",cmd=self.control2)
#        btn2=Button(fondo,bg="blue",fg="white",text="REGISTRAR USUARIO",command=self.control2)
#        btn2.place(x=700,y=520)

#------------------------  clase Registro
#--> Vamos a crear una clase llamada Registro, donde se creará un frame que contenga
#    el usuario y la contraseña
class Registro(Frame):
    def __init__(self,padre,controlador):
        super().__init__(padre)
        self.pack()
        self.place(x=0,y=0,width=1200,height=900)
        self.controlador=controlador
        self.widgest()

#--> Le damos un movimiento de color, al paso del mouse/enter por las teclas de los botones
    def botones(self,x,y,text,bcolor,fcolor,cmd):
        def on_enter(e):
            btn["background"]=bcolor
            btn["foreground"]=fcolor
        def on_leave(e):
            btn["background"]=fcolor
            btn["foreground"]=bcolor
        btn=Button(self,text=text,
        fg=bcolor,
        bg=fcolor,
        border=1,
        activeforeground=fcolor,
        activebackground=bcolor,
        command=cmd)
        btn.bind("<Enter>",on_enter)
        btn.bind("<Leave>",on_leave)
        btn.place(x=x,y=y,width=120)

    def validacion(self,user,pas):
        return len(user)>0 and len(pas)>0            

    def eje_consulta(self,consulta,parametros=()):
        db=Datos()
        db.consultas(consulta,parametros)

#--> Definimos dos funciones que iran asociados al command de btn2
    def registro(self):
        user=self.username.get()
        pas=self.password.get()
        if self.validacion(user,pas):
            if len(pas)<8:                
                messagebox.showinfo(title="Error",message="Contraseña corta, minimo 8 caracteres")
                self.username.delete(0,END)
                self.password.delete(0,END)
            else:
                consulta="INSERT INTO usuarios VALUES(?,?,?)"
                parametros=(None,user,pas)
                self.eje_consulta(consulta,parametros)
                self.control1()  
        else:
            messagebox.showerror(title="Error",message="Rellene Usuario y/o contraseña")              
        
    def control1(self):
        self.controlador.show_frame(Container)

    def control2(self):
        self.controlador.show_frame(Login)    

#--> Vamos a crear una funcion que comprende los widgest y crear un frame llamado "fondo"
    def widgest(self):
        fondo=Frame(self,bg="cyan")
        fondo.pack()
        fondo.place(x=0,y=0,width=1200,height=900)
        user=Label(fondo,text="Nombre de Usuario",font="Arial 16",bg="cyan")
        user.place(x=580,y=320)
        self.username=Entry(fondo,font="Arial 16")
        self.username.place(x=580,y=360,width=240,height=40)
        pas=Label(fondo,text="Contraseña",font="Arial 16",bg="cyan")
        pas.place(x=580,y=410)
        self.password=Entry(fondo,show="*",font="16")
        self.password.place(x=580,y=450,width=240,height=40)
#--> Dentro de la pantalla fondo vamos a craer un boton llamado "REGISTRAR" y otro "REGRESAR",
#    para volver a la pantalla anterior.
        btn1=self.botones(560,540,"REGRESAR","blue","white",cmd=self.control2)
        btn=self.botones(700,540,"REGISTRAR","blue","white",cmd=self.registro)
#        btn2=Button(fondo,bg="blue",fg="white",text="REGISTRAR",command=self.registro)
#        btn2.place(x=605,y=540)

#--------------> clase Container
#--> Vamos a crear el contenedor, con su controlador, y sus botones para "Gestion Socios" y
#     "Gestion Actividades".
class Container(Frame):
    def __init__(self,padre,controlador):
        super().__init__(padre)
        self.controlador=controlador
        self.pack()
        self.place(x=0,y=0,width=1200,height=900) 
        self.widgets()
        self.frames={}
#--> Iteramos con una instruccion "for", tanto a Socios como a Actividad.        
        for i in (Socios,Actividad):
            frame=i(self)
            self.frames[i]=frame
            frame.pack()
            frame.config(bg="red")
            frame.place(x=0,y=40,width=1200,height=900)
        self.show_frames(Socios)    
#--> Creamos una funcion show_frames para almacenar los diferentes frames
    def show_frames(self,container):
        frame=self.frames[container]
        frame.tkraise()

    def socios(self):
        self.show_frames(Socios)

    def actividad(self):
        self.show_frames(Actividad)        

    def widgets(self):
        socios=Button(self,text="Gestion Socios",command=self.socios)
        socios.pack()
        socios.place(x=0,y=0,width=300,height=40)
        actividad=Button(self,text="Gestion Actividades",command=self.actividad)
        actividad.pack()
        actividad.place(x=300,y=0,width=300,height=40)

#--> Creamos dos clases, de momento, una que será de Socios y otro que será de Actividades.
class Socios(Frame):
    def __init__(self,padre): 
        super().__init__(padre)
        self.widgets()
    def widgets(self):
        socios=Label(self,text="Socios")
        socios.pack()
        socios.place(x=558,y=450)           

class Actividad(Frame):
    def __init__(self,padre): 
        super().__init__(padre)
        self.widgets()
    def widgets(self):
        actividad=Label(self,text="Actividad")
        actividad.pack()
        actividad.place(x=558,y=450)           

