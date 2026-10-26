print("Starting")

import board

import digitalio

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import make_key
from kmk.scanners.touch import TouchScanner
from kmk.extensions.media_keys import MIDI

#toggle switch
toggle_switch_up = digitalio.DigitalInOut(board.RX)
toggle_switch_down = digitalio.DigitalInOut(board.TX)
toggle_switch_up.direction = digitalio.Direction.INPUT
toggle_switch_down.direction = digitalio.Direction.INPUT
toggle_switch_up.pull = digitalio.Pull.UP
toggle_switch_down.pull = digitalio.Pull.UP
previous_state_up = True
previous_state_down = True

#button for modes
mode = digitalio.DigitalInOut(board.IO1)
mode.direction = digitalio.Direction.INPUT
mode.pull = digitalio.Pull.UP
previous_state_button = True

#capacitive keys
keyboard = KMKKeyboard()
midi = MIDI()
octave = 0
currentMode = 0
volume = 64


#on or off note, octave will change
def note(keyboard, coordinate, is_played):
   
    actual = MIDDLE_OCTAVE[coordinate] + (octave*12)

    if is_played:
        midi.note_on(actual, velocity=volume)
    else:
        midi.note_off(actual)
    

def change_toggle():
    global currentMode
    global volume
    global octave
    #previous states to detect edge (so continously pressed down doesn't matter)
    global previous_state_up
    global previous_state_down
    global previous_state_button
    if mode.value == False and previous_state_button == True:
        #1 means 2 modes b/c final case will add it up to 1 before run again and find it, can change amount of modes easily
        if currentMode < 1:
            currentMode += 1
        else:
            currentMode = 0
    else:
        #changes octave variable based on toggle switch input
        if currentMode == 0:
            if toggle_switch_up.value == False and previous_state_up == True:
                octave += 1
                
            elif toggle_switch_down.value == False and previous_state_down == True:
                octave -= 1
            print("Octave: ", octave)
        #changes volume variable
        else:
            if toggle_switch_up.value == False and previous_state_up == True:
                volume += 16
            elif toggle_switch_down.value == False and previous_state_down == True:
                volume -= 16    
            print("Bolume: ", volume)
    previous_state_up = toggle_switch_up.value
    previous_state_down = toggle_switch_down.value  
    previous_state_button = mode.value


MIDDLE_OCTAVE = [60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71]

keyboard.matrix = TouchScanner(
    pins=[board.IO2, board.IO3, board.IO4, board.IO5, board.IO6, board.IO7, board.IO8, board.IO9, board.IO10, board.IO11, board.IO12, board.IO13]
)

def pressed(coordinate, keyboard, *a):
    note(keyboard, coordinate.meta, True)

def released(coordinate, keyboard, *a):
    note(keyboard, coordinate.meta, False)

MIDI_Keys = [
    make_key(on_press = pressed, on_release = released, meta=i)    
    for i in range (0, 12)
]

keyboard.keymap = [
    MIDI_Keys
]

keyboard.loop = change_toggle

if __name__ == '__main__':
    keyboard.go()