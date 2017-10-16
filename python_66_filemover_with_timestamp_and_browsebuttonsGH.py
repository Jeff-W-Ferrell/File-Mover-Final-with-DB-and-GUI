#   Jeff W. Ferrell 10/16/17
#   Python Course, item 66
#   Moving recently updated (within 24 hours).txt files from one folder to another
#   Made with Python 3.6 using tkinter, datetime, filedialog, sqlite3, shutil, and os modules; and including browse buttons and a file move initiate button.

from tkinter import *
import tkinter as tk
import tkinter.filedialog

import sqlite3
import datetime as dt
import shutil
import os

root = Tk()
varS = StringVar()
varD = StringVar()


class ParentWindow(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        conn = sqlite3.connect('db_filemoverlog.db')
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT col_lastmove FROM tbl_filemoves ORDER BY id DESC LIMIT 1")
            row = cur.fetchall()
            print(row)

        self.master = master
        self.master.minsize(375,160)
        self.master.maxsize(375,160)
        self.master.title("Select Folders and Move Recent Files")

        self.lbl_MoveFiles = tk.Label(self.master,text="Last Time Files Were Moved:   " +str(row))
        self.lbl_MoveFiles.grid(row=2,column=0,padx=(15,0),pady=(1,0),sticky=N+S+E+W)
        self.lbl_pathLabel1 = tk.Entry(text = varS).grid(row = 0, column = 0, padx = 15, pady = 10, sticky = N+W+E)
        self.lbl_pathLabel2 = tk.Entry(text = varD).grid(row = 1, column = 0, padx = 15, pady = 5, sticky = W+E)
        self.lbl_browseButton1 = tk.Button(text = 'Source File Folder', command = self.SelectSource).grid(row = 0, column = 0, padx = (1,0), pady = 10, sticky = N+E)
        self.lbl_browseButton2 = tk.Button(text = 'Destination Folder', command = self.SelectDestination).grid(row = 1, column = 0, padx = (1,0), pady = 5, sticky = E)       
        self.btn_MoveFiles = tk.Button(self.master,width=48,height=2, text='Move Recently Modified .txt Files to the Destination Folder',command = lambda: self.MoveRecentlyModified(source,destination))
        self.btn_MoveFiles.grid(row=3,column=0,padx=(15,0),pady=(5,0),sticky=N+S+E+W)


    def create_db():
        conn = sqlite3.connect('db_filemoverlog.db')
        with conn:
            cur = conn.cursor()
            cur.execute("CREATE TABLE if not exists tbl_filemoves( \
                ID INTEGER PRIMARY KEY AUTOINCREMENT, \
                 col_lastmove TEXT\
                );")
            conn.commit()
        conn.close()
    create_db()

    def SelectSource(self):
        global source
        source = tkinter.filedialog.askdirectory(parent=root,initialdir="/Source_Options",title='Select a Folder to Sort and Move Recent Text Files From')   
        varS.set(source)
        print(source)
        return source
    

    def SelectDestination(self):
        global destination
        destination = tkinter.filedialog.askdirectory(parent=root,initialdir="/Destination_Options",title='Select a Folder to Move Text Files Modified Within the Last 24 Hours To')
        varD.set(destination)
        print(destination)
        return destination


    def MoveRecentlyModified(self,source,destination):
        now = dt.datetime.now()
        ago = now-dt.timedelta(hours=24)
        folder = os.listdir(source)
    
        for files in folder:
            path = os.path.join(source, files)
            st = os.stat(path)
            mtime = dt.datetime.fromtimestamp(st.st_mtime)

            if mtime > ago: 
                recents = ('%s modified %s'%(path, mtime))
                if files.endswith('.txt'):
                    shutil.move(os.path.join(source, files), os.path.join(destination))
                    print(files)

                    conn = sqlite3.connect('db_filemoverlog.db')
                    with conn:
                        cur = conn.cursor()
                        cur.execute("INSERT INTO tbl_filemoves (col_lastmove) VALUES (?)", (now,)) 
                    conn.close()

                    
    def fetchrow():
        conn = sqlite3.connect('db_filemoverlog.db')
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT col_lastmove FROM tbl_filemoves ORDER BY id DESC LIMIT 1")
            row = cur.fetchall()
            print(row)
                                 

if __name__== '__main__':
    App=ParentWindow(root)
