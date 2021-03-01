import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import datetime
import sql
from config import DBI


class NewOrg(tk.Frame,DBI):
    def __init__(self,parent,*args,**kwargs):
        self.parent = parent
        self.refineOrgs = kwargs['refineOrgs']
        self.orgNameDD = kwargs['orgNameDD']
        self.OName = kwargs['orgName']
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
        if self.orgName.index("end") != 0:
            vals+= (self.orgName.get(),)
            cols+='name,'
            colVals+='%s,'
        if self.orgAddress.index("end") != 0:
            vals += (self.orgAddress.get(),)
            cols+='address,'
            colVals+='%s,'
        if self.orgPhone.index("end") != 0:
            vals += (self.orgPhone.get(),)
            cols+='phone,'
            colVals+='%s,'
        if self.orgEmail.index("end") != 0:
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
        self.orgNameDD['menu'].delete(0,'end')
        for org in refined_orgs:
            self.orgNameDD['menu'].add_command(label=org[0],
                command=tk._setit(self.OName,org[0]))

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
        self.orgNameDD = tk.OptionMenu(parent,self.orgName,self.orgName.get(),*orgs)
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
        self.notesLabel = tk.Label(parent,text='notes:')
        self.notes = tk.Text(parent,height=4,width=25)
        self.contactNameLabel.grid(row=2,column=0)
        self.contactName.grid(row=2,column=1)
        self.contactPhoneLabel.grid(row=3,column=0)
        self.contactPhone.grid(row=3,column=1)
        self.contactEmailLabel.grid(row=4,column=0)
        self.contactEmail.grid(row=4,column=1)
        self.notesLabel.grid(row=5,column=0)
        self.notes.grid(row=5,column=1)
        self.insertNewContact = tk.Button(parent,
            text='insert Contact',
            width=15,height=2,
            bg='blue',fg='yellow',)
        self.insertNewContact.bind('<Button-1>',self.insertContact)
        self.insertNewContact.grid(row=6,column=1)
        self.flag = tk.StringVar(parent)
        self.err = tk.Label(parent,textvariable=self.flag)
        self.err.grid(row=6,column=0)
    def insertContact(self,event):
        vals = (self.orgName.get(),)
        cols = ''
        colVals = '(SELECT org_id from Organizations o WHERE o.name = %s),'
        empty = True
        if self.contactName.index("end") != 0:
            vals+= (self.contactName.get(),)
            cols+='name,'
            colVals+='%s,'
        if self.contactPhone.index("end") != 0:
            vals += (self.contactPhone.get(),)
            cols+='phone,'
            colVals+='%s,'
        if self.contactEmail.index("end") != 0:
            vals += (self.contactEmail.get(),)
            cols+='email,'
            colVals+='%s,'
        if self.notes.index("end") != 0:
            vals +=(self.notes.get('1.0',tk.END),)
            cols+='notes,'
            colVals+='%s,'
        cols = cols[:-1]
        colVals = colVals[:-1]
        insertContact = sql.ContactInfo.insertContact % (cols,colVals)
        self.flag.set(self.insertToDB(insertContact,*vals))
        self.contactName.delete(0,'end')
        self.contactPhone.delete(0,'end')
        self.contactEmail.delete(0,'end')
        self.notes.delete('1.0',tk.END)
    def refineDD(self,event):
        refined_orgs = self.fetchall(sql.ContactInfo.getOrgs,
                                        self.refineOrgs.get())
        self.orgNameDD['menu'].delete(0,'end')
        for org in refined_orgs:
            self.orgNameDD['menu'].add_command(label=org[0],
                command=tk._setit(self.orgName,org[0]))
    def newOrg(self,event):
        pop_up = tk.Toplevel(self.parent)
        pop_up.title('New Organization')
        NewOrg(pop_up,
            ini_section = self.ini_section,
            orgNameDD=self.orgNameDD,
            orgName=self.orgName,
            refineOrgs=self.refineOrgs)
