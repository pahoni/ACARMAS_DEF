#--> Importamos las librerias necesarias
from tkinter import *
from tkinter import ttk, messagebox
from dataDB import Datos
from datetime import datetime
from PIL import Image, ImageTk
import cv2
import imutils
import sqlite3
import json
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
        btn.place(x=x,y=y,width=120,height=30)

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
        fondo.place(x=0,y=0,width=1200,height=800)
        self.perfil=Label(fondo)
        self.perfil.place(x=540,y=150)
        user=Label(fondo,text="Nombre de Usuario",font="Arial 16",bg="cyan")
        user.place(x=540,y=370) 
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
#    el usuario y la contraseña para caso de ser validos se darán de alta al usuario y contraseña.
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
        self.fondo=Frame(self,bg="cyan")
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
#     "Gestion Actividades","Proveedores", "Caja" y "Varios".
class Container(Frame):
    def __init__(self,padre,controlador):
        super().__init__(padre)
        self.controlador=controlador
        self.pack()
        self.place(x=0,y=0,width=1200,height=800) 
        self.widgets()
        self.frames={}
#--> Iteramos con una instruccion "for", tanto a Socios, Actividad, Proveedor, Apunte diario y Recibo,
#     para que la primera pantalla que se activa es la de Socios.        
        for i in (Socios,Actividad,Proveedor,Apuntediario,Recibo):
            frame=i(self)
            self.frames[i]=frame
            frame.pack()
            frame.config(bg="#fbcada")
            frame.place(x=0,y=40,width=1200,height=800)
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

    def widgets(self):
        socios=self.botones(0,0,"GESTION SOCIOS","blue","white",cmd=self.socios)               
        actividad=self.botones(240,0,"GESTION ACTIVIDAD","blue","white",cmd=self.actividad)
        proveedor=self.botones(480,0,"PROVEEDORES","blue","white",cmd=self.proveedor)
        apuntediario=self.botones(720,0,"APUNTE DIARIO","blue","white",cmd=self.apuntediario)
        recibo=self.botones(960,0,"RECIBO","blue","white",cmd=self.recibo)


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

    def apuntediario(self):
        self.show_frames(Apuntediario)        

    def recibo(self):
        self.show_frames(Recibo)        

#--> Creamos las clases, de Socios, de Actividad, de Proveedor, de Apuntediario y de Recibo.
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
        font="Arial 16",
        activeforeground=fcolor,
        activebackground=bcolor,
        command=cmd)
        btn.bind("<Enter>",on_enter)
        btn.bind("<Leave>",on_leave)
        btn.place(x=x,y=y,width=160,height=40)    
  
#--> Funcion para realizar instrucciones sobre la BD y recuperar el ultimo numero de socio y mostrarlo.
    def recuperar_numso(self):
        with sqlite3.connect("database.db") as conn:
            cursor=conn.cursor()
            cursor.execute("SELECT numsoc FROM socio ORDER BY numsoc DESC LIMIT 1")
            resultado=cursor.fetchone()
            if resultado is NONE:
                messagebox.showwarning(title="Error",message="NO EXISTE REGISTROS EN socio") 
            else:    
                self.ultnumsoc.delete(0,END)
                self.ultnumsoc.insert(END,resultado[0])
            conn.commit()
            #self.ultnumsoc=Entry(state="readonly")


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
        return len(nombre)>0 and len(apellidos)>0 and len(fecA)>0 and len(numsoc)>0        
   
    def valfecha(self,fechv):
        try:              
            fechv=datetime.strptime(fechv,'%Y-%m-%d').date()            
            return True
        except ValueError:                                
            return False

    def valida_numero(self,numero):
        return  numero.isdecimal()

#--> Funcion de dar de alta un socio al pulsar el boton "ALTA SOCIO"-------------------------
    def altasocio(self):
#---> Recogemos los datos introducidos por el usuario        
        nombre=self.nombre.get()
        apellidos=self.apellidos.get()
        fecA=self.fecA.get()
        fecN=self.fecN.get()
        fecB=self.fecB.get()
        motB=self.motB.get()
        dni=self.dni.get()
        profe=self.profe.get()
        deudapen=self.deudapen.get()
        check_1=self.check_1.get()
        CargoMember=self.CargoMember.get()
        numsoc=self.numsoc.get()
        estciv=self.estciv.get()
        discapaci=self.discapaci.get()
        calle=self.calle.get()
        muni=self.muni.get()
        prov=self.prov.get()
        pais=self.pais.get()
        codpos=self.codpos.get()
        telmov=self.telmov.get()
        telfij=self.telfij.get()
        corE=self.corE.get()
        nomcon=self.nomcon.get()
        apellcon=self.apellcon.get()
        telcon=self.telcon.get()
        relcon=self.relcon.get()
        check_2=self.check_2.get()
        check_3=self.check_3.get()
        check_4=self.check_4.get()

#---> Compruebo si  los datos minimos de entrada han sido RELLENADOS
        if self.validacion_entrada(nombre,apellidos,fecA,numsoc):            
