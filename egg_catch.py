from tkinter import *
from random import randrange
from itertools import cycle
from tkinter import messagebox

canvas_height = 400
canvas_width = 800

win = Tk()
c=Canvas(win, width = canvas_width, height=canvas_height, background='deep sky blue')
c.create_rectangle(-10,canvas_height-100,canvas_width+5,canvas_height+5 ,fill='sea green',width=0)
c.create_oval(-80,-80,120,120,fill='orange',width=0)
c.create_line(0,0,120,120,fill='orange')
c.create_line(110,0,150,10,fill='orange')
c.create_line(0,110,10,150,fill='orange')
c.create_line(20,100,40,160,fill='orange')
c.create_line(100,20,160,40,fill='orange')
c.create_line(45,45,90,150,fill='orange')
c.create_line(45,45,150,90,fill='orange')
c.pack()

color_cycle=cycle(['light blue','cyan','light pink','light yellow','white','red','green','blue'])
egg_w,egg_h=(45,55)
egg_score=10
egg_speed=500
egg_interval=4000
difficulty=0.95

catcher_color='blue'
catcher_w=100
catcher_h=100
catcher_start_x=canvas_width / 2 - catcher_w / 2
catcher_start_y=canvas_height -catcher_h - 20
catcher_start_x2= catcher_start_x + catcher_w
catcher_start_y2=catcher_start_y + catcher_h

catcher=c.create_arc(catcher_start_x,catcher_start_y,catcher_start_x2,catcher_start_y2,start=200,extent=140,style='arc',outline=catcher_color,width=3)

#score
score=0
score_text=c.create_text(10,10,anchor='nw',fill='darkblue',font=('Arial',14,'bold'),text='Score : '+ str(score))

#lives
live=3
live_text=c.create_text(780,10,anchor='ne',fill='black',font=('Arial',14,'bold'),text='Lives : '+str(live))

egg=[]
def create_eggs():
    x = randrange(20,740)
    y=40
    new_egg = c.create_oval(x,y,egg_w+x,egg_h+y,fill=next(color_cycle),width=0)
    egg.append(new_egg)
    win.after(egg_interval,create_eggs)

def move_eggs():
    for i in egg:
        (i_x,i_y,i_x2,i_y2)=c.coords(i)
        c.move(i,0,10)
        if i_y2>canvas_height:
            egg_dropped(i)
    win.after(egg_speed,move_eggs)

def egg_dropped(i):
    egg.remove(i)
    lose_a_life()
    if live==0:
        messagebox.showinfo('GAME OVER' , 'Final Score : ' +str(score))
        win.destroy()
def lose_a_life():
    global live
    live = live -1
    c.itemconfigure(live_text, text='Lives : ' + str(live))

def catch_check():
    (catcher_x,catcher_y,catcher_x2,catcher_y2) = c.coords(catcher)
    for i in egg:
        (i_x,i_y,i_x2,i_y2)=c.coords(i)
        if catcher_x < i_x and i_x2 < catcher_x2 and catcher_y2 - i_y2<40:
            egg.remove(i)
            c.delete(i)
            increase_score(egg_score)
    win.after(100,catch_check)


def increase_score(points):
    global score , egg_speed , egg_interval
    score+=points
    egg_speed=int(egg_speed * difficulty)
    egg_interval=int(egg_interval * difficulty)
    c.itemconfigure(score_text, text = 'Score : '+ str(score))

#move

def move_left(event):
    (x1,y1,x2,y2)=c.coords(catcher)
    if x1>0:
        c.move(catcher,-20,0)

def move_right(event):
    (x1, y1, x2, y2) = c.coords(catcher)
    if x2 < canvas_width:
        c.move(catcher, 20, 0)

c.bind('<Left>', move_left)
c.bind('<Right>',move_right)
c.focus_set()

win.after(1000,create_eggs)
win.after(1000,move_eggs)
win.after(1000,catch_check)

win.mainloop()