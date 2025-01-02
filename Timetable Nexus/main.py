from tkinter import *
from PIL import ImageTk,Image
from tkinter import messagebox
import os, sys
sys.path.insert(0, 'windows/')
import timetable_stud
import timetable_fac
import sqlite3

def submit():
    conn = sqlite3.connect(r'files/timetable.db')

    user = str(click.get())
    if user == "Student":
        cursor = conn.execute(f"SELECT PASSW, SECTION, NAME, ROLL FROM STUDENT WHERE SID='{user_id.get()}'")
        cursor = list(cursor)
        if len(cursor) == 0:
            messagebox.showwarning('Bad id', 'No such user found!')
        elif passw_entry.get() != cursor[0][0]:
            messagebox.showerror('Bad pass', 'Incorret Password!')
        else:
            nw = Tk()
            Label(
                nw,
                text=f'{cursor[0][2]}\tCourse: {cursor[0][1]}\tYear : {cursor[0][3]}',
                font=('Consolas', 12, 'italic'),
            ).pack()
            root.destroy()
            timetable_stud.student_tt_frame(nw, cursor[0][1])
            nw.mainloop()

    elif user == "Faculty":
        cursor = conn.execute(f"SELECT PASSW, INI, NAME, EMAIL FROM FACULTY WHERE FID='{user_id.get()}'")
        cursor = list(cursor)
        if len(cursor) == 0:
            messagebox.showwarning('Bad id', 'No such user found!')
        elif passw_entry.get() != cursor[0][0]:
            messagebox.showerror('Bad pass', 'Incorret Password!')
        else:
            nw = Tk()
            Label(nw,
                text=f'{cursor[0][2]} ({cursor[0][1]})\tEmail: {cursor[0][3]}',
                font=('Consolas', 12, 'italic'),
            ).pack()
            root.destroy()
            timetable_fac.fac_tt_frame(nw, cursor[0][1])
            nw.mainloop()

    elif user == "Admin":
        if user_id.get() == '8821103006' and passw_entry.get() == 'Anuj@123':
            root.destroy()
            os.system('py windows\\admin_screen.py')
            sys.exit()
        else:
            messagebox.showerror('Bad Input', 'Incorret Username/Password!')
            

root=Tk()
root.title("Login Page")
root.geometry('925x505+300+200')
root.configure(bg="#fff")
root.resizable(False,False)
Label(root,relief=SUNKEN).pack(side=BOTTOM,fill=X)
Label(root,text="Time Table Management System",font=("Arial",20,"bold"),padx=15,pady=15,border=0,relief=GROOVE,bg="teal",foreground="white").pack(side=TOP,fill=X)
img=ImageTk.PhotoImage(Image.open("C:/Users/AdityaGarg/OneDrive/Desktop/login.jpg"))
Label(root,image=img,bg='white').place(x=20,y=62,relx=0)
frame=Frame(root,width=350,height=350,bg='white')
frame.place(x=480,y=70)
heading=Label(frame,text='Sign In',fg='#57a1f8',bg='white',font=('Microsoft YaHei UI Light',23,'bold'))
heading.place(x=100,y=5)
def on_enter(e):
    user_id.delete(0,END)
def on_leave(e):
    name=user_id.get()
    if name=='':
        user_id.insert(0,'User Id')
user_id=Entry(frame,width=25,fg='black',border=0,font=('arial 15'))
user_id.place(x=30,y=80)
user_id.insert(0,"Use Id")
user_id.bind('<FocusIn>',on_enter)
user_id.bind('<FocusOut>',on_leave)
Frame(frame,width=295, height=2,bg='black').place(x=25,y=107)

def on_enter(e):
    passw_entry.delete(0,END)
def on_leave(e):
    name=passw_entry.get()
    if name=='':
        passw_entry.insert(0,'Password')

def show_passw():
    if passw_entry['show'] == "●":
        passw_entry['show'] = ""
        B1_show['text'] = '●'
        B1_show.update()
    elif passw_entry['show'] == "":
        passw_entry['show'] = "●"
        B1_show['text'] = '○'
        B1_show.update()
    passw_entry.update()

passw_entry = Entry(frame,width=25,font=('arial 15'),border=0,show="●")
passw_entry.place(x=30,y=150)
passw_entry.insert(0,"Password")
passw_entry.bind('<FocusIn>',on_enter)
passw_entry.bind('<FocusOut>',on_leave)
Frame(frame,width=295, height=2,bg='black').place(x=25,y=177)
B1_show=Button(frame,text='○',border=0,font=('Consolas', 12, 'bold'),command=show_passw,padx=5)
B1_show.place(x=10,y=145,relx=0.8)

var=["Student", "Faculty", "Admin"]
click=StringVar()
click.set(var[0])
drop=OptionMenu(frame,click,*var)
drop.place(x=40,y=210,relx=0.25) 
Button(frame, width=39,pady=8,text='SignIn',bg='#57a1f8',fg='white',border=0,command=submit).place(x=35,y=270)
root.mainloop()