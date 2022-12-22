#--> Importamos las librerias necesarias
from tkinter import *
from tkinter import ttk,messagebox
from dataDB import Datos
from PIL import Image, ImageTk
import cv2
import imutils
import sqlite3
#-------------------- clase Login
#--> Empezamos definiendo la clase login y el metodo init con sus caracteristicas, donde el usuario
#    se loga y se identifica, con sus controles.
class Login(Frame):
    image=None
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.pack
        self.place(x=0,y=0,width=1200,height=900)
        self.controlador=controlador
        self.widgets()
        self.imagen()

#--> Definimos la funcion para representar una imagen en la pantalla de logon
    def imagen(self):
        global image
        image=cv2.imread("acarmas.png")
        image_show=imutils.resize(image,width=240,height=240)
        image_show=cv2.cvtColor(image_show,cv2.COLOR_BGR2RGB)
        im=Image.fromarray(image_show)
        img=ImageTk.PhotoImage(image=im)
        self.perfil.configure(image=img)
        self.perfil.image=img

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
        self.perfil=Label(fondo)
        self.perfil.place(x=540,y=150)
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
#     "Gestion Actividades","Proveedores", "Caja" y "Varios".
class Container(Frame):
    def __init__(self,padre,controlador):
        super().__init__(padre)
        self.controlador=controlador
        self.pack()
        self.place(x=0,y=0,width=1200,height=900) 
        self.widgets()
        self.frames={}
#--> Iteramos con una instruccion "for", tanto a Socios como a Actividad.        
        for i in (Socios,Actividad,Proveedor,Caja,Varios):
            frame=i(self)
            self.frames[i]=frame
            frame.pack()
            frame.config(bg="red")
            frame.place(x=0,y=40,width=1200,height=900)
        self.show_frames(Socios)  

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
        btn.place(x=x,y=y,width=240,height=40)    

#--> Creamos una funcion show_frames para almacenar los diferentes frames
    def show_frames(self,container):
        frame=self.frames[container]
        frame.tkraise()

#--> Definimos varias funciones para posicionar los botones en la parte superior
#    de cada frame.
    def socios(self):
        self.show_frames(Socios)

    def actividad(self):
        self.show_frames(Actividad)        

    def proveedor(self):
        self.show_frames(Proveedor)        

    def caja(self):
        self.show_frames(Caja)        

    def varios(self):
        self.show_frames(Varios)        

    def widgets(self):
        socios=self.botones(0,0,"GESTION SOCIOS","blue","white",cmd=self.socios)       
        actividad=self.botones(240,0,"GESTION ACTIVIDAD","blue","white",cmd=self.actividad)
        proveedor=self.botones(480,0,"PROVEEDORES","blue","white",cmd=self.proveedor)
        caja=self.botones(720,0,"CAJA","blue","white",cmd=self.caja)
        varios=self.botones(960,0,"VARIOS","blue","white",cmd=self.varios)

#--> Creamos las clases, de Socios, de Actividad, de Proveedor, de Caja y de Varios.
class Socios(Frame):
    def __init__(self,padre): 
        super().__init__(padre)
        self.widgets()
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
        btn.place(x=x,y=y,width=240,height=40)    
#--> Funcion de dar de alta un socio al pulsar el boton "ALTA SOCIO"
    def altasocio(self):
        pass

    def widgets(self):
        socios=Label(self,text="SOCIOS",bg="greenyellow")
        socios.pack()
        socios.place(x=0,y=0,height=30,width=1200)
        self.frame=Frame(self,bg="lime green")   
        self.frame.place(x=0,y=30,width=1200,height=800) 
#---> vamos a definir todos los campos de entrada de socios.  
#--> Nombre (nombre)      
        lblnombre=Label(self.frame,text="Nombre:",font="16",bg="aquamarine")
        lblnombre.grid(row=0,column=0,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)
        self.nombre=Entry(self.frame,width=(35))
        self.nombre.grid(row=0,column=1,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)     
#--> Primer apellido (apel1)        
        lblapel1=Label(self.frame,text="Apellido 1:",font="16",bg="aquamarine")
        lblapel1.grid(row=1,column=0,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)
        self.apel1=Entry(self.frame,width=35)
        self.apel1.grid(row=1,column=1,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)      
#--> Segundo apellido (apel2)        
        lblapel2=Label(self.frame,text="Apellido 2:",font="16",bg="aquamarine")
        lblapel2.grid(row=2,column=0,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)
        self.apel2=Entry(self.frame,width=35)
        self.apel2.grid(row=2,column=1,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)      
