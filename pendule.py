#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk, messagebox
import tkinter.font as tkFont
import tkinter
import threading
import math as m

class Pendule(object):
    "Définition de la classe de l'objet pendule"

    def __init__(self):
        "Constructeur de la classe pendule"

        self.t0=0
        self.tn=10000
        self.u10=1.55
        self.u20=0
        self.v10=1
        self.v20=1
        self.m1=10
        self.m2=10
        self.l1=10
        self.l2=10
        self.g=9.81
        self.n=1000000

        self.i=1
        self.T=[]
        self.U1=[]
        self.U2=[]
        self.V1=[]
        self.V2=[]

    def home(self):
        "Fenêtre de configuration"

        self.fenetre_home=Tk()
        self.fenetre_home.title('Configuration')
        self.fenetre_home.geometry('520x290')
        self.fenetre_home.resizable(width=False, height=False)
        icon=tkinter.Image("photo", file='icons/settings.gif')  #Fichier de l'icône
        self.fenetre_home.tk.call('wm', 'iconphoto', self.fenetre_home._w, icon)

        self.ButtonFrame=LabelFrame(self.fenetre_home, text='Actions')
        self.ButtonFrame.place(bordermode=OUTSIDE, x=360, y=10, height=180, width=155)
        self.TimeFrame=LabelFrame(self.fenetre_home, text='Temps')
        self.TimeFrame.place(bordermode=OUTSIDE, x=10, y=10, height=75, width=175)
        self.InitValuesFrame=LabelFrame(self.fenetre_home, text='Conditions Inititales')
        self.InitValuesFrame.place(bordermode=OUTSIDE, x=10, y=95, height=150, width=175)
        self.WeightFrame=LabelFrame(self.fenetre_home, text='Masses')
        self.WeightFrame.place(bordermode=OUTSIDE, x=195, y=10, height=75, width=150)
        self.LengthFrame=LabelFrame(self.fenetre_home, text='Longueurs')
        self.LengthFrame.place(bordermode=OUTSIDE, x=195, y=95, height=95, width=150)
        self.ConstFrame=LabelFrame(self.fenetre_home, text='Constantes')
        self.ConstFrame.place(bordermode=OUTSIDE, x=195, y=195, height=50, width=150)
        self.MiscFrame=LabelFrame(self.fenetre_home, text='Résolution')
        self.MiscFrame.place(bordermode=OUTSIDE, x=360, y=195, height=50, width=155)

        self.TimeFrame.grid_columnconfigure(0, minsize=5)
        self.InitValuesFrame.grid_columnconfigure(0, minsize=5)
        self.InitValuesFrame.grid_rowconfigure(0, minsize=10)
        self.WeightFrame.grid_columnconfigure(0, minsize=5)
        self.LengthFrame.grid_columnconfigure(0, minsize=5)
        self.LengthFrame.grid_rowconfigure(0, minsize=5)
        self.ConstFrame.grid_columnconfigure(0, minsize=5)
        self.MiscFrame.grid_columnconfigure(0, minsize=5)

        icon_start=PhotoImage(file='icons/start.gif')
        self.bouton_start=Button(self.ButtonFrame, text="Démarrer", image=icon_start, compound="left", command=self.start, height=30, width=110)
        self.bouton_start.grid(row=0, column=0, padx=5, pady=5)
        icon_reset=PhotoImage(file='icons/recycle.gif')
        self.bouton_reset=Button(self.ButtonFrame, text="Réinitialiser", image=icon_reset, compound="left", command=self.reset, height=30, width=110)
        self.bouton_reset.grid(row=1, column=0, padx=5, pady=0)
        icon_quit=PhotoImage(file='icons/quit.gif')
        self.bouton_quit=Button(self.ButtonFrame, text="Quitter", image=icon_quit, compound="left", command=self.fenetre_home.destroy, height=30, width=110)
        self.bouton_quit.grid(row=2, column=0, padx=5, pady=5)


        self.t0_txt=Label(self.TimeFrame, text ='Date initiale:')
        self.t0_txt.grid(row=0, column=1)
        self.tn_txt=Label(self.TimeFrame, text ='Date finale:')
        self.tn_txt.grid(row=1, column=1, sticky='w')
        self.t0_ent=Entry(self.TimeFrame, width=7)
        self.t0_ent.grid(row=0, column=2)
        self.tn_ent=Entry(self.TimeFrame, width=7)
        self.tn_ent.grid(row=1, column=2)

        self.u10_txt=Label(self.InitValuesFrame, text ='θ1(0):')
        self.u10_txt.grid(row=1, column=1)
        self.u20_txt=Label(self.InitValuesFrame, text ='θ2(0):')
        self.u20_txt.grid(row=2, column=1)
        self.u10_ent=Entry(self.InitValuesFrame, width=12)
        self.u10_ent.grid(row=1, column=2)
        self.u20_ent=Entry(self.InitValuesFrame, width=12)
        self.u20_ent.grid(row=2, column=2, pady=5)
        self.v10_txt=Label(self.InitValuesFrame, text ='v1(0):')
        self.v10_txt.grid(row=3, column=1)
        self.v20_txt=Label(self.InitValuesFrame, text ='v2(0):')
        self.v20_txt.grid(row=4, column=1)
        self.v10_ent=Entry(self.InitValuesFrame, width=12)
        self.v10_ent.grid(row=3, column=2)
        self.v20_ent=Entry(self.InitValuesFrame, width=12)
        self.v20_ent.grid(row=4, column=2, pady=5)

        self.m1_txt=Label(self.WeightFrame, text ='Masse 1:')
        self.m1_txt.grid(row=0, column=1)
        self.m2_txt=Label(self.WeightFrame, text ='Masse 2:')
        self.m2_txt.grid(row=1, column=1)
        self.m1_ent=Entry(self.WeightFrame, width=7)
        self.m1_ent.grid(row=0, column=2)
        self.m2_ent=Entry(self.WeightFrame, width=7)
        self.m2_ent.grid(row=1, column=2)

        self.l1_txt=Label(self.LengthFrame, text ='Longueur 1:')
        self.l1_txt.grid(row=1, column=1)
        self.l2_txt=Label(self.LengthFrame, text ='Longueur 2:')
        self.l2_txt.grid(row=2, column=1)
        self.l1_ent=Entry(self.LengthFrame, width=5)
        self.l1_ent.grid(row=1, column=2)
        self.l2_ent=Entry(self.LengthFrame, width=5)
        self.l2_ent.grid(row=2, column=2, pady=10)

        self.n_txt=Label(self.MiscFrame, text ='Précision:')
        self.n_txt.grid(row=1, column=1, sticky='w')
        self.n_ent=Entry(self.MiscFrame, width=7)
        self.n_ent.grid(row=1, column=2)

        self.g_txt=Label(self.ConstFrame, text ='Pesenteur:')
        self.g_txt.grid(row=1, column=1, sticky='w')
        self.g_ent=Entry(self.ConstFrame, width=6)
        self.g_ent.grid(row=1, column=2)

        self.t0_ent.insert(0, self.t0) #Remplissage des entry
        self.tn_ent.insert(0, self.tn)
        self.u10_ent.insert(0, self.u10)
        self.u20_ent.insert(0, self.u20)
        self.v10_ent.insert(0, self.v10)
        self.v20_ent.insert(0, self.v20)
        self.m1_ent.insert(0, self.m1)
        self.m2_ent.insert(0, self.m2)
        self.l1_ent.insert(0, self.l1)
        self.l2_ent.insert(0, self.l2)
        self.g_ent.insert(0, self.g)
        self.n_ent.insert(0, self.n)

        self.progressbar=ttk.Progressbar(self.fenetre_home, orient="horizontal", length=300, mode="indeterminate") #Définition de la progressbar
        self.progressbar.place(bordermode=OUTSIDE, x=10, y=260, height=20, width=505)


        self.fenetre_home.mainloop() #Appel de la mainloop


    def pendule(self):
        "Méthode définissant le pendule"

        if (self.thread.is_alive()): #Vérification de l'exécution de thread
            self.fenetre_home.after(200, self.pendule)
            return

        else:
            self.fenetre_home.withdraw() #Cache fenêtre home
            self.progressbar.stop() #Arrêt de prograssbar

            self.fenetre_pendule=Toplevel()  #Définition de la fenêtre et du canvas
            self.fenetre_pendule.title('Pendule double')
            icon=tkinter.Image("photo", file='icons/pendule.gif')  #Fichier de l'icône
            self.fenetre_pendule.tk.call('wm', 'iconphoto', self.fenetre_pendule._w, icon)
            self.can = Canvas(self.fenetre_pendule, width = 500, height = 500, bg='grey', highlightthickness=0)
            self.can.pack()

            self.menu_bar=Menu(self.fenetre_pendule)  #Création des menus
            self.fenetre_pendule.config(menu=self.menu_bar)
            self.file_menu=Menu(self.menu_bar, tearoff=0)
            self.help_menu=Menu(self.menu_bar, tearoff=0)
            self.menu_bar.add_cascade(label="Fichier", menu=self.file_menu)
            self.file_menu.add_command(label="Nouveau", command=self.new)
            self.file_menu.add_command(label="Quitter", command=self.fenetre_home.destroy)
            self.menu_bar.add_cascade(label="Aide", menu=self.help_menu)
            self.help_menu.add_command(label="À propos", command=self.about)

            self.cx,self.cy=250,250 #Définition du système de coordonnées
            x1,y1=self.COORD1[0]
            x2,y2=self.COORD2[0]

            self.bras1 = self.can.create_line(self.cx, self.cy, self.cx+x1, self.cy+y1, fill = 'blue', width = 3)  #Création des objets du pendule
            self.bras2 = self.can.create_line(self.cx+x1, self.cy+y1, self.cx+x1+x2, self.cy+y1+y2, fill = 'green', width = 3)
            self.can.create_oval(self.cx-6,self.cy-6,self.cx+6,self.cy+6,fill='red')
            self.rond1 = self.can.create_oval(self.cx+x1-4, self.cy+y1-4, self.cx+x1+4, self.cy+y1+4, fill='black')
            self.rond2 = self.can.create_oval(self.cx+x1+x2-4, self.cy+y1+y2-4, self.cx+x1+x2+4, self.cy+y1+y2+4, fill='black')

            #self.fenetre_pendule.protocol("WM_DELETE_WINDOW", self.fenetre_home.deiconify())

            self.move()  #Appel de la méthode d'animation


    def resolution(self,t0,tn,u10,u20,v10,v20,m1,m2,l1,l2,g,n):
        "Méthode permettant la résolution des équations différentielles (Euler explicite)"

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
            self.T.append(t1)
            self.U1.append(u11)
            self.U2.append(u21)
            self.V1.append(v11)
            self.V2.append(v21)
            t0=t1
            u10=u11
            u20=u21
            v10=v11
            v20=v21

        self.COORD1=self.conversion(self.U1,100)
        self.COORD2=self.conversion(self.U2,100)


    def conversion(self,ANGLE,l):
        "Méthode permettant de passer des coordonnées polaires à carthésiennes"

        COORD=[]
        for k in range(len(ANGLE)): #Projection dans le repère carthésien
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
            self.can.after(self.periode, self.move)  #Répetition de la méthode


    def about(self):
        "Fenêtre About"

        self.fenetre_about=Toplevel() #Définition de la fenêtre
        self.fenetre_about.title('À propos')
        self.fenetre_about.geometry('250x150')
        icon=tkinter.Image("photo", file='icons/about.gif')  #Fichier de l'icône
        self.fenetre_about.tk.call('wm', 'iconphoto', self.fenetre_about._w, icon)
        self.fenetre_about.resizable(width=False, height=False)
        self.fenetre_about.transient(self.fenetre_pendule)
        self.fenetre_about.grab_set()
        font=tkFont.Font(size=13)
        Label(self.fenetre_about, text='Développé avec amour\npar Marc-Antoine GODDE', font=font).pack(padx=5, pady=10)
        Label(self.fenetre_about, text='Copyright © 2019').pack(padx=5, pady=5)
        self.bouton_ok=Button(self.fenetre_about, text='Ok', command=self.fenetre_about.destroy).pack(padx=5, pady=5)


    def start(self):
        "Double commande démarrage"

        self.settings() #Récupérations des paramètres
        if self.flag==1:
            return
        self.periode=int(((self.tn-self.t0)/self.n)*1E3) #Définition d'une période constante
        self.bouton_start.config(state=DISABLED) #Désactivation de l'interface
        self.bouton_reset.config(state=DISABLED)
        self.bouton_quit.config(state=DISABLED)
        self.t0_ent.config(state=DISABLED)
        self.tn_ent.config(state=DISABLED)
        self.u10_ent.config(state=DISABLED)
        self.u20_ent.config(state=DISABLED)
        self.v10_ent.config(state=DISABLED)
        self.v20_ent.config(state=DISABLED)
        self.m1_ent.config(state=DISABLED)
        self.m2_ent.config(state=DISABLED)
        self.l1_ent.config(state=DISABLED)
        self.l2_ent.config(state=DISABLED)
        self.g_ent.config(state=DISABLED)
        self.n_ent.config(state=DISABLED)


        self.thread=threading.Thread(target=self.resolution, args=(self.t0,self.tn,self.u10,self.u20,self.v10,self.v20,self.m1,self.m2,self.l1,self.l2,self.g,self.n))
        self.thread.start() #Gestion de la résolution en parallèle
        self.progressbar.start() #Démarrage de la progressbar
        self.fenetre_home.after(200, self.pendule) #Appel de pendule


    def settings(self):
        "Récupération des paramètres"

        try:
            self.t0=int(self.t0_ent.get())
            self.tn=int(self.tn_ent.get())
            self.u10=float(self.u10_ent.get())
            self.u20=float(self.u20_ent.get())
            self.v10=float(self.v10_ent.get())
            self.v20=float(self.v20_ent.get())
            self.m1=float(self.m1_ent.get())
            self.m2=float(self.m2_ent.get())
            self.l1=float(self.l1_ent.get())
            self.l2=float(self.l2_ent.get())
            self.g=float(self.g_ent.get())
            self.n=int(self.n_ent.get())
            self.flag=0

        except ValueError:
            messagebox.showerror("Erreur", "Les paramètres doivent être des valeurs numériques")
            self.flag=1

 
    def reset(self):
        "Réinitialisation des paramètres"

        self.t0_ent.delete(0,END)
        self.tn_ent.delete(0,END)
        self.u10_ent.delete(0,END)
        self.u20_ent.delete(0,END)
        self.v10_ent.delete(0,END)
        self.v20_ent.delete(0,END)
        self.m1_ent.delete(0,END)
        self.m2_ent.delete(0,END)
        self.l1_ent.delete(0,END)
        self.l2_ent.delete(0,END)
        self.g_ent.delete(0,END)
        self.n_ent.delete(0,END)

        self.t0_ent.insert(0, 0)
        self.tn_ent.insert(0, 10000)
        self.u10_ent.insert(0, 1.55)
        self.u20_ent.insert(0, 0)
        self.v10_ent.insert(0, 1)
        self.v20_ent.insert(0, 1)
        self.m1_ent.insert(0, 10)
        self.m2_ent.insert(0, 10)
        self.l1_ent.insert(0, 10)
        self.l2_ent.insert(0, 10)
        self.g_ent.insert(0, 9.81)
        self.n_ent.insert(0, 1000000)


    def new(self):
        "Double commande panneau configuration"

        self.bouton_start.config(state=NORMAL) #Réactivation de l'interface
        self.bouton_reset.config(state=NORMAL)
        self.bouton_quit.config(state=NORMAL)
        self.t0_ent.config(state=NORMAL)
        self.tn_ent.config(state=NORMAL)
        self.u10_ent.config(state=NORMAL)
        self.u20_ent.config(state=NORMAL)
        self.v10_ent.config(state=NORMAL)
        self.v20_ent.config(state=NORMAL)
        self.m1_ent.config(state=NORMAL)
        self.m2_ent.config(state=NORMAL)
        self.l1_ent.config(state=NORMAL)
        self.l2_ent.config(state=NORMAL)
        self.g_ent.config(state=NORMAL)
        self.n_ent.config(state=NORMAL)
        self.fenetre_pendule.destroy()
        self.fenetre_home.deiconify()

        self.i=1
        self.T=[]
        self.U1=[]
        self.U2=[]
        self.V1=[]
        self.V2=[]



if __name__ == "__main__":

    pendule = Pendule()
    pendule.home()
