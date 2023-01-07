#--> gestionamos las tablas usadas en este proyecto, creandolas
import sqlite3

conn=sqlite3.connect("database.db")
cursor=conn.cursor()

#--> Creamos la tabla de Socios  >> socio  <<:
cursor.execute("""CREATE TABLE IF NOT EXISTS socio (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(20) NOT NULL,
    apel1 VARCHAR(25) NOT NULL,
    apel2 VARCHAR(25) NOT NULL,
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
    apecon1 VARCHAR(25),
    apecon2 VARCHAR(25),
    telcon VARCHAR(12),
    relcon VARCHAR(20),
    RGPD INTEGER DEFAULT 0,
    WhatsApp INTEGER DEFAULT 0,
    ImgOk INTEGER DEFAULT 0,
    fecUltAct DATE NOT NULL)""")

conn.commit
conn.close    
