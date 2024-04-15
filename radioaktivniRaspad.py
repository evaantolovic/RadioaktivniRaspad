import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
import matplotlib.pyplot as plt 
                                
                                
import time
class LoadingBar: # klasa za simulaciju
    def __init__(self, master, unos): # izgradnja konstruktora
        self.master = master
        self.unos = unos

        self.progress = ttk.Progressbar(self.master, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=20)
        
    def start_loading(self):
        target_percent = self.unos  # Postotak na koji zelim doci
        
        # Postavljanje maksimalne vrijednosti na 100%
        self.progress["maximum"] = 100
        
        # Postavljanje trenutne vrijednosti na 100%
        self.progress["value"] = 100
        
        # Pokretanje brojača unatrag do zadanog postotka
        for i in range(100, target_percent, -1):
            self.progress["value"] = i
            self.master.update_idletasks()  # azuriranje GUI-a
            time.sleep(0.05)  # cekanje 0.05 sekundi da se vidi animacija

fig = None
canvas = None #moramo ih staviti tu jer ih koristimo kasnije bez inicijalizacije
postotak = 0.0

#kreiramo tkinter
root = tk.Tk()
root.title("Radioaktivni raspadi - simulacija radioaktivnog raspada") #nije tocno odreden jedan element nego je lambo promjenjiv kako bi provjerili za vise elemenata

#slider za provedeno vrijeme
slider_1 = tk.Label(root, text="Provedeno vrijeme ")
broj_slider_1 = tk.Scale(root, from_=1, to=100000, orient=tk.HORIZONTAL, #takoder u danima da matcha vrijeme poluraspada
                        sliderlength=20, sliderrelief=tk.RAISED, 
                        bg="lightgray", fg="blue")
broj_slider_1.pack(pady=10)
slider_1.pack()

#slider za selectanje elementa tjst mjenjanje lambde
slider_2 = tk.Label(root, text="Vrijeme poluraspada (element u pitanju) ")
broj_slider_2 = tk.Scale(root, from_=1, to=100000, orient=tk.HORIZONTAL, #moze se mjenjati od - do, stavila sam vrijeme u danima jer to pokriva dosta elemenata 
                        sliderlength=20, sliderrelief=tk.RAISED, 
                        bg="lightgray", fg="blue")
broj_slider_2.pack(pady=10)
slider_2.pack()

#slider za selectanje broja cestica na pocetku
slider_3 = tk.Label(root, text="Broj cestica na pocetku ")
broj_slider_3 = tk.Scale(root, from_=100, to=1000, orient=tk.HORIZONTAL,  # nisam mogla pronac realisticne vrijednosti za ovo
                        sliderlength=20, sliderrelief=tk.RAISED, 
                        bg="lightgray", fg="blue")
broj_slider_3.pack(pady=10)
slider_3.pack()

def nacrtaj_graf(list1, list2):
    # Kreiranje figure
    fig = Figure(figsize=(5, 4), dpi=100)
    
    # Dodavanje subplota
    plot = fig.add_subplot(1, 1, 1)
    
    # Crtanje grafa
    plot.plot(list1, list2)

    # Stvaranje Tkinter prozora
    prozor_grafa = tk.Toplevel()
    prozor_grafa.title("Graf u Tkinteru")

    # Stvaranje Tkinter canvasa
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def simulacija(unos):
    # Stvaranje novog prozora
    novi_prozor = tk.Toplevel(root)
    novi_prozor.title("Simulacija poluraspada elementa")
    # Dodavanje teksta u novi prozor
    label = tk.Label(novi_prozor, text="Nakon " + str(broj_slider_1.get()) + " dana ostati ce ovoliko cestica od 100%:\n" + str(int(postotak * broj_slider_3.get()) / 100) + "/" + str(broj_slider_3.get()))
    label.pack()
    app = LoadingBar(novi_prozor, unos)
    LoadingBar.start_loading(app)

def dobivanje_vrijednosti():
    global fig, canvas, postotak #globalne varijable s pocetka, da se zna da nisu privatne iz funkcije
    provedeno_vrijeme = broj_slider_1.get()  # dohvacanje pocetnog broja sa slidera
    lambda_elementa = broj_slider_2.get()  # dohvacanje pocetnog broja sa slidera
    pocetni_broj_cestica = broj_slider_3.get()  # dohvacanje pocetnog broja sa slidera
    cestice = []
    for i in range(provedeno_vrijeme):
        broj_cestica_tmp = pocetni_broj_cestica * 2 ** (-(i/lambda_elementa)) #racunanje broja cestica
        cestice.append(broj_cestica_tmp)
    postotak = (cestice[provedeno_vrijeme - 1] / broj_slider_3.get()) * 100
    if canvas:
        canvas.get_tk_widget().destroy()  # brisem stari graf kad se nes updatea
    fig = Figure(figsize=(5, 4), dpi=100)
    plot = fig.add_subplot(1, 1, 1)
    plot.plot(range(len(cestice)), cestice)
    plot.set_xlabel('Broj provedenih dana')
    plot.set_ylabel('Broj cestica')
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()
def update(): 
    dobivanje_vrijednosti()  
    root.after(100, update) #rekurvizna funkcija
gumb = tk.Button(root, text="Simulacija", command=lambda:simulacija(int(postotak))) #lambda da mi se ne runna funkcija simulacija prije klika na gumb
gumb.pack()
update()
root.mainloop() #runnam tkinter