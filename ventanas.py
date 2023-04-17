#--> Importamos las librerias necesarias
from tkinter import *
from tkinter import ttk, messagebox
from dataDB import Datos
from datetime import datetime
from PIL import Image, ImageTk
import cv2
import imutils
import sqlite3
import itertools
# import pandas as pd


#-------------------- clase Login
#--> Empezamos definiendo la clase login y el metodo init con sus caracteristicas, donde el usuario
#    se loga y se identifica, con sus controles.
class Login(Frame):
    image=None
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.pack
        self.place(x=0,y=0,width=1200,height=800)
        self.controlador=controlador
        self.widgets()
        self.imagen()      

#--> Definimos la funcion para representar una imagen en la pantalla de logon
    def imagen(self):
        global image
        image=cv2.imread("acarmas.png")
        image_show=imutils.resize(image,width=270,height=270)
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
        btn.place(x=x,y=y,width=120,height=50)

    def validacion(self,user,pas):
        return len(user)>0 and len(pas)>0    

#--> Hacemos una select contra la BD usuarios para comprobas si existe el usuario y su contraseña, y 
#    validamos que rellene los campos.
    def login(self):
        global usuario
        with sqlite3.connect("database.db") as conn:
            cursor=conn.cursor()
            user=self.username.get()
            pas=self.password.get()
            usuario=user
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

#--> Creamos la funcion control1, para ser llamada en login si va bien usuario/contraseña,
#    sera dirigido a la Clase Container donde se inicia la seleccion de las partes de la
#    aplicacion de Socios.
    def control1(self):
        self.controlador.show_frame(Container)    

#--> Creamos una funcion para ser llamada en el btn1, en command

    def control2(self):
        self.controlador.show_frame(Registro)           

#--> Definimos la funcion widgest, que contendrá el frame de usuario/contraseña con sus entry's
#    y botones de registrarse o conectarse.        
    def widgets(self):
        fondo=Frame(self,bg="cyan",bd=15,relief="groove")
        fondo.pack
        fondo.place(x=0,y=0,width=1200,height=800)
        self.perfil=Label(fondo)
        self.perfil.place(x=540,y=150)
        user=Label(fondo,text="Nombre de Usuario",font="Arial 16",bg="cyan")
        user.place(x=540,y=320)
        self.username=Entry(fondo,font="Arial 16")
        self.username.place(x=540,y=360,width=240,height=40)
        pas=Label(fondo,text="Contraseña",font="Arial 16",bg="cyan")
        pas.place(x=540,y=410)
        self.password=Entry(fondo,show="*",font="16")
        self.password.place(x=540,y=450,width=240,height=40)
        btn=self.botones(540,520,"INICIAR SESION","blue","white",cmd=self.login)
        btn1=self.botones(700,520,"REGISTRAR USUARIO","blue","white",cmd=self.control2)      
       
#------------------------  clase Registro
#--> Vamos a crear una clase llamada Registro, donde se creará un frame que contenga
#    el usuario y la contraseña del Administrador, para caso de ser validos se darán de alta 
#    al usuario y contraseña.
class Registro(Frame):
    image=None
    def __init__(self,padre,controlador):
        super().__init__(padre)
        self.pack()
        self.place(x=0,y=0,width=1200,height=800)
        self.controlador=controlador
        self.widgest()
        self.imagen()

#--> Definimos la funcion para representar una imagen en la pantalla de logon
    def imagen(self):
        global image
        image=cv2.imread("acarmas.png")
        image_show=imutils.resize(image,width=270,height=270)
        image_show=cv2.cvtColor(image_show,cv2.COLOR_BGR2RGB)
        im=Image.fromarray(image_show)
        img=ImageTk.PhotoImage(image=im)
        self.perfil.configure(image=img)
        self.perfil.image=img

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
        btn.place(x=x,y=y,width=140)

    def validacion(self,user,pas):
        return len(user)>0 and len(pas)>0            

    def eje_consulta(self,consulta,parametros=()):
        db=Datos()
        db.consultas(consulta,parametros)

#--> Definimos dos funciones que iran asociados al command de btn2
    def registro(self):
        user=self.username.get()
        pas=self.password.get()
        secret_key=self.secret.get()
        if self.validacion(user,pas):
            if len(pas)<6:                
                messagebox.showinfo(title="Error",message="Contraseña corta, minimo 6 caracteres")
                self.username.delete(0,END)
                self.password.delete(0,END)
            else:
                if secret_key=="samraca":
                    consulta="INSERT INTO usuarios VALUES(?,?,?)"
                    parametros=(None,user,pas)
                    self.eje_consulta(consulta,parametros)
                    self.control1()  
                else:
                    messagebox.showerror(title="ADMINISTRADOR",message="Error en contraseña del Administrador")            
        else:
            messagebox.showerror(title="Error",message="Rellene Usuario y/o contraseña")              
        
    def control1(self):
        self.controlador.show_frame(Container)

    def control2(self):
        self.controlador.show_frame(Login)    

#--> Vamos a crear una funcion que comprende los widgest y crear un frame llamado "fondo"
    def widgest(self):
        self.fondo=Frame(self,bg="#33FFDD",bd=15,relief="groove")
        self.fondo.pack()
        self.fondo.place(x=0,y=0,width=1200,height=800)
        self.perfil=Label(self.fondo)
        self.perfil.place(x=540,y=130)   
        key=Label(self.fondo,text="Contraseña Administrador",font="Arial 16",bg="cyan")
        key.place(x=560,y=300) 
        self.secret=Entry(self.fondo,show="*")
        self.secret.place(x=560,y=330,width=240,height=40)    
        user=Label(self.fondo,text="NOMBRE USUARIO",font="Arial 16",bg="cyan")
        user.place(x=560,y=380)
        self.username=Entry(self.fondo,font="Arial 16")
        self.username.place(x=560,y=410,width=240,height=40)
        pas=Label(self.fondo,text="CONTRASEÑA",font="Arial 16",bg="cyan")
        pas.place(x=560,y=460)
        self.password=Entry(self.fondo,show="*",font="16")
        self.password.place(x=560,y=490,width=240,height=40)
#--> Dentro de la pantalla fondo vamos a craer un boton llamado "REGISTRAR" y otro "REGRESAR",
#    para volver a la pantalla anterior.
        btn1=self.botones(560,580,"REGRESAR","blue","white",cmd=self.control2)
        btn=self.botones(680,580,"REGISTRAR","blue","white",cmd=self.registro)

#--------------> clase Container  <----------------------------------------------------------------
#--> Vamos a crear el contenedor, con su controlador, y sus botones para "Gestion Socios" y
#     "Gestion Actividades","Partticipes", "Apunte Diario" y "Proveedores", .
class Container(Frame):
    def __init__(self,padre,controlador):
        super().__init__(padre)
        self.controlador=controlador
        self.pack()
        self.place(x=0,y=0,width=1200,height=800) 
        self.widgets()
        self.frames={}
#--> Iteramos con una instruccion "for", tanto a Socios, Actividad, Participes, Apunte diario 
# y Proveedor. Para que la primera pantalla que se activa es la de Socios.        
        for i in (Socios,Actividad,Participes,Apuntediario,Proveedor):
            frame=i(self)
            self.frames[i]=frame
            frame.pack()
            frame.config(bg="#fbcada")
            frame.place(x=0,y=40,width=1200,height=800)
        self.show_frames(Socios)  

#--> Le damos un movimiento de color, al paso del mouse/enter por las teclas de los botones
#    Ajustamos las cuatro pantallas al ancho de la pantalla principal
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
        font="Arial 15",
        justify=CENTER,
        activeforeground=fcolor,
        activebackground=bcolor,
        command=cmd)
        btn.bind("<Enter>",on_enter)
        btn.bind("<Leave>",on_leave)
        btn.place(x=x,y=y,width=240,height=40)  

    def widgets(self):
        socios=self.botones(0,0,"GESTION SOCIOS","greenyellow","grey",cmd=self.socios)               
        actividad=self.botones(240,0,"GESTION ACTIVIDADES","#33CBFF","grey",cmd=self.actividad)
        participes=self.botones(480,0,"PARTICIPES","blue","grey",cmd=self.participes)
        apuntediario=self.botones(720,0,"APUNTE DIARIO","yellow","grey",cmd=self.apuntediario)
        proveedor=self.botones(960,0,"PROVEEDORES","#FF6633","grey",cmd=self.proveedor)

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

    def participes(self):
        self.show_frames(Participes)        

    def apuntediario(self):
        self.show_frames(Apuntediario)        

    def proveedor(self):
        self.show_frames(Proveedor)        

#--> Creamos las clases, de Socios, de Actividad, Participes, de Apuntediario y de Proveedor, 
#==============================================================================================
#                                        >>  SOCIOS <<
#==============================================================================================

class Socios(Frame):
    def __init__(self,padre): 
        super().__init__(padre)
        self.widgets()
        self.id=-1
        self.recuperar_numso()       

#--> Le damos un movimiento de color, al paso del mouse/enter por las teclas de los botones
    def botones(self,x,y,text,bcolor,fcolor,cmd):
        def on_enter(e):
            btn["background"]=bcolor
            btn["foreground"]=fcolor
        def on_leave(e):
            btn["background"]=fcolor
            btn["foreground"]=bcolor
        btn=Button(self.frame,text=text,
        fg=bcolor,
        bg=fcolor,
        border=1,
        font="Arial 12",
        activeforeground=fcolor,
        activebackground=bcolor,
        command=cmd)
        btn.bind("<Enter>",on_enter)
        btn.bind("<Leave>",on_leave)
        btn.place(x=x,y=y,width=200,height=40)    
  
#--> Funcion para realizar instrucciones sobre la BD y recuperar el ultimo numero de socio y 
#    mostrarlo, el superior a 9000 que son no-socios y socios-honorarios. 
#    Falta recuperar el ultimo menor a 5000

    def recuperar_numso(self):
        with sqlite3.connect("database.db") as conn:
            cursor=conn.cursor()
            cursor.execute("SELECT numsoc FROM socio WHERE numsoc < 5000 ORDER BY numsoc DESC LIMIT 1")
            resultado=cursor.fetchone()
            if resultado is None:
                messagebox.showwarning(title="Error",message="NO EXISTE REGISTROS EN socio") 
            else:    
                self.ultnumsoc.delete(0,END)
                self.ultnumsoc.insert(END,resultado[0])
            conn.commit()
            #self.ultnumsoc=Entry(state="readonly")
        with sqlite3.connect("database.db") as conn:
            cursor=conn.cursor()
            cursor.execute("SELECT numsoc FROM socio WHERE numsoc > 5000 ORDER BY numsoc DESC LIMIT 1")
            resultado=cursor.fetchone()
            if resultado is None:
                messagebox.showwarning(title="Error",message="NO EXISTE REGISTROS EN socio") 
            else:    
                self.ultnumNosoc.delete(0,END)
                self.ultnumNosoc.insert(END,resultado[0])
            conn.commit()            

#--> Funcion para Habilitar/Deshabilitar los campos de entrada - DE MOMENTO NO SE USA
    def habilitar_campos(self,estado):
        self.nombre.configure(state=estado)
        self.apellidos.configure(state=estado)
        self.fecA.configure(state=estado)
        self.fecN.configure(state=estado)
        self.fecB.configure(state=estado)
        self.motB.configure(state=estado)
        self.dni.configure(state=estado)
        self.profe.configure(state=estado)
        self.deudapen.configure(state=estado)
        self.CargoMember.configure(state=estado)
        self.numsoc.configure(state=estado)
        self.estciv.configure(state=estado)
        self.discapaci.configure(state=estado)
        self.calle.configure(state=estado)
        self.muni.configure(state=estado)
        self.prov.configure(state=estado)
        self.pais.configure(state=estado)
        self.codpos.configure(state=estado)
        self.telmov.configure(state=estado)
        self.telfij.configure(state=estado)
        self.corE.configure(state=estado)
        self.nomcon.configure(state=estado)
        self.apellcon.configure(state=estado)
        self.telcon.configure(state=estado)
        self.relcon.configure(state=estado)

