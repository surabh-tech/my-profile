from tkinter import *
import os
from tkinter import messagebox
import pygame
from mutagen.mp3 import MP3
import functools
import time
from tkinter import font
from tkinter import colorchooser
from tkinter import ttk
base=Tk()
base.geometry("800x700")
base.configure(bg='white')
base.title("Music PLayer")

def changedark():
    play.configure(bg='black')
    frame.configure(bg='black',fg='#F0FFF0')
    status.configure(bg='black')
    timel.configure(fg='#7CFC00',bg='black')
    for i in songlist:
        i.configure(bg='black',fg='#F0FFF0',border=2)
def changelight():
    play.configure(bg='#F0FFF0')
    frame.configure(bg='#FFF8DC',fg='black')
    status.configure(bg='white')
    timel.configure(fg='black',bg='white')
    for i in songlist:
        i.configure(bg='#F0FFFF',fg='black',activebackground='#FFD700')

def btncolor():
        ch=colorchooser.askcolor()
        for i in songlist:
            i.configure(bg=f'{ch[1]}')

def allbackground():
    ch=colorchooser.askcolor()
    frame.configure(bg=f'{ch[1]}')

def textcolor():
    ch=colorchooser.askcolor()
    for i in songlist:
        i.configure(fg=f'{ch[1]}')

def fontchanger():
    root=Toplevel(base)
    root.geometry("500x300")
    def fontchangerdone():
        for i in songlist:
            i.configure(font=(f"{fontselected}", 15))
        root.destroy()
    l=Label(root,text="Select Font :")
    l.place(y=50,x=100)
    f=font.families()
    fontselected=StringVar()
    fontselecter=ttk.Combobox(root,values=f,textvariable=fontselected,state="readonly")
    fontselecter.current(5)
    fontselecter.place(y=50,x=200)
    submit=Button(root,text="Submit",command=fontchangerdone)
    submit.place(y=100,x=170)
theme=Menu(base)
colour=Menu(theme,tearoff=False)
colour.add_command(label='Dark',command=changedark)
colour.add_command(label='Light',command=changelight)

custome=Menu(colour,tearoff=False)
custome.add_command(label='Background',command=allbackground)
custome.add_command(label='Song Background',command=btncolor)
custome.add_command(label='Song Text Colour',command=textcolor)

colour.add_cascade(menu=custome,label='Custome')
theme.add_cascade(menu=colour,label='Change Theme')
theme.add_command(labe='Font',command=fontchanger)

base.configure(menu=theme)


def timetaken():
    t=pygame.mixer.music.get_pos()/1000
    cut=time.strftime('%H:%M:%S',time.gmtime(t))
    timel.configure(text=cut)
    myslier.configure(value=t)
    timel.after(1000,timetaken)
def slide(x):
    pygame.mixer.music.set_pos(float(x))


play=Frame(base,width=50,height=100,bg='#F0FFF0')
play.pack(side=BOTTOM,fill=BOTH,padx=2,pady=2)

status=Frame(base)
status.pack(side=BOTTOM,fill=X)


myslier=ttk.Scale(status,from_=0,to=100,orient=HORIZONTAL,value=0,command=slide,length=500)
myslier.pack(side=TOP,padx=2,fill=X)
timel=Label(status,text="",font=("arial bold",10))
timel.pack(side=TOP,padx=10)
pygame.mixer.init()


frame=LabelFrame(base,text="My Music",font='Verdana 32 bold',bd=4,relief=RIDGE,bg='#FFF8DC',width=100,height=600)
frame.pack(side=TOP,fill=BOTH,padx=2,pady=2,expand=TRUE)



mycanvas=Canvas(frame,bg='white')
mycanvas.pack(side=LEFT,fill=BOTH,expand=1)

# add ascroll bar in canvas
sroll=Scrollbar(frame,orient=VERTICAL,command=mycanvas.yview)
sroll.pack(side=RIGHT,fill=Y)

#configure the canvas
mycanvas.configure(yscrollcommand=sroll.set)

#create another frame in canvas
second=Frame(mycanvas,bg='white',width=100)


