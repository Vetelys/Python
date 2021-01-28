import pyaudio
import wave
import numpy as np
import crepe
import time
from tkinter import *
import tk_tools

notes = dict({
82.41:"E2",
110:"A2",
146.83:"D3",
196:"G3",
246.94:"B3",
329.63:"E4",
})

FORMAT = pyaudio.paInt16
CHANNELS = 1
SR = 44100
SAMPLES = 4096
WINDOW = np.blackman(SAMPLES)


def closest(freq):
    closest = 82.41
    prev = 1000
    for key in notes:
        if np.abs(freq-key) < prev:
            prev = np.abs(freq-key)
            closest = key
    return closest



def plotFFT(stream):
    streamData = stream.read(SAMPLES, exception_on_overflow=False)
    data = wave.struct.unpack("%dh"%(SAMPLES), streamData)
    npData = np.array(data)
    filteredData = npData*WINDOW
    timer, frequency, confidence, activation = crepe.predict(filteredData, SR, viterbi=True, step_size=50)
    freq = sum(frequency)/len(frequency)
    note = closest(freq)
    error = np.abs(freq-note)
    lbl.configure(text=notes[note])

    if np.abs(error) < 25:
        gauge.set_value(freq-note)

    if error < 3:
        print("Done tuning ", notes[note])
        led.to_green()
    else:
        led.to_red()
    window.update()
    time.sleep(0.05)

def start_button_clicked():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=SR, input=True, frames_per_buffer=SAMPLES)
    while 1:
        plotFFT(stream)

def quit_button_clicked():
    window.destroy()

window = Tk()
window.title("Kitaranviritin by Joona")
window.geometry('415x300')
lbl = Label(window, text="-")
quit_btn = Button(window, text="Lopeta", command=quit_button_clicked)
start_btn = Button(window, text="Käynnistä", command=start_button_clicked)
start_btn.grid(column=1, row=0)
quit_btn.grid(column=3, row=0)
lbl.grid(column=2, row=0)
gauge = tk_tools.Gauge(window, width=300, height=200, label="Error",
                       min_value=-10.0, max_value=10.0, divisions=50, red_low=20,
                       red=80, yellow_low=45, yellow=55)
led = tk_tools.Led(window, size=50)
led.grid(column=2, row=1)
gauge.grid(row=2, column=2)
window.mainloop()
