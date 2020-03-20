import tkinter as tk
from tkinter import filedialog, Text, messagebox
import os
import time
import random
import turtle
from applicationinsights import TelemetryClient
import sys
import logging

root=tk.Tk()

def send_event():
    tc = TelemetryClient('<YOUR INSTRUMENTATION KEY GOES HERE>')
    tc.track_event('Test event')
    tc.flush()
    messagebox.showinfo("updates","sent")

#Sending an event telemetry item with custom properties and measurements

def send_specific():
    filename=filedialog.askopenfilename(initialdir="/" , title="selectfile", filetypes=(("executables","*.exe"),("allfiles","*.*")))
    tc = TelemetryClient('<YOUR INSTRUMENTATION KEY GOES HERE>')
    tc.track_event(filename, { 'foo': 'bar' }, { 'baz': 42 })
    tc.flush()
    messagebox.showinfo("updates","sent")
#Sending an event telemetry item with custom properties and measurements
def costum_event():
    tc = TelemetryClient('<YOUR INSTRUMENTATION KEY GOES HERE>')
    tc.track_event('Test event', { 'foo': 'bar' }, { 'baz': 42 })
    tc.flush()
    messagebox.showinfo("updates","sent")
#Sending a trace telemetry item with custom properties

def trace_item():
    tc = TelemetryClient('<YOUR INSTRUMENTATION KEY GOES HERE>')
    tc.track_trace('Test trace', { 'foo': 'bar' })#trace function to be given 
    tc.flush()

canvas=tk.Canvas(root , height=200, width=200 , bg="#263D42")
canvas.pack()
sendEvent=tk.Button(root,text="send event" , padx=20 , pady=5 , fg="black" , bg="white" ,command=send_event)
sendEvent.pack()
sendSpec=tk.Button(root,text="send sepc event" , padx=20 , pady=5 , fg="black" , bg="white" ,command=send_specific)
sendSpec.pack()
sendCost=tk.Button(root,text="send costum event" , padx=20 , pady=5 , fg="black" , bg="white" ,command=costum_event)
sendCost.pack()
traceItem=tk.Button(root,text="trace event" , padx=20 , pady=5 , fg="black" , bg="white" ,command=trace_item)
traceItem.pack()

root.mainloop()

    
