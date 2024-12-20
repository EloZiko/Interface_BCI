from tkinter import*
import time
import winsound
import random
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, BrainFlowPresets
import argparse

global nombre_mouvements,nombre_repetitions,mouvements,temps_action,temps_pause

mouvements=["Gauche","Droite","Langue","Pieds"]
nombre_mouvements=4
nombre_repetitions=30
temps_action=4
temps_pause=3
temps_pauselongue=10
temps_sur_la_croix=2
conditions = list(['_right_','_left_','_feets_', '_tongue_'])


dict_c = {
'_right_':2,
'_left_':3,
'_feets_':4,
'_tongue_':5
}

BoardShim.enable_dev_board_logger()
parser = argparse.ArgumentParser()
# use docs to check which parameters are required for specific board, e.g. for Cyton - set serial port
parser.add_argument('--timeout', type=int, help='timeout for device discovery or connection', required=False,
                    default=0)
parser.add_argument('--ip-port', type=int, help='ip port', required=False, default=0)
parser.add_argument('--ip-protocol', type=int, help='ip protocol, check IpProtocolType enum', required=False,
                    default=0)
parser.add_argument('--ip-address', type=str, help='ip address', required=False, default='')
parser.add_argument('--serial-port', type=str, help='serial port', required=False, default='')
parser.add_argument('--mac-address', type=str, help='mac address', required=False, default='')
parser.add_argument('--other-info', type=str, help='other info', required=False, default='')
parser.add_argument('--serial-number', type=str, help='serial number', required=False, default='')
parser.add_argument('--board-id', type=int, help='board id, check docs to get a list of supported boards',
                    required=False, default=0)
parser.add_argument('--file', type=str, help='file', required=False, default='')
parser.add_argument('--master-board', type=int, help='master board id for streaming and playback boards',
                    required=False, default=BoardIds.NO_BOARD)
parser.add_argument('--preset', type=int, help='preset for streaming and playback boards',
                    required=False, default=BrainFlowPresets.DEFAULT_PRESET)
args = parser.parse_args()
params = BrainFlowInputParams()
params.ip_port = args.ip_port
params.serial_port = args.serial_port
params.mac_address = args.mac_address
params.other_info = args.other_info
params.serial_number = args.serial_number
params.ip_address = args.ip_address
params.ip_protocol = args.ip_protocol
params.timeout = args.timeout
params.file = args.file
params.master_board = args.master_board
params.preset = args.preset

board = BoardShim(args.board_id, params)




#Création fenêtre   
fenetre_acquisition=Tk()
fenetre_acquisition.title("fenetre_acquisition")
fenetre_acquisition.columnconfigure([0,1,2,3], weight=1, minsize=75)
fenetre_acquisition.rowconfigure([0,1,2,3], weight=1, minsize=50)

       
menu_bar=Menu(fenetre_acquisition)
#Un premier menu
file_menu=Menu(menu_bar,tearoff=0)
file_menu.add_command(label="Quitter",command=fenetre_acquisition.quit)
menu_bar.add_cascade(label="Fichier",menu=file_menu)
fenetre_acquisition.config(menu=menu_bar)

#Gauche
frame= Frame(fenetre_acquisition,relief=RAISED,borderwidth=1)
frame.grid(row=1,column=0,padx=5, pady=5)

label_mouvements1=Label(frame,text="Gauche",font=('Arial', 12), width=20, anchor='w')
label_mouvements1.pack()
point1 = Label(frame,text=" ", font=('Arial', 80))
point1.pack()

#Droite
frame= Frame(fenetre_acquisition,relief=RAISED,borderwidth=1)
frame.grid(row=1,column=2,padx=5, pady=5)
label_mouvements2=Label(frame,text="Droite",font=('Arial',12),width=20,anchor='w')
label_mouvements2.pack()
point2 = Label(frame,text=" ", font=('Arial', 80))
point2.pack()

