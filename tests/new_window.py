from tkinter import *   

###################################################################################
# Classe définissant l'objet représentant la fenêtre principale de l'application
###################################################################################
class Application(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Application du tonnerre !")   # Le titre de la fenêtre
        
        self.geometry('200x100')      #taille de fenêtre
        
        # Une méthode séparée pour construire le contenu de la fenêtre
        self.createWidgets()

    # Méthode de création des widgets
    def createWidgets(self):
             # Choix du mode d'arrangement
        self.win = Toplevel(root)
        self.root = Tk()
        self.root.geometry('200x100')  
        self.btn = Button(root, text="Créer une nouvelle fenêtre", command = create)
        self.btn.pack(pady = 10) 
       
        # Création des widgets
        # ...........
        # ...........
        # ...........

        # Un bouton pour quitter l'application
        self.quitButton = Button(self, text = "Quitter", 
                                 command = self.destroy)
        self.quitButton.grid()

        
    # D'autres méthodes ....
    # ......................

app = Application()
app.mainloop()