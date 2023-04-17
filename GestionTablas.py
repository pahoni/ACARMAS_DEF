#--> gestionamos las tablas usadas en este proyecto, creandolas
import sqlite3

conn=sqlite3.connect("database.db")
cursor=conn.cursor()

#--> Creamos la tabla de Socios  >> socio  <<:
cursor.execute("""CREATE TABLE IF NOT EXISTS socio (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(20) NOT NULL,
    apellidos VARCHAR(50) NOT NULL,
    fecA DATE,
    fecN DATE,
    fecb DATE,
    motB VARCHAR(25),
    dni VARCHAR(12),
    profe VARCHAR(20),
    deudapen REAL DEFAULT 0,
    MemberDir INTEGER DEFAULT 0,
    CargoMember VARCHAR(15),
    numsoc INTEGER NOT NULL DEFAULT 0,
    estciv VARCHAR(15),
    discapaci REAL DEFAULT 0,
    calle VARCHAR(50),
    muni VARCHAR(20),
    prov VARCHAR(20),
    pais VARCHAR(15),
    codpos INTEGER DEFAULT 0,
    telmov VARCHAR(12),
    telfij VARCHAR(12),
    corE VARCHAR(40),
    nomcon VARCHAR(20),
    apellcon VARCHAR(50),
    telcon VARCHAR(12),
    relcon VARCHAR(20),
    RGPD INTEGER DEFAULT 0,
    WhatsApp INTEGER DEFAULT 0,
    ImgOk INTEGER DEFAULT 0,
    fecUltAct DATE NOT NULL)""")
conn.commit
conn.close    

#--> Creamos la tabla de Proveedor  >> proveedor  <<:
cursor.execute("""CREATE TABLE IF NOT EXISTS proveedor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombrepro VARCHAR(30) NOT NULL,
    cifpro VARCHAR(12),
    relpro VARCHAR(100),
    fecApro DATE,   
    fecBpro DATE,
    fecUltActpro DATE NOT NULL)""")
conn.commit
conn.close    

#--> Creamos la tabla de Apunte  >> Apunte Diario  <<:
cursor.execute("""CREATE TABLE IF NOT EXISTS apunte (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecAapu DATE NOT NULL,
    conceptoapu VARCHAR(200),
    impDebeapu REAL DEFAULT 0,
    impHaberapu REAL DEFAULT 0,    
    saldoToapu REAL,
    userapu VARCHAR(20),
    fecUltActapu DATE NOT NULL)""")
conn.commit
conn.close    

#--> Creamos la tabla de Actividad:
cursor.execute("""CREATE TABLE IF NOT EXISTS actividad (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    claveAct VARCHAR(11),
    nombreAct VARCHAR(200),
    responAct VARCHAR(200),
    finiAct DATE NOT NULL,
    ffinAct DATE NOT NULL,
    cosresAct REAL DEFAULT 0,
    cosparAct REAL DEFAULT 0,
    nummaxAct INTEGER NOT NULL,
    diasemAct VARCHAR(15),
    HiniAct VARCHAR(10),
    HfinAct VARCHAR(20),
    userAct VARCHAR(20),
    fecUltActAct DATE NOT NULL)""")
conn.commit
conn.close

#--> Creamos la tabla de Participes:
cursor.execute("""CREATE TABLE IF NOT EXISTS participes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    clavePar VARCHAR(11),
    nombrePar VARCHAR(20) NOT NULL,
    apellidosPar VARCHAR(50) NOT NULL,
    esperaPar VARCHAR(01),   
    userPar VARCHAR(20),
    fecUltActPar DATE NOT NULL)""")
conn.commit
conn.close