#---> Validamos fecha de alta
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
                    messagebox.showerror(title="ALTA SOCIO",message="Numero de socio debe ser Numerico")
            else:
                messagebox.showerror(title="FECHA ALTA",message="Fecha debe ser formato AAAA-MM-DD")
        else:
            messagebox.showwarning(title="ALTA SOCIO",message="Rellene los campos,Nombre,Apellidos,Fecha Alta y nº Socio")

#--> Funcion para CONSULTAR un socio al pulsar el boton "CONSULTA"-------------------------
    def consulta_socio(self):            
            nombre=self.nombre.get()            
            apellidos=self.apellidos.get()                
            if (nombre=="") and (apellidos==""):            
               messagebox.showwarning(title="CONSULTA SOCIO",message="Rellene los campos >> Nombre y 2 Apellidos << ")
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
                       print("Eror en Consulta BD: ", error)
                       messagebox.showwarning(title="Error",message="Error en CONSULTA SOCIO") 

                if resultado is None:
                    self.nombre.delete(0,END)
                    self.apellidos.delete(0,END)
                    messagebox.showinfo(title="CONSULTA",message="Socio no existe")                 
                else:
                    self.mostrar_campos(resultado)

    def mostrar_campos(self,resultado):
        self.id=resultado[0]
        self.nombre.insert(END,resultado[1])
        self.apellidos.insert(END,resultado[2])
        self.fecA.insert(END,resultado[3])
        self.fecN.insert(END,resultado[4])
        self.fecB.insert(END,resultado[5])
        self.motB.insert(END,resultado[6])
        self.dni.insert(END,resultado[7])
        self.profe.insert(END,resultado[8])
        self.deudapen.insert(END,resultado[9])       
        self.CargoMember.insert(END,resultado[11])
        self.numsoc.insert(END,resultado[12])
        self.estciv.insert(END,resultado[13])
        self.discapaci.insert(END,resultado[14])
        self.calle.insert(END,resultado[15])
        self.muni.insert(END,resultado[16])
        self.prov.insert(END,resultado[17])
        self.pais.insert(END,resultado[18])
        self.codpos.insert(END,resultado[19])
        self.telmov.insert(END,resultado[20])
        self.telfij.insert(END,resultado[21])
        self.corE.insert(END,resultado[22])
        self.nomcon.insert(END,resultado[23])
        self.apellcon.insert(END,resultado[24])
        self.telcon.insert(END,resultado[25])
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
            nombre=self.nombre.get()            
            apellidos=self.apellidos.get() 
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
                        print("resultado",resultado)
                except sqlite3.OperationalError as error:
                    print("Eror en Modificacion/consul BD: ", error)
                    messagebox.showwarning(title="Error",message="Error en MODIFICACION/select SOCIO") 
                if resultado is None:
                    self.nombre.delete(0,END)
                    self.apellidos.delete(0,END)
                    messagebox.showinfo(title="MODIFICACION",message="SOCIO no existe")                 
                else:
                    messagebox.showinfo(title="Modificacion",message="Haga las modificaciones y pulse MODIFICACION")     
                    self.limpiar_campos()
                    self.mostrar_campos(resultado)
                    print("self.id: ", self.id)
                    id=resultado[0]
        else:
            self.nombre.focus_get()
            #self.nombre.get()
            self.apellidos.get()
            self.fecA.get()
            self.fecN.get()
            self.fecB.get()
            self.motB.get()
            self.dni.get()
            try:
                parametro1=[self.id,self.nombre.get(),self.apellidos.get(),self.fecA.get(),self.fecN.get()]#,
                    #self.fecB.get(),self.motB.get(),self.dni.get(),self.profe.get(),self.deudapen.get(),
                    #self.check_1.get(),self.CargoMember.get(),self.numsoc.get(),self.estciv.get(),
                    #self.discapaci.get(),self.calle.get(),self.muni.get(),self.prov.get(),self.pais.get(),
                    #self.codpos.get(),self.telmov.get(),self.telfij.get(),self.corE.get(),self.nomcon.get(),
                    #self.apellcon.get(),self.telcon.get(),self.relcon.get(),self.check_2.get(),
                    #self.check_3.get(),self.check_4.get(),self.fecUltAct)
                consulta1="""UPDATE socio SET nombre=?,apellidos=?,fecA=?,fecN=? WHERE id=?"""
                    #,fecB=?,motB=?,dni=?
                    #profe=?,deudapen=?,MemberDir=?,CargoMember=?,numsoc=?,estciv=?,discapaci=?,calle=?,
                    #muni=?,prov=?,pais=?,codpos=?,telmov=?,telfij=?,corE=?,nomcon=?,apellcon=?,telcon=?,
                    #relcon=?,RGPD=?,WhatsApp=?,ImgOk=?  WHERE id=?"""
                print("parametro1: ",parametro1)
                print("consulta1: ",consulta1)    
                with sqlite3.connect("database.db") as conn:
                     cursor=conn.cursor()
                     cursor.execute(consulta1,parametro1)                    
                     conn.commit
                     messagebox.showinfo(title="Modificacion",message="MODIFICACION REALIZADA CON EXITO")
                     self.limpiar_campos()
                     self.id=-1
            except sqlite3.OperationalError as error:
                    print("Eror en Modificacion BD: ", error)
        
        #self.mostrar_campos()



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