class ReviewContact(NewContact):
    def __init__(self,*args,**kwargs):
        NewContact.__init__(self,*args,ini_section = kwargs['ini_section'])
        self.notes.insert('1.0',kwargs['notes'].get())
        self.contactName.insert(0,kwargs['name'].get())
        self.contactEmail.insert(0,kwargs['email'].get())
        self.contactPhone.insert(0,kwargs['phone'].get())
        self.orgName.set(kwargs['org'].get())
        self.id=kwargs['id']
    def insertContact(self,event):
        cols=' SET'
        empty = True
        vals = tuple()
        if self.contactName.index("end") != 0:
            vals+= (self.contactName.get(),)
            cols+=' name = %s,'
        if self.contactPhone.index("end") != 0:
            vals += (self.contactPhone.get(),)
            cols+=' phone = %s,'
        if self.contactEmail.index("end") != 0:
            vals += (self.contactEmail.get(),)
            cols+=' email = %s,'
        if self.notes.index("end") != 0:
            vals +=(self.notes.get('1.0',tk.END),)
            cols+=' notes = %s,'
        cols = cols[:-1]
        updateContact = sql.ContactInfo.updateContact % (cols,self.id.get())
        self.flag.set(self.insertToDB(updateContact,*vals))
        self.contactName.delete(0,'end')
        self.contactPhone.delete(0,'end')
        self.contactEmail.delete(0,'end')
        self.notes.delete('1.0',tk.END)
class FindContact(tk.Frame,DBI):
    def __init__(self,parent,*args,**kwargs):
        self.parent = parent
        tk.Frame.__init__(self,parent,*args)
        self.name=kwargs['name']
        self.org=kwargs['org']
        self.email=kwargs['email']
        self.phone=kwargs['phone']
        self.id = kwargs['id']
        self.nb = tk.StringVar(parent)
        self.ini_section=kwargs['ini_section']
        DBI.__init__(self,ini_section = kwargs['ini_section'])
        self.nameFilter = tk.Entry(parent,fg='black',bg='white',width=10)
        self.orgFilter =tk.Entry(parent,fg='black',bg='white',width=10)
        self.emailFilter = tk.Entry(parent,fg='black',bg='white',width=10)
        self.phoneFilter = tk.Entry(parent,fg='black',bg='white',width=10)
        self.nameLabel=tk.Label(parent,text='Name:')
        self.orgLabel=tk.Label(parent,text='Organization:')
        self.emailLabel=tk.Label(parent,text='Email:')
        self.phoneLabel=tk.Label(parent,text='Phone:')
        self.FilterButton=tk.Button(parent,
            text='Filter',
            width=15,height=2,
            bg='blue',fg='yellow',)
        self.FilterButton.bind('<Button-1>',self.getContacts)
        self.nameFilter.grid(row=0,column=1)
        self.nameLabel.grid(row=0,column=0)
        self.orgFilter.grid(row=1,column=1)
        self.orgLabel.grid(row=1,column=0)
        self.emailFilter.grid(row=2,column=1)
        self.emailLabel.grid(row=2,column=0)
        self.phoneFilter.grid(row=3,column=1)
        self.phoneLabel.grid(row=3,column=0)
        self.FilterButton.grid(row=4,column=1)

        self.contactInfoVar = tk.StringVar(parent,value="Name, Organization, Email, Phone")
        self.contactsDD = tk.OptionMenu(parent,self.contactInfoVar,self.contactInfoVar.get())
        self.contactsDD.grid(row=5,column=0,columnspan=3)
        self.NewContact=tk.Button(parent,
            text='Add New Contact',
            width=15,height=2,
            bg='blue',fg='yellow',)
        self.NewContact.bind('<Button-1>',self.newContact)
        self.NewContact.grid(row=7,column=1)
        self.passBackContact=tk.Button(parent,
            text='Pass Back Contact',
            width=15,height=2,
            bg='blue',fg='yellow',)
        self.passBackContact.bind('<Button-1>',self.retrieveContact)
        self.passBackContact.grid(row=6,column=1)
        self.getContactInfo=tk.Button(parent,
            text='Update Contact',
            width=15,height=2,
            bg='blue',fg='yellow',)
        self.getContactInfo.bind('<Button-1>',self.reviewContact)
        self.getContactInfo.grid(row=6,column=0)
    def newContact(self,event):
        pop_up = tk.Toplevel(self.parent)
        pop_up.title('New Contact')
        NewContact(pop_up,
            ini_section=self.ini_section)
    def getContacts(self,event):
        cname = str(self.nameFilter.get())
        oname=str(self.orgFilter.get())
        cemail=str(self.emailFilter.get())
        cphone=str(self.phoneFilter.get())
        params = tuple()
        whereClauses =''
        sqlStr = sql.ContactInfo.getContact
        first = False
        if self.nameFilter.index("end") != 0:
            if first is True:
                sqlStr += 'AND c.name ~* %s '
            else:
                sqlStr += ' WHERE c.name ~* %s '
                first = True
            params+= (self.nameFilter.get(),)
        if self.orgFilter.index("end") != 0:
            if first is True:
                sqlStr += 'AND o.name ~* %s '
            else:
                sqlStr += ' WHERE o.name ~* %s '
                first = True
            params+= (self.orgFilter.get(),)
        if self.emailFilter.index("end") != 0:
            if first is True:
                sqlStr += 'AND c.email ~* %s '
            else:
                sqlStr += ' WHERE c.email ~* %s '
                first = True
            params+= (self.emailFilter.get(),)
        if self.phoneFilter.index("end") != 0:
            if first is True:
                sqlStr += 'AND c.phone ~* %s '
            else:
                sqlStr += ' WHERE c.phone ~* %s '
                first = True
            params+= (self.phoneFilter.get(),)
        filtered_contactInfo = self.fetchall(sqlStr,*params)
        self.contactsDD['menu'].delete(0,'end')
        for cInfo in filtered_contactInfo:
            cinfoStr = str(cInfo[0]) + ', '+cInfo[1]+', '+str(cInfo[2])+', '+str(cInfo[3])
            l = len(cinfoStr)
            cinfoStr+=', '+str(cInfo[4]) + ', '+ str(cInfo[5])
            self.contactsDD['menu'].add_command(label=cinfoStr[:l+1],
                command=tk._setit(self.contactInfoVar,cinfoStr))
    def updateContactInfo(self):
        vals = self.contactInfoVar.get().split(',')
        self.name.set(vals[0])
        self.org.set(vals[1])
        self.email.set(vals[2])
        self.phone.set(vals[3])
        self.nb.set(vals[4])
        self.id.set(vals[5])
    def retrieveContact(self,event):
        self.updateContactInfo()
        self.parent.destroy()
    def reviewContact(self,event):
        pop_up=tk.Toplevel(self.parent)
        pop_up.title('Update Contact')
        self.updateContactInfo()
        ReviewContact(pop_up,
            ini_section=self.ini_section,
            name=self.name,
            org=self.org,
            email=self.email,
            phone=self.phone,
            notes=self.nb,
            id=self.id)

