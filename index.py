#--> Con index.py, lanzamos la aplicacion, conteniendo manager la ventana principal
#    donde alojaremos las diferentes frames.
from manager import Manager
if __name__=="__main__":
    app=Manager()
    app.mainloop()