from tkinter import*
import time
import winsound
import random

global nombre_mouvements,nombre_repetitions,mouvements

mouvements=[]
nombre_mouvements=0
nombre_repetitions=0

#fonction boutton valider
def set_validation():
    global nombre_mouvements,nombre_repetitions,mouvements,temps
    nombre_mouvements = int(entry_mouvements.get())
    entry_mouvements.config(state='disabled')
    nombre_repetitions = int(entry_repetitions.get())
    entry_repetitions.config(state='disabled')
    temps= int(entry_temps.get())
    entry_temps.config(state='disabled')
    button_validation.config(state='disabled')

##


#fonction ajout mouvement
def ajouter_mouvement():
    global nombre_mouvements,nombre_repetitions,mouvements
    mouvement= entry_configmouv.get()
    mouvements.append(mouvement)
    entry_configmouv.delete(0, 'end')
##


#fonction démarrage inquisition
def commencer_inquisition():
    global nombre_mouvements,nombre_repetitions,mouvements
    if len(mouvements) == nombre_mouvements:
            open_fenetre_inquisition()
    else:
        print("Veuillez configurer tous les mouvements avant de commencer l'inquisition.")
##

#fonction ouverture de la fenetre d'inquisition
def open_fenetre_inquisition():
    global nombre_mouvements,nombre_repetitions,mouvements,fenetre_inquisition,points,labels,pointPause,label_pause
    fenetre_inquisition=Tk()
    fenetre_inquisition.title("fenetre_inquisition")
    
    menu_bar=Menu(fenetre_inquisition)
    #un premier menu
    file_menu=Menu(menu_bar,tearoff=0)
    file_menu.add_command(label="Quitter",command=fenetre_inquisition.quit)
    menu_bar.add_cascade(label="Fichier",menu=file_menu)

    fenetre_inquisition.config(menu=menu_bar)

    points = []
    labels = []

    for mouvs in mouvements:
        frame = Frame(fenetre_inquisition)
        frame.pack()
        label_mouvement = Label(frame, text=mouvs, font=('Arial', 12), width=20, anchor='w')
        label_mouvement.pack(side='left')
        labels.append(label_mouvement)

        point = Label(frame, text=" ", font=('Arial', 80))
        point.pack(side='left')
        points.append(point)

    frameptpause=Frame(fenetre_inquisition)
    frameptpause.pack()
    label_pause=Label(frameptpause,text='Pause',font=('Arial', 12), width=20, anchor='w') 
    label_pause.pack(side='left')
    labels.append(label_pause) 

    pointPause = Label(frame, text=" ", font=('Arial', 80))
    pointPause.pack(side='left')
    

    allumer_les_points(points, labels)
## 

#fonction pour allumer les points
def allumer_les_points(points, labels):
    global nombre_mouvements,nombre_repetitions,mouvements

    fenetre_inquisition.title(f"Inquisition - Répétition 1/{nombre_repetitions}")
    for repetition in range(1, nombre_repetitions + 1):
        for i, (point, label) in enumerate(zip(points, labels)):
                
            couleur = "green"
            point.config(text=".", fg=couleur)
            label.config(fg=couleur)
            winsound.Beep(1000, 200)
            fenetre_inquisition.update()
            time.sleep(temps)
            pointPause.config(text=".", fg="red")
            label_pause.config(fg="red")
            fenetre_inquisition.update()
            point.config(text=" ")
            label.config(fg="black")
            fenetre_inquisition.update()
            time.sleep(temps)
            pointPause.config(text=" ",)
            label_pause.config(fg="black")
            


        if repetition < nombre_repetitions:
            fenetre_inquisition.title(f"Inquisition - Répétition {repetition + 1}/{nombre_repetitions}")


window = Tk()
window.title("Interface graphic")
window.geometry('600x480')


label_mouvements=Label(window,text="Nombre de mouvements :")
label_mouvements.pack()

entry_mouvements= Entry(window)
entry_mouvements.pack()

label_repetitions=Label(window,text="Nombre de repetitions :")
label_repetitions.pack()

entry_repetitions= Entry(window)
entry_repetitions.pack()

label_temps=Label(window,text="Temps entre chq bip :")
label_temps.pack()

entry_temps= Entry(window)
entry_temps.pack()

button_validation=Button(window,text='Valider',command=set_validation)   
button_validation.pack()  

label_configmouv=Label(window,text="Configurer les mouvements :")
label_configmouv.pack(pady=20)

entry_configmouv= Entry(window)
entry_configmouv.pack()

button_ajout=Button(window,text="Ajouter",command=ajouter_mouvement)
button_ajout.pack()

button_inquisition=Button(window,text="Commencer l'inquisition",command=commencer_inquisition)
button_inquisition.pack(expand=YES,pady=20)

print(mouvements)   

window.mainloop()