# used anchor="nw" and added tag="second"
mycanvas.create_window((0,0),window=second,anchor='nw',tag="second")

# callback for updating scrollregion
def update_scrollregion(event):
    mycanvas.configure(scrollregion=mycanvas.bbox("all"))

# callback for resizing width of "second" frame when "mycanvas" is resized
def resize_frame(event):
    # should apply on the item created by create_window(), not "second" frame
    mycanvas.itemconfigure("second", width=event.width)

mycanvas.bind("<Configure>", resize_frame) # resize "second" frame whenever "mycanvas" is resized
second.bind("<Configure>", update_scrollregion)
global songlenght
def playercmd(s):
    if s==None:
        messagebox.showerror("No Music"," No Music Selected to Play..!")
    else:
        pygame.mixer.music.load(s)
        pygame.mixer.music.play(loops=0)
        timetaken()
        temp=MP3(s)
        songlenght=int(temp.info.length)
        print(songlenght)
        myslier.configure(to=songlenght,value=0)
current=None
playercount=0
def press(event,element,song):
    print(song)
    s="C:/Users/Saurabh/Music/"+song
    global current
    global playercount
    current=s
    playercount=element
    playercmd(s)
song=os.listdir(r"C:\Users\Saurabh\Music")
i=0
length=len(song)
songlist=list()
while(i<length):
    b=Button(second,text=f'{song[i]}',bd=4,height=2,font=('arial bold',20),bg='#F0FFFF',activebackground='#FFD700',relief=GROOVE,activeforeground='#000000')
    b.pack(side=TOP,fill=X,padx=4,pady=4)
    b.bind("<Button>",functools.partial(press,element=i,song=song[i]))
    songlist.append(b)
    i=i+1

def stop():
    pygame.mixer.music.stop()
    timel.configure(text="00:00:00")
global pauseflag
pauseflag=True
def pause():
    global pauseflag
    if pauseflag==True:
        pygame.mixer.music.pause()
        pauseflag=False
    else:
        pygame.mixer.music.unpause()
        pauseflag=True



def forward():
    global playercount
    print(playercount)
    if (playercount+1)<len(songlist):
        song=songlist[playercount+1].cget('text')
        s = "C:/Users/AMEY/Music/" +song
        pygame.mixer.music.load(s)
        pygame.mixer.music.play(loops=0)
        playercount=playercount+1
        print(playercount)
        timetaken()
        temp = MP3(s)
        songlenght = int(temp.info.length)
        myslier.configure(to=songlenght,value=0)

    else:
        messagebox.showwarning("END","Can't Forward .. No Song Ahead..!")
def backward():
    global playercount
    if playercount>0:
        song=songlist[playercount-1].cget('text')
        s = "C:/Users/Saurabh/Music/" + song
        pygame.mixer.music.load(s)
        pygame.mixer.music.play(loops=0)
        playercount=playercount-1
        print(playercount)
        timetaken()
        temp = MP3(s)
        songlenght = int(temp.info.length)
        myslier.configure(to=songlenght,value=0)
    else:
        messagebox.showwarning("Start","No Song Backward..!")
player=Frame(play)
player.pack()
playimg=PhotoImage(file="play.png")
pauseimg=PhotoImage(file="pause.png")
stopimg=PhotoImage(file="stop.png")
forwardimg=PhotoImage(file="forward.png")
backwardimg=PhotoImage(file="backward.png")

playb=Button(player,image=playimg,borderwidth=0,command=functools.partial(playercmd,current))
pauseb=Button(player,image=pauseimg,borderwidth=0,command=pause)
stopb=Button(player,image=stopimg,borderwidth=0,command=stop)
forwardb=Button(player,image=forwardimg,borderwidth=0,command=forward)
backwardb=Button(player,image=backwardimg,borderwidth=0,command=backward)


backwardb.grid(row=0,column=1,padx=50)
pauseb.grid(row=0,column=2,padx=20)
playb.grid(row=0,column=3,padx=10)
stopb.grid(row=0,column=4,padx=20)
forwardb.grid(row=0,column=5,padx=50)


base.mainloop()