#--> Botones de las acciones "ALTA" - "BAJA" - "CONSULTA" - "MODIFICACIONES" - "LISTADO"
        btnAlSo=self.botones(20,650,"ALTA","blue","white",cmd=self.altasocio)    
        btnBaSo=self.botones(200,650,"BAJA","blue","white",cmd="")    
        btnCoSo=self.botones(400,650,"CONSULTA","blue","white",cmd=self.consulta_socio)
        btnMoSo=self.botones(600,650,"MODIFICACION","blue","white",cmd=self.modifica_socio)        
        btnlISo=self.botones(800,650,"LISTADO","blue","white",cmd="")

        
#==============================================================================================
#                                        >>  ACTIVIDAD <<
#==============================================================================================

class Actividad(Frame):
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

#--> Funcion de dar de alta una actividad al pulsar el boton "ALTA "
    def altaactividad(self):
        pass

    def widgets(self):
        actividad=Label(self,text="GESTION DE ACTIVIDADES",bg="#33CBFF",font="Arial 18")
        actividad.pack()
        actividad.place(x=0,y=0,height=30,width=1200)
        self.frame=Frame(self,bg="#9ACDD7",bd=15,relief="groove")   
        self.frame.place(x=0,y=30,width=1200,height=800) 

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
        result=self.tre.get_children()
        for i in result:
            self.tre.delete(i)
        conn=sqlite3.connect("database.db")
        cursor=conn.cursor()    
        result=cursor.execute("SELECT * FROM proveedor ORDER BY id DESC")      
        for elem in result:
            self.tre.insert("",0,text=elem[0],values=(elem[1],elem[2],elem[3],elem[4],elem[5]))

#--> Antes de cada alta se borra el contenido del treview, para una vez realizada la alta, seleccionar
#    todos los registros de la BD de proveedor. Si self.id == -1, es una Alta, sino es una modificacion. 
    def altaproveedor(self):
        result=self.tre.get_children()
        for i in result:
            self.tre.delete(i)
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
        #self.mostrar()     
        self.btn_agregar("normal")
        self.btn_refrescar("normal")
        self.btn_actualizar("disable")
        self.btn_cancelar("disable")
        self.btn_eliminar("disable")           

#--> Funcion que limpia los campos.
    def cancelar(self):
        self.limpiar()

#--> Control de los eventos de los botones, activandolos o desactivandolos
    def evento1(self,event):
        self.btn_actualizar("normal")
        self.btn_eliminar("normal")
        self.btn_agregar("disable")
        self.btn_refrescar("disable")           
    def evento2(self,event):
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

#--> Boton de  "ALTA" de proveedor, "REFRESCAR" "MODIFICACION", "ELIMINAR", "CANCELAR" 
        self.btnagregar=self.botones(30,300,"ALTA PROVEEDOR","blue","white",cmd=self.altaproveedor)
        self.btnrefrescar=self.botones(30,350,"REFRESCAR","blue","white",cmd=self.mostrar)
        self.btnactualizar=self.botones(30,400,"ACTUALIZAR","blue","white",cmd=self.seleccionar) 
        self.btnactualizar.configure(state="disable")              
        self.btneliminar=self.botones(30,450,"BAJA PROVEEDOR","blue","white",cmd=self.eliminar)
        self.btneliminar.configure(state="disable")        
        self.btncancelar=self.botones(30,500,"CANCELAR","blue","white",cmd=self.cancelar) 
        self.btncancelar.configure(state="disable")   

#--> Creo ahora el Treframe con su Treeview con sus cabeceras de columnas (Heading) 

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



#==============================================================================================
#                                 >>  APUNTES / DIARIO <<
#==============================================================================================

class Apuntediario(Frame):
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

    def widgets(self):
        apuntediario=Label(self,text="APUNTES - DIARIO",bg="yellow",font="Arial 18")
        apuntediario.pack()
        apuntediario.place(x=0,y=0,height=30,width=1200)
        self.frame=Frame(self,bg="#DADB7F",bd=15,relief="groove")   
        self.frame.place(x=0,y=30,width=1200,height=800) 

#==============================================================================================
#                                        >>  RECIBO <<
#==============================================================================================

class Recibo(Frame):
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

    def widgets(self):
        recibo=Label(self,text="RECIBO",bg="#E2C5E0",font="Arial 18")
        recibo.pack()
        recibo.place(x=0,y=0,height=30,width=1200)
        self.frame=Frame(self,bg="#E2C5E0",bd=15,relief="groove")   
        self.frame.place(x=0,y=30,width=1200,height=800) 
    

    