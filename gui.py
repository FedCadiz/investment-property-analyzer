from ast import Delete
import tkinter as tk
from tkinter import CENTER, END, HORIZONTAL, DoubleVar
from analyzer import Analyzer
import threading
import time




class MyGui:
    font = ("Helvetica",20)

    
    def analyze(self):
        if "%" in self.dpspin.get():
            self.downpayment = int(self.dpspin.get().split("%")[0])
        elif "$" in self.dpspin.get():
            self.downpayment = self.dpspin.get().split('$')[1]
            self.downpayment = (int(self.downpayment) / int(self.lpspinbox.get())) * 100
            
        self.downpaymentdollar = "${:0,.2f}".format((self.downpayment / 100) * int(self.lpspinbox.get()))
        # self.analyze = Analyzer("Garden Grove,California",500000,10,5,2,30)
        self.analyze = Analyzer(self.csentry.get(),int(self.lpspinbox.get()),int(self.downpayment),int(self.irentry.get()),int(self.urspinbox.get()),int(self.mlspinbox.get()))
        self.loading = True


        def analyze_window():     
            self.analyzeWindow = tk.Toplevel()
            self.analyzeFrame = tk.Frame(self.analyzeWindow)
            self.analyzeFrame.pack()
            self.a_title = tk.Label(self.analyzeFrame,text="Analysis Results",font=("helvetica",25,"bold"),justify=CENTER)
            self.a_title.grid(row=0,column=1,padx=100)

            self.purchase_price = tk.Label(self.analyzeFrame,text=" ",font=(self.font))
            self.purchase_price.grid(row=1,column=0,padx=(40,0),pady=10)

            self.down_payment = tk.Label(self.analyzeFrame,text=" ",font=(self.font))
            self.down_payment.grid(row=1,column=1,padx=40)

            self.interest_rate = tk.Label(self.analyzeFrame,text=" ",font=(self.font))
            self.interest_rate.grid(row=1,column=2,padx=(0,20))

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
            self.gar_label.config(text=f"Annual Gross Revenue: {self.analyze.totalRevenue}")
            self.net_profit.config(text=f"Annual Net Profit: {self.analyze.netProfit}")
            self.roi_label.config(text=f"ROI: {format(self.analyze.roi,'.2%')}")
            self.purchase_price.config(text=f"Purchase Price: {self.analyze.price}")
            self.down_payment.config(text=f"Down Payment: {self.analyze.downPayment}% | {self.downpaymentdollar}")
            self.interest_rate.config(text=f"Interest Rate: {self.analyze.interestRate}%")
            self.mortgage_length.config(text=f"Mortgage Length: {self.analyze.length} years")
            self.city_state.config(text=f"Location: {self.analyze.city}, {self.analyze.state}")
            self.units_rented.config(text=f"Units Rented: {self.analyze.units}")

            self.csentry.delete(0,END)
            self.lpspinbox.delete(0,END)
            self.lpspinbox.insert(0,0)
            self.dpspin.delete(0,END)
            self.dpspin.insert(0,0)
            self.irentry.delete(0,END)
            self.urspinbox.delete(0,END)
            self.urspinbox.insert(0,0)
            self.mlspinbox.delete(0,END)
            self.mlspinbox.insert(0,15)
                
        t1 = threading.Thread(target=analyze_window)
        t2 = threading.Thread(target=execute_analyze)
        t1.start()
        t2.start()

    def __init__(self,master):
        windowFrame = tk.Frame(master)
        windowFrame.pack()
        
        self.title = tk.Label(windowFrame,text="Investment Property Analyzer",font=("helvetica",25,"bold"))
        self.title.pack(pady=(10,30),padx=20)

        self.label = tk.Label(windowFrame,text="City,State",font=(self.font))
        self.label.pack()

        self.csentry = tk.Entry(windowFrame,font=self.font)
        self.csentry.pack()

        self.label = tk.Label(windowFrame,text="Listing Price",font=(self.font))
        self.label.pack(pady=(10,0))

        self.lpspinbox = tk.Spinbox(windowFrame,from_=0, to=1000000,increment=1000,font=(self.font),justify=CENTER)
        self.lpspinbox.pack()


        self.label = tk.Label(windowFrame, text="Down Payment (%/$)",font=(self.font))
        self.label.pack(pady=(10,0))
        
        self.dpspin = tk.Spinbox(windowFrame,from_=0,to=100,increment=1,font=(self.font),justify=CENTER)
        self.dpspin.pack(pady=(0,5))

        self.label = tk.Label(windowFrame,text="Interest Rate",font=(self.font))
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