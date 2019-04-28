#!/usr/local/bin/python
# coding: latin-1
# to avoid: sys:1: DeprecationWarning: Non-ASCII character '\xe0' in file D:\bin\mef2html\tk
# mef2html2.PY on line 146, but no encoding declared; see http://www.python.org/peps/pep-0263.html for details
'''
This module shows how making a quick interface for text processing,
with common dialog box.
'''

from tkinter import *
from Dialog import Dialog
from FileDialog import LoadFileDialog
from ScrolledText import ScrolledText

from mywidget import *

import os

from meftohtml import *
from mef2html import *
# -----------------------------------------------------------------------------
# global configuration
PROG_BROWSER='C:\\cmd\\Firefox2\\firefox.exe '
PROG_EDITOR='C:\\cmd\\opt\\ConTEXT\\ConTEXT.exe'
# -----------------------------------------------------------------------------
class FilenameEntry(Frame):
    """a widget for displaying a input edit box and a browser to choose a file """
    def __init__(self, master, text):
        Frame.__init__(self, master)
        Label(self, text=text,width=15).pack(side=LEFT)
        self.filename = StringVar()
        Entry(self, textvariable=self.filename, width=40).pack(side=LEFT, fill=X,padx=15)
        Button(self, text="Browse...", command=self.browse).pack(side=RIGHT)

    def browse(self):
        file = LoadFileDialog(self).go(pattern='*')
        if file:
            self.filename.set(file)

    def get(self):
        return self.filename.get()

    def put(self,val):
        self.filename.set(val)

class ButtonBar(Frame):
    """ a button bar widget """
    def __init__(self, master, left_button_list, right_button_list):
        Frame.__init__(self, master, bd=2, relief=SUNKEN)
        for button, action in left_button_list:
            Button(self, text=button, command=action).pack(side=LEFT)
        for button, action in right_button_list:
            Button(self, text=button, command=action).pack(side=RIGHT)


class FileNotFoundMessage(Dialog):
    """ dialog message """
    def __init__(self, master, filename):
        Dialog.__init__(self, master, title = 'File not found',
                        text = 'File ' + filename + ' does not exist',
                        bitmap = 'warning', default = 0,
                        strings = ('Ok',))

class InfoMessage(Dialog):
    """ dialog message """
    def __init__(self, master):
        Dialog.__init__(self, master, title = 'About box',
                        text = __doc__,
                        bitmap = 'warning', default = 0,
                        strings = ('Ok',))

class NoFileMessage(Dialog):
    """ dialog message """
    def __init__(self, master):
        Dialog.__init__(self, master, title = 'About box',
                        text = 'There no entry',
                        bitmap = 'warning', default = 0,
                        strings = ('Ok',))

class TextWindow(Frame):
    """ a text window widget to show text"""
    def __init__(self, master, text):
        Frame.__init__(self, master)
        text_field = ScrolledText(self)
        text_field.insert(At(0,0), text)
        text_field.pack(side=TOP)
        text_field.config(state=DISABLED)
        ButtonBar(self, [],[('Close', self.master.destroy)]).pack(side=BOTTOM, fill=X)


class MainWindow(Frame):
    """ the min window: tipic window :
           - file input
           - file output
           - a button bar action
           - a button bar editionand quit
    """
    def __init__(self, master):
        Frame.__init__(self, master,relief=RAISED, bd=2)
       	Label(self, text='mef2html', font=('Helvetica', 12, 'italic bold'),background='blue', foreground='white').pack(side=TOP, expand=NO, fill=X)
        Label(self, text="Enter a filename and " +
                         "select an action").pack(side=TOP)
        self.filename_field = FilenameEntry(self, "Source filename: ")
        self.filename_field.pack(side=TOP, fill=X)

        self.filedest_field = FilenameEntry(self, "Dest filename: ")
        self.filedest_field.pack(side=TOP, fill=X)
        Label(self,text=" ").pack(side=TOP)


        ButtonBar(self,[('Show Input', self.input),('Clear Ouput', self.clear_output),('Rename Ouput', self.adapt_output),
                          ('Show Output', self.output),('Mef2html', self.mef2html),('About',self.about),('Quit', self.quit)]

                         ,[]).pack(side=BOTTOM, fill=X,pady=2)
    def show(self):
        """ shows the file """
        filename = self.filename_field.get()
        try:
            text = open(filename).read()
        except IOError:
            FileNotFoundMessage(self, filename)
        else:
            new_window = Toplevel()
            new_window.title(filename)
            TextWindow(new_window, text).pack()

    def mef2html(self):
        """ process the file """
        filename = self.filename_field.get()
        if filename == "":
           NoFileMessage(self)
        dest = self.filedest_field.get()
        if dest =="":
          dest=filename[:-4]+'.html'
          self.filedest_field.put(dest)
        process(filename,dest)

    def clear_output(self):
        dest=""
        self.filedest_field.put(dest)

    def adapt_output(self):
        filename = self.filename_field.get()
        if filename == "":
           NoFileMessage(self)
        dest = self.filedest_field.get()
        if dest =="":
           dest=filename[:-4]+'.html'
           self.filedest_field.put(dest)

    def input(self):
        """ edit the input file with an editor  """
        filename = self.filename_field.get()
        if filename == "":
           NoFileMessage(self)
        else:
           os.system(PROG_EDITOR+" "+filename)

    def output(self):
        """ show the result with a browser  """
        filename = self.filedest_field.get()
        if filename == "":
           NoFileMessage(self)
        else:
          os.system(PROG_BROWSER+" "+filename)

    def about(self):
        """About message box"""
        InfoMessage(self)

#================================================================================
root = Tk()
root.title('mef2html converter v 1.0')
mw = MainWindow(None)
mw.pack()
mw.mainloop()
