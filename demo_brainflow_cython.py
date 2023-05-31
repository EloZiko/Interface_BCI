
import numpy as np
import PySimpleGUI as sg
import time
import random
#from utils_mi import *
import argparse
import time
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, BrainFlowPresets


n_runs = 1  # nombre de runs
n_conditions = 1 # nombre de type de mouvement par run
conditions = list(['_right_','_left_','_feets_'])*n_conditions
np.random.shuffle(conditions)

dict_c = {
'_right_':2,
'_left_':3,
'_feets_':4
}
# dictionnaire pour indiquer les triggers dans le signal, Ne pas utiliser 0


layout = [[sg.Text('Motor Imagery', size=(20,1))],
        [sg.Text('', size=(8, 2), font=('Helvetica', 20),justification='center', key='text'),sg.Text('Cue'),LEDIndicator('_cue_')],
        [sg.Text('Left'), LEDIndicator('_left_'),sg.Text('Right'), LEDIndicator('_right_')],
          [sg.Text(''),sg.Text('Feets'),LEDIndicator('_feets_')],
         [sg.Text('', size=(8, 2), font=('Helvetica', 20),justification='center', key='MI')],

          [sg.Button('Exit')]]

window = sg.Window('My new window', layout, default_element_size=(12, 1), auto_size_text=False, finalize=True)
current_time, paused_time, paused = 0, 0, False

def time_int():
    return int(round(time.time() * 100))

def LEDIndicator(key=None, radius=100):
    return sg.Graph(canvas_size=(radius, radius),
             graph_bottom_left=(-radius, -radius),
             graph_top_right=(radius, radius),
             pad=(0, 0), key=key)



def SetLED(window, key, color):
    graph = window[key]
    graph.erase()
    graph.draw_circle((0, 0), 12, fill_color=color, line_color=color)

def set_leds_gray():
    SetLED(window, '_left_',  'gray')
    SetLED(window, '_right_', 'gray')
    SetLED(window, '_feets_', 'gray')
    SetLED(window, '_cue_',   'blue')



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
                    required=True)
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



def main():

    board.prepare_session()
    board.start_stream()
    time.sleep(10)
    for run in range(n_runs):
        i = 0
        for condition in conditions:
            window['text'].update('REST')
            #start_time = time_int()
            #current_time = time_int() - start_time
            set_leds_gray()
            event, values = window.read(timeout=10)
            time.sleep(3) #3
            SetLED(window, '_cue_',   'yellow')
            event, values = window.read(timeout=10)
            time.sleep(1) #1
            window['text'].update('START')
            SetLED(window, '_cue_',   'green')
            event, values = window.read(timeout=10)
            SetLED(window, condition,   'green')
            board.insert_marker(dict_c[condition])
            event, values = window.read(timeout=10)
            time.sleep(2) #2
            SetLED(window, condition,   'gray')
            SetLED(window, '_cue_',   'gray')
            event, values = window.read(timeout=10)
            time.sleep(4) #4
            board.insert_marker(1)
            time.sleep(2) #2  #PROBLEME ICI le sleep est au mauvais endroit
            i+=1
            if i!=0 and i%30==0:
                time.sleep(15) #15
                window['text'].update('BREAK')
        time.sleep(5) #5
        data = board.get_board_data()
        np.save('data_'+str(time_int()),data)
        board.stop_stream()
        board.release_session()
    window.close()

   

if __name__ == "__main__":
    main()


    