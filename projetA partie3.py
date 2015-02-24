from tkinter import *
from tkinter.simpledialog import *
from math import *

class NetworkFrame:
    def __init__(self, parent, w_canvas, h_canvas, r_canvas):
        self.r_canvas = r_canvas
        self.center_node = []
        self.parent = parent
        self.radius = IntVar()
        self.radius.set(r_canvas)
        self.w = w_canvas
        self.h = h_canvas
        self.canva = Canvas(
                    self.parent,
                    width=self.w,
                    height=self.h
                )
        self.update_canvas()
        self.canva.pack()
        
    def update_canvas(self, nbr_people=0):
        radius = self.radius.get()
        self.canva.delete(ALL)
        self.canva.create_oval(
                radius*2,
                radius*2,
                self.w-radius*2,
                self.h-radius*2
            )
        Link(self.canva, self.center_node, self.r_canvas)
            
        #Je passe les ronds qui représente les gens du réseau
        for i in range(nbr_people):
            coor_x = \
                self.w/2 - ((self.w-radius*4)/2 * 
                                        cos((i*(360/nbr_people)-45) * pi/180))
            coor_y = \
                self.h/2 + ((self.h-radius*4)/2 *
                                        sin((i*(360/nbr_people)-45) * pi/180))
            self.canva.create_oval(
                            coor_x - radius,
                            coor_y - radius,
                            coor_x + radius,
                            coor_y + radius,
                            fill="black",
                            activeoutline="red",
                            )
            if (coor_x, coor_y) not in self.center_node:
                self.center_node.append((coor_x,coor_y))
        
class Person:
    def __init__(self):
        pass
        
class Link:
    def __init__(self, canva, center_node, r_canvas):
        self.link_person = None
        self.pos_link = []
        self.r_canvas = r_canvas
        self.center_node = center_node
        self.canva = canva
        self.drawn = None
        self.right_pos = False
        self.right_pos_end = False
        self.canva.bind("<Button-1>", self.onStart)
        self.canva.bind("<B1-Motion>", self.drawing_line)
        self.canva.bind("<ButtonRelease-1>", self.onEnd)
        
    def onStart(self, event):
        i = 0
        self.right_pos = False
        self.start = event
        self.drawn = None
        while not self.right_pos and i < len(self.center_node):
            if self.center_node[i][0] - self.r_canvas <= self.start.x \
                            <= self.center_node[i][0] + self.r_canvas \
                            and \
                            self.center_node[i][1] - self.r_canvas \
                            <= self.start.y <= self.center_node[i][1] + \
                            self.r_canvas:
                self.right_pos = True
            i += 1
        
    def onEnd(self, event):
        canva = event.widget
        i = 0
        self.right_pos_end = False
        self.end = event
        while not self.right_pos_end and i < len(self.center_node):
            if self.center_node[i][0] - self.r_canvas <= self.end.x \
                            <= self.center_node[i][0] + self.r_canvas \
                            and \
                            self.center_node[i][1] - self.r_canvas \
                            <= self.end.y <= self.center_node[i][1] + \
                            self.r_canvas:
                self.right_pos_end = True
            i += 1
        canva.delete(self.link_person)
        if self.right_pos_end:
            canva.create_line(
                        self.center_node[i][0],
                        self.center_node[i][1]
        
    def drawing_line(self, event):
        canva = event.widget
        if self.drawn:
            canva.delete(self.drawn)
        if self.right_pos:
            self.link_person = canva.create_line(
                                    self.start.x,
                                    self.start.y,
                                    event.x,
                                    event.y,
                                    width=2,
                                    activefill="blue",
                                    fill="black"
                                )
            self.drawn = self.link_person
        
class GUI:
    def __init__(self):
        self.master = Tk()
        
        self.names = []
        W_CANVAS, H_CANVAS, R_CANVAS = 750, 300, 20
        
        #Les Frame pour mieux gérer la place dans l'interface graphique
        self.canvaframe = Frame(
                            self.master,
                            borderwidth=2,
                            relief="groove",
                            padx=5,
                            pady=5
                        )
        self.canvaframe.pack(side=TOP)
        
        self.under_canva = Frame(
                            self.master,
                            borderwidth=2,
                            relief="groove",
                            padx=5,
                            pady=5
                        )
        self.under_canva.pack()
        
        self.under_right = Frame(self.under_canva)
        self.under_right.pack(side=RIGHT)
        self.under_left = Frame(self.under_canva)
        self.under_left.pack(side=LEFT)
                            
        
        self.canva = NetworkFrame(self.canvaframe, W_CANVAS, H_CANVAS, R_CANVAS)
                            
        addpeople_name = StringVar()
        addpeople_name.set("Nom de la personne à ajouter au réseau")
        
        #/!\ Ajoute un rond même si on annule, ferme la fenetre qui pop /!\
        self.addpeople_button = Button(
                            self.under_canva,
                            text="Ajouter une personne au réseau",
                            command=self.more_people,
                            cursor = "hand2"
                        )
        self.addpeople_button.pack()
        
        self.radius_scalebar = Scale(
                            self.under_right,
                            to=50,
                            cursor="hand2",
                            variable=self.canva.radius,
                            command=lambda x: \
                            self.canva.update_canvas(len(self.names))
                        )
        self.radius_scalebar.pack(side=BOTTOM)
        
        radius_text = Label(self.under_right, text="Rayon").pack()
        
        #Les listboxes qui permet de modifier la rumeur
        listbox_text = Label(self.under_left, text="Modification de la rumeur")
        listbox_text.pack()
        
        self.modif_choicenib = Listbox(
                            self.under_left,
                            height=3,
                            exportselection=False
                        )
        self.modif_choicenib.insert(1, "None")
        self.modif_choicenib.insert(2, "Incremental")
        self.modif_choicenib.insert(3, "Bitflip")
        self.modif_choicenib.pack(side=LEFT)
        
        self.modif_choicersr = Listbox(
                            self.under_left,
                            height=3,
                            exportselection=False
                        )
        self.modif_choicersr.insert(1, "Random")
        self.modif_choicersr.insert(2, "Stable")
        self.modif_choicersr.insert(3, "Rewrite")
        self.modif_choicersr.pack(side=RIGHT)
        
    def modif_rumor(self):
        modifnib = self.modif_choicenib.curselection()
        modifrsr = self.modif_choicersr.curselection()
        #à relier au code principale avec la modification de la rumeur
        if modifnib == 1:
            pass
        elif modifnib == 2:
            pass
        else:
            pass
        if modifrsr == 1:
            pass
        elif modifrsr == 2:
            pass
        else:
            pass
        
    def more_people(self):
        name_perso = askstring("Ajout de personne",
                               "Nom de la personne à ajouter au réseau")
        self.names.append(name_perso)
        self.canva.update_canvas(len(self.names))

    def start(self):
        self.master.mainloop()

def GUI_main():
    #créer les variables informedPeople, names, etc.
    
    application = GUI()
    application.network = [[True, True], [True, True]]
    application.start()

if __name__ == "__main__":
    GUI_main()