class Banner(tk.Frame):
    def __init__(self,parent,*args,**kwargs):
        tk.Frame.__init__(self,parent)
        self.parent=parent
        self.ini_section=kwargs['ini_section']
        self.id=kwargs['id']
        message = \
        """
        Select a Contact and then \n\tenter a new log or \n\tretrieve an old log.
        """
        tk.Label(parent,text=message).grid(row=0,column=0,columnspan=2)
        self.name = tk.StringVar(parent,value='No Contact Selected.')
        self.org = tk.StringVar(parent,value='')
        self.email = tk.StringVar(parent,value='')
        self.phone=tk.StringVar(parent,value='')
        tk.Label(parent,text='Contact Name:').grid(row=1,column=0)
        tk.Label(parent,text='Contact Org:').grid(row=2,column=0)
        tk.Label(parent,text='Contact Phone:').grid(row=3,column=0)
        tk.Label(parent,text='Contact Email:').grid(row=4,column=0)
        tk.Label(parent,textvariable=self.name).grid(row=1,column=1)
        tk.Label(parent,textvariable=self.org).grid(row=2,column=1)
        tk.Label(parent,textvariable=self.phone).grid(row=3,column=1)
        tk.Label(parent,textvariable=self.email).grid(row=4,column=1)
        self.getContact = tk.Button(parent,
            text='Retrieve Contact',
            width=15,height=2,
            bg='blue',fg='yellow',)
        self.getContact.bind('<Button-1>',self.findContact)
        self.getContact.grid(row=5,column=1)
    def findContact(self,event):
        pop_up=tk.Toplevel(self.parent)
        pop_up.title('Retrieve Contact')
        FindContact(pop_up,
            ini_section=self.ini_section,
            name=self.name,
            org=self.org,
            email=self.email,
            phone=self.phone,
            id=self.id)

