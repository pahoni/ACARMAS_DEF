# Proyecto Acarmas Definitivo


## Estructura de directorios
 +- Data ( Información del cliente para cargar la Base de datos)
 +- Docu ( Documentación de requisitos del proyecto )


## Crear un ejecutable
Instalar PyInstaller en el entorno:
   $> pip install pyinstaller

Crear un instalable con la siguiente instrucción:
   $> pyinstaller --onefile index.py

Creará el directorio [dist] y copiara el ejecutable.
Incluir la base de datos (database.db) y la imagen (acarmas.png)
