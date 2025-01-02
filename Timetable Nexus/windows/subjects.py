import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys

# inputs in this window
subcode = subname = subtype = None
def create_treeview():
    tree['columns']=("ID","Name","Batch")
    tree.column("#0",width=0,stretch=NO)
    tree.column("Name",width=190)
    tree.column("ID",anchor=CENTER,width=120)
    tree.column("Batch",width=100)  
    tree.heading("#0",text="",anchor=W)
    tree.heading("Name",text="Code",anchor=W)
    tree.heading("ID",text="Name",anchor=CENTER)
    tree.heading("Batch",text="Type",anchor=W)
    tree['height'] = 15
    tree.pack()
def update_treeview():
    t='Lecture'
    p='Practical'
    for row in tree.get_children():
        tree.delete(row)
    cursor = conn.execute("SELECT * FROM SUBJECTS")
    for row in cursor:
        if row[2] == 'T':
            tree.insert("",0,values=(row[0],row[1],t))
        elif row[2] == 'P':
            tree.insert("",0,values=(row[0],row[1],p))
        
    tree.pack()

def parse_data():
    subcode = str(subcode_entry.get()).upper()
    subname = str(subname_entry.get()).upper()
    subtype = str(radio_var.get()).upper()

    if subcode=="":
        subcode = None
    if subname=="":
        subname = None

    if subcode is None or subname is None:
        messagebox.showerror("Bad Input", "Please fill up Subject Code and/or Subject Name!")
        subcode_entry.delete(0, tk.END)
        subname_entry.delete(0, tk.END)
        return

    conn.execute(f"REPLACE INTO SUBJECTS (SUBCODE, SUBNAME, SUBTYPE)\
        VALUES ('{subcode}','{subname}','{subtype}')")
    conn.commit()
    update_treeview()
    
    subcode_entry.delete(0, tk.END)
    subname_entry.delete(0, tk.END)


# update a row in the database
def update_data():
    subcode_entry.delete(0, tk.END)
    subname_entry.delete(0, tk.END)
    try:
        # print(tree.selection())
        if len(tree.selection()) > 1:
            messagebox.showerror("Bad Select", "Select one subject at a time to update!")
            return

        row = tree.item(tree.selection()[0])['values']
        subcode_entry.insert(0, row[0])
        subname_entry.insert(0, row[1])
        if row[2][0] == "T":
            R1.select()
        elif row[2][0] == "P":
            R2.select()

        conn.execute(f"DELETE FROM SUBJECTS WHERE SUBCODE = '{row[0]}'")
        conn.commit()
        update_treeview()

    except IndexError:
        messagebox.showerror("Bad Select", "Please select a subject from the list first!")
        return

def remove_data():
    if len(tree.selection()) < 1:
        messagebox.showerror("Bad Select", "Please select a subject from the list first!")
        return
    for i in tree.selection():
        conn.execute(f"DELETE FROM SUBJECTS WHERE SUBCODE = '{tree.item(i)['values'][0]}'")
        conn.commit()
        tree.delete(i)
        update_treeview()
def clear():
    subcode_entry.delete(0,END)
    subname_entry.delete(0,END)
    radio_var.set('L')

if __name__ == "__main__":  

    conn = sqlite3.connect(r'files/timetable.db')

    conn.execute('CREATE TABLE IF NOT EXISTS SUBJECTS\
    (SUBCODE CHAR(10) NOT NULL PRIMARY KEY,\
    SUBNAME CHAR(50) NOT NULL,\
    SUBTYPE CHAR(1) NOT NULL)')

    root=Tk()
    root.geometry("900x510")
    root.resizable(False,False)
    Label(root,text="Subjects Details",font=("Arial",40,"bold"),padx=15,pady=15,border=0,relief=GROOVE,bg="teal",foreground="white").pack(side=TOP,fill=X)
    Label(root,relief=SUNKEN).pack(side=BOTTOM,fill=X)
    frame=LabelFrame(root,text="List of Subjects",font=("Arial",14),relief=GROOVE,width=400,height=500)
    frame.place(x=470,y=120)

    tree=ttk.Treeview(frame)
    create_treeview()
    update_treeview()
    fr=LabelFrame(root,text="Add/Update Details",font=("Arial",14),relief=GROOVE).place(x=40,y=120,width=420,height=352)
    Label(fr,text='Subject Code:',font=('Consolas', 12),).place(x=50, y=160)
    subcode_entry = Entry(fr,font=('Consolas', 12),width=20)
    subcode_entry.place(x=200, y=160)
    Label(fr,text='Subject Name:',font=('Consolas', 12)).place(x=50, y=210)
    subname_entry = Entry(fr,font=('Consolas', 12),width=20)
    subname_entry.place(x=200, y=210)
    Label(fr,text='Subject Type:',font=('Consolas', 12)).place(x=50, y=260)
    radio_var = StringVar()
    R1 = Radiobutton(fr,text='Lecture',font=('Consolas', 12),variable=radio_var,value="T")
    R1.place(x=190, y=260)
    R1.select()
    R2 = Radiobutton(fr,text='Practical',font=('Consolas', 12),variable=radio_var,value="P")
    R2.place(x=190, y=290)
    R2.select()
    B1 = Button(fr,text='Add Subject',font=('Consolas', 12),bg="teal",fg="white",command=parse_data)
    B1.place(x=80,y=380)
    B2 = Button(fr,text='Update Subject',font=('Consolas', 12),bg="teal",fg="white",command=update_data)
    B2.place(x=240,y=380)
    B3 = Button(fr,text='Delete Subject(s)',font=('Consolas', 12),bg="teal",fg="white",command=remove_data)
    B3.place(x=80,y=430)
    Button(fr,text="Clear",font=('Consolas', 12),bg="teal",fg="white",command=clear,width=10).place(x=280,y=430)
    root.mainloop()
    conn.close() # close database ad=fter all operations