#!/usr/bin/python3
import tkinter,tkinter.ttk,subprocess

KEYS=['qwert789','asdfg465','zxcvb123']
REFOCUS='xdotool windowfocus `xdotool search --name "LMMS pad"`'

class Group:
  def __init__(self,keys,color):
    self.keys=keys
    self.color=color

root=tkinter.Tk()
frame=tkinter.ttk.Frame(root,padding="3 3 12 12")
groups=[[Group('qwer','red'),Group('789','red')],
        [Group('asdf','yellow'),Group('456','red')],
        [Group('zxcv','blue'),Group('123','red')]]
origin=[78,186]
active=set()

def run(command):
  subprocess.run(command,shell=True)
  
def find(key):
  i=0
  for row in groups:
    for group in row:
      for k in group.keys:
        if k==key:
          return origin[1]+32*i
        i+=1
        
def group(key):
  for row in groups:
    for group in row:
      if key in group.keys:
        return group
  return False

def press(key):
  if key in active:
    return
  for k in group(key).keys:
    if k==key:
      active.add(k)
    elif k in active:
      active.remove(k)
    else:
      continue
    x=origin[0]
    y=find(k)
    run(f'xdotool mousemove {x} {y} click 1')
  run(REFOCUS)
  
def calibrate():
  print('calibrate')

def setup():
  root.title("LMMS pad")
  root.columnconfigure(0,weight=1)
  root.rowconfigure(0,weight=1)
  frame.grid(column=0,row=0)
  tkinter.ttk.Button(frame,text='Calibrate',command=calibrate).grid(column=0,row=0)
  for i,row in enumerate(groups):
    column=0
    for group in row:
      for k in group.keys:
        tkinter.ttk.Button(frame,text=k,command=lambda k=k:press(k)).grid(column=column,row=i+1)
        root.bind(k,lambda x,k=k:press(k))
        if k.isnumeric():
          root.bind(f'<KP_{k}>',lambda x,k=k:press(k))
        column+=1
  #for c in frame.winfo_children(): 
  #    c.grid_configure(padx=5,pady=5)
  root.bind('<Escape>',lambda x:root.destroy())
  root.mainloop()

setup()
