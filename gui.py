from cgitb import text
import tkinter as tk
from tkinter import CENTER, HORIZONTAL
from analyzer import Analyzer
import threading
import time




class MyGui:
    font = ("Helvetica",20)

    def show_down_payment(self,percentage = 0):
        purchasePrice = self.lpspinbox.get()
        percentage = float(percentage) * .01
        downPayment = (float(purchasePrice) * percentage)
        self.dplabel.config(text=("${:0,.2f}".format(downPayment)))
        global dollardownpayment
        dollardownpayment = ("${:0,.2f}".format(downPayment))
    
    def analyze(self):
        # self.analyze = Analyzer("Garden Grove,California",500000,10,5,2,30)
        self.analyze = Analyzer(self.csentry.get(),int(self.lpspinbox.get()),int(self.scale.get()),int(self.irentry.get()),int(self.urspinbox.get()),int(self.mlspinbox.get()))
        self.loading = True
        def analyze_window():     
            self.analyzeWindow = tk.Toplevel()
            self.analyzeFrame = tk.Frame(self.analyzeWindow)
            self.analyzeFrame.pack()
            self.a_title = tk.Label(self.analyzeFrame,text="Analysis Results",font=("helvetica",25,"bold"))
            self.a_title.grid(row=0,columnspan=3,padx=500)

            self.purchase_price = tk.Label(self.analyzeFrame,text=" ",font=(self.font))
            self.purchase_price.grid(row=1,column=0,padx=20,pady=10)

            self.down_payment = tk.Label(self.analyzeFrame,text=" ",font=(self.font))
            self.down_payment.grid(row=1,column=1,padx=20)

            self.interest_rate = tk.Label(self.analyzeFrame,text=" ",font=(self.font))
            self.interest_rate.grid(row=1,column=2,padx=20)

            self.mortgage_length = tk.Label(self.analyzeFrame,text=" ",font=(self.font))
            self.mortgage_length.grid(row=2,column=0,pady=10)
            
            self.monthly_label = tk.Label(self.analyzeFrame,text=" ",font=(self.font))
            self.monthly_label.grid(row=2,column=1)

            self.city_state = tk.Label(self.analyzeFrame,text=" ",font=(self.font))
            self.city_state.grid(row=4,column=1)

            self.units_rented = tk.Label(self.analyzeFrame,text=" ",font=(self.font))
            self.units_rented.grid(row=2,column=2)

            self.gar_label = tk.Label(self.analyzeFrame,text=" ",font=(self.font))
            self.gar_label.grid(row=3,column=1,)

            self.roi_label = tk.Label(self.analyzeFrame,text=" ",font=(self.font))
            self.roi_label.grid(row=3,column=2)

            self.net_profit = tk.Label(self.analyzeFrame,text=" ",font=(self.font))
            self.net_profit.grid(row=3,column=0,pady=10)

            while self.loading == True:
                self.monthly_label.config(text="Loading")
                time.sleep(.5)
                self.monthly_label.config(text="Loading.")
                time.sleep(.5)
                self.monthly_label.config(text="Loading..")
                time.sleep(.5)
                self.monthly_label.config(text="Loading...")
                time.sleep(.5)

        def execute_analyze():
            self.analyze.calculate()
            self.loading = False
            time.sleep(2)
            self.monthly_label.config(text=f"Monthly Payment: {self.analyze.monthlyPayment}")
            self.gar_label.config(text=f"Gross Annual Rent: {self.analyze.totalRevenue}")
            self.net_profit.config(text=f"Net Profit: {self.analyze.netProfit}")
            self.roi_label.config(text=f"ROI: {format(self.analyze.roi,'.2%')}")
            self.purchase_price.config(text=f"Purchase Price: {self.analyze.price}")
            self.down_payment.config(text=f"Down Payment: {self.analyze.downPayment}% | {dollardownpayment}")
            self.interest_rate.config(text=f"Interest Rate: {self.analyze.interestRate}%")
            self.mortgage_length.config(text=f"Mortgage Length: {self.analyze.length} years")
            self.city_state.config(text=f"Location: {self.analyze.city}, {self.analyze.state}")
            self.units_rented.config(text=f"Units Rented: {self.analyze.units}")
            
        t1 = threading.Thread(target=analyze_window)
        t2 = threading.Thread(target=execute_analyze)
        t1.start()
        t2.start()

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