#--> Numero de Socio (numsoc)
        lblnumsoc=Label(self.frame,text="Numero de Socio:",font="16",bg="aquamarine")
        lblnumsoc.grid(row=0,column=2,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)
        self.numsoc=Entry(self.frame,width=7)
        self.numsoc.grid(row=0,column=3,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)      
#--> Fecha Alta (fecA)
        lblfecA=Label(self.frame,text="Fecha Alta:",font="16",bg="aquamarine")
        lblfecA.grid(row=1,column=2,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)
        self.fecA=Entry(self.frame,width=10)
        self.fecA.grid(row=1,column=3,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)      
#--> Fecha Baja (fecB), Motivo de baja(motB)
        lblfecB=Label(self.frame,text="Fecha Baja:",font="16",bg="aquamarine")
        lblfecB.grid(row=2,column=2,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)
        self.fecB=Entry(self.frame,width=10)
        self.fecB.grid(row=2,column=3,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)      
        lblmotB=Label(self.frame,text="Motivo Baja:",font="16",bg="aquamarine")
        lblmotB.grid(row=2,column=4,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)
        self.motB=Entry(self.frame,width=25)
        self.motB.grid(row=2,column=5,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)  
#--> Fecha Nacimiento (fecN)
        lblfecN=Label(self.frame,text="Fecha Nacimiento:",font="16",bg="aquamarine")
        lblfecN.grid(row=3,column=2,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)
        self.fecN=Entry(self.frame,width=10)
        self.fecN.grid(row=3,column=3,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)  
        lblfofe=Label(self.frame,text="FECHAS: aaaa/mm/dd",font="16",bg="orange")
        lblfofe.grid(row=3,column=4,sticky="e",padx=10,pady=10,ipadx=5,ipady=5,columnspan=2)

#--> Profesion (profe), Estado civil(estciv)
        lblprofe=Label(self.frame,text="Profesion:",font="16",bg="aquamarine")
        lblprofe.grid(row=0,column=4,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)
        self.profe=Entry(self.frame,width=15)
        self.profe.grid(row=0,column=5,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)      
        lblestciv=Label(self.frame,text="Estado Civil:",font="16",bg="aquamarine")
        lblestciv.grid(row=1,column=4,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)
        self.estciv=Entry(self.frame,width=15)
        self.estciv.grid(row=1,column=5,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)      
#--> D.N.I. (dni)
        lbldni=Label(self.frame,text="D.N.I.:",font="16",bg="aquamarine")
        lbldni.grid(row=3,column=0,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)
        self.dni=Entry(self.frame,width=10)
        self.dni.grid(row=3,column=1,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)      
#--> DIRECCION
#--> Calle (calle), Numero (num), Escalera (esc), Letra (let)
        lbldirec=Label(self.frame,text=">> DIRECCION <<",font="16",bg="orange")
        lbldirec.grid(row=4,column=1,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)
        lblcalle=Label(self.frame,text="Calle\Plaza:",font="16",bg="aquamarine")
        lblcalle.grid(row=5,column=0,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)
        self.calle=Entry(self.frame,width=30)
        self.calle.grid(row=5,column=1,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)      
        lblnum=Label(self.frame,text="Numero:",font="16",bg="aquamarine")
        lblnum.grid(row=5,column=2,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)
        self.num=Entry(self.frame,width=4)
        self.num.grid(row=5,column=3,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)      
        lblesc=Label(self.frame,text="Escalera:",font="16",bg="aquamarine")
        lblesc.grid(row=5,column=4,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)
        self.esc=Entry(self.frame,width=4)
        self.esc.grid(row=5,column=5,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)      
        lbllet=Label(self.frame,text="Letra:",font="16",bg="aquamarine")
        lbllet.grid(row=5,column=6,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)
        self.let=Entry(self.frame,width=4)
        self.let.grid(row=5,column=7,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)     
#-->  Provincia (prov), Pais (pais)
        lblmuni=Label(self.frame,text="Ciudad:",font="16",bg="aquamarine")
        lblmuni.grid(row=6,column=0,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)
        self.muni=Entry(self.frame,width=20)
        self.muni.grid(row=6,column=1,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)     
        lblprov=Label(self.frame,text="Provincia:",font="16",bg="aquamarine")
        lblprov.grid(row=6,column=2,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)
        self.prov=Entry(self.frame,width=20)
        self.prov.grid(row=6,column=3,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)     
        lblpais=Label(self.frame,text="Pais:",font="16",bg="aquamarine")
        lblpais.grid(row=6,column=4,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)
        self.pais=Entry(self.frame,width=15)
        self.pais.grid(row=6,column=5,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)  
