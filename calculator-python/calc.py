from tkinter import Tk, Label, Button, Entry, IntVar, END, W, E, S, N, Frame

class Calculator:

    def __init__(self, master):
        self.master = master
        master.title("Calculator")
        self.frame1 = Frame(self.master)

        self.total = 0
        self.entered_number = 0

        self.total_label_text = IntVar()
        self.total_label_text.set(self.total)
        self.total_label = Label(master, textvariable=self.total_label_text)

        self.label = Label(master, text="Total:")

        vcmd = master.register(self.validate) # we have to wrap the command
        self.entry = Entry(master, validate="key", validatecommand=(vcmd, '%P'))

        self.add_button = Button(self.frame1, text="+", command=lambda: self.update("add"))
        self.subtract_button = Button(self.frame1, text="-", command=lambda: self.update("subtract"))
        self.division_button = Button(self.frame1, text="/", command=lambda: self.update("division"))
        self.multiplication_button = Button(self.frame1, text="*", command=lambda: self.update("multiplication"))
        self.reset_button = Button(self.frame1, text="Reset", command=lambda: self.update("reset"))

        # Insert numbers and symbols 
        self.period_button = Button(self.frame1, text=".", command=lambda: self.insert_number("."))
        self.zero_button = Button(self.frame1, text="0", command=lambda: self.insert_number("0"))
        self.one_button = Button(self.frame1, text="1", command=lambda: self.insert_number("1"))
        self.two_button = Button(self.frame1, text="2", command=lambda: self.insert_number("2"))
        self.three_button = Button(self.frame1, text="3", command=lambda: self.insert_number("3"))
        self.four_button = Button(self.frame1, text="4", command=lambda: self.insert_number("4"))
        self.five_button = Button(self.frame1, text="5", command=lambda: self.insert_number("5"))
        self.six_button = Button(self.frame1, text="6", command=lambda: self.insert_number("6"))
        self.seven_button = Button(self.frame1, text="7", command=lambda: self.insert_number("7"))
        self.eight_button = Button(self.frame1, text="8", command=lambda: self.insert_number("8"))
        self.nine_button = Button(self.frame1, text="9", command=lambda: self.insert_number("9"))
            

        # LAYOUT
        # master
        self.label.grid(row=0, column=0, sticky=W+E)
        self.total_label.grid(row=0, column=1, columnspan=2, sticky=W+E)
        self.entry.grid(row=1, column=0, columnspan=3, sticky=W+E)

        # frame
        self.frame1.grid(row=2, column=0, columnspan=3, sticky=W+E)
        
        self.seven_button.grid(row=0, column=0, sticky=W+E)
        self.eight_button.grid(row=0, column=1, sticky=W+E)
        self.nine_button.grid(row=0, column=2, sticky=W+E)

        self.four_button.grid(row=1, column=0, sticky=W+E)
        self.five_button.grid(row=1, column=1, sticky=W+E)
        self.six_button.grid(row=1, column=2, sticky=W+E)

        self.one_button.grid(row=2, column=0, sticky=W+E)
        self.two_button.grid(row=2, column=1, sticky=W+E)
        self.three_button.grid(row=2, column=2, sticky=W+E)

        self.zero_button.grid(row=3, column=1, sticky=W+E)
        self.period_button.grid(row=3, column=0, sticky=W+E) 
        self.division_button.grid(row=3, column=3, sticky=W+E)
        self.multiplication_button.grid(row=4, column=3, sticky=W+E)


        
        self.add_button.grid(row=0, column=3, sticky=W+E)
        self.subtract_button.grid(row=1, column=3, sticky=W+E)
        self.reset_button.grid(row=2, column=3, sticky=W+E)


    def validate(self, new_text):
        if not new_text: # the field is being cleared
            self.entered_number = 0
            return True

        try:
            self.entered_number = float(new_text)
            return True
        except ValueError:
            return False
    
    def insert_number(self, number):
        self.entry.insert(END, number)
        
    def update(self, method):
        if method == "add":
            self.total += self.entered_number
        elif method == "subtract":
            self.total -= self.entered_number
        elif method == "division":
            if(not self.total or self.total == 0 or self.total == 0.0):
                self.total = self.entered_number
            else:
                try:
                    self.total /= self.entered_number
                except ZeroDivisionError:
                    pass
        elif method == "multiplication":
            if(not self.total or self.total == 0 or self.total == 0.0):
              self.total = self.entered_number
            else:  
                self.total *= self.entered_number
        else: # reset
            self.total = 0

        self.total_label_text.set(self.total)
        self.entry.delete(0, END)

root = Tk()

# Prevent from resizing
root.resizable(False,False)

my_gui = Calculator(root)
root.mainloop()