# %load Grid-testing.py
import tkinter as tk
from tkinter import ttk
import numpy as np
from cellular_automaton import *
import argparse

import multiprocessing as mp
import time
##############
##re-organise
#############
n=10
parser = argparse.ArgumentParser(description='grid size')
parser.add_argument('integer',metavar=n,type=int)
n=parser.parse_args().integer


A =  np.random.randint(0,2,(n,n))
Grid_obj = Grid(A)

Dynamic_windows = []

def close_dynamic_window(window):
    if window not in Dynamic_windows:
        pass
    elif window in Dynamic_windows:
        Dynamic_windows.remove(window)
        window.destroy()


class App(tk.Frame, tk.Toplevel):
    def __init__(self, n_rows, n_cols,*args, **kwargs):
        #tk.Frame.__init__(self, *args, **kwargs)
        tk.Toplevel.__init__(self, *args, **kwargs)

        self.title("Grid")
        self.resizable(tk.FALSE,tk.FALSE)
        self.option_add('*tearOff', tk.FALSE)
        self.protocol("WM_DELETE_WINDOW", self.exit)
        #self.controls = tk.Frame(self).grid(sticky='nw',row=0,column=0,columnspan=2,rowspan=2)

        self.threshold=5

        self.n_rows = n_rows
        self.n_cols = n_cols

        self.grid_matrix = A

        self.cells = list()

        self.blank = tk.PhotoImage(file="blank.png")

        self.menubar = Menubar(self)
        self['menu'] = self.menubar

        self.speed = 1

        self.speed_scale = tk.Scale(self, orient=tk.VERTICAL, from_=0.1, to_=10,variable=self.speed, label="Seconds",resolution=0.1)
        self.speed_scale.set(self.speed)
        self.speed_scale.grid(sticky='nw',row=1,column=n, rowspan=10)


        self.pause_flag=False

        self.pause_button = tk.Checkbutton(self, text="Pause", command=lambda: self.pause(), variable=self.pause_flag)
        self.pause_button.grid(sticky='w',row=0,column=n)

        self.threshold_scale = tk.Scale(self,orient=tk.VERTICAL, from_=0,to_=8,variable=self.threshold,label="Neighbours")
        self.threshold_scale.set(self.threshold)
        self.threshold_scale.grid(sticky='nw',row=1,column=n+1,rowspan=10)

        self.model_type = tk.StringVar()
        self.model_type.set("Moore")
        self.moore_button = tk.Radiobutton(self, text='Moore', variable=self.model_type, value="Moore")
        self.conway_button = tk.Radiobutton(self, text='Game of Life', variable=self.model_type, value="Conway")
        self.moore_button.grid(sticky='w',row=0,column=n+1)
        self.conway_button.grid(sticky='w',row=0,column=n+2)

        self.proc = mp.Process(target=self.load_cells)
        self.proc.start()
        self.proc.join()
        self.mainloop()

    def exit(self):
        for i in range(0,len(self.cells)):
            self.cells[i].destroy()
        self.grab_release()
        self.quit()
        T.grab_release()
        T.quit()

    def load_cells(self):
        s = time.time()
        for i in range(0,self.n_rows*self.n_cols):
            print(i)
            self.cells.append(Cell(self,image=self.blank,width=10,height=10))
            row,col = divmod(i,self.n_cols)
            self.cells[i].grid(sticky='nsew', row=row, column=col)
            if (self.grid_matrix[row,col]==1):
                self.cells[i].configure(bg='white')
                self.cells[i].configure(activebackground='white')
            else:
                self.cells[i].configure(bg='black')
                self.cells[i].configure(activebackground='black')
            self.update()
        e = time.time()
        print(e-s)
        self.mainloop()

    def pause(self):
        if (self.pause_flag == True):
            self.pause_flag = False
            self.animate()
        elif (self.pause_flag == False):
            self.pause_flag = True


    def get_random_grid(self):
        self.grid_matrix = np.random.randint(0,2,(n,n))
        Grid_obj.set_grid(self.grid_matrix)
        self.update_cells()


    def next_grid(self):
        self.grid_matrix = Grid_obj.get_next_gen(self.threshold_scale.get())
        self.update_cells()


    def update_cells(self):
        for i in range(0,self.n_rows*self.n_cols):
            row,col = divmod(i,self.n_cols)
            if (self.grid_matrix[row,col]==1):
                if self.cells[i].cget('bg')=='black':
                    self.cells[i].change_state(to_state=1)
            else:
                if self.cells[i].cget('bg')=='white':
                    self.cells[i].change_state(to_state=0)


    def animate(self):
        Grid_obj.set_model(self.model_type.get())
        if (self.pause_flag):
            return
        self.update_cells()
        prev = (self.grid_matrix).copy()
        print(prev)
        self.next_grid()
        if (np.array_equal(prev,self.grid_matrix)):
            return
        self.after(int(1000*self.speed_scale.get()),self.animate)


    def update_grid(self):
        for i in range(0,self.n_rows*self.n_cols):
            row,col = divmod(i,self.n_cols)
            if self.cells[i].cget('bg') == 'white':
                self.grid_matrix[row,col] = 1
            elif self.cells[i].cget('bg') == 'black':
                self.grid_matrix[row,col] = 0
        Grid_obj.set_grid(self.grid_matrix)
        print(self.grid_matrix)