#--> Codigo postal (codpos), Telefono movil (telmov), Telefono Fijo (telfij), Correo electronico (corE)
        lblcodpos=Label(self.frame,text="Cod/postal:",font="16",bg="aquamarine")
        lblcodpos.grid(row=7,column=0,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)
        self.codpos=Entry(self.frame,width=5)
        self.codpos.grid(row=7,column=1,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)     
        lbltelmov=Label(self.frame,text="Tlfno. Movil:",font="16",bg="aquamarine")
        lbltelmov.grid(row=7,column=2,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)
        self.telmov=Entry(self.frame,width=10)
        self.telmov.grid(row=7,column=3,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)  
        lbltelfij=Label(self.frame,text="Tlfno. Fijo:",font="16",bg="aquamarine")
        lbltelfij.grid(row=7,column=4,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)
        self.telfij=Entry(self.frame,width=10)
        self.telfij.grid(row=7,column=5,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)  
        lblcorE=Label(self.frame,text="Correo @:",font="16",bg="aquamarine")
        lblcorE.grid(row=7,column=6,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)
        self.corE=Entry(self.frame,width=10)
        self.corE.grid(row=7,column=7,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)  
#--> PERSONA DE CONTACTO
        lblpercon=Label(self.frame,text=">> PERSONA DE CONTACTO <<",font="16",bg="orange")
        lblpercon.grid(row=9,column=0,sticky="e",padx=10,pady=10,ipadx=5,ipady=5,columnspan=2)
#--> Nombre (nomcon)      
        lblnomcon=Label(self.frame,text="Nombre:",font="16",bg="aquamarine")
        lblnomcon.grid(row=10,column=0,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)
        self.nomcon=Entry(self.frame,width=20)
        self.nomcon.grid(row=10,column=1,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)    
#--> Primer apellido (apecon1)        
        lblapecon1=Label(self.frame,text="Apellido 1:",font="16",bg="aquamarine")
        lblapecon1.grid(row=11,column=0,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)
        self.apecon1=Entry(self.frame,width=35)
        self.apecon1.grid(row=11,column=1,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)      
#--> Segundo apellido (apecon2)        
        lblapecon2=Label(self.frame,text="Apellido 2:",font="16",bg="aquamarine")
        lblapecon2.grid(row=12,column=0,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)
        self.apecon2=Entry(self.frame,width=35)
        self.apecon2.grid(row=12,column=1,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)      
#--> Telefono de contacto (telcon)        
        lbltelcon=Label(self.frame,text="Telefono contacto:",font="16",bg="aquamarine")
        lbltelcon.grid(row=10,column=2,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)
        self.telcon=Entry(self.frame,width=10)
        self.telcon.grid(row=10,column=3,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)      
#--> Relacion de contacto (relcon)        
        lblrelcon=Label(self.frame,text="Relacion contacto:",font="16",bg="aquamarine")
        lblrelcon.grid(row=11,column=2,sticky="e",padx=10,pady=10,ipadx=5,ipady=5)
        self.relcon=Entry(self.frame,width=20)
        self.relcon.grid(row=11,column=3,sticky="e",padx=10,pady=10,ipadx=5,ipady=5) 

        btn=self.botones(50,675,"ALTA SOCIO","blue","white",cmd=self.altasocio)    




class Actividad(Frame):
    def __init__(self,padre): 
        super().__init__(padre)
        self.widgets()
    def widgets(self):
        actividad=Label(self,text="Actividad")
        actividad.pack()
        actividad.place(x=558,y=450)           

class Proveedor(Frame):
    def __init__(self,padre): 
        super().__init__(padre)
        self.widgets()
    def widgets(self):
        proveedor=Label(self,text="Proveedor")
        proveedor.pack()
        proveedor.place(x=558,y=450) 

class Caja(Frame):
    def __init__(self,padre): 
        super().__init__(padre)
        self.widgets()
    def widgets(self):
        caja=Label(self,text="Caja")
        caja.pack()
        caja.place(x=558,y=450)

class Varios(Frame):
    def __init__(self,padre): 
        super().__init__(padre)
        self.widgets()
    def widgets(self):
        varios=Label(self,text="Varios")
        varios.pack()
        varios.place(x=558,y=450)        