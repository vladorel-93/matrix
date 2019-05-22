import tkinter as tk
import numpy as nm


LARGE_FONT= ("Verdana", 12)


class Calc(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, Mult):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

class SimpleTableInput(tk.Frame):
    def __init__(self, parent, rows, columns):
        tk.Frame.__init__(self, parent)

        self._entry = {}
        self.rows = rows
        self.columns = columns

        # register a command to use for validation
        vcmd = (self.register(self._validate), "%P")

        # create the table of widgets
        for row in range(self.rows):
            for column in range(self.columns):
                index = (row, column)
                e = tk.Entry(self, validate="key", validatecommand=vcmd)
                e.grid(row=row, column=column, stick="nsew")
                self._entry[index] = e
        # adjust column weights so they all expand equally
        for column in range(self.columns):
            self.grid_columnconfigure(column, weight=1)
        # designate a final, empty row to fill up any extra space
        self.grid_rowconfigure(rows, weight=1)

    def get(self):
        '''Return a list of lists, containing the data in the table'''
        result = []
        for row in range(self.rows):
            current_row = []
            for column in range(self.columns):
                index = (row, column)
                current_row.append(self._entry[index].get())
            result.append(current_row)
        return result

    def _validate(self, P):
        '''Perform input validation. 

        Allow only an empty value, or a value that can be converted to a float
        '''
        if P.strip() == "":
            return True

        try:
            f = float(P)
        except ValueError:
            self.bell()
            return False
        return True


class SizeChooser(tk.Frame):
    
    def __init__(self, parent):
        tk.Frame.__init__(self,parent)
        self.rows = tk.Entry(self)
        self.rows.grid(row=0,column=0)
        label = tk.Label(self, text=" x ", font=LARGE_FONT)
        label.grid(row=0,column=1)
        self.columns = tk.Entry(self)
        self.columns.grid(row=0,column=2)


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.grid(row=0,column=0)

        button = tk.Button(self, text="Multiple",
                            command=lambda: controller.show_frame(Mult))
        button.grid(row=1,column=0)
        '''
        button2 = tk.Button(self, text="Visit Page 2",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()'''


class Mult(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="A x B", font=LARGE_FONT)
        label.grid(row=0, column=1)
        
        size_A = label = tk.Label(self, text="Size A", font=LARGE_FONT)
        size_A.grid(row=1, column=0)
        size_B = label = tk.Label(self, text="Size B", font=LARGE_FONT)
        size_B.grid(row=1, column=2)
        
        self.size_1 = SizeChooser(self)
        self.size_1.grid(row=2, column=0)
        self.size_2 = SizeChooser(self)
        self.size_2.grid(row=2, column=2)
        
        self.table_1 = SimpleTableInput(self, 2, 2)
        self.table_1.grid(row=4, column=0)
        self.table_2 = SimpleTableInput(self, 2, 2)
        self.table_2.grid(row=4, column=2)

        self.set_1 = tk.Button(self, text="Set", command=lambda: self.update_matrix('A'))
        self.set_1.grid(row=3, column=0)
        self.set_2 = tk.Button(self, text="Set", command=lambda: self.update_matrix('B'))
        self.set_2.grid(row=3, column=2)

        self.result = tk.Button(self, text="multiply", command=self.get_mult)
        self.result.grid(row=5, column=1)
        mult_symbol = tk.Label(self, text="X", font=LARGE_FONT)
        mult_symbol.grid(row=4, column=1)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.grid(row=6, column=1)


    def update_matrix(self, matrix):
        if matrix == 'A':
            self.table_1.destroy()
            self.table_1 = SimpleTableInput(self, int(self.size_1.rows.get()), int(self.size_1.columns.get()))
            self.table_1.grid(row=4, column=0)
        else:
            self.table_2.destroy()
            self.table_2 = SimpleTableInput(self, int(self.size_2.rows.get()), int(self.size_2.columns.get()))
            self.table_2.grid(row=4, column=2)

    def get_mult(self):
        #proceed

        cols_1 = len(self.table_1.get()[0])
        rows_2 = len(self.table_2.get())
        if (cols_1 != rows_2):
            print ('Multiplication is impossible')
        else:
            mult = nm.dot(self.table_1.get(), self.table_2.get())
            print (mult)
        '''
        button2 = tk.Button(self, text="Page Two",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()'''

'''
class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()


'''        


app = Calc()
app.mainloop()
