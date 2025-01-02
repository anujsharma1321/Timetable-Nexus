import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys

fid = passw = conf_passw = name = ini = email = subcode1 = subcode2 = None
def clear():
    fid_entry.delete(0,END)
    passw_entry.delete(0,END)
    conf_passw_entry.delete(0,END)
    name_entry.delete(0,END)
    email_entry.delete(0,END)
    ini_entry.delete(0,END)
    combo1.current(0)
    combo2.current(0)
# create treeview (call this function once)
def create_treeview():
    tree['columns']=("ID","Name","Subject1","Subject2")
    tree.column("#0",width=0,stretch=NO)
    tree.column("Name",width=150)
    tree.column("ID",anchor=CENTER,width=110)
    tree.column("Subject1",width=100)
    tree.column("Subject2",width=90)

    tree.heading("#0",text="",anchor=W)
    tree.heading("Name",text="Name",anchor=W)
    tree.heading("ID",text="ID",anchor=CENTER)
    tree.heading("Subject2",text="Subject2",anchor=W)
    tree.heading("Subject1",text="Subject1",anchor=W)
    tree['height'] = 20
    tree.pack()

def update_treeview():
    for row in tree.get_children():
        tree.delete(row)
    cursor = conn.execute("SELECT FID, NAME, SUBCODE1, SUBCODE2 FROM FACULTY")
    for row in cursor:
        tree.insert( "",0,values=(row[0], row[1], row[2], row[3]))
    tree.pack()

def parse_data():
    fid = str(fid_entry.get())
    passw = str(passw_entry.get())
    conf_passw = str(conf_passw_entry.get())
    name = str(name_entry.get()).upper()
    ini = str(ini_entry.get()).upper()
    email = str(email_entry.get())
    subcode1 = str(combo1.get())
    subcode2 = str(combo2.get())

    if fid == "" or passw == "" or conf_passw == "" or name == "":
        messagebox.showwarning("Bad Input", "Some fields are empty! Please fill them out!")
        return

    if passw != conf_passw:
        messagebox.showerror("Passwords mismatch", "Password and confirm password didnt match. Try again!")
        passw_entry.delete(0, tk.END)
        conf_passw_entry.delete(0, tk.END)
        return

    if subcode1 == "NULL":
        messagebox.showwarning("Bad Input", "Subject 1 cant be NULL")
        return
    
    conn.execute(f"REPLACE INTO FACULTY (FID, PASSW, NAME, INI, EMAIL, SUBCODE1, SUBCODE2)\
        VALUES ('{fid}','{passw}','{name}', '{ini}', '{email}', '{subcode1}', '{subcode2}')")
    conn.commit()
    update_treeview()
    
    fid_entry.delete(0, tk.END)
    passw_entry.delete(0, tk.END)
    conf_passw_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    ini_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    combo1.current(0)
    combo2.current(0)
    
def update_data():
    fid_entry.delete(0, tk.END)
    passw_entry.delete(0, tk.END)
    conf_passw_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    ini_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    combo1.current(0)
    combo2.current(0)
    try:
        if len(tree.selection()) > 1:
            messagebox.showerror("Bad Select", "Select one faculty at a time to update!")
            return

        q_fid = tree.item(tree.selection()[0])['values'][0]
        cursor = conn.execute(f"SELECT * FROM FACULTY WHERE FID = '{q_fid}'")

        cursor = list(cursor)
        fid_entry.insert(0, cursor[0][0])
        passw_entry.insert(0, cursor[0][1])
        conf_passw_entry.insert(0, cursor[0][1])
        name_entry.insert(0, cursor[0][2])
        ini_entry.insert(0, cursor[0][3])
        email_entry.insert(0, cursor[0][4])
        combo1.current(subcode_li.index(cursor[0][5]))
        combo2.current(subcode_li.index(cursor[0][6]))

        conn.execute(f"DELETE FROM FACULTY WHERE FID = '{cursor[0][0]}'")
        conn.commit()
        update_treeview()

    except IndexError:
        messagebox.showerror("Bad Select", "Please select a faculty from the list first!")
        return

