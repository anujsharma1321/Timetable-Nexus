import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys

fid = passw = conf_passw = name = roll = section = None
def create_treeview():
    tree['columns']=("ID","Name","Batch")
    tree.column("#0",width=0,stretch=NO)
    tree.column("Name",width=190)
    tree.column("ID",anchor=CENTER,width=120)
    tree.column("Batch",width=90)
    tree.heading("#0",text="",anchor=W)
    tree.heading("Name",text="Name",anchor=W)
    tree.heading("ID",text="ID",anchor=CENTER)
    tree.heading("Batch",text="Course",anchor=W)
    tree['height'] = 18
    tree.pack()
def update_treeview():
    for row in tree.get_children():
        tree.delete(row)
    cursor = conn.execute("SELECT SID, NAME, SECTION FROM STUDENT")
    for row in cursor:
        tree.insert("",0,values=(row[0], row[1], row[2]))
    tree.place()
def parse_data():
    fid = str(fid_entry.get())
    passw = str(passw_entry.get())
    conf_passw = str(conf_passw_entry.get())
    name = str(name_entry.get()).upper()
    roll = str(roll_entry.get())
    section = str(sec_entry.get()).upper()

    if fid == "" or passw == "" or conf_passw == "" or name == "" or roll == "" or section == "":
        messagebox.showwarning("Bad Input", "Some fields are empty! Please fill them out!")
        return

    if passw != conf_passw:
        messagebox.showerror("Passwords mismatch", "Password and confirm password didnt match. Try again!")
        passw_entry.delete(0, tk.END)
        conf_passw_entry.delete(0, tk.END)
        return
  
    conn.execute(f"INSERT INTO STUDENT (SID, PASSW, NAME, ROLL, SECTION)\
        VALUES ('{fid}','{passw}','{name}', '{roll}', '{section}')")
    conn.commit()
    update_treeview()
    
    fid_entry.delete(0, tk.END)
    passw_entry.delete(0, tk.END)
    conf_passw_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    roll_entry.delete(0, tk.END)
    sec_entry.delete(0, tk.END)
    
def update_data():
    fid_entry.delete(0, tk.END)
    passw_entry.delete(0, tk.END)
    conf_passw_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    roll_entry.delete(0, tk.END)
    sec_entry.delete(0, tk.END)
    try:
        if len(tree.selection()) > 1:
            messagebox.showerror("Bad Select", "Select one student at a time to update!")
            return

        q_fid = tree.item(tree.selection()[0])['values'][0]
        cursor = conn.execute(f"SELECT * FROM STUDENT WHERE SID = '{q_fid}'")

        cursor = list(cursor)
        fid_entry.insert(0, cursor[0][0])
        passw_entry.insert(0, cursor[0][1])
        conf_passw_entry.insert(0, cursor[0][1])
        name_entry.insert(0, cursor[0][2])
        roll_entry.insert(0, cursor[0][3])
        sec_entry.insert(0, cursor[0][4])
        
        conn.execute(f"DELETE FROM STUDENT WHERE SID = '{cursor[0][0]}'")
        conn.commit()
        update_treeview()

    except IndexError:
        messagebox.showerror("Bad Select", "Please select a student from the list first!")
        return

def remove_data():
    if len(tree.selection()) < 1:
        messagebox.showerror("Bad Select", "Please select a student from the list first!")
        return
    for i in tree.selection():
        # print(tree.item(i)['values'][0])
        conn.execute(f"DELETE FROM STUDENT WHERE SID = '{tree.item(i)['values'][0]}'")
        conn.commit()
        tree.delete(i)
        update_treeview()

def clear():
    fid_entry.delete(0,END)
    passw_entry.delete(0,END)
    conf_passw_entry.delete(0,END)
    name_entry.delete(0,END)
    roll_entry.delete(0,END)
    sec_entry.delete(0,END)
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



if __name__ == "__main__":  

    '''
        DATABASE CONNECTIONS AND SETUP
    '''

    conn = sqlite3.connect(r'files/timetable.db')

    # creating Table in the database
    conn.execute('CREATE TABLE IF NOT EXISTS STUDENT\
    (SID CHAR(10) NOT NULL PRIMARY KEY,\
    PASSW CHAR(50) NOT NULL,\
    NAME CHAR(50) NOT NULL,\
    ROLL INTEGER NOT NULL,\
    SECTION CHAR(5) NOT NULL)')

root =Tk()
root.geometry("900x580")
root.resizable(False,False)
Label(root,text="Students Details",font=("Arial",40,"bold"),padx=15,pady=15,border=0,relief=GROOVE,bg="teal",foreground="white").pack(side=TOP,fill=X)
Label(root,relief=SUNKEN).pack(side=BOTTOM,fill=X)
frame=LabelFrame(root,text="List of Students",font=("Arial",14),relief=GROOVE,width=400,height=500)
frame.place(x=470,y=120)

tree=ttk.Treeview(frame)
create_treeview()
update_treeview()

fr=LabelFrame(root,text="Add/Update Details",font=("Arial",14),relief=GROOVE).place(x=40,y=120,width=420,height=410)
Label(fr,text='Student id:',font=('Consolas', 12)).place(x=50, y=160)
fid_entry = Entry(fr,font=('Consolas', 12),width=20)
fid_entry.place(x=200, y=160)
Label(fr,text='Password:',font=('Consolas', 12)).place(x=50, y=200)
passw_entry = Entry(fr,font=('Consolas', 12),width=20,show="●")
passw_entry.place(x=200, y=200)
B1_show = Button(fr,text='○',font=('Consolas', 8, 'bold'),command=show_passw,width=3)
B1_show.place(x=390,y=200)
Label(fr,text='Confirm Password:',font=('Consolas', 12)).place(x=50, y=250)
conf_passw_entry = Entry(fr,font=('Consolas', 12),width=20,show="●")
conf_passw_entry.place(x=200, y=250)
Label(fr,text='Student Name:',font=('Consolas', 12)).place(x=50, y=290)
name_entry = Entry(fr,font=('Consolas', 12),width=20,)
name_entry.place(x=200, y=290,relx=0)
Label(fr,text='Year:',font=('Consolas', 12)).place(x=50, y=330)
roll_entry = Entry( fr, font=('Consolas', 12), width=20,)
roll_entry.place(x=200, y=330)
Label(fr,text='Course:',font=('Consolas', 12)).place(x=50, y=370)
sec_entry = Entry(fr,font=('Consolas', 12),width=20)
sec_entry.place(x=200, y=370)
B1 = Button(fr,text='Add Student',font=('Consolas', 12),bg="teal",fg="white",command=parse_data)
B1.place(x=80,y=430)
B2 = Button(fr,text='Update Student',font=('Consolas', 12),bg="teal",fg="white",command=update_data)
B2.place(x=240,y=430)
B3 = Button(fr,text='Delete Student(s)',font=('Consolas', 12),bg="teal",fg="white",command=remove_data)
B3.place(x=80,y=480)
Button(fr,text="Clear",font=('Consolas', 12),bg="teal",fg="white",command=clear,width=10).place(x=280,y=480)
root.mainloop()
conn.close() # close database after all operations
