# %load Grid-testing.py
import tkinter as tk
from tkinter import ttk
import numpy as np
from cellular_automaton import *

n=20
A =  np.random.randint(0,2,(n,n))
Grid_obj = Grid(A)

Dynamic_windows = []

class App(tk.Frame):
    def __init__(self, parent, n_rows, n_cols, threshold, *args, **kwargs):
        self.parent = parent
        tk.Frame.__init__(self,parent, *args, **kwargs)
        self.controls = tk.Frame(self).grid(sticky='nw',row=0,column=0,columnspan=2,rowspan=2)

        self.threshold=threshold

        self.n_rows = n_rows
        self.n_cols = n_cols

        self.grid_matrix = A

        self.cells = list()
        for i in range(0,self.n_rows*self.n_cols):
            self.cells.append(Cell(self))
            row,col = divmod(i,self.n_cols)
            self.cells[i].grid(sticky='nsew', row=row, column=col)
            if (self.grid_matrix[row,col]==1):
                self.cells[i].configure(bg='white')
                self.cells[i].configure(activebackground='white')
            else:
                self.cells[i].configure(bg='black')
                self.cells[i].configure(activebackground='black')

        self.menubar = Menubar(self)
        self.parent['menu'] = self.menubar

        self.speed = 750

        self.speed_scale = tk.Scale(self.controls, orient=tk.VERTICAL, from_=0.1, to_=10,variable=self.speed, label="Seconds",resolution=0.1)
        self.speed_scale.grid(sticky='nw',row=0,column=n, rowspan=10)
        self.speed_scale.set(self.speed)
        #self.animate()
    def next_grid(self):
        self.grid_matrix = Grid_obj.get_next_gen(self.threshold)
        self.update_cells()
    def update_cells(self):
        print("u")
        for i in range(0,self.n_rows*self.n_cols):
            row,col = divmod(i,self.n_cols)
            if (self.grid_matrix[row,col]==1):
                if self.cells[i].cget('bg')=='black':
                    self.cells[i].change_state(to_state=1)
            else:
                if self.cells[i].cget('bg')=='white':
                    self.cells[i].change_state(to_state=0)
    def animate(self):
        self.update_cells()
        prev = (self.grid_matrix).copy()
        print(prev)
        self.next_grid()
        if (np.array_equal(prev,self.grid_matrix)):
            return
        self.after(int(1000*self.speed_scale.get()),self.animate)
    def update_grid(self):
        print("Ugrid")
        for i in range(0,self.n_rows*self.n_cols):
            row,col = divmod(i,self.n_cols)
            if self.cells[i].cget('bg') == 'white':
                self.grid_matrix[row,col] = 1
            elif self.cells[i].cget('bg') == 'black':
                self.grid_matrix[row,col] = 0
        print(type(Grid_obj))
        Grid_obj.set_grid(self.grid_matrix)
        print(self.grid_matrix)

class Menubar(tk.Menu, App):
    def __init__(self,parent,*args,**kwargs):
        self.parent=parent
        tk.Menu.__init__(self,parent,*args,**kwargs)

        self.about_window=None

        # initialise menu vars
        self.menu_file=tk.Menu(self)
        self.menu_simulation=tk.Menu(self)
        self.add_command(label="About",command=lambda: self.about())

        self.menu_file.add_command(label="Save", command=lambda: self.save_gridfile)
        self.menu_file.add_command(label="Open", command=lambda: self.open_gridfile)

        self.menu_simulation.add_command(label="Run", command=lambda: parent.animate())
        self.menu_simulation.add_command(label="Update", command=lambda: parent.update_grid())

        #collect them in a list
        menus = ((self.menu_file,"File"),
                 (self.menu_simulation,"Simulation"))
        # quickly deploy the menus
        for i,(var,lab) in enumerate(menus):
            self.add_cascade(menu=var,label=lab)
    def save_gridfile(self):
        pass
    def open_gridfile(self):
        pass
    def about(self):
        if self.about_window not in Dynamic_windows:
            self.about_window = tk.Toplevel()
            self.about_window.title("About")
            s = """This is a cellular automaton simulator.

https://en.wikipedia.org/wiki/Cellular_automaton

-GUI written in python 2.7 Tkinter.
-Simulator engine written in C++ with boost.
-Harvey Devereux.
-harveydevereux@googlemail.com.
-version 0.2
"""
            info = tk.Label(self.about_window, text=s)
            info.grid(column=0,row=0)
            Dynamic_windows.append(self.about_window)



class Cell(tk.Button, App):
    def __init__(self,parent,*args,**kwargs):
        tk.Button.__init__(self, parent, bg="white",activebackground="white",
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
    root = tk.Tk()
    root.title("Grid")
    root.resizable(tk.FALSE,tk.FALSE)
    root.option_add('*tearOff', tk.FALSE)
    main = App(root,n_rows=n,n_cols=n,threshold=4).grid(column=0,row=0,sticky='nesw')
    root.mainloop()
