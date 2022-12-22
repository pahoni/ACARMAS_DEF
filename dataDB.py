#--> Creamos la base de datos que contendrá las tablas usadas en este proyecto
import sqlite3

class Datos:
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.name="database.db"

#--> Se crea la tabla de usuarios y contraseña
    def crear(self):
        conn=sqlite3.connect(self.name)
        cursor=conn.cursor()
        cursor.execute("""CREATE TABLE socios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL(20),
            apel1 TEXT NOT NULL(35),
            apel2 TEXT NOT NULL(35),
            numsoc INTEGER NOT NULL(7),
            dni VARCHAR(10),
            fecN TEXT NOT NULL(10),
            fecA TEXT NOT NULL(10),
            fecb TEXT(10),
            motB VARCHAR(25),
            """)
        cursor.execute("""CREATE TABLE usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(50),
            password VARCHAR(20)
            )""")    

#--> Se crea la consulta de la tabla de usuarios y contraseña            
    def consultas(self,consulta,parametros=()):
        conn=sqlite3.connect(self.name)
        cursor=conn.cursor()
        result=cursor.execute(consulta,parametros)
        conn.commit()
        return result

