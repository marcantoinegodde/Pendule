from tkinter import *
import tkinter.font as tkFont
import math as m
import matplotlib.pyplot as pl

class Pendule(object):
    "Instanciation de l'objet pendule"
   
    def __init__(self, t0, tn, u10, u20, v10, v20, m1, m2, l1, l2, g, n):
        "Constructeur de la classe pendule"

        self.t0=t0
        self.tn=tn
        self.u10=u10
        self.u20=u20
        self.v10=v10
        self.v20=v20
        self.m1=m1
        self.m2=m2
        self.l1=l1
        self.l2=l2
        self.g=g
        self.n=n
        self.i=1

    def pendule(self):
        "Méthode définissant le pendule"

        self.fenetre = Tk()  #Définition de la fenêtre et du canvas
        self.fenetre.title('Pendule double')        
        self.can = Canvas(self.fenetre, width = 500, height = 500, bg='grey', highlightthickness=0)
        self.can.pack()
        
        self.menu_bar=Menu(self.fenetre)  #Création des menus
        self.fenetre.config(menu=self.menu_bar)
        self.file_menu=Menu(self.menu_bar, tearoff=0)
        self.help_menu=Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Fichier", menu=self.file_menu)
        self.file_menu.add_command(label="Nouveau")
        self.file_menu.add_command(label="Quitter", command=self.fenetre.quit)
        self.menu_bar.add_cascade(label="Aide", menu=self.help_menu)
        self.help_menu.add_command(label="À propos", command=self.about)

        (self.T,self.U1,self.U2,self.V1,self.V2)=self.resolution(self.t0,self.tn,self.u10,self.u20,self.v10,self.v20,self.m1,self.m2,self.l1,self.l2,self.g,self.n)  #Appel de la résolution
        self.COORD1=self.conversion(self.U1,100)
        self.COORD2=self.conversion(self.U2,100)
        
        self.cx,self.cy=250,250 #Définition du système de coordonnées
        x1,y1=self.COORD1[0]
        x2,y2=self.COORD2[0]
        
        self.bras1 = self.can.create_line(self.cx, self.cy, self.cx+x1, self.cy+y1, fill = 'blue', width = 3)  #Création des objets du pendule
        self.bras2 = self.can.create_line(self.cx+x1, self.cy+y1, self.cx+x1+x2, self.cy+y1+y2, fill = 'green', width = 3)
        self.can.create_oval(self.cx-6,self.cy-6,self.cx+6,self.cy+6,fill='red')
        self.rond1 = self.can.create_oval(self.cx+x1-4, self.cy+y1-4, self.cx+x1+4, self.cy+y1+4, fill='black')
        self.rond2 = self.can.create_oval(self.cx+x1+x2-4, self.cy+y1+y2-4, self.cx+x1+x2+4, self.cy+y1+y2+4, fill='black')

        self.move()  #Appel de la méthode d'animation
     
        self.fenetre.mainloop() 
        
    def resolution(self,t0,tn,u10,u20,v10,v20,m1,m2,l1,l2,g,n):
        "Méthode permettant la résolution des équations différentielles"

        pas=(tn-t0)/n
        T=[t0]
        U1=[u10]
        U2=[u20]
        V1=[v10]
        V2=[v20]
        for k in range(n):
            t1=t0+pas
            u11=u10+pas*v10
            u21=u20+pas*v20
            v11=v10+pas*((-g*(2*m1+m2)*m.sin(u10)-m2*g*m.sin(u10-2*u20)-2*m2*m.sin(u10-u20)*(l2*(v20)**2+l1*(v10)**2*m.cos(u10-u20)))/(l1*(2*m1+m2-m2*m.cos(2*u10-2*u20))))
            v21=v20+pas*(2*m.sin(u10-u20)*(l1*(m1+m2)*(v10)**2+g*(m1+m2)*m.cos(u10)+l2*m2*(v20)**2*m.cos(u10-u20))/(l2*(2*m1+m2-m2*m.cos(2*u10-2*u20))))
            T.append(t1)
            U1.append(u11)
            U2.append(u21)
            V1.append(v11)
            V2.append(v21)
            t0=t1
            u10=u11
            u20=u21
            v10=v11
            v20=v21
        return (T,U1,U2,V1,V2)
        

    def conversion(self,ANGLE,l):
        "Méthode permettant de passer des coordonnées polaires à carthésiennes"

        COORD=[]
        for k in range(len(ANGLE)):
            COORD.append((l*m.sin(ANGLE[k]),l*m.cos(ANGLE[k])))
        return COORD
        
        
    def move(self):
        "Méthode permettant l'animation du pendule"

        if self.i<len(self.COORD1):
            x1,y1=self.COORD1[self.i]
            x2,y2=self.COORD2[self.i]
            self.can.coords(self.bras1, self.cx, self.cy, self.cx+x1, self.cy+y1)  #Déplacement des objets
            self.can.coords(self.rond1, self.cx+x1-4, self.cy+y1-4, self.cx+x1+4, self.cy+y1+4)
            self.can.coords(self.bras2, self.cx+x1, self.cy+y1, self.cx+x1+x2, self.cy+y1+y2)
            self.can.coords(self.rond2, self.cx+x1+x2-4, self.cy+y1+y2-4, self.cx+x1+x2+4, self.cy+y1+y2+4)
            self.i+=1
            self.can.after(5, self.move)  #Répetition de la méthode
            
    def about(self):
        "Fenêtre About"

        self.fenetre_about=Tk() #Définition de la fenêtre
        self.fenetre_about.title('À propos')
        self.fenetre_about.geometry('250x150')
        self.fenetre_about.resizable(width=False, height=False)
        font=tkFont.Font(size=15)
        Label(self.fenetre_about, text='Développé avec amour\npar Marc-Antoine GODDE', font=font).pack(padx=5, pady=10)
        Label(self.fenetre_about, text='Copyright © 2019').pack(padx=5, pady=5)
        self.bouton_ok=Button(self.fenetre_about, text='Ok', command=self.fenetre_about.destroy)
        self.bouton_ok.pack(padx=5, pady=5)

       
                
if __name__ == "__main__": 
 
    pendule = Pendule(0,10000,m.pi/2,0,0,0,3,3,4,4,5,1000000)
    pendule.pendule()