class Menubar(tk.Menu, App):
    def __init__(self,parent,*args,**kwargs):
        self.parent=parent
        tk.Menu.__init__(self,parent,*args,**kwargs)

        self.about_window=None
        self.save_window=None
        self.open_window=None

        # initialise menu vars
        self.menu_file=tk.Menu(self)
        self.menu_simulation=tk.Menu(self)
        self.add_command(label="About",command=lambda: self.about())

        self.menu_file.add_command(label="Save", command=lambda: self.save)
        self.menu_file.add_command(label="Open", command=lambda: self.open)

        self.menu_simulation.add_command(label="Run", command=lambda: parent.animate())
        self.menu_simulation.add_command(label="Update", command=lambda: parent.update_grid())
        self.menu_simulation.add_command(label="Random Grid", command=lambda: parent.get_random_grid())

        #collect them in a list
        menus = ((self.menu_file,"File"),
                 (self.menu_simulation,"Simulation"))
        # quickly deploy the menus
        for i,(var,lab) in enumerate(menus):
            self.add_cascade(menu=var,label=lab)
    def save(self):
        pass
    def open(self):
        pass
    def about(self):
        if self.about_window not in Dynamic_windows:
            self.about_window = tk.Toplevel()
            self.about_window.title("About")
            self.about_window.protocol(name="WM_DELETE_WINDOW", func=lambda: close_dynamic_window(self.about_window))
            s = """This is a cellular automaton simulator.

https://en.wikipedia.org/wiki/Cellular_automaton

-GUI written in python 2.7 Tkinter.
-Simulator written in C++ with boost.
-Harvey Devereux.
-harveydevereux@googlemail.com.
"""
            info = tk.Label(self.about_window, text=s)
            info.grid(column=0,row=0)
            Dynamic_windows.append(self.about_window)



class Cell(tk.Button, App):
    def __init__(self,parent,*args,**kwargs):
        tk.Button.__init__(self, parent, bg="white", bd=0, highlightthickness = 0, activebackground="white",
                           relief="flat", overrelief="flat",
                           command=self.change_state,
                           *args, **kwargs)
        self.parent = parent
    def change_state(self, to_state=None):
        if (self.cget('bg') == 'white' or to_state == 0) :
            self.configure(bg='black')
            self.configure(activebackground='black')
        elif (self.cget('bg') == 'black' or to_state == 1):
            self.configure(bg='white')
            self.configure(activebackground='white')
        if (to_state == None):
            self.parent.update_grid()
        #if (to_state==None):
        #    self.parent.update_cells()

if __name__ == "__main__":
    T = tk.Tk()
    T.withdraw()
    main = App(n_rows=n,n_cols=n)
