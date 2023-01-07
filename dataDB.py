#--> Creamos la base de datos que contendrá las tablas usadas en este proyecto
import sqlite3

class Datos:
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.name="database.db"


    def crear(self):
        conn=sqlite3.connect(self.name)
        cursor=conn.cursor()


#--> Se crea la tabla de usuarios y contraseña        
        cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios (
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
        cursor.close()
        return result

                           


