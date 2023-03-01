#!/usr/bin/python3
import tkinter,tkinter.ttk,subprocess

KEYS=['qwert789','asdfg465','zxcvb123']
REFOCUS='xdotool windowfocus `xdotool search --name "LMMS pad"`'

class Group:
  def __init__(self,keys):
    self.keys=keys

root=tkinter.Tk()
frame=tkinter.ttk.Frame(root,padding="3 3 12 12")
groups=[[Group('qwer')],
        [Group('asdf')],
        [Group('zxcv')],
        [Group('7'),Group('8'),Group('9')],
        [Group('4'),Group('5'),Group('6')],
        [Group('1'),Group('2'),Group('3')]]
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

def activate(key):
  for k in group(key).keys:
    if k==key and k not in active:
      active.add(k)
    elif k in active:
      active.remove(k)
    else:
      continue
    x=origin[0]
    y=find(k)
    run(f'xdotool mousemove {x} {y} click 1')
  run(REFOCUS)
  
def mute():
  for a in list(active):
    activate(a)

def setup():
  root.title("LMMS pad")
  root.columnconfigure(0,weight=1)
  root.rowconfigure(0,weight=1)
  frame.grid(column=0,row=0)
  for i,row in enumerate(groups):
    column=0
    for group in row:
      for k in group.keys:
        do=lambda k=k:activate(k)
        tkinter.ttk.Button(frame,text=k,command=do).grid(column=column,row=i)
        root.bind(k,lambda x,k=k:activate(k))
        if k.isnumeric():
          root.bind(f'<KP_{k}>',lambda x,k=k:activate(k))
        column+=1
  tkinter.ttk.Button(frame,text='Mute',command=mute).grid(column=0,row=6)
  root.bind('m',lambda x:mute())
  root.bind('<Escape>',lambda x:root.destroy())
  root.mainloop()

setup()