def remove_data():
    if len(tree.selection()) < 1:
        messagebox.showerror("Bad Select", "Please select a faculty from the list first!")
        return
    for i in tree.selection():
        conn.execute(f"DELETE FROM FACULTY WHERE FID = '{tree.item(i)['values'][0]}'")
        conn.commit()
        tree.delete(i)
        update_treeview()

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

    # connecting database
    conn = sqlite3.connect(r'files/timetable.db')

    # creating Tabe in the database
    conn.execute('CREATE TABLE IF NOT EXISTS FACULTY\
    (FID CHAR(10) NOT NULL PRIMARY KEY,\
    PASSW CHAR(50) NOT NULL,\
    NAME CHAR(50) NOT NULL,\
    INI CHAR(5) NOT NULL,\
    EMAIL CHAR(50) NOT NULL,\
    SUBCODE1 CHAR(10) NOT NULL,\
    SUBCODE2 CHAR(10)    )')


    '''
        TKinter WINDOW SETUP WITH WIDGETS
            * Label(1-11)
            * Entry(6)
            * ComboBox(1-2)
            * Treeview(1)
            * Button(1-3)
    '''

    root =Tk()
    root.geometry("950x600")
    root.resizable(False,False)
    Label(root,text="Faculty Details ",font=("Arial",40,"bold"),padx=15,pady=15,border=0,relief=GROOVE,bg="teal",foreground="white").pack(side=TOP,fill=X)
    Label(root,relief=SUNKEN).pack(side=BOTTOM,fill=X)
    frame=LabelFrame(root,text="List of Faculties",font=("Arial",14),relief=GROOVE,width=400,height=500)
    frame.place(x=485,y=120)
    fr=LabelFrame(root,text="Add/Update Details",font=("Arial",14),relief=GROOVE).place(x=40,y=120,width=420,height=450)
    Label(fr,text='Faculty id:',font=('Consolas', 12)).place(x=50, y=160)
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
    Label(fr,text='Faculty Name:',font=('Consolas', 12)).place(x=50, y=290)
    name_entry = Entry(fr,font=('Consolas', 12),width=20,)
    name_entry.place(x=200, y=290,relx=0)
    Label(fr,text='Email:',font=('Consolas', 12)).place(x=50, y=330)
    email_entry = Entry( fr, font=('Consolas', 12), width=20,)
    email_entry.place(x=200, y=330)
    Label(fr,text='Initial:',font=('Consolas', 12)).place(x=50, y=370)
    ini_entry = Entry(fr,font=('Consolas', 12),width=5)
    ini_entry.place(x=200, y=370)
    cursor = conn.execute("SELECT SUBCODE FROM SUBJECTS")
    subcode_li = [row[0] for row in cursor]
    subcode_li.insert(0, 'NULL')

    tk.Label(root,text='Subjects:',font=('Consolas', 12)).place(x=50, y=410)
    combo1 = ttk.Combobox(root,values=subcode_li,width=12)
    combo1.place(x=200, y=410)
    combo1.current(0)
    combo2 = ttk.Combobox(root,values=subcode_li,width=12)
    combo2.place(x=320, y=410)
    combo2.current(0)

    tree = ttk.Treeview(frame)
    create_treeview()
    update_treeview()

    B1 = Button(fr,text='Add Faculty',font=('Consolas', 12),bg="teal",fg="white",command=parse_data)
    B1.place(x=80,y=470)
    B2 = Button(fr,text='Update Faculty',font=('Consolas', 12),bg="teal",fg="white",command=update_data)
    B2.place(x=240,y=470)
    B3 = Button(fr,text='Delete Faculty(s)',font=('Consolas', 12),bg="teal",fg="white",command=remove_data)
    B3.place(x=80,y=520)
    Button(fr,text="Clear",font=('Consolas', 12),bg="teal",fg="white",command=clear,width=10).place(x=280,y=520)
    mainloop()
    conn.close() # close database after all operations
