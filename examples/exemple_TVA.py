#Initialisation fenêtre
from tkinter import *

root = Tk()
root.title("Films")
root.resizable(False, False)
root.geometry('800x700')
 
#Création des Frames principaux
frame1 = LabelFrame(root, borderwidth=3)
frame1.grid(row=0, column=0, padx=10, pady=10)
  
#Création des sous widgets du 1er Frame
tvaFrame = LabelFrame(frame1, text='TVA', borderwidth=2, width=120, height=100)
tvaFrame.grid(row=0, column=0, padx=10, pady=10)
value = IntVar()
bouton1 = Radiobutton(tvaFrame, text="5.50%", variable=value, value=1)
bouton1.grid(row=0, column=0, padx=(10, 40), pady=10)
bouton2 = Radiobutton(tvaFrame, text="19.60%", variable=value, value=2)
bouton2.grid(row=1, column=0, padx=(10, 40), pady=10)
 
root.mainloop()
