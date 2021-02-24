import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import datetime

import sql
from config import DBI

class NewComms(tk.Frame,DBI):
    def __init__(self,parent,*args,**kwargs):
        self.parent = parent
        tk.Frame.__init__(self,parent,*args)
        DBI.__init__(self,ini_section = kwargs['ini_section'])
class NewOrg(tk.Frame,DBI):
    def __init__(self,parent,*args,**kwargs):
        self.parent = parent
        self.refineOrgs = kwargs['refineOrgs']
        self.orgNameDD = kwargs['orgNameDD']
        tk.Frame.__init__(self,parent,*args)
        DBI.__init__(self,ini_section = kwargs['ini_section'])
        self.orgNameLabel = tk.Label(parent,text='Name:')
        self.orgName = tk.Entry(parent,fg='black',bg='white',width=40)
        self.orgAddressLabel = tk.Label(parent,text='Address')
        self.orgAddress = tk.Entry(parent,fg='black',bg='white',width=70)
        self.orgPhoneLabel = tk.Label(parent,text='Phone:')
        self.orgPhone = tk.Entry(parent,fg='black',bg='white',width=30)
        self.orgEmailLabel = tk.Label(parent,text='Email:')
        self.orgEmail = tk.Entry(parent,fg='black',bg='white',width=30)

        self.orgNameLabel.grid(row=0,column=0)
        self.orgName.grid(row=0,column=1)
        self.orgAddressLabel.grid(row=1,column=0)
        self.orgAddress.grid(row=1,column=1)
        self.orgPhoneLabel.grid(row=2,column=0)
        self.orgPhone.grid(row=2,column=1)
        self.orgEmailLabel.grid(row=3,column=0)
        self.orgEmail.grid(row=3,column=1)

        self.orgButton = tk.Button(parent,
            text='Insert Org',
            width=15,height=2,
            bg='blue',fg='yellow',)
        self.orgButton.bind('<Button-1>',self.insertOrg)
        self.flag = tk.StringVar(parent)
        self.insertFlag = tk.Label(parent,textvariable=self.flag)
        self.orgButton.grid(row=4,column=1)
    def insertOrg(self,event):
        vals = tuple()
        cols = ''
        colVals = ''
        if self.orgName.index("end") == 0:
            vals+= (self.orgName.get(),)
            cols+='name,'
            colVals+='%s,'
        if self.orgAddress.index("end") == 0:
            vals += (self.orgAddress.get(),)
            cols+='address,'
            colVals+='%s,'
        if self.orgPhone.index("end") == 0:
            vals += (self.orgPhone.get(),)
            cols+='phone,'
            colVals+='%s,'
        if self.orgEmail.index("end") == 0:
            vals += (self.orgEmail.get(),)
            cols+='email,'
            colVals+='%s,'
        cols = cols[:-1]
        colVals = colVals[:-1]
        insertOrg = sql.ContactInfo.insertOrg % (cols,colVals)
        self.flag.set(self.insertToDB(insertOrg,*vals))
        self.orgName.delete(0,'end')
        self.orgAddress.delete(0,'end')
        self.orgPhone.delete(0,'end')
        self.orgEmail.delete(0,'end')
        self.updateDD()
    def updateDD(self):
        refined_orgs = self.fetchall(sql.ContactInfo.getOrgs,
                                        self.refineOrgs.get())
        for org in refined_orgs:
            self.orgNameDD['menu'].add_command(label=org[0],
                command=tk._setit(self.orgName,org[0]))