#Langue
frame= Frame(fenetre_acquisition,relief=RAISED,borderwidth=1)
frame.grid(row=0,column=1,padx=5, pady=5)
label_mouvements3=Label(frame,text="Langue",font=('Arial', 12), width=20, anchor='w')
label_mouvements3.pack()
point3 = Label(frame,text=" ", font=('Arial', 80))
point3.pack()

#Pieds
frame= Frame(fenetre_acquisition,relief=RAISED,borderwidth=1)
frame.grid(row=3,column=1,padx=5, pady=5)
label_mouvements4=Label(frame,text="Pieds",font=('Arial', 12), width=20, anchor='w')
label_mouvements4.pack()
point4 = Label(frame,text=" ", font=('Arial', 80))
point4.pack()


#Croix
frame=Frame(fenetre_acquisition)
frame.grid(row=1,column=1,padx=10, pady=5,sticky="e")
label_croix=Label(frame,text="                     +",font=('Arial',30),width=20,anchor='w')
label_croix.pack()



frame=Frame(fenetre_acquisition,relief=RAISED,borderwidth=1)
frame.grid(row=3,column=3,padx=5, pady=5,sticky="e")
label_pause=Label(frame,text='Pause',font=('Arial', 12), width=20, anchor='w') 
label_pause.pack()



#Pause
pointPause = Label(frame, text=" ", font=('Arial', 80))
pointPause.pack()


labels =[label_mouvements1,label_mouvements2,label_mouvements3,label_mouvements4]
points=[point1,point2,point3,point4]


#Pour ajouter des points supplémentaires (modifier le nombre de mouvements et aussi les listes points et labels)
'''
    frame= Frame(fenetre_acquisition)
    frame.grid(row=0,column=1) #où on veut le placer (c'est un tableau)
    label_name=Label(frame,text="Autre",font=('Arial',12),width=20,anchor='w')
    label_name.pack()

    pt_name = Label(frame,text=" ", font=('Arial', 80))
    pt_name.pack()
'''

fenetre_acquisition.title(f"Acquisition - Répétition 1/{nombre_repetitions}")

#fonction pour allumer les points
def acquisition():

    global nombre_mouvements,nombre_repetitions,mouvements,temps_action,temps_pause,labels,points,pointPause,label_pause,label_croix
    #board.prepare_session()
    #board.start_stream()
    time.sleep(2)

    for repetition in range(1, nombre_repetitions + 1):
        for i, (point, label) in enumerate(zip(points, labels)):
            
            if repetition == 10:
                time.sleep(temps_pauselongue)
                
            
            winsound.Beep(500, 200)
            label_croix.config(fg="red")
            fenetre_acquisition.update()
            time.sleep(temps_sur_la_croix)
            

            label_croix.config(fg="black")
            label.config(fg="green")
            point.config(text=".", fg="green")
            winsound.Beep(1000, 200)
            for (point2,label2) in zip(points,labels):
                if point2 != point:
                    point2.config(text=" ")
                    label2.config(fg="#F0F0F0")
            fenetre_acquisition.update()
            time.sleep(1)

            #Ajouter la partie Motor imagery


            time.sleep(1)

            point.config(text=" ")
            label.config(fg="black")
            fenetre_acquisition.update()

            time.sleep(temps_action)


            #Pause
            
            winsound.Beep(700, 200) 
            pointPause.config(text=".", fg="red")
            label_pause.config(fg="red")
            
            
            for (point2,label2) in zip(points,labels):
                if point2 != point:
                    point2.config(text=" ")
                    label2.config(fg="black")
                
            
            fenetre_acquisition.update()

            time.sleep(temps_pause)    
            pointPause.config(text=" ",)
            label_pause.config(fg="black")
            


        if repetition < nombre_repetitions:
            fenetre_acquisition.title(f"Acquisition - Répétition {repetition + 1}/{nombre_repetitions}")


    


    
## 

    
acquisition()
    
print(mouvements)   

fenetre_acquisition.mainloop()