#--> Funcion para realizar instrucciones sobre la BD
    def eje_consulta(self,consulta,parametros=()):
        db=Datos()
        try:
           result=db.consultas(consulta,parametros) 
        except:            
           pass
        return result 

#--> Funcion para limpiar campos de entrada
    def limpiar_campos(self):
        self.nombre.delete(0,END)
        self.apellidos.delete(0,END)
        self.fecA.delete(0,END)
        self.fecN.delete(0,END)
        self.fecB.delete(0,END)
        self.motB.delete(0,END)
        self.dni.delete(0,END)
        self.profe.delete(0,END)
        self.deudapen.delete(0,END)
        self.check_1.set(0)
        self.CargoMember.delete(0,END)
        self.numsoc.delete(0,END)
        self.estciv.delete(0,END)
        self.discapaci.delete(0,END)
        self.calle.delete(0,END)
        self.muni.delete(0,END)
        self.prov.delete(0,END)
        self.pais.delete(0,END)
        self.codpos.delete(0,END)
        self.telmov.delete(0,END)
        self.telfij.delete(0,END)
        self.corE.delete(0,END)
        self.nomcon.delete(0,END)
        self.apellcon.delete(0,END)
        self.telcon.delete(0,END)
        self.relcon.delete(0,END)
        self.check_2.set(0)
        self.check_3.set(0)
        self.check_4.set(0)

#--> Funcion para validar campos de entrada minimos
    def validacion_entrada(self,nombre,apellidos,fecA,numsoc):
        if len(nombre) > 0 and len(apellidos) > 0 and len(fecA) > 0 and numsoc > 0: 
           return True

#--> Funcion para validar la fecha de entrada (obligatoria)        
    def valfecha(self,fechv):
        try:              
            fechv=datetime.strptime(fechv,'%Y-%m-%d').date()            
            return True
        except ValueError:                                
            return False
        
#--> Funcion para validar que el campo de entrada sea numerico (numero de socio)
    def valida_numero(self,numero):
        numero = int(numero)
        if numero < 1:
            return False  
        else:     
            return True 
        
#--> Funcion para Cancelar una operacion
    def cancelar_operacion(self):
        res = messagebox.askquestion(title="Cancelar",message="Esta seguro que desea cancelar la operacion actual?")
        if res == messagebox.YES:
            self.limpiar_campos()


#--> Funcion de dar de alta un socio al pulsar el boton "ALTA SOCIO"-------------------------
    def altasocio(self):
#---> Recogemos los datos introducidos por el usuario   
        self.nombre.focus()
        nombre=self.nombre.get().upper()
        apellidos=self.apellidos.get().upper()
        fecA=self.fecA.get()
        fecN=self.fecN.get()
        fecB=self.fecB.get()
        motB=self.motB.get().upper()
        dni=self.dni.get()
        profe=self.profe.get().upper()
        deudapen=self.deudapen.get()
        check_1=self.check_1.get()
        CargoMember=self.CargoMember.get().upper()
        numsoc=self.numsoc.get().isnumeric()
        estciv=self.estciv.get().upper()
        discapaci=self.discapaci.get()
        calle=self.calle.get()
        muni=self.muni.get().upper()
        prov=self.prov.get().upper()
        pais=self.pais.get().upper()
        codpos=self.codpos.get().isnumeric()
        telmov=self.telmov.get()
        telfij=self.telfij.get()
        corE=self.corE.get()
        nomcon=self.nomcon.get().upper()
        apellcon=self.apellcon.get().upper()
        telcon=self.telcon.get()
        relcon=self.relcon.get().upper()
        check_2=self.check_2.get()
        check_3=self.check_3.get()
        check_4=self.check_4.get()

#---> Compruebo si  los datos minimos de entrada han sido RELLENADOS
#---> Validamos fecha de alta
#---> Validamos que el numero de socio, sea numerico  

        if self.validacion_entrada(nombre,apellidos,fecA,numsoc):          
          fechv=fecA                    
          if self.valfecha(fechv):       
            numero=numsoc
            if self.valida_numero(numero):
                try:
                    consulta=("""INSERT INTO socio VALUES(NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""")                                            
                    parametros=(nombre,apellidos,fecA,fecN,fecB,motB,dni,profe,deudapen,
                                check_1,CargoMember,numsoc,estciv,discapaci,calle,muni,prov,
                                pais,codpos,telmov,telfij,corE,nomcon,apellcon,telcon,relcon,
                                check_2,check_3,check_4,self.hoy)
                    self.eje_consulta(consulta,parametros)
                    messagebox.showinfo(title="ALTA SOCIO",message="Alta Socio realizado con exito")                   
                    self.limpiar_campos()                                       
                except sqlite3.OperationalError as error:
                    print("Eror en Alta BD: ", error)
                    messagebox.showwarning(title="Error",message="ERROR AL DAR DE ALTA SOCIO") 
            else:
                    messagebox.showerror(title="ALTA SOCIO",message="La informacion solo debe ser numerica")
          else:
                messagebox.showerror(title="FECHA ALTA",message="Fecha debe ser formato AAAA-MM-DD")
        else:
            messagebox.showwarning(title="ALTA SOCIO",message="Rellene los campos,Nombre,Apellidos,Fecha Alta y nº Socio")

#--> Funcion para CONSULTAR un socio al pulsar el boton "CONSULTA"-------------------------
    def consulta_socio(self):            
        nombre=self.nombre.get().upper()            
        apellidos=self.apellidos.get().upper()   
        if (nombre=="") and (apellidos==""):            
            messagebox.showwarning(title="CONSULTA SOCIO",message="Rellene los campos >> Nombre y 2 Apellidos << ")
        else:    
            try:
                with sqlite3.connect("database.db") as conn:
                 cursor = conn.cursor()
                 consulta ='SELECT * FROM socio WHERE nombre = ? and apellidos = ?;'
                 parametros = (nombre,apellidos,)
                 cursor.execute(consulta, parametros)
                 resultado = cursor.fetchone()
                 conn.commit()
            except sqlite3.OperationalError as error:
                    print("Eror en Consulta BD: ", error)
                    messagebox.showwarning(title="Error",message="Error en CONSULTA SOCIO") 

            if resultado is None:
                self.nombre.delete(0,END)
                self.apellidos.delete(0,END)
                messagebox.showinfo(title="CONSULTA",message="Socio no existe")                 
            else:
                self.limpiar_campos()
                self.mostrar_campos(resultado)

#--> Se controla los campos NULL de la BD, para evitar errores
    def mostrar_campos(self,resultado):
        self.id=resultado[0]
        self.nombre.insert(END,resultado[1])
        self.apellidos.insert(END,resultado[2])
        self.fecA.insert(END,resultado[3])
        if resultado[4] != None:
           self.fecN.insert(END,resultado[4])
        if resultado[5] != None:
           self.fecB.insert(END,resultado[5])
        if resultado[6] != None:   
           self.motB.insert(END,resultado[6])
        self.dni.insert(END,resultado[7])
        if resultado[8] != None:        
           self.profe.insert(END,resultado[8])
        self.deudapen.insert(END,resultado[9])       
        if resultado[11] != None:        
           self.CargoMember.insert(END,resultado[11])
        self.numsoc.insert(END,resultado[12])
        if resultado[13] != None:        
           self.estciv.insert(END,resultado[13])
        self.discapaci.insert(END,resultado[14])
        if resultado[15] != None:        
           self.calle.insert(END,resultado[15])
        if resultado[16] != None:        
           self.muni.insert(END,resultado[16])
        if resultado[17] != None:        
           self.prov.insert(END,resultado[17])
        if resultado[18] != None:           
           self.pais.insert(END,resultado[18])
        if resultado[19] != None:        
           self.codpos.insert(END,resultado[19])
        if resultado[20] != None:        
           self.telmov.insert(END,resultado[20])
        if resultado[21] != None:           
           self.telfij.insert(END,resultado[21])
        if resultado[22] != None:           
           self.corE.insert(END,resultado[22])
        if resultado[23] != None:           
           self.nomcon.insert(END,resultado[23])
        if resultado[24] != None:        
           self.apellcon.insert(END,resultado[24])
        if resultado[25] != None:        
           self.telcon.insert(END,resultado[25])
        if resultado[26] != None:        
           self.relcon.insert(END,resultado[26])
        self.check_1.set(resultado[10])
        self.check_2.set(resultado[27])
        self.check_3.set(resultado[28])
        self.check_4.set(resultado[29])
        self.fecUltAct=self.hoy

#--> Funcion para MODIFICAR un socio, al pulsar el boton "MODIFICAR", compruebo si self.id==-1, en cuyo 
#    caso realizo una consulta y muestro los datos recuperados, para que los modifique. Y si self.id no es -1,
#    es que ya tiene almazenado el id del socio y solo falta updatear el registro.
    def modifica_socio(self):
        if self.id==-1:
            nombre=self.nombre.get().upper()            
            apellidos=self.apellidos.get().upper() 
            if (nombre=="") or (apellidos==""):            
                messagebox.showwarning(title="MODIFICACION SOCIO",message="Rellene los campos >> Nombre y 2 Apellidos << ")
            else:            
                try:
                    with sqlite3.connect("database.db") as conn:                    
                        cursor=conn.cursor()
                        consulta=("SELECT * FROM socio WHERE nombre=? and apellidos=?")
                        parametros=(nombre,apellidos)
                        cursor.execute(consulta,parametros)
                        resultado=cursor.fetchone()
                        conn.commit() 
                except sqlite3.OperationalError as error:
                    print("Eror en Modificacion/consul BD: ", error)
                    messagebox.showwarning(title="Error",message="Error en MODIFICACION/select SOCIO") 
                if resultado is None:
                    self.nombre.delete(0,END)
                    self.apellidos.delete(0,END)
                    messagebox.showinfo(title="MODIFICACION",message="SOCIO no existe")                 
                else:
                    self.limpiar_campos()
                    self.mostrar_campos(resultado)
                    messagebox.showinfo(title="Modificacion",message="Haga las modificaciones y pulse MODIFICACION")     
                    _id=resultado[0]
        else:    
            _nombre=self.nombre.get().upper()
            _apellidos=self.apellidos.get().upper()
            _fecA=self.fecA.get()
            _fecN=self.fecN.get()
            _fecB=self.fecB.get()
            _motB=self.motB.get().upper()
            _dni=self.dni.get()
            _profe=self.profe.get().upper()
            _deudapen=self.deudapen.get()
            _check_1=self.check_1.get()
            _CargoMember=self.CargoMember.get().upper()
            _numsoc=self.numsoc.get()
            _estciv=self.estciv.get().upper()
            _discapaci=self.discapaci.get()
            _calle=self.calle.get()
            _muni=self.muni.get().upper()
            _prov=self.prov.get().upper()
            _pais=self.pais.get().upper()
            _codpos=self.codpos.get()
            _telmov=self.telmov.get()
            _telfij=self.telfij.get()
            _corE=self.corE.get()
            _nomcon=self.nomcon.get().upper()
            _apellcon=self.apellcon.get().upper()
            _telcon=self.telcon.get()
            _relcon=self.relcon.get().upper()
            _check_2=self.check_2.get()
            _check_3=self.check_3.get()
            _check_4=self.check_4.get()
            _fecUltAct=self.hoy
            _id=self.id
            try:
                parametro1=[_nombre,_apellidos,_fecA,_fecN,_fecB,_motB,_dni,_profe,_deudapen,
                    _check_1,_CargoMember,_numsoc,_estciv,_discapaci,_calle,_muni,_prov,_pais,
                    _codpos,_telmov,_telfij,_corE,_nomcon,_apellcon,_telcon,_relcon,_check_2,
                    _check_3,_check_4,_fecUltAct,_id,]
                consulta1="""UPDATE socio SET nombre = ?,apellidos = ?,fecA = ?,
                            fecN = ?,fecB = ?,motB = ?,dni = ?,profe = ?,deudapen = ?,MemberDir = ?,
                            CargoMember = ?,numsoc = ?,estciv = ?,discapaci = ?,calle = ?,muni = ?,
                            prov = ?,pais = ?,codpos = ?,telmov = ?,telfij = ?,corE = ?,nomcon = ?,
                            apellcon = ?,telcon = ?,relcon = ?,RGPD = ?,WhatsApp = ?,ImgOk = ?,
                            fecUltAct = ?  WHERE id = ?"""
                with sqlite3.connect("database.db") as conn:
                     cursor=conn.cursor()
                     cursor.execute(consulta1,parametro1)                    
                     conn.commit
                     messagebox.showinfo(title="Modificacion",message="MODIFICACION REALIZADA CON EXITO")
                     self.limpiar_campos()
                     self.id=-1
            except sqlite3.OperationalError as error:
                    print("Eror en Modificacion BD: ", error)

