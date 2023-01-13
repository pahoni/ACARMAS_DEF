#--> Importamos las librerias necesarias
from tkinter import *
from tkinter import ttk, messagebox
from dataDB import Datos
from datetime import datetime
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
#--> Dentro de la pantalla fondo vamos a craer un boton llamado "REGISTRAR" y otro "REGRESAR",
#    para volver a la pantalla anterior.
        btn1=self.botones(560,540,"REGRESAR","blue","white",cmd=self.control2)
        btn=self.botones(700,540,"REGISTRAR","blue","white",cmd=self.registro)

#--------------> clase Container
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
            frame.config(bg="red")
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
        font="Arial 16",
        activeforeground=fcolor,
        activebackground=bcolor,
        command=cmd)
        btn.bind("<Enter>",on_enter)
        btn.bind("<Leave>",on_leave)
        btn.place(x=x,y=y,width=160,height=40)    
  

#--> Funcion para realizar instrucciones sobre la BD
    def eje_consulta(self,consulta,parametros=()):
        db=Datos()
        try:
           result=db.consultas(consulta,parametros) 
        except:            
           pass
        return result 

#--> Funcion para validar las fechas de Alta, Nacimiento Y Baja



#--> Funcion para validar campos de entrada minimos
    def validacion(self,nombre,apel1,apel2,fecA,numsoc,):
        return len(nombre)>0 and len(apel1)>0 and len(apel2)>0 and len(fecA)>0 and len(numsoc)>0

#--> Funcion de dar de alta un socio al pulsar el boton "ALTA SOCIO"
    def altasocio(self):

#---> Recogemos los datos introducidos por el usuario        
        nombre=self.nombre.get()
        apel1=self.apel1.get()
        apel2=self.apel2.get()
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
        apecon1=self.apecon1.get()
        apecon2=self.apecon2.get()
        telcon=self.telcon.get()
        relcon=self.relcon.get()
        check_2=self.check_2.get()
        check_3=self.check_3.get()
        check_4=self.check_4.get()

#---> Compruebo si la validacion de los datos minimos de entrada han sido correctos
        if self.validacion(nombre,apel1,apel2,fecA,numsoc):
#---> Compruebo fechas validas, caso de ser cumplimentadas.
            
                try:
            
                    consulta=("""INSERT INTO socio VALUES(NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""")                                                   
                    
                    parametros=(nombre,apel1,apel2,fecA,fecN,fecB,motB,dni,profe,deudapen,
                    check_1,CargoMember,numsoc,estciv,discapaci,calle,muni,prov,
                    pais,codpos,telmov,telfij,corE,nomcon,apecon1,apecon2,telcon,relcon,
                    check_2,check_3,check_4,self.hoy)

                    self.eje_consulta(consulta,parametros)

                    messagebox.showinfo(title="ALTA SOCIO",message="Alta Socio realizado con exito")

                except sqlite3.OperationalError as error:
                    print("Eror en Alta: ", error)
                    messagebox.showwarning(title="Error",message="ERROR AL DAR DE ALTA SOCIO")
        else:
            messagebox.showwarning(title="Error",message="Rellene los campos,Nombre,Apellidos,Fecha Alta y nº Socio")


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
        


#---> vamos a definir todos los campos de entrada de socios.  
#--> Nombre (nombre)      
        lblnombre=Label(self.frame,text="Nombre:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblnombre.place(x=5,y=15)
        self.nombre=Entry(self.frame,width=20,relief="raised",font="Ariel 13")
        self.nombre.place(x=80,y=15,height=25)  
#--> Primer apellido (apel1)        
        lblapel1=Label(self.frame,text="Apellido 1:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblapel1.place(x=295,y=15)
        self.apel1=Entry(self.frame,width=25,relief="raised",font="Ariel 13")
        self.apel1.place(x=380,y=15,height=25)    
#--> Segundo apellido (apel2)        
        lblapel2=Label(self.frame,text="Apellido 2:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblapel2.place(x=630,y=15)
        self.apel2=Entry(self.frame,width=25,relief="raised",font="Ariel 13")
        self.apel2.place(x=715,y=15,height=25)  

#--> FECHAS
        lblfofe=Label(self.frame,text=">> FECHAS: aaaa/mm/dd <<",font="Ariel 12",bg="orange",relief="sunken")
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
#--> Nombre (nomcon), Primer apellido (apecon1), Segundo apellido (apecon2)      
        lblnomcon=Label(self.frame,text="Nombre:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblnomcon.place(x=5,y=420)
        self.nomcon=Entry(self.frame,width=20,relief="raised",font="Ariel 13")
        self.nomcon.place(x=80,y=420,height=25)
        lblapecon1=Label(self.frame,text="Apellido 1:",font="Ariel 12",bg="aquamarine",relief="sunken")
        lblapecon1.place(x=295,y=420)
        self.apecon1=Entry(self.frame,width=25,relief="raised",font="Ariel 13")
        self.apecon1.place(x=380,y=420,height=25)
        lblapecon2=Label(self.frame,text="Apellido 2:",font="16",bg="aquamarine")
        lblapecon2.place(x=630,y=420)
        self.apecon2=Entry(self.frame,width=25,relief="raised",font="Ariel 13")
        self.apecon2.place(x=715,y=420,height=25)  

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
        btnCoSo=self.botones(400,650,"CONSULTA","blue","white",cmd="")
        btnMoSo=self.botones(600,650,"MODIFICACION","blue","white",cmd="")        
        btnlISo=self.botones(800,650,"LISTADO","blue","white",cmd="")

        
#
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
        actividad=Label(self,text="ACTIVIDADES",bg="#33CBFF",font="Arial 18")
        actividad.pack()
        actividad.place(x=0,y=0,height=30,width=1200)
        self.frame=Frame(self,bg="#5AC8EB",bd=15,relief="groove")   
        self.frame.place(x=0,y=30,width=1200,height=800) 


class Proveedor(Frame):
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

    def altaactividad(self):
        pass

    def widgets(self):
        proveedor=Label(self,text="PROVEEDORES",bg="orange",font="Arial 18")
        proveedor.pack()
        proveedor.place(x=0,y=0,height=30,width=1200)
        self.frame=Frame(self,bg="#FF6633",bd=15,relief="groove")   
        self.frame.place(x=0,y=30,width=1200,height=800) 


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
        self.frame=Frame(self,bg="#D9FF33",bd=15,relief="groove")   
        self.frame.place(x=0,y=30,width=1200,height=800) 


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
        recibo=Label(self,text="RECIBO",bg="#FF33C9",font="Arial 18")
        recibo.pack()
        recibo.place(x=0,y=0,height=30,width=1200)
        self.frame=Frame(self,bg="#FF33B7",bd=15,relief="groove")   
        self.frame.place(x=0,y=30,width=1200,height=800) 
    

    