class NewContact(tk.Frame,DBI):
    def __init__(self,parent,*args,**kwargs):
        self.parent = parent
        self.ini_section=kwargs['ini_section']
        tk.Frame.__init__(self,parent,*args)
        DBI.__init__(self,ini_section = kwargs['ini_section'])
        self.refineOrgsLabel = tk.Label(parent,text='search orgs:')
        self.refineOrgs = tk.Entry(parent,fg='black',bg='white',width=10)
        self.refineOrgsLabel.grid(row=0,column=0)
        self.refineOrgs.grid(row=0,column=1)
        self.refine = tk.Button(parent,
            text='refine orgs',
            width=15,height=2,
            bg='blue',fg='yellow',)
        self.refine.bind('<Button-1>',self.refineDD)
        self.refine.grid(row=0,column=2)
        orgs = self.fetchall(sql.ContactInfo.getOrgs,'')
        if len(orgs)>0:
            orgs =[org[0] for org in orgs]
        else:
            orgs = []
        self.orgName = tk.StringVar(parent,value="select an Organization:")
        self.orgNameDD = tk.OptionMenu(parent,self.orgName,"select a Organization:",*orgs)
        self.orgNameDD.grid(row=1,column=0,columnspan=2)

        self.insertNewOrg = tk.Button(parent,
            text='insert new org',
            width=15,height=2,
            bg='blue',fg='yellow',)
        self.insertNewOrg.bind('<Button-1>',self.newOrg)
        self.insertNewOrg.grid(row=1,column=2)

        self.contactNameLabel = tk.Label(parent,text='Name:')
        self.contactName = tk.Entry(parent,fg='black',bg='white',width=40)
        self.contactPhoneLabel = tk.Label(parent,text='Phone:')
        self.contactPhone = tk.Entry(parent,fg='black',bg='white',width=30)
        self.contactEmailLabel = tk.Label(parent,text='Email:')
        self.contactEmail = tk.Entry(parent,fg='black',bg='white',width=30)

        self.contactNameLabel.grid(row=2,column=0)
        self.contactName.grid(row=2,column=1)
        self.contactPhoneLabel.grid(row=3,column=0)
        self.contactPhone.grid(row=3,column=1)
        self.contactEmailLabel.grid(row=4,column=0)
        self.contactEmail.grid(row=4,column=1)

        self.insertNewContact = tk.Button(parent,
            text='insert Contact',
            width=15,height=2,
            bg='blue',fg='yellow',)
        self.insertNewContact.bind('<Button-1>',self.insertContact)
        self.insertNewContact.grid(row=5,column=1)
        self.flag = tk.StringVar(parent)
        self.err = tk.Label(parent,textvariable=self.flag)
        self.err.grid(row=5,column=0)
    def insertContact(self,event):
        vals = (self.orgName.get(),)
        cols = ''
        colVals = ''
        if self.contactName.index("end") == 0:
            vals+= (self.contactName.get(),)
            cols+='name,'
            colVals+='%s,'
        if self.contactPhone.index("end") == 0:
            vals += (self.contactPhone.get(),)
            cols+='phone,'
            colVals+='%s,'
        if self.contactEmail.index("end") == 0:
            vals += (self.contactEmail.get(),)
            cols+='email,'
            colVals+='%s,'
        cols = cols[:-1]
        colVals = colVals[:-1]
        insertOrg = sql.ContactInfo.insertOrg % (cols,colVals)
        self.flag.set(self.insertToDB(insertOrg,*vals))
        self.orgName.delete(0,'end')
        self.orgAddress.delete(0,'end')
        self.orgPhone.delete(0,'end')
        self.orgEmail.delete(0,'end')
        self.updateDD()
    def refineDD(self,event):
        refined_orgs = self.fetchall(sql.ContactInfo.getOrgs,
                                        self.refineOrgs.get())
        for org in refined_orgs:
            self.orgNameDD['menu'].add_command(label=org[0],
                command=tk._setit(self.orgName,org[0]))
    def newOrg(self,event):
        pop_up = tk.Toplevel(self.parent)
        NewOrg(pop_up,
            ini_section = self.ini_section,
            orgNameDD=self.orgNameDD,
            refineOrgs=self.refineOrgs)

class Banner(tk.Frame):
    def __init__(self,parent,*args,**kwargs):
        tk.Frame.__init__(self,parent)
        message = \
        """
        Enter New call logs, \n Review logs, \n or insert new contacts.
        """
        tk.Label(parent,text=message).pack()
class commsGUI(ttk.Notebook):
    def __init__(self,parent,*args,**kwargs):
        ttk.Notebook.__init__(self,parent,*args)
        self.tab1 = ttk.Frame()
        self.tab2 = ttk.Frame()
        self.tab3 = ttk.Frame()
        Banner(parent)
        NewComms(self.tab1,ini_section=kwargs['ini_section'])
        ReviewComms(self.tab3,ini_section=kwargs['ini_section'])
        NewContact(self.tab2,ini_section=kwargs['ini_section'])
        self.add(self.tab1,text="New Log")
        self.add(self.tab3,text="View Logs")
        self.add(self.tab2,text="New Contact")
        self.pack(expand=True,fill='both')
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Communications Log")
    app = commsGUI(root,ini_section='local_comms')
    app.mainloop()
