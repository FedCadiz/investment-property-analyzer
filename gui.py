import tkinter as tk
from tkinter import CENTER, HORIZONTAL, Label, font
from tkinter.tix import COLUMN
from analyzer import Analyzer




class MyGui:
    font = ("Helvetica",20)

    def show_down_payment(self,percentage = 0):
        purchasePrice = self.lpspinbox.get()
        percentage = float(percentage) * .01
        downPayment = (float(purchasePrice) * percentage)
        self.dplabel.config(text=("${:0,.2f}".format(downPayment)))
    
    def analyze(self):
        # self.analyze = Analyzer(self.csentry.get(),int(self.lpspinbox.get()),int(self.scale.get()),int(self.irentry.get()),int(self.urspinbox.get()),int(self.mlspinbox.get()))
        self.analyze = Analyzer("Garden Grove,California",500000,10,5,2,30)
        self.analyze.calculate()
        self.analyzeWindow = tk.Toplevel()
        self.analyzeFrame = tk.Frame(self.analyzeWindow)
        self.analyzeFrame.pack()
        self.a_title = tk.Label(self.analyzeFrame,text="Analysis Results",font=("helvetica",25,"bold"))
        self.a_title.grid(row=0,columnspan=3)

        self.label = tk.Label(self.analyzeFrame,text=f"Monthly Payment: ${self.analyze.monthlyPayment}",font=(self.font))
        self.label.grid(row=1,column=0)

        self.label = tk.Label(self.analyzeFrame,text=f"Gross Annual Rent: ${self.analyze.totalRevenue}",font=(self.font))
        self.label.grid(row=1,column=1)

        self.label = tk.Label(self.analyzeFrame,text=f"ROI: {format(self.analyze.totalReturn,'.2%')}",font=(self.font))
        self.label.grid(row=1,column=2)
        
        

        


    def __init__(self,master):
        windowFrame = tk.Frame(master)
        windowFrame.pack()
        
        self.title = tk.Label(windowFrame,text="Investment Property Analyzer",font=("helvetica",25,"bold"))
        self.title.pack(pady=(10,30))

        self.label = tk.Label(windowFrame,text="City,State",font=(self.font))
        self.label.pack()

        self.csentry = tk.Entry(windowFrame,font=self.font)
        self.csentry.pack()

        self.label = tk.Label(windowFrame,text="Listing Price",font=(self.font))
        self.label.pack(pady=(10,0))

        self.lpspinbox = tk.Spinbox(windowFrame,from_=0, to=1000000,increment=1000,font=(self.font),justify=CENTER,command=self.show_down_payment)
        self.lpspinbox.pack()


        self.label = tk.Label(windowFrame, text="Down Payment (%)",font=(self.font))
        self.label.pack(pady=(10,0))
    
        self.scale = tk.Scale(windowFrame,from_= 0, to=100,orient=HORIZONTAL,font=(self.font),length=200,command=self.show_down_payment)
        self.scale.pack()

        self.dplabel = tk.Label(windowFrame,text=" ",font=("Helvetica", 15))
        self.dplabel.pack()

        self.label = tk.Label(windowFrame,text="Interest Rate (%)",font=(self.font))
        self.label.pack(pady=(10,0))

        self.irentry = tk.Entry(windowFrame,font=self.font,width=5,justify=CENTER)
        self.irentry.pack()

        self.label = tk.Label(windowFrame,text="Mortgage Length",font=self.font)
        self.label.pack(pady=(10,0))

        self.mlspinbox = tk.Spinbox(windowFrame,from_=15,to=30,increment=15,font=self.font,justify=CENTER)
        self.mlspinbox.pack()

        self.label = tk.Label(windowFrame,text="Units Rented",font=(self.font))
        self.label.pack(pady=(10,0))

        self.urspinbox = tk.Spinbox(windowFrame,from_=0,to=4,increment=1,font=(self.font),justify=CENTER,width=8)
        self.urspinbox.pack()

        self.button = tk.Button(windowFrame,text="Analyze",font=("helvetica",20,"bold"),command=self.analyze)
        self.button.pack(pady=(10))

def run():
    root = tk.Tk()
    app = MyGui(root)
    root.mainloop()

    
run()