class NewComms(tk.Frame,DBI):
    #ignroe me fornow
    def __init__(self,parent,*args,**kwargs):
        self.parent = parent
        tk.Frame.__init__(self,parent,*args)
        DBI.__init__(self,ini_section = kwargs['ini_section'])
        self.id=kwargs['id']
        self.notesLabel=tk.Label(parent,text='call log:')
        self.notes = tk.Text(parent,height=4,width=25)
        self.notes.pack()
        self.insertLog = tk.Button(parent,
            text='log it',
            width=15,height=2,
            bg='blue',fg='yellow',)
        self.insertLog.bind('<Button-1>',self.insertit)
        self.insertLog.pack(padx=2,pady=2)
        self.updateOrder = tk.Button(parent,
            text='update order assoc. with contact',
            width=25,height=2,
            bg='blue',fg='yellow',)
        self.updateOrder.bind('<Button-1>',self.annoying)
        self.updateOrder.pack(padx=2,pady=2)
    def insertit(self,event):
        self.insertToDB(sql.Comms.insertCommsLog,self.id.get(),
            datetime.datetime.now(),
            self.notes.get('1.0',tk.END))
        self.notes.delete('1.0',tk.END)
    def annoying(self,event):
        pop_up=tk.Toplevel(self.parent)
        pop_up.title('boo')
        tk.Label(pop_up,text='turtle.turtle.')
class ReviewComms(tk.Frame,DBI):
    def __init__(self,parent,*args,**kwargs):
        self.parent = parent
        tk.Frame.__init__(self,parent,*args)
        DBI.__init__(self,ini_section = kwargs['ini_section'])
        self.id=kwargs['id']
        self.dt=None
        self.notes = tk.Text(parent,height=4,width=25)
        self.gettheLog = tk.Button(parent,
            text='Get Log',
            width=15,height=2,
            bg='blue',fg='yellow',)
        self.gettheLog.bind('<Button-1>',self.getLog)
        self.logDT=tk.StringVar(parent)
        self.gettheLog.pack(padx=2,pady=2)
        tk.Label(parent,textvariable=self.logDT).pack(padx=2,pady=2)
        self.notes.pack(padx=2,pady=2)
    def getLog(self,event):
        if self.dt is None:
            back = self.fetchone(sql.Comms.getMostRecentLog,self.id.get())
        else:
            back = self.fetchone(sql.Comms.getNextLog,self.id.get(),self.dt)
        if back is not None:
            self.dt=back[0]
            self.logDT.set('log timestamp: '+self.dt.strftime("%m/%d/%Y %H:%M"))
            self.notes.delete('1.0',tk.END)
            self.notes.insert('1.0',back[1])
        else:
            back = self.fetchone(sql.Comms.getMostRecentLog,self.id.get())
            self.dt=back[0]
            self.logDT.set('log timestamp: '+self.dt.strftime("%m/%d/%Y %H:%M"))
            self.notes.delete('1.0',tk.END)
            self.notes.insert('1.0',back[1])
class commsGUI(ttk.Notebook):
    def __init__(self,parent,*args,**kwargs):
        ttk.Notebook.__init__(self,parent,*args)
        self.tab1 = ttk.Frame()
        self.tab2 = ttk.Frame()
        self.tab3 = ttk.Frame()
        self.contactID = tk.IntVar(parent)
        Banner(parent,ini_section=kwargs['ini_section'],id=self.contactID)
        NewComms(self.tab1,ini_section=kwargs['ini_section'],id=self.contactID)
        ReviewComms(self.tab3,ini_section=kwargs['ini_section'],id=self.contactID)
        self.add(self.tab1,text="New Log")
        self.add(self.tab3,text="View Logs")
        self.grid(columnspan=2)
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Communications Log")
    app = commsGUI(root,ini_section='local_comms')
    app.mainloop()
