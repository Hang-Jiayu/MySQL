import tkinter.messagebox
from tkinter import *
import pymysql
import tkinter.tix
import json
#----------------------------------
def saveToJSON(filename,dicObject):
    flag=False
    if type(dicObject)!=dict:
        return flag
    try:
        j_file=open(filename,'w')
        json.dump(dicObject,j_file,ensure_ascii=False)
        flag=True
    except:
        print('往%s写数据出错!'%(filename))
    finally:
        if flag:
            j_file.close()
    return flag
#=========================
def GetFromJSON(filename):
    flag=False
    dicObject={}
    try:
        j_file=open(filename,'r')
        dicObject=json.load(j_file)
        flag=True
    except:
        print('从%s读JSON数据出错!'%(filename))
    finally:
        if flag:
            j_file.close()
    return dicObject
#-----------------------------------
root=tkinter.tix.Tk()
#----------------------------------------
al=GetFromJSON("user's.json")
#----------------------------------
host=StringVar()
host.set(al['Host'])
user=tkinter.StringVar()
user.set(al['User'])
password=tkinter.StringVar()
database=tkinter.StringVar()
database.set(al['Database'])
port=tkinter.StringVar()
port.set(al['Port'])
charset=tkinter.StringVar()
charset.set(al['Charset'])
T_put=tkinter.StringVar()
#----------------------------------
def log_in(event):
    try:
        conn=pymysql.connect(host=host.get(),user=user.get(),password=password.get(),db=database.get(),port=int(port.get()),charset=charset.get())
        tkinter.messagebox.showinfo("Tips:","Welcome to MySQL,"+user.get()+"!")
        dk={}
        dk.setdefault('Host',host.get())
        dk.setdefault("User",user.get())
        dk.setdefault("Port",port.get())
        dk.setdefault("Charset",charset.get())
        dk.setdefault("Database",database.get())
        h=saveToJSON("user's.json",dk)
    except:
        tkinter.messagebox.showinfo("Tips:","Mabe your wrote the wrong user name or password!")
        dk={}
        dk.setdefault('Host',host.get())
        dk.setdefault("User",user.get())
        dk.setdefault("Port",port.get())
        dk.setdefault("Charset",charset.get())
        dk.setdefault("Database",database.get())
        h=saveToJSON("user's.json",dk)
        conn.close()



#----------------------------------
def exe(event):
    try:
        conn=pymysql.connect(host=host.get(),user=user.get(),password=password.get(),db=database.get(),port=int(port.get()),charset=charset.get())
        cur=conn.cursor()
    except:
        tkinter.messagebox.showinfo("Tips:","There is something wrong with connecting it!")
        conn.close()
    try:
        cur.execute(T_put.get())
        T_put.set('')
        tkinter.messagebox.showinfo("Tips:","Execute it successfully!")
    except:
        tkinter.messagebox.showinfo("Tips:","There is something wrong with executing it!")
    try:
        s_text.delete('1.0','end')
        n=cur.fetchall()
        s_text.insert(END,n)
        s_text.update()
        conn.commit()
        cur.close()
        conn.close()
    except:
        tkinter.messagebox.showinfo("Tips:","Tere is something wrong with showing it!")
        conn.commit()
        cur.close()
        conn.close()

#-----------------------------------------------------------------------

root.geometry("710x600")
root.title("MySQL-Connecter")
root.iconbitmap("D:\MicrosoftEdge\\bitbug_favicon.ico")
#-----------------------------------------------------------------
conA=tkinter.Label(root,text="MySQL-Connecter",font=('Arial', 32))
conA.pack(side='top')
#-----------------------------------------------------------------
top=tkinter.tix.Frame(root,height=300,width=5,relief=FLAT,bd=1)
top.pack(side='top')
#----------------------------------------------------------------------------
users=tkinter.tix.Frame(root,height=300,width=5,relief=FLAT,bd=1)
users.pack(side='top')
#------------------------------------------------------------------------------------
top.host=tkinter.tix.LabelEntry(top,label="Host:                ",labelside='top')
top.host.pack(side='left')
top.host.entry['textvariable']=host
#----------------------------------------------------------------------------------
top.user=tkinter.tix.LabelEntry(users,label="User:                ",labelside='top')
top.user.pack(side='top')
top.user.entry['textvariable']=user
#------------------------------------------------------------------------------
top.passwdA=tkinter.tix.Label(users,text="Password:")
top.passwdA.pack(anchor='sw')
top.passwdB=tkinter.Entry(users,textvariable=password,show='*')
top.passwdB.pack(anchor='sw')
#---------------------------------------------------------------------------------
Log_in=tkinter.Button(users,text="  Log in  ",fg="black")
Log_in.bind("<Button-1>",log_in)
Log_in.pack(anchor='s',pady='3m')
#-----------------------------------------------------------------------------
top.database=tkinter.tix.LabelEntry(top,label="Database:            ",labelside='top')
top.database.pack(side='left')
top.database.entry['textvariable']=database
#----------------------------------------------------------------------------------
top.port=tkinter.tix.LabelEntry(top,label="port:            ",labelside='top')
top.port.pack(side='left')
top.port.entry['textvariable']=port
#-------------------------------------------------------------------------------
top.charset=tkinter.tix.LabelEntry(top,label='Charset:      ',labelside='top')
top.charset.pack(side='left')
top.charset.entry['textvariable']=charset
#--------------------------------------------------------------------------
console=tkinter.Frame(root,height=10,width=300,relief=FLAT,bd=1)
console.pack(side='top')
#-----------------------------------------------------------------------------
conB=tkinter.tix.LabelEntry(console,label='Console:                                                                                                                  ',labelside='top')
conB.pack(side='left')
conB.entry['textvariable']=T_put
#----------------------------------------------------------------------------
exebtn=tkinter.Button(console,text='Implement')
exebtn.bind("<Button-1>",exe)
exebtn.pack(side='bottom',padx='2m')
#-----------------------------------------------------------------------------------
lab=tkinter.Label(root,text='Interactive interface',font=('Arial',16))
lab.pack(side="top")
#-------------------------------------------------------------------------------
surface=tkinter.Frame(root,height=10,width=300,relief=FLAT,bd=1)
surface.pack(side='top')
#-----------------------------------------------------
s_text=tkinter.Text(surface,width=80,height=20)
s_text.pack(side='left',pady='3m',fill=Y)
s=Scrollbar(surface)
s.pack(side='right',fill=Y)
s.config(command=s_text.yview)
s_text.config(yscrollcommand=s.set)
#---------------------------------------------------------
root.mainloop()
