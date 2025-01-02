from tkinter import *
import sys
import os
import threading

def run_sub(): os.system('py windows\\subjects.py')
def run_fac(): os.system('py windows\\faculty.py')
def run_stud(): os.system('py windows\\student.py')
def run_sch(): os.system('py windows\\scheduler.py')
def run_tt_s(): os.system('py windows\\timetable_stud.py')
def run_tt_f(): os.system('py windows\\timetable_fac.py')

root=Tk()
root.geometry("700x540")
root.resizable(False,False)
Label(root,relief=SUNKEN).pack(side=BOTTOM,fill=X)
Label(root,text="A D M I N I S T R A T O R",font=("Arial",40,"bold"),padx=15,pady=15,border=0,relief=GROOVE,bg="teal",foreground="white").pack(side=TOP,fill=X)
mframe = LabelFrame(text='Modify', font=('Consolas'), padx=20)
mframe.place(x=50, y=100)

b1=Button(mframe,text="Students",font=('arial',20),command=run_stud).grid(row=0,column=0,padx=30,pady=30)
b2=Button(mframe,text="Faculties",font=('arial',20),command=run_fac).grid(row=0,column=1,padx=30)
b3=Button(mframe,text="Subjects",font=('arial',20),command=run_sub).grid(row=0,column=2,padx=30)

ttframe = LabelFrame(text='TimeTable', font=('Consolas'), padx=20)
ttframe.place(x=50, y=280)

Button(ttframe,text="Student",font=('arial',20),command=run_tt_s).grid(row=0,column=0,padx=20,pady=30)
Button(ttframe,text="Faculty",font=('arial',20),command=run_tt_f).grid(row=0,column=1,padx=20)
Button(ttframe,text="Schedule-periods",font=('arial',20),command=run_sch).grid(row=0,column=2,padx=20)

Button(root,text='Quit',font=('Consolas'),command=root.destroy,width=15,pady=10,bg="teal",fg="white").place(x=250, y=450)
root.mainloop()