#--> Vamos a crear el metodo de listar la informacion de los socios, escogiendo los campos fundamentales.
#    Realmente no se está listando, sino exportando un fichero, en formato PDF o xlsx.
    def listar_socios(self):
        pass

#--> Creamos los widgets y variables para Socios.
    def widgets(self):
        socios=Label(self,text="SOCIOS",bg="greenyellow",font="Arial 18")
        socios.pack()
        socios.place(x=0,y=0,height=30,width=1200)
        self.frame=Frame(self,bg="lime green",bd=15,relief="groove")   
        self.frame.place(x=0,y=30,width=1200,height=800) 
        self.check_1=IntVar()
        self.check_2=IntVar()
        self.check_3=IntVar()
        self.check_4=IntVar()
        self.hoy=(datetime.today().strftime("%Y-%m-%d"))
        self.fecha=IntVar
        self.valido=False
        self.formato=ttk.Combobox(self,font="16",values=["xlsx","PDF"])
        self.formato.place(x=755,y=665)
        self.btnexportar=self.botones(740,580,"LISTADO","blue","white",cmd=self.listar_socios)

#---> vamos a definir todos los campos de entrada de socios.  
#--> Nombre (nombre)      
        lblnombre=Label(self.frame,text="Nombre:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblnombre.place(x=5,y=15)
        self.nombre=Entry(self.frame,width=20,relief="raised",font="Ariel 13")
        self.nombre.place(x=80,y=15,height=25)  
#--> Apellidos (apellidos)        
        lblapellidos=Label(self.frame,text="Apellidos :",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblapellidos.place(x=295,y=15)
        self.apellidos=Entry(self.frame,width=50,relief="raised",font="Ariel 13")
        self.apellidos.place(x=380,y=15,height=25)    

#--> FECHAS
        lblfofe=Label(self.frame,text=">> FECHAS: aaaa-mm-dd <<",font="Ariel 12",bg="orange",relief="sunken")
        lblfofe.place(x=5,y=55)
#--> Fecha Alta (fecA)
        lblfecA=Label(self.frame,text="Fecha Alta:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblfecA.place(x=250,y=55)
        self.fecA=Entry(self.frame,width=10,relief="raised",font="Ariel 13")
        self.fecA.place(x=345,y=55,height=25)      
#--> Fecha Nacimiento (fecN)
        lblfecN=Label(self.frame,text="Fecha Nacimiento:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblfecN.place(x=445,y=55)
        self.fecN=Entry(self.frame,width=10,relief="raised",font="Ariel 13")
        self.fecN.place(x=590,y=55,height=25)  
#--> Fecha Baja (fecB), Motivo de baja(motB)
        lblfecB=Label(self.frame,text="Fecha Baja:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblfecB.place(x=5,y=95)
        self.fecB=Entry(self.frame,width=10,relief="raised",font="Ariel 13")
        self.fecB.place(x=100,y=95,height=25)      
        lblmotB=Label(self.frame,text="Motivo Baja:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblmotB.place(x=200,y=95)
        self.motB=Entry(self.frame,width=25,relief="raised",font="Ariel 13")
        self.motB.place(x=300,y=95,height=25)  

#--> D.N.I. (dni), Profesion (profe), Deuda pendiente socio (deudapen), Miembro de la Directiva (MemberDir), 
#    Cargo (CargoMember)
        lbldni=Label(self.frame,text="D.N.I.:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lbldni.place(x=5,y=135)
        self.dni=Entry(self.frame,width=12,relief="raised",font="Ariel 13")
        self.dni.place(x=60,y=135,height=25)  
        lblprofe=Label(self.frame,text="Profesion:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblprofe.place(x=165,y=135)
        self.profe=Entry(self.frame,width=20,relief="raised",font="Ariel 13")
        self.profe.place(x=250,y=135,height=25)      
        lbldeudapen=Label(self.frame,text="Deuda pendiente:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lbldeudapen.place(x=445,y=135)
        self.deudapen=Entry(self.frame,width=6,relief="raised",font="Ariel 13")
        self.deudapen.place(x=580,y=135,height=25) 
        lbleuro=Label(self.frame,text="€",font="Ariel 14",bg="aquamarine",relief="sunken")
        lbleuro.place(x=640,y=135)
        ChkMemberDir=Checkbutton(self.frame,text="Miembro de la Directiva S/N",onvalue=1,offvalue=0,
        variable=self.check_1,font="Ariel 12",bg="aquamarine")
        ChkMemberDir.place(x=685,y=135,height=25)
        lblCargoMember=Label(self.frame,text="Cargo:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblCargoMember.place(x=920,y=135)
        self.CargoMember=Entry(self.frame,width=15,relief="raised",font="Ariel 13")
        self.CargoMember.place(x=985,y=135,height=25)      

#--> Numero de Socio (numsoc), Estado civil (estciv), Grado Discapacidad (discapaci).
        lblnumsoc=Label(self.frame,text="Numero de Socio:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblnumsoc.place(x=5,y=175)
        self.numsoc=Entry(self.frame,width=7,relief="raised",font="Ariel 13")
        self.numsoc.place(x=150,y=175,height=25)      
        lblestciv=Label(self.frame,text="Estado Civil:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblestciv.place(x=250,y=175)
        self.estciv=Entry(self.frame,width=15,relief="raised",font="Ariel 13")
        self.estciv.place(x=350,y=175,height=25)      
        lbldiscapaci=Label(self.frame,text="Grado Discapacidad:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lbldiscapaci.place(x=530,y=175)
        self.discapaci=Entry(self.frame,width=4,relief="raised",font="Ariel 13")
        self.discapaci.place(x=690,y=175,height=25)      
        lblporcien=Label(self.frame,text="%",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblporcien.place(x=735,y=175)
#--> Voy a crear un texto y un entry para reflejar el ultimo numero de socio.
        lblultnumsoc=Label(self.frame,text="Ultimo nº socio:",font="Ariel 12",bg="greenyellow",relief="sunken")
        lblultnumsoc.place(x=5,y=220)
        self.ultnumsoc=Entry(self.frame,width=7,relief="raised",font="Ariel 13",bg="greenyellow")
        self.ultnumsoc.place(x=130,y=220,height=25)      
#--> Voy a crear un texto y un entry para reflejar el ultimo numero de No-socio.
        lblultnumNosoc=Label(self.frame,text="Ultimo nº No-socio:",font="Ariel 12",bg="greenyellow",relief="sunken")
        lblultnumNosoc.place(x=530,y=220)
        self.ultnumNosoc=Entry(self.frame,width=7,relief="raised",font="Ariel 13",bg="greenyellow")
        self.ultnumNosoc.place(x=680,y=220,height=25)     

#--> DIRECCION
#--> Calle (calle-Numero-Piso-Letra-Escalera) 
        lbldirec=Label(self.frame,text=">> DIRECCION <<",font="16",bg="orange",relief="sunken")
        lbldirec.place(x=340,y=220)
        lblcalle=Label(self.frame,text="Calle-Numero-Piso-Letra-Escal.:",font="Ariel 12",
        bg="aquamarine",relief="sunken")
        lblcalle.place(x=5,y=260)
        self.calle=Entry(self.frame,width=50,relief="raised",font="Ariel 13")
        self.calle.place(x=245,y=260,height=25)       

#--> Ciudad/Municipio (muni), Provincia (prov), Pais (pais) Codigo postal (codpos).        
        lblmuni=Label(self.frame,text="Ciudad:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblmuni.place(x=5,y=300)
        self.muni=Entry(self.frame,width=20,relief="raised",font="Ariel 13")
        self.muni.place(x=75,y=300,height=25)     
        lblprov=Label(self.frame,text="Provincia:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblprov.place(x=275,y=300)
        self.prov=Entry(self.frame,width=20,relief="raised",font="Ariel 13")
        self.prov.place(x=360,y=300,height=25)     
        lblpais=Label(self.frame,text="Pais:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblpais.place(x=550,y=300)
        self.pais=Entry(self.frame,width=15,relief="raised",font="Ariel 13")
        self.pais.place(x=600,y=300,height=25)  
        lblcodpos=Label(self.frame,text="Cod/postal:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblcodpos.place(x=755,y=300)
        self.codpos=Entry(self.frame,width=5,relief="raised",font="Ariel 13")
        self.codpos.place(x=855,y=300,height=25)   

#--> Telefono movil (telmov), Telefono Fijo (telfij), Correo electronico (corE)    
        lbltelmov=Label(self.frame,text="Tlfno. Movil:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lbltelmov.place(x=5,y=350)
        self.telmov=Entry(self.frame,width=12,relief="raised",font="Ariel 13")
        self.telmov.place(x=100,y=350,height=25)  
        lbltelfij=Label(self.frame,text="Tlfno. Fijo:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lbltelfij.place(x=225,y=350)
        self.telfij=Entry(self.frame,width=12,relief="raised",font="Ariel 13")
        self.telfij.place(x=315,y=350,height=25)  
        lblcorE=Label(self.frame,text="Correo @:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblcorE.place(x=440,y=350)
        self.corE=Entry(self.frame,width=40,relief="raised",font="Ariel 13")
        self.corE.place(x=530,y=350,height=25)  

#--> PERSONA DE CONTACTO
        lblpercon=Label(self.frame,text=">> PERSONA DE CONTACTO <<",font="16",bg="orange",relief="sunken")
        lblpercon.place(x=340,y=390)
#--> Nombre (nomcon), Apellidos (apellcon)      
        lblnomcon=Label(self.frame,text="Nombre:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblnomcon.place(x=5,y=420)
        self.nomcon=Entry(self.frame,width=20,relief="raised",font="Ariel 13")
        self.nomcon.place(x=80,y=420,height=25)
        lblapellcon=Label(self.frame,text="Apellidos :",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblapellcon.place(x=295,y=420)
        self.apellcon=Entry(self.frame,width=50,relief="raised",font="Ariel 13")
        self.apellcon.place(x=380,y=420,height=25)

#--> Telefono de contacto (telcon), Relacion de contacto (relcon)        
        lbltelcon=Label(self.frame,text="Telefono contacto:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lbltelcon.place(x=5,y=460)
        self.telcon=Entry(self.frame,width=12,relief="raised",font="Ariel 13")
        self.telcon.place(x=150,y=460,height=25)
        lblrelcon=Label(self.frame,text="Relacion contacto:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblrelcon.place(x=260,y=460)
        self.relcon=Entry(self.frame,width=20,relief="raised",font="Ariel 13")
        self.relcon.place(x=405,y=460,height=25) 

#--> 3 checkbutton para la aceptacion del nuevo Reglamento General de Proteccion de Datos.
        ChkRGPD=Checkbutton(self.frame,text="Acepto las condiciones expresadas en el aviso legal del RGPD",
        onvalue=1,offvalue=0,variable=self.check_2,font="Ariel 12",bg="aquamarine")
        ChkRGPD.place(x=5,y=490,height=25)
        ChkWhatsApp=Checkbutton(self.frame,text="Solicito mi inclusión en los grupos de Whatsapp de Acarmas",
        onvalue=1,offvalue=0,variable=self.check_3,font="Ariel 12",bg="aquamarine")
        ChkWhatsApp.place(x=520,y=490,height=25)
        ChkImgOk=Checkbutton(self.frame,text="Autorizo el uso de mi imagen en las publicaciones de Acarmas",
        onvalue=1,offvalue=0,variable=self.check_4,font="Ariel 12",bg="aquamarine")
        ChkImgOk.place(x=5,y=530,height=25)

#--> Botones de las acciones "ALTA" - "CONSULTA" - "MODIFICACIONES/BAJA" 
        btnAlSo=self.botones(20,580,"ALTA","blue","white",cmd=self.altasocio)    
        btnCoSo=self.botones(250,580,"CONSULTA","blue","white",cmd=self.consulta_socio)
        btnMoSo=self.botones(500,580,"MODIFICACION/BAJA","blue","white",cmd=self.modifica_socio)        
        btnCancelar=self.botones(950,580,"CANCELAR","blue","red",cmd=self.cancelar_operacion)

#==============================================================================================
#                    >>  REPORTE - Pertenece a los informes de Socios <<
#==============================================================================================

class Reporte:
    def __init__(self): 
        super(Reporte,self).__init__()
        self.titulo="LISTA DE SOCIOS"
        self.nombre="INFORME.pdf"
        
#==============================================================================================
#                                        >>  ACTIVIDAD <<
#==============================================================================================

class Actividad(Frame):
    def __init__(self,padre): 
        super().__init__(padre)
        self.id=-1   
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
        btn.place(x=x,y=y,width=150,height=40)  
        return btn

#--> Funcion para validar las fechas.
    def valfecha(self,fechv):
        if fechv == ' ':
            return False
        else:
            try:
                fechv=datetime.strptime(fechv,'%Y-%m-%d').date()            
                return True
            except ValueError:                                
                return False

#--> Funcion acceso a Base de Datos
    def eje_consulta(self,consulta,parametros=()):
        db=Datos()       
        result=db.consultas(consulta,parametros)
        return result        

#--> Funcion para validar campos de entrada minimos
    def validacion(self,_claveAct,_nombreAct,_responAct,_finiAct):        
        if len(_claveAct) > 0 and len(_nombreAct) > 0 and len(_responAct) > 0 and len(_finiAct) > 0:
          return True
        
#    Con el boton "REFRESCAR". Se borra el contenido del treview, y se seleccionan todos los registros 
#    de la BD de actividad.
    def mostrar(self):
        colores=("pink1","LightPink1")
        for color in colores:
            self.tre.tag_configure(color,background=color)
        result=self.tre.get_children()
        for i in result:
            self.tre.delete(i)
        conn=sqlite3.connect("database.db")
        cursor=conn.cursor()    
        result=cursor.execute("SELECT * FROM actividad ORDER BY claveAct,id DESC")  
        colores=itertools.cycle(colores)   
        for elem,color in zip(result,colores):
            self.tre.insert("",0,text=elem[0],tag=("fuente",color),values=(elem[1],elem[2],elem[3],elem[4],
                                                                           elem[5],elem[10],elem[11],elem[8],elem[6],elem[7],elem[9]))
        if len(self.tre.get_children()) > 0:
            self.tre.selection_set(self.tre.get_children()[0])   

#--> Funcion de dar de alta una actividad al pulsar el boton "ALTA "
    def alta_actividad(self):
        _claveAct=self.claveAct.get().upper()
        _nombreAct=self.nombreAct.get().upper()
        _responAct=self.responAct.get().upper()           
        _finiAct=self.finiAct.get()
        _ffinAct=self.ffinAct.get()
        _cosresAct=self.cosresAct.get()
        if _cosresAct == False or _cosresAct == "":
            _cosresAct=0.0
        _cosparAct=self.cosparAct.get()
        if _cosparAct == False or _cosparAct == "":
            _cosparAct=0.0
        _nummaxAct=self.nummaxAct.get()
        _diasemAct=self.diasemAct.get().upper()
        _HiniAct=self.HiniAct.get().upper()
        _HfinAct=self.HfinAct.get().upper()

#--> Validamos que se introduzca la clave de Actividad, el nombre de la Actividad, el responsable
#    de la Actividad y la fecha inicial, como minimo.
        if self.validacion(_claveAct,_nombreAct,_responAct,_finiAct):       
           fechv=_finiAct
           #---> Validamos fecha de de inicio de la Actividad              
           if self.valfecha(fechv) == False:
            messagebox.showerror(title="Fecha INICIO de Actividad",message="Fecha debe ser formato AAAA-MM-DD y Valida")                
           else:  
              if self.id==-1:  
                try:                
                    consulta=("""INSERT INTO actividad VALUES(null,?,?,?,?,?,?,?,?,?,?,?,?,?)""")
                    parametros=(_claveAct,_nombreAct,_responAct,_finiAct,_ffinAct,
                                _cosresAct,_cosparAct,_nummaxAct,_diasemAct,_HiniAct,
                                _HfinAct,usuario,self.hoy)                    
                    self.eje_consulta(consulta,parametros)
                    messagebox.showinfo(title="Alta Actividad",message="ALTA REALIZADA CON EXITO")
                    self.limpiar()       
                    self.mostrar()
                except:  
                    messagebox.showwarning(title="Error Alta",message="Error en Alta de actividad")           
              else:           
                consulta1=f"UPDATE actividad SET claveAct=?,nombreAct=?,responAct=?,finiAct=?,ffinAct=?,cosresAct=?,cosparAct=?,nummaxAct=?,diasemAct=?,HiniAct=?,HfinAct=?,userAct=?,fecUltActAct=? WHERE id={self.id}"
                parametro1=(_claveAct,_nombreAct,_responAct,_finiAct,_ffinAct,
                                _cosresAct,_cosparAct,_nummaxAct,_diasemAct,_HiniAct,
                                _HfinAct,usuario,self.hoy)
                with sqlite3.connect("database.db") as conn:
                    cursor=conn.cursor()
                    cursor.execute(consulta1,parametro1)
                    self.id=-1
                    conn.commit                    
                    messagebox.showinfo(title="Modificacion",message="MODIFICACION REALIZADA CON EXITO")    
                self.limpiar()
                self.mostrar()
        else:        
         messagebox.showwarning(title="Error Alta",message="Rellene Clave, Nombre, Responsable y Fecha inicial como minimo")   
    
#--> Limpiamos los campos de entrada.
    def limpiar(self):
        self.claveAct.delete(0,END)
        self.nombreAct.delete(0,END)        
        self.responAct.delete(0,END)
        self.finiAct.delete(0,END)
        self.ffinAct.delete(0,END)
        self.cosresAct.delete(0,END)
        self.cosparAct.delete(0,END)
        self.nummaxAct.delete(0,END)
        self.diasemAct.delete(0,END)
        self.HiniAct.delete(0,END)
        self.HfinAct.delete(0,END)

#--> Funcion para seleccionar un registro en el treeview para actualizar
    def seleccionar(self):
        self.btn_actualizar("disable")
        self.btn_cancelar("normal")
        self.btn_agregar("normal")
        self.btn_eliminar("disable")
        self.btn_refrescar("disable")           
        id=self.tre.item(self.tre.selection())["text"]
        if id=="":
            messagebox.showerror(title="ACTUALIZAR",message="Error, Seleccione una Actividad")
        else:
            self.id=id
            self.limpiar()
            valor=self.tre.item(self.tre.selection())["values"]
            self.claveAct.insert(0,valor[0])
            self.nombreAct.insert(0,valor[1])            
            self.responAct.insert(0,valor[2])
            self.finiAct.insert(0,valor[3])
            self.ffinAct.insert(0,valor[4])
            self.HiniAct.insert(0,valor[5])
            self.HfinAct.insert(0,valor[6])
            self.nummaxAct.insert(0,valor[7])
            self.cosresAct.insert(0,valor[8])
            self.cosparAct.insert(0,valor[9])
            self.diasemAct.insert(0,valor[10])
 
#--> Funcion para eliminar un registro de Actividad. Se borra el registro. Pero esto implica que 
#    se ELIMINARAN TODOS los registros de esta actividad de la B.D. de participes.
    def eliminar(self):  
        clavePar2=""
        id=self.tre.item(self.tre.selection())["text"]
        valor=self.tre.item(self.tre.selection())["values"]
        clavePar2=valor[0]
        res=messagebox.askquestion(title="Eliminar",message="¿Esta seguro de querer eliminar el la Actividad -- Se ELIMINARAN todos los participes?")
        if res=="yes":
            consulta="DELETE FROM actividad WHERE id=?"
            parametros=(id,)
            self.eje_consulta(consulta,parametros)
            messagebox.showinfo(title="Baja Actividad",message="BAJA DE ACTIVIDAD REALIZADA CON EXITO")            
            self.eliminar_participes(clavePar2)
        self.mostrar()   
        self.btn_agregar("normal")
        self.btn_refrescar("normal")
        self.btn_actualizar("disable")
        self.btn_cancelar("disable")
        self.btn_eliminar("disable")       

#--> Funcion eliminar los participes inscritos en una Actividad.
    def eliminar_participes(self,clavePar2):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            consulta ='SELECT * FROM participes WHERE clavePar = ?'
            parametros = (clavePar2,)
            cursor.execute(consulta, parametros)
            resultado = cursor.fetchall()
            conn.commit()
            if resultado is None:
                messagebox.showinfo(title="Eliminar Participes",message="No existen Participes para esta Actividad")                 
            else:
                consulta="DELETE FROM participes WHERE clavePar=?"
                parametros=(clavePar2,)
                self.eje_consulta(consulta,parametros)
                messagebox.showinfo(title="Baja Participes",message="BAJA DE PARTICIPES REALIZADA CON EXITO")            

#--> Funcion que limpia los campos al cancelar una operacion.
    def cancelar(self):
        self.limpiar()

#--> Control de los eventos de los botones, activandolos o desactivandolos
    def evento1(self,estado):
        self.btn_actualizar("normal")
        self.btn_eliminar("normal")
        self.btn_agregar("disable")
        self.btn_refrescar("disable")   

    def evento2(self,estado):
        self.btn_actualizar("disable")
        self.btn_eliminar("disable")
        self.btn_agregar("normal")
        self.btn_refrescar("normal") 
        self.btn_cancelar("disable")          
               
#--> Definicion generica del estado de los botones.
    def btn_agregar(self,estado):
        self.btnagregar.configure(state=estado)
    def btn_refrescar(self,estado):
        self.btnrefrescar.configure(state=estado)    
    def btn_actualizar(self,estado):
        self.btnactualizar.configure(state=estado)    
    def btn_eliminar(self,estado):
        self.btneliminar.configure(state=estado)    
    def btn_cancelar(self,estado):
        self.btncancelar.configure(state=estado)    
        self.limpiar()

    def dia_semana(self):
        pass

    def widgets(self):
        actividad=Label(self,text="ACTIVIDADES",bg="#33CBFF",font="Arial 18")
        actividad.pack()
        actividad.place(x=0,y=0,height=30,width=1200)
        self.frame=Frame(self,bg="#9ACDD7",bd=15,relief="groove")   
        self.frame.place(x=0,y=30,width=1200,height=800) 
        self.hoy=(datetime.today().strftime("%Y-%m-%d"))
        clavePar2 = ''

#--> Nombre de la actividad (nombreAct)      
        lblnombreAct=Label(self.frame,text="Nombre actividad:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblnombreAct.place(x=10,y=15)
        self.nombreAct=Entry(self.frame,width=20,relief="raised",font="Ariel 13")
        self.nombreAct.place(x=145,y=15,height=25)

#--> Responsable de la actividad (responAct)      
        lblresponAct=Label(self.frame,text="Responsable actividad:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblresponAct.place(x=340,y=15)
        self.responAct=Entry(self.frame,width=20,relief="raised",font="Ariel 13")
        self.responAct.place(x=510,y=15,height=25)   

#--> Fecha de inicio de la actividad (finiAct)
        lblfiniAct=Label(self.frame,text="Fecha inicio Act.:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblfiniAct.place(x=710,y=15)
        self.finiAct=Entry(self.frame,width=10,relief="raised",font="Ariel 13")
        self.finiAct.place(x=840,y=15,height=25)       

#--> Fecha fin de la actividad (ffinAct)
        lblffinAct=Label(self.frame,text="Fecha fin Act.:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblffinAct.place(x=950,y=15)
        self.ffinAct=Entry(self.frame,width=10,relief="raised",font="Ariel 13")
        self.ffinAct.place(x=1060,y=15,height=25)       

#--> Clave de la actividad (claveAct)
        lblclaveAct=Label(self.frame,text="Clave Actividad:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblclaveAct.place(x=10,y=45)
        self.claveAct=Entry(self.frame,width=12,relief="raised",font="Ariel 13")
        self.claveAct.place(x=130,y=45,height=25)       

#--> Coste mes Responsable (cosresAct)
        lblcosresAct=Label(self.frame,text="Coste mes Responsable:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblcosresAct.place(x=250,y=45)
        self.cosresAct=Entry(self.frame,width=5,relief="raised",font="Ariel 13")
        self.cosresAct.place(x=440,y=45,height=25)       
        lbleuroR=Label(self.frame,text="€",font="Ariel 12",bg="aquamarine",relief="sunken")
        lbleuroR.place(x=490,y=45)

#--> Coste mes Participe (cosparAct)
        lblcosparAct=Label(self.frame,text="Coste mes Participe:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblcosparAct.place(x=530,y=45)
        self.cosparAct=Entry(self.frame,width=5,relief="raised",font="Ariel 13")
        self.cosparAct.place(x=690,y=45,height=25)
        lbleuroP=Label(self.frame,text="€",font="Ariel 12",bg="aquamarine",relief="sunken")
        lbleuroP.place(x=740,y=45)

#--> Numero maximo de Participes por Actividad (nummaxAct)
        lblnummaxAct=Label(self.frame,text="Numero maximo Participes/Activi.:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblnummaxAct.place(x=800,y=45)
        self.nummaxAct=Entry(self.frame,width=8,relief="raised",font="Ariel 13")
        self.nummaxAct.place(x=1070,y=45,height=25)

#--> Dia semanal de la actividad (diasemAct)
        lbldiasemAct=Label(self.frame,text="Dia semanal Actividad:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lbldiasemAct.place(x=10,y=80)
        self.diasemAct=Entry(self.frame,width=12,relief="raised",font="Ariel 13")
        self.diasemAct.place(x=180,y=80,height=25)       
        lblnomdiaAct=Label(self.frame,text="Lunes,Martes,Miercoles,Jueves,Viernes,Sabado,Domingo",font="Ariel 8",bg="aquamarine",relief="sunken")
        lblnomdiaAct.place(x=10,y=110)

#--> Hora comienzo de la actividad (HiniAct)
        lblHiniAct=Label(self.frame,text="Hora inicio Actividad:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblHiniAct.place(x=360,y=80)
        self.HiniAct=Entry(self.frame,width=5,relief="raised",font="Ariel 13")
        self.HiniAct.place(x=520,y=80,height=25)    
        lblhorminAct=Label(self.frame,text="Hora/minutos : hh:mm ",font="Ariel 8",bg="aquamarine",relief="sunken")
        lblhorminAct.place(x=360,y=110)           

#--> Hora finalizacion de la actividad (HfinAct)
        lblHfinAct=Label(self.frame,text="Hora final Actividad:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblHfinAct.place(x=610,y=80)
        self.HfinAct=Entry(self.frame,width=5,relief="raised",font="Ariel 13")
        self.HfinAct.place(x=765,y=80,height=25)      

#--> Botones de  "ALTA ACT.", "REFRESCAR", 
#    "MODIFICACION ACT.", "ELIMINAR ACT." y  "CANCELAR" de Actividad
 
        self.btnagregar=self.botones(45,650,"ALTA ACT.","blue","white",cmd=self.alta_actividad)
        self.btnrefrescar=self.botones(215,650,"REFRESCAR","blue","white",cmd=self.mostrar)
        self.btnactualizar=self.botones(395,650,"ACTUALIZAR ACT.","blue","white",cmd=self.seleccionar) 
        self.btnactualizar.configure(state="disable")
        self.btneliminar=self.botones(595,650,"ELIMINAR ACT.","blue","white",cmd=self.eliminar)
        self.btneliminar.configure(state="disable")        
        self.btncancelar=self.botones(795,650,"CANCELAR","blue","white",cmd=self.cancelar) 
        self.btncancelar.configure(state="disable")   

#--> Creo ahora el Treframe con su Treeview con sus cabeceras de columnas (Heading)
#    Codigo(id) [0], Nombre de la actividad (nombreAct) [1], 
#    Responsable de la actividad (responAct) [2], Fecha de inicio de la actividad (finiact) [3]  

        treFrame=Frame(self.frame,bg="cyan")
        treFrame.place(x=15,y=140,width=1150,height=450)
        scroll=Scrollbar(treFrame)
        scroll.pack(side=RIGHT,fill=Y)
        self.tre=ttk.Treeview(treFrame,yscrollcommand=scroll.set,height=40,columns=("#0","#1","#2","#3","#4","#5","#6","#7","#8","#9","#10"))
        self.tre.pack() 
        scroll.config(command=self.tre.yview)
        for i in [2,3]:
            self.tre.column(f"#{i}",width=180,anchor=CENTER)
        colors=("cyan","green")
        for color in colors:
            self.tre.tag_configure(color,background=color)
        self.tre.column("#0",width=35,anchor=CENTER)
        self.tre.column("#1",width=110,anchor=CENTER)
        self.tre.column("#4",width=85,anchor=CENTER)
        self.tre.column("#5",width=85,anchor=CENTER)
        self.tre.column("#6",width=80,anchor=CENTER)
        self.tre.column("#7",width=80,anchor=CENTER)
        self.tre.column("#8",width=70,anchor=CENTER)
        self.tre.column("#9",width=70,anchor=CENTER)
        self.tre.column("#10",width=70,anchor=CENTER)
        self.tre.column("#11",width=100,anchor=CENTER)       
        self.tre.heading("#0",text="COD.",anchor=CENTER)
        self.tre.heading("#1",text="CLAVE ACTIVIDAD",anchor=CENTER)
        self.tre.heading("#2",text="NOMBRE ACTIVIDAD",anchor=CENTER)
        self.tre.heading("#3",text="RESPONSABLE ACTIVIDAD",anchor=CENTER)        
        self.tre.heading("#4",text="FECHA INICIO",anchor=CENTER)
        self.tre.heading("#5",text="FECHA FIN",anchor=CENTER)
        self.tre.heading("#6",text="HORA INICIO",anchor=CENTER)
        self.tre.heading("#7",text="HORA FIN",anchor=CENTER)
        self.tre.heading("#8",text="NUM. PARTI.",anchor=CENTER)
        self.tre.heading("#9",text="COST.RESP.",anchor=CENTER)
        self.tre.heading("#10",text="COST.PARTI.",anchor=CENTER)
        self.tre.heading("#11",text="DIA SEM.",anchor=CENTER)
        try:            
           self.mostrar()
        except:
            pass
        self.tre.bind("<Double-1>",self.evento1)
        self.tre.bind("<Button-1>",self.evento2)              

#==============================================================================================
#                                 >>  PARTICIPES (ACTIVIDADES) <<
#==============================================================================================

class Participes(Frame):
    def __init__(self,padre):
        super().__init__(padre)
        self.pack()
        self.place(x=0,y=0,width=1200,height=800)
        self.id=-1 
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
        btn.place(x=x,y=y,width=150,height=40)    
        return btn

#--> Funcion para validar las fechas.
    def valfecha(self,fechv):
        if fechv == ' ':
            return False
        else:
            try:
                fechv=datetime.strptime(fechv,'%Y-%m-%d').date()            
                return True
            except ValueError:                                
                return False

#--> Funcion acceso a Base de Datos
    def eje_consulta(self,consulta,parametros=()):
        db=Datos()       
        result=db.consultas(consulta,parametros)
        return result        

#--> Funcion para validar campos de entrada minimos
    def validacion(self,_clavePar,_nombrePar,_apellidosPar):        
        if len(_clavePar) > 0 and len(_nombrePar) > 0 and len(_apellidosPar) > 0:
          return True

#    Con el boton "REFRESCAR". Se borra el contenido del treview, y se seleccionan todos los registros 
#    de la BD de participes.
    def mostrar(self):
        colores=("pink1","LightPink1")
        for color in colores:
            self.tre.tag_configure(color,background=color)
        result=self.tre.get_children()
        for i in result:
            self.tre.delete(i)
        conn=sqlite3.connect("database.db")
        cursor=conn.cursor()    
        result=cursor.execute("SELECT * FROM participes ORDER BY clavePar,esperaPar DESC")  
        colores=itertools.cycle(colores)   
        for elem,color in zip(result,colores):
            self.tre.insert("",0,text=elem[0],tag=("fuente",color),values=(elem[1],elem[2],elem[3],elem[4]))
        if len(self.tre.get_children()) > 0:
            self.tre.selection_set(self.tre.get_children()[0])   

#--> Funcion de dar de alta un participe de una Actividad al pulsar el boton "ALTA "
    def alta_participe(self):
        _clavePar=self.clavePar.get().upper()
        _nombrePar=self.nombrePar.get().upper()
        _apellidosPar=self.apellidosPar.get().upper()           
        _esperaPar=self.esperaPar.get().upper() 
        if _esperaPar == "":
            _esperaPar = "N"    
#--> Validamos que se introduzca la clave de Participe/Actividad, el nombre del participe,
#    el apellido del participe y si es activo o en lista de espera, si este ultimo campo no se 
#    cumplimenta se asume automatico que es "N".

        if self.validacion(_clavePar,_nombrePar,_apellidosPar):   
            if self.id==-1:  
                try:                
                    consulta=("""INSERT INTO participes VALUES(null,?,?,?,?,?,?)""")
                    parametros=(_clavePar,_nombrePar,_apellidosPar,_esperaPar,usuario,self.hoy)                    
                    self.eje_consulta(consulta,parametros)                                           
                    messagebox.showinfo(title="Alta Participe",message="ALTA REALIZADA CON EXITO")
                    self.limpiar()       
                    self.mostrar()
                except:  
                    messagebox.showwarning(title="Error Alta",message="Error en Alta de actividad")           
            else:           
                consulta1=f"UPDATE participes SET clavePar=?,nombrePar=?,apellidosPar=?,esperaPar=?,userPar=?,fecUltActPar=? WHERE id={self.id}"
                parametro1=(_clavePar,_nombrePar,_apellidosPar,_esperaPar,usuario,self.hoy)
                with sqlite3.connect("database.db") as conn:
                    cursor=conn.cursor()
                    cursor.execute(consulta1,parametro1)
                    self.id=-1
                    conn.commit                    
                    messagebox.showinfo(title="Modificacion",message="MODIFICACION REALIZADA CON EXITO")    
                self.limpiar()
                self.mostrar()
        else:        
         messagebox.showwarning(title="Error Alta",message="Rellene Clave, Nombre y Apellidos como minimo")   

#--> Limpiamos los campos de entrada.
    def limpiar(self):
        self.clavePar.delete(0,END)
        self.nombrePar.delete(0,END)        
        self.apellidosPar.delete(0,END)
        self.esperaPar.delete(0,END)

#--> Funcion para seleccionar un registro en el treeview para actualizar
    def seleccionar(self):
        self.btn_actualizar("disable")
        self.btn_cancelar("normal")
        self.btn_agregar("normal")
        self.btn_eliminar("disable")
        self.btn_refrescar("disable")           
        id=self.tre.item(self.tre.selection())["text"]
        if id=="":
            messagebox.showerror(title="ACTUALIZAR",message="Error, Seleccione una Actividad")
        else:
            self.id=id
            self.limpiar()
            valor=self.tre.item(self.tre.selection())["values"]
            self.clavePar.insert(0,valor[0])
            self.nombrePar.insert(0,valor[1])            
            self.apellidosPar.insert(0,valor[2])
            self.esperaPar.insert(0,valor[3])

#--> Funcion para eliminar un registro de un participe. Se borra solo este registro. 
    def eliminar(self):  
        #clavePar2=""
        id=self.tre.item(self.tre.selection())["text"]
        #valor=self.tre.item(self.tre.selection())["values"]
        #print("valor :",valor)
        #clavePar2=valor[0]
        #print("clavePar2 :",clavePar2)
        res=messagebox.askquestion(title="Eliminar",message="¿Esta seguro de querer eliminar el participe?")
        if res=="yes":
            consulta="DELETE FROM participes WHERE id=?"
            parametros=(id,)
            self.eje_consulta(consulta,parametros)
        self.mostrar()   
        self.btn_agregar("normal")
        self.btn_refrescar("normal")
        self.btn_actualizar("disable")
        self.btn_cancelar("disable")
        self.btn_eliminar("disable")           

#--> Funcion que limpia los campos al cancelar una operacion.
    def cancelar(self):
        self.limpiar()

#--> Control de los eventos de los botones, activandolos o desactivandolos
    def evento1(self,estado):
        self.btn_actualizar("normal")
        self.btn_eliminar("normal")
        self.btn_agregar("disable")
        self.btn_refrescar("disable")   

    def evento2(self,estado):
        self.btn_actualizar("disable")
        self.btn_eliminar("disable")
        self.btn_agregar("normal")
        self.btn_refrescar("normal") 
        self.btn_cancelar("disable")          
               
#--> Definicion generica del estado de los botones.
    def btn_agregar(self,estado):
        self.btnagregar.configure(state=estado)
    def btn_refrescar(self,estado):
        self.btnrefrescar.configure(state=estado)    
    def btn_actualizar(self,estado):
        self.btnactualizar.configure(state=estado)    
    def btn_eliminar(self,estado):
        self.btneliminar.configure(state=estado)    
    def btn_cancelar(self,estado):
        self.btncancelar.configure(state=estado)    
        self.limpiar()

    def widgets(self):
        actividad=Label(self,text="PARTICIPES",bg="#3368FF",font="Arial 18")
        actividad.pack()
        actividad.place(x=0,y=0,height=30,width=1200)
        self.frame=Frame(self,bg="#339EFF",bd=15,relief="groove")   
        self.frame.place(x=0,y=30,width=1200,height=800) 
        self.hoy=(datetime.today().strftime("%Y-%m-%d"))

#--> Clave de la actividad/Participe (clavePar)
        lblclavePar=Label(self.frame,text="Clave Actividad/Participe:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblclavePar.place(x=15,y=15)
        self.clavePar=Entry(self.frame,width=12,relief="raised",font="Ariel 13")
        self.clavePar.place(x=210,y=15,height=25)    
#--> Nombre participe (nombrePar)      
        lblnombrePar=Label(self.frame,text="Nombre:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblnombrePar.place(x=325,y=15)
        self.nombrePar=Entry(self.frame,width=20,relief="raised",font="Ariel 13")
        self.nombrePar.place(x=400,y=15,height=25)  
#--> Apellidos (apellidos)        
        lblapellidosPar=Label(self.frame,text="Apellidos :",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblapellidosPar.place(x=610,y=15)
        self.apellidosPar=Entry(self.frame,width=50,relief="raised",font="Ariel 13")
        self.apellidosPar.place(x=700,y=15,height=25)    
#--> Clave de lista de espera S/N (esperaPar)
        lblesperaPar=Label(self.frame,text="Lista de espera S/N:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblesperaPar.place(x=15,y=45)
        self.esperaPar=Entry(self.frame,width=3,relief="raised",font="Ariel 13")
        self.esperaPar.place(x=170,y=45,height=25)    

#--> Botones de  "ALTA", "REFRESCAR", 
#    "MODIFICACION", "ELIMINAR" y  "CANCELAR" de un Participe
#---> Boton de acceso a Gestion de Participes 
        self.btnagregar=self.botones(45,650,"ALTA","blue","white",cmd=self.alta_participe)
        self.btnrefrescar=self.botones(215,650,"REFRESCAR","blue","white",cmd=self.mostrar)
        self.btnactualizar=self.botones(395,650,"ACTUALIZAR","blue","white",cmd=self.seleccionar) 
        self.btnactualizar.configure(state="disable")
        self.btneliminar=self.botones(595,650,"ELIMINAR","blue","white",cmd=self.eliminar)
        self.btneliminar.configure(state="disable")        
        self.btncancelar=self.botones(795,650,"CANCELAR","blue","white",cmd=self.cancelar) 
        self.btncancelar.configure(state="disable")   

#--> Creo ahora el Treframe con su Treeview con sus cabeceras de columnas (Heading)
#    Codigo(id) [0], Nombre de la actividad (nombreAct) [1], 
#    Responsable de la actividad (responAct) [2], Fecha de inicio de la actividad (finiact) [3]  
 
        treFrame=Frame(self.frame,bg="cyan")
        treFrame.place(x=15,y=100,width=1100,height=500)
        scroll=Scrollbar(treFrame)
        scroll.pack(side=RIGHT,fill=Y)
        self.tre=ttk.Treeview(treFrame,yscrollcommand=scroll.set,height=40,columns=("#0","#1","#2","#3","#4"))
        self.tre.pack() 
        scroll.config(command=self.tre.yview)
        colors=("cyan","green")
        for color in colors:
            self.tre.tag_configure(color,background=color)
        self.tre.column("#0",width=60,anchor=CENTER)
        self.tre.column("#1",width=200,anchor=CENTER)
        self.tre.column("#2",width=200,anchor=CENTER)
        self.tre.column("#3",width=450,anchor=CENTER)
        self.tre.column("#4",width=200,anchor=CENTER)       
        self.tre.heading("#0",text="CODIGO",anchor=CENTER)
        self.tre.heading("#1",text="CLAVE PARTICIPE/ACTIVIDAD",anchor=CENTER)
        self.tre.heading("#2",text="NOMBRE",anchor=CENTER)
        self.tre.heading("#3",text="APELLIDOS",anchor=CENTER)        
        self.tre.heading("#4",text="LISTA ESPERA S/N",anchor=CENTER)
        try:            
           self.mostrar()
        except:
            pass
        self.tre.bind("<Double-1>",self.evento1)
        self.tre.bind("<Button-1>",self.evento2) 

#==============================================================================================
#                                 >>  APUNTES / DIARIO <<
#==============================================================================================

class Apuntediario(Frame):
    def __init__(self,padre): 
        super().__init__(padre)
        self.id=-1
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
        btn.place(x=x,y=y,width=150,height=40)    
        return btn

#--> Funcion para recuperar el Saldo Total (suma de todos los importes de impDebeapu, restando
#    la suma de todos los importes de impHaberapu)
    def recuperar_saldo(self):
        with sqlite3.connect("database.db") as conn:
            cursor=conn.cursor()
            cursor.execute("SELECT sum(impDebeapu-impHaberapu)  FROM apunte ORDER BY id DESC")
            resultado=cursor.fetchone()
            if resultado is None:
                messagebox.showwarning(title="Error",message="NO EXISTE REGISTROS EN apuntes diarios") 
            else:   
                self.saldoFinal=resultado[0]
                self.saldoToapu.delete(0,END)
                self.saldoToapu.insert(END,resultado[0])
        conn.commit()

#--> Funcion para validar fecha de entrada.
    def valfecha(self,fechv):
        if fechv == ' ':
            return False
        else:
            try:              
                fechv=datetime.strptime(fechv,'%Y-%m-%d').date()            
                return True
            except ValueError:                                
                return False

#--> Funcion acceso a Base de Datos
    def eje_consulta(self,consulta,parametros=()):
        db=Datos()       
        result=db.consultas(consulta,parametros)
        return result

#--> Funcion para validar campos de entrada minimos
    def validacion(self,_fecAapu,_conceptoapu,_impDebeapu,_impHaberapu):
        
        if len(_fecAapu) > 0 and len(_conceptoapu) > 0 and (_impDebeapu != False or _impHaberapu != False):
          return True
        
#--> No uso el metodo "eje_consulta", por ser una select masiva sin parametros. 
#    bOTON "REFRESCAR". Se borra el contenido del treview, y se seleccionan todos los registros 
#    de la BD de apuntes.
    def mostrar(self):
        colores=("pink1","LightPink1")
        for color in colores:
            self.tre.tag_configure(color,background=color)
        result=self.tre.get_children()
        for i in result:
            self.tre.delete(i)
        conn=sqlite3.connect("database.db")
        cursor=conn.cursor()    
        result=cursor.execute("SELECT * FROM apunte ORDER BY id DESC")  
        colores=itertools.cycle(colores)   
        for elem,color in zip(result,colores):
            self.tre.insert("",0,text=elem[0],tag=("fuente",color),values=(elem[1],elem[2],elem[3],elem[4]))
        if len(self.tre.get_children()) > 0:
            self.tre.selection_set(self.tre.get_children()[0])   

#--> Antes de cada alta se borra el contenido del treview, para una vez realizada la alta, seleccionar
#    todos los registros de la BD de apuntes. Si self.id == -1, es una Alta, sino es una modificacion. 
    def altaapuntes(self):
        _fecAapu=self.fecAapu.get()
        _conceptoapu=self.conceptoapu.get().upper()
        _impDebeapu=self.impDebeapu.get()           
        _impHaberapu=self.impHaberapu.get() 
        if _impDebeapu == False or _impDebeapu == "":
            _impDebeapu=0.0
        if _impHaberapu == False or _impHaberapu == "":
            _impHaberapu=0.0            
        _impDebeapu=float(_impDebeapu)
        _impHaberapu=float(_impHaberapu)
#--> Validamos que se introduzca Fecha de alta, Concepto y un importe como minimo.
        if self.validacion(_fecAapu,_conceptoapu,_impDebeapu,_impHaberapu):       
           fechv=_fecAapu
           #---> Validamos fecha de alta              
           if self.valfecha(fechv) == False:
            messagebox.showerror(title="Fecha ALTA apuntes",message="Fecha debe ser formato AAAA-MM-DD y Valida")                
           else:  
              if self.id==-1:  
                self.recuperar_saldo()                    
                self.saldoFinal+=(_impDebeapu-_impHaberapu)
                try:                
                    consulta=("""INSERT INTO apunte VALUES(null,?,?,?,?,?,?,?)""")
                    parametros=(_fecAapu,_conceptoapu,_impDebeapu,_impHaberapu,
                    self.saldoFinal,usuario,self.hoy)
                    self.eje_consulta(consulta,parametros)                                           
                    messagebox.showinfo(title="Alta apuntes",message="ALTA REALIZADA CON EXITO")
                    self.limpiar()
                    self.recuperar_saldo()        
                    self.mostrar()
                except:  
                    messagebox.showwarning(title="Error Alta",message="Error en Alta de apuntes")           
              else:           
                self.saldoFinal+=(_impDebeapu-_impHaberapu)
                consulta1=f"UPDATE apunte SET fecAapu=?,conceptoapu=?,impDebeapu=?,imphaberapu=?,saldoToapu=?,userapu=?,fecUltActapu=? WHERE id={self.id}"
                parametro1=(_fecAapu,_conceptoapu,_impDebeapu,_impHaberapu,
                self.saldoFinal,usuario,self.hoy)
                with sqlite3.connect("database.db") as conn:
                    cursor=conn.cursor()
                    cursor.execute(consulta1,parametro1)
                    self.id=-1
                    conn.commit                    
                    messagebox.showinfo(title="Modificacion",message="MODIFICACION REALIZADA CON EXITO")    
                self.limpiar()
                self.recuperar_saldo()        
                self.mostrar()
        else:        
         messagebox.showwarning(title="Error Alta",message="Rellene Fecha de alta, Concepto y un importe, minimo")   

#--> Limpiamos los campos de entrada.
    def limpiar(self):
        self.fecAapu.delete(0,END)
        self.conceptoapu.delete(0,END)        
        self.impDebeapu.delete(0,END)
        self.impHaberapu.delete(0,END)

#--> Funcion para seleccionar un registro en el treeview para actualizar
    def seleccionar(self):
        self.btn_actualizar("disable")
        self.btn_cancelar("normal")
        self.btn_agregar("normal")
        self.btn_eliminar("disable")
        self.btn_refrescar("disable")           
        id=self.tre.item(self.tre.selection())["text"]
        if id=="":
            messagebox.showerror(title="ACTUALIZAR",message="Error, Seleccione un Apunte")
        else:
            self.id=id
            self.limpiar()
            valor=self.tre.item(self.tre.selection())["values"]
            self.fecAapu.insert(0,valor[0])
            self.conceptoapu.insert(0,valor[1])            
            self.impDebeapu.insert(0,valor[2])
            self.impHaberapu.insert(0,valor[3])


#--> Funcion para eliminar un registro de Apuntes Diario. Se borra el registro.
    def eliminar(self):
        id=self.tre.item(self.tre.selection())["text"]
        valor=messagebox.askquestion(title="Eliminar",message="¿Esta seguro de querer eliminar el Apunte?")
        if valor=="yes":
            consulta="DELETE FROM apunte WHERE id=?"
            parametros=(id,)
            self.eje_consulta(consulta,parametros)
        self.mostrar() 
        self.recuperar_saldo()    
        self.btn_agregar("normal")
        self.btn_refrescar("normal")
        self.btn_actualizar("disable")
        self.btn_cancelar("disable")
        self.btn_eliminar("disable")           

#--> Funcion que limpia los campos al cancelar una operacion.
    def cancelar(self):
        self.limpiar()

#--> Control de los eventos de los botones, activandolos o desactivandolos
    def evento1(self,estado):
        self.btn_actualizar("normal")
        self.btn_eliminar("normal")
        self.btn_agregar("disable")
        self.btn_refrescar("disable")   

    def evento2(self,estado):
        self.btn_actualizar("disable")
        self.btn_eliminar("disable")
        self.btn_agregar("normal")
        self.btn_refrescar("normal") 
        self.btn_cancelar("disable")          
               
#--> Definicion generica del estado de los botones.
    def btn_agregar(self,estado):
        self.btnagregar.configure(state=estado)
    def btn_refrescar(self,estado):
        self.btnrefrescar.configure(state=estado)    
    def btn_actualizar(self,estado):
        self.btnactualizar.configure(state=estado)    
    def btn_eliminar(self,estado):
        self.btneliminar.configure(state=estado)    
    def btn_cancelar(self,estado):
        self.btncancelar.configure(state=estado)    
        self.limpiar()

    def widgets(self):
        apuntediario=Label(self,text="APUNTES - DIARIO",bg="yellow",font="Arial 18")
        apuntediario.pack()
        apuntediario.place(x=0,y=0,height=30,width=1200)
        self.frame=Frame(self,bg="#DADB7F",bd=15,relief="groove")   
        self.frame.place(x=0,y=30,width=1200,height=800) 
        self.hoy=(datetime.today().strftime("%Y-%m-%d"))
        self.saldoFinal=0

#---> vamos a definir todos los campos de entrada de los Apuntes Diario.  
#--> Fecha de alta del apunte (fecAapu)      
        lblfecAapu=Label(self.frame,text="Fecha Movimiento:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblfecAapu.place(x=10,y=15)
        self.fecAapu=Entry(self.frame,width=10,relief="raised",font="Ariel 13")
        self.fecAapu.place(x=155,y=15,height=25)

#--> Concepto del apunte (conceptoapu)      
        lblconceptoapu=Label(self.frame,text="Concepto",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblconceptoapu.place(x=255,y=15)
        self.conceptoapu=Entry(self.frame,width=30,relief="raised",font="Ariel 13")
        self.conceptoapu.place(x=335,y=15,height=25)

#--> Importe Debe del apunte - entrada (impDebeapu)      
        lblimpDebeapu=Label(self.frame,text="Importe entrada (D)",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblimpDebeapu.place(x=625,y=15)
        self.impDebeapu=Entry(self.frame,width=10,relief="raised",font="Ariel 13")
        self.impDebeapu.place(x=770,y=15,height=25)
        lbleuroD=Label(self.frame,text="€",font="Ariel 14",bg="aquamarine",relief="sunken")
        lbleuroD.place(x=865,y=15)

#--> Importe Haber del apunte - salida (impHaberapu)      
        lblimpHaberapu=Label(self.frame,text="Importe salida (H)",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblimpHaberapu.place(x=900,y=15)
        self.impHaberapu=Entry(self.frame,width=10,relief="raised",font="Ariel 13")
        self.impHaberapu.place(x=1035,y=15,height=25)
        lbleuroH=Label(self.frame,text="€",font="Ariel 14",bg="aquamarine",relief="sunken")
        lbleuroH.place(x=1120,y=15)

#--> Saldo total (Sum(impDebeapu) - Sum(impHaberapu)) (saldoToapu)      
        lblsaldoToapu=Label(self.frame,text="Saldo TOTAL",font="Ariel 12",bg="greenyellow",relief="sunken")
        lblsaldoToapu.place(x=755,y=70)
        self.saldoToapu=Entry(self.frame,width=10,relief="sunken",font="Ariel 13",bg="greenyellow",justify=RIGHT)
        self.saldoToapu.place(x=860,y=70,height=25)
        lbleuroT=Label(self.frame,text="€",font="Ariel 14",bg="greenyellow",relief="sunken")
        lbleuroT.place(x=955,y=70)

#--> Botones de  "ALTA", "REFRESCAR" "MODIFICACION", "ELIMINAR" y  "CANCELAR" de Apuntes 
        self.btnagregar=self.botones(45,650,"ALTA APUNTE","blue","white",cmd=self.altaapuntes)
        self.btnrefrescar=self.botones(250,650,"REFRESCAR","blue","white",cmd=self.mostrar)
        self.btnactualizar=self.botones(480,650,"ACTUALIZAR","blue","white",cmd=self.seleccionar) 
        self.btnactualizar.configure(state="disable")
        self.btneliminar=self.botones(710,650,"ELIMINAR","blue","white",cmd=self.eliminar)
        self.btneliminar.configure(state="disable")        
        self.btncancelar=self.botones(940,650,"CANCELAR","blue","white",cmd=self.cancelar) 
        self.btncancelar.configure(state="disable")   

#--> Creo ahora el Treframe con su Treeview con sus cabeceras de columnas (Heading)
#    Codigo(id) [0], Fecha de alta del apunte(fecAapu) [1], Importe de entrada Debe(impDebeapu) [2], 
#    Importe de salida Haber(impHaberapu) [3], Concepto del apunte(conceptoapu) [4], 
 
        treFrame=Frame(self.frame,bg="cyan")
        treFrame.place(x=30,y=100,width=1000,height=500)
        scroll=Scrollbar(treFrame)
        scroll.pack(side=RIGHT,fill=Y)
        self.tre=ttk.Treeview(treFrame,yscrollcommand=scroll.set,height=40,columns=("#0","#1","#2","#3","#4"))
        self.tre.pack() 
        scroll.config(command=self.tre.yview)
        for i in [3,4]:
            self.tre.column(f"#{i}",width=180,anchor=CENTER)
        colors=("cyan","green")
        for color in colors:
            self.tre.tag_configure(color,background=color)
        self.tre.column("#0",width=60,anchor=CENTER)
        self.tre.column("#1",width=150,anchor=CENTER)
        self.tre.column("#2",width=410,anchor=CENTER)        
        self.tre.heading("#0",text="CODIGO",anchor=CENTER)
        self.tre.heading("#1",text="FECHA MOVIMIENTO",anchor=CENTER)
        self.tre.heading("#2",text="CONCEPTO",anchor=CENTER) 
        self.tre.heading("#3",text="IMPORTE ENTRADA",anchor=CENTER)
        self.tre.heading("#4",text="IMPORTE SALIDA",anchor=CENTER)
        try:
            self.mostrar()
            self.recuperar_saldo()
        except:
            pass
        self.tre.bind("<Double-1>",self.evento1)
        self.tre.bind("<Button-1>",self.evento2)    
    
#==============================================================================================
#                                        >>  PROVEEDOR <<
#==============================================================================================
#--> Creo una variable id, que me va a indicar que tipo de accion voy a realizar(que boton). Lo inicializo a -1,
#    porque no existe un id(identificador de registro) negativo.
class Proveedor(Frame):
    def __init__(self,padre): 
        super().__init__(padre)
        self.id=-1
        self.widgets()

#--> Le damos un movimiento de color, al paso del mouse/enter por las teclas de los botones
    def botones(self,x,y,text,bcolor,fcolor,cmd):
        def on_enter(e):
            btn["background"]=bcolor
            btn["foreground"]=fcolor
        def on_leave(e):
            btn["background"]=fcolor
            btn["foreground"]=bcolor
        btn=Button(self.frame,text=text,
        fg=bcolor,
        bg=fcolor,
        border=1,
        activeforeground=fcolor,
        activebackground=bcolor,        
        command=cmd)
        btn.bind("<Enter>",on_enter)
        btn.bind("<Leave>",on_leave)
        btn.place(x=x,y=y,width=150,height=40)    
        return btn

    def eje_consulta(self,consulta,parametros=()):
        db=Datos()       
        result=db.consultas(consulta,parametros)
        return result

    def validacion(self,nombrep,cifp):
        return len(nombrep)>0 and len(cifp)>0    

    def valfecha(self,fechv):
        try:              
            fechv=datetime.strptime(fechv,'%Y-%m-%d').date()            
            return True
        except ValueError:                                
            return False

#--> No uso el metodo "eje_consulta", por ser una select masiva sin parametros. 
#    bOTON "REFRESCAR". Se borra el contenido del treview, y se seleccionan todos los registros 
#    de la BD de proveedor.
    def mostrar(self):
        colores=("pink1","LightPink1")
        for color in colores:
            self.tre.tag_configure(color,background=color)
        result=self.tre.get_children()
        for i in result:
            self.tre.delete(i)
        conn=sqlite3.connect("database.db")
        cursor=conn.cursor()    
        result=cursor.execute("SELECT * FROM proveedor ORDER BY id DESC")  
        colores=itertools.cycle(colores)   
        for elem,color in zip(result,colores):
            self.tre.insert("",0,text=elem[0],tag=("fuente",color),values=(elem[1],elem[2],elem[3],elem[4],elem[5]))
        if len(self.tre.get_children()) > 0:
            self.tre.selection_set(self.tre.get_children()[0])    


#--> Antes de cada alta se borra el contenido del treview, para una vez realizada la alta, seleccionar
#    todos los registros de la BD de proveedor. Si self.id == -1, es una Alta, sino es una modificacion. 
    def altaproveedor(self):
        self.nombrepro.focus()
        nombrep=self.nombrepro.get()
        cifp=self.cifpro.get()
        relp=self.relpro.get("1.0",END)
        fecAp=self.fecApro.get()
        fecBp=self.fecBpro.get()  
        if self.id==-1:            
            if self.validacion(nombrep,cifp):
                #---> Validamos fecha de alta
                fechv=fecAp    
                if self.valfecha(fechv):
                    try:                
                        consulta=("""INSERT INTO proveedor VALUES(null,?,?,?,?,?,?)""")
                        parametros=(nombrep,cifp,relp,fecAp,fecBp,self.hoy)
                        self.eje_consulta(consulta,parametros)                    
                        messagebox.showinfo(title="Alta Proveedor",message="ALTA REALIZADA CON EXITO")
                    except:  
                        messagebox.showwarning(title="Error",message="Error en Alta de proveedor")
                else:
                    messagebox.showerror(title="Fecha ALTA Proveedor",message="Fecha debe ser formato AAAA-MM-DD")                
            else:
                messagebox.showwarning(title="Error",message="Rellene Nombre y CIF")   
        else:
            if self.validacion(nombrep,cifp):
                #---> Validamos fecha de alta
                fechv=fecAp    
                if self.valfecha(fechv):
                    consulta1=f"UPDATE proveedor SET nombrepro=?,cifpro=?,relpro=?,fecApro=?,fecBpro=?,fecUltActpro=? WHERE id={self.id}"
                    parametro1=(nombrep,cifp,relp,fecAp,fecBp,self.hoy)
                    with sqlite3.connect("database.db") as conn:
                        cursor=conn.cursor()
                        cursor.execute(consulta1,parametro1)
                        self.id=-1
                        conn.commit
                    messagebox.showinfo(title="Modificacion",message="MODIFICACION REALIZADA CON EXITO")    
                else:
                    messagebox.showerror(title="Fecha ALTA Proveedor",message="Fecha debe ser formato AAAA-MM-DD")                
            else:
                messagebox.showwarning(title="Error",message="Rellene Nombre y CIF")   
        self.limpiar()
        self.mostrar()


    def limpiar(self):
        self.nombrepro.delete(0,END)
        self.cifpro.delete(0,END)
        self.relpro.delete("1.0",END)
        self.fecApro.delete(0,END)
        self.fecBpro.delete(0,END)   

    def seleccionar(self):
        self.btn_actualizar("disable")
        self.btn_cancelar("normal")
        self.btn_agregar("normal")
        self.btn_eliminar("disable")
        self.btn_refrescar("disable")           
        id=self.tre.item(self.tre.selection())["text"]
        if id=="":
            messagebox.showerror(title="ACTUALIZAR",message="Error, Seleccione un proveedor")
        else:
            self.id=id
            self.limpiar()
            valor=self.tre.item(self.tre.selection())["values"]
            self.nombrepro.insert(0,valor[0])
            self.cifpro.insert(0,valor[1])
            self.relpro.insert("1.0",valor[2])
            self.fecApro.insert(0,valor[3])
            self.fecBpro.insert(0,valor[4])   

#--> Funcion para eliminar un proveedor. Se borra el registro
    def eliminar(self):
        id=self.tre.item(self.tre.selection())["text"]
        valor=messagebox.askquestion(title="Eliminar",message="¿Esta seguro de querer eliminar al proveedor?")
        if valor=="yes":
            consulta="DELETE FROM proveedor WHERE id=?"
            parametros=(id,)
            self.eje_consulta(consulta,parametros)
        self.mostrar()     
        self.btn_agregar("normal")
        self.btn_refrescar("normal")
        self.btn_actualizar("disable")
        self.btn_cancelar("disable")
        self.btn_eliminar("disable")           

#--> Funcion que limpia los campos al cancelar una operacion.
    def cancelar(self):
        self.limpiar()

#--> Control de los eventos de los botones, activandolos o desactivandolos
    def evento1(self,estado):
        self.btn_actualizar("normal")
        self.btn_eliminar("normal")
        self.btn_agregar("disable")
        self.btn_refrescar("disable")    

    def evento2(self,estado):
        self.btn_actualizar("disable")
        self.btn_eliminar("disable")
        self.btn_agregar("normal")
        self.btn_refrescar("normal") 
        self.btn_cancelar("disable")          
               
#--> Definicion generica del estado de los botones
    def btn_agregar(self,estado):
        self.btnagregar.configure(state=estado)
    def btn_refrescar(self,estado):
        self.btnrefrescar.configure(state=estado)    
    def btn_actualizar(self,estado):
        self.btnactualizar.configure(state=estado)    
    def btn_eliminar(self,estado):
        self.btneliminar.configure(state=estado)    
    def btn_cancelar(self,estado):
        self.btncancelar.configure(state=estado)    
        self.limpiar()

    def widgets(self):
        proveedor=Label(self,text="PROVEEDORES",bg="#FF6633",font="Arial 18")
        proveedor.pack()
        proveedor.place(x=0,y=0,height=30,width=1200)
        self.frame=Frame(self,bg="#EEAF82",bd=15,relief="groove")   
        self.frame.place(x=0,y=30,width=1200,height=800) 
        self.hoy=(datetime.today().strftime("%Y-%m-%d"))

#---> vamos a definir todos los campos de entrada de proveedor.  
#--> Nombre (nombre)      
        lblnombrepro=Label(self.frame,text="Nombre:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblnombrepro.place(x=10,y=30)
        self.nombrepro=Entry(self.frame)
        self.nombrepro.place(x=110,y=30,width=120)

#--> CIF del proveedor (cifpro)      
        lblcifpro=Label(self.frame,text="C.I.F.:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblcifpro.place(x=10,y=60)
        self.cifpro=Entry(self.frame)
        self.cifpro.place(x=110,y=60,width=120)

#--> Relacion con el proveedor (relpro)      
        lblrelpro=Label(self.frame,text="Relaciones:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblrelpro.place(x=10,y=90)
        self.relpro=Text(self.frame)
        self.relpro.place(x=110,y=90,height=50,width=120)

#--> Texto indicando "Empresa sin CIF, ponga B0 en CIF"
        lblnombrecif=Label(self.frame,text="Empresa sin CIF, ponga B0 en CIF",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblnombrecif.place(x=10,y=150)

#--> Fecha de alta (fecApro)      
        lblfecApro=Label(self.frame,text="Fecha Alta:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblfecApro.place(x=10,y=190)
        self.fecApro=Entry(self.frame)
        self.fecApro.place(x=110,y=190,width=120)

#--> Fecha de baja (fecBpro)      
        lblfecBpro=Label(self.frame,text="Fecha Baja:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblfecBpro.place(x=10,y=220)
        self.fecBpro=Entry(self.frame)
        self.fecBpro.place(x=110,y=220,width=120)

#--> Boton de  "ALTA PROVEEDOR", "REFRESCAR" "MODIFICAR", "ELIMINAR", "CANCELAR" 
        self.btnagregar=self.botones(30,300,"ALTA PROVEEDOR","blue","white",cmd=self.altaproveedor)
        self.btnrefrescar=self.botones(30,350,"REFRESCAR","blue","white",cmd=self.mostrar)
        self.btnactualizar=self.botones(30,400,"MODIFICAR","blue","white",cmd=self.seleccionar) 
        self.btnactualizar.configure(state="disable")              
        self.btneliminar=self.botones(30,450,"ELIMINAR","blue","white",cmd=self.eliminar)
        self.btneliminar.configure(state="disable")        
        self.btncancelar=self.botones(30,500,"CANCELAR","blue","white",cmd=self.cancelar) 
        self.btncancelar.configure(state="disable")   

#--> Creo ahora el Treframe con su Treeview con sus cabeceras de columnas (Heading).
#    Codigo(id) [0], Nombre Proveedor(nombrepro) [1], C.I.F.(cifpro) [2], 
#    Relacion con el Proveedor(relpro) [3], Fecha de Alta(fecApro) [4], Fecha de Baja(fecBpro) [5],
#    Fecha ultima actualizacion(fecUltActpro) [6]  

        treFrame=Frame(self.frame,bg="cyan")
        treFrame.place(x=280,y=30,width=860,height=600)
        scroll=Scrollbar(treFrame)
        scroll.pack(side=RIGHT,fill=Y)
        self.tre=ttk.Treeview(treFrame,yscrollcommand=scroll.set,height=40,columns=("#0","#1","#2","#3","#4","#5"))
        self.tre.pack() 
        scroll.config(command=self.tre.yview)
        colors=("cyan","green")
        for color in colors:
            self.tre.tag_configure(color,background=color)
        for i in [2,4,5]:
            self.tre.column(f"#{i}",width=80,anchor=CENTER)
        self.tre.column("#1",width=270,anchor=CENTER)
        self.tre.column("#3",width=250,anchor=CENTER)
        self.tre.column("#0",width=60,anchor=CENTER)      
        self.tre.heading("#0",text="CODIGO",anchor=CENTER)
        self.tre.heading("#1",text="NOMBRE",anchor=CENTER)
        self.tre.heading("#2",text="C.I.F.",anchor=CENTER)
        self.tre.heading("#3",text="RELACION",anchor=CENTER)
        self.tre.heading("#4",text="FECHA ALTA",anchor=CENTER)
        self.tre.heading("#5",text="FECHA BAJA",anchor=CENTER)
        try:
            self.mostrar()
        except:
            pass
        self.tre.bind("<Double-1>",self.evento1)
        self.tre.bind("<Button-1>",self.evento2)    


    