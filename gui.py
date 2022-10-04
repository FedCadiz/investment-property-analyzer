from sre_parse import State
import tkinter as tk
import customtkinter
from analyzer import Analyzer
import threading
import time

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"


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
        self.analyze = Analyzer(self.csentry.get(),int(self.lpspinbox.get()),int(self.downpayment),int(self.irentry.get()),int(self.urspinbox.get()),int(self.mlspinbox.get()),int(self.customentry.get()))
        self.loading = True

        self.purchase_price.configure(text=" ")
        self.down_payment.configure(text=" ")
        self.interest_rate.configure(text=" ")
        self.mortgage_length.configure(text=" ")
        self.monthly_label.configure(text=" ")
        self.units_rented.configure(text=" ")
        self.gar_label.configure(text=" ")
        self.roi_label.configure(text=" ")
        self.city_state.configure(text=" ")
        self.net_profit.configure(text=" ")

        def analyze_window():     
            while self.loading == True:
                self.monthly_label.configure(text="Loading")
                time.sleep(.5)
                self.monthly_label.configure(text="Loading.")
                time.sleep(.5)
                self.monthly_label.configure(text="Loading..")
                time.sleep(.5)
                self.monthly_label.configure(text="Loading...")
                time.sleep(.5)

        def execute_analyze():
            self.analyze.calculate()
            self.loading = False
            time.sleep(2)
            self.monthly_label.configure(text=f"Monthly Payment: \n{self.analyze.monthlyPayment}")
            self.gar_label.configure(text=f"Annual Gross Revenue: \n{self.analyze.totalRevenue}")
            self.net_profit.configure(text=f"Annual Net Profit: \n{self.analyze.netProfit}")
            self.roi_label.configure(text=f"ROI: {format(self.analyze.roi,'.2%')}")
            self.purchase_price.configure(text=f"Purchase Price: \n{self.analyze.price}")
            self.down_payment.configure(text=f"Down Payment: \n{self.analyze.downPayment}% | {self.downpaymentdollar}")
            self.interest_rate.configure(text=f"Interest Rate: \n{self.analyze.interestRate}%")
            self.mortgage_length.configure(text=f"Mortgage Length: \n{self.analyze.length} years")
            self.city_state.configure(text=f"Location: {self.analyze.city}, {self.analyze.state}")
            self.units_rented.configure(text=f"Units Rented: \n{self.analyze.units} units")

            self.csentry.delete(0,tk.END)
            self.lpspinbox.delete(0,tk.END)
            self.lpspinbox.insert(0,0)
            self.dpspin.delete(0,tk.END)
            self.dpspin.insert(0,0)
            self.irentry.delete(0,tk.END)
            self.urspinbox.delete(0,tk.END)
            self.urspinbox.insert(0,0)
            self.mlspinbox.delete(0,tk.END)
            self.mlspinbox.insert(0,15)
            self.customentry.delete(0,tk.END)
                
        t1 = threading.Thread(target=analyze_window)
        t2 = threading.Thread(target=execute_analyze)
        t1.start()
        t2.start()

        

    def __init__(self,master):
        # ============== Create Initial Frame ============== #
        
        master.title("Investment Property Analyzer")
        
        self.windowFrame = customtkinter.CTkFrame(master)
        self.windowFrame.grid_columnconfigure(1,weight=1)
        self.windowFrame.grid_rowconfigure(0,weight=1)
        self.windowFrame.pack()
        # ============== Create Left Frame ============== #
        self.leftwindowFrame = customtkinter.CTkFrame(self.windowFrame)
        self.leftwindowFrame.grid(column=0,row=0)
        self.leftwindowFrame.grid_columnconfigure(2,weight=1)
        self.leftwindowFrame.grid_rowconfigure(16,weight=1)
        
        # self.windowtitle = customtkinter.CTkLabel(self.leftwindowFrame,text="",text_font=("helvetica",25,"bold"))
        # self.windowtitle.grid(row=0,column=0,padx=10,pady=10,columnspan=3)

        self.label = customtkinter.CTkLabel(self.leftwindowFrame,text="City,State",text_font=(self.font))
        self.label.grid(row=1,column=1,pady=(20,0))

        self.csentry = customtkinter.CTkEntry(self.leftwindowFrame,text_font=self.font,width=375)
        self.csentry.grid(row=2,column=0,columnspan=3)

        self.label = customtkinter.CTkLabel(self.leftwindowFrame,text="Listing Price",text_font=(self.font))
        self.label.grid(row=3,column=1,pady=(10,0))

        self.lpspinbox = customtkinter.CTkEntry(self.leftwindowFrame,text_font=(self.font),justify=tk.CENTER,width=250)
        self.lpspinbox.grid(row=4,column=0,columnspan=3)


        self.label = customtkinter.CTkLabel(self.leftwindowFrame, text="Down Payment",text_font=(self.font))
        self.label.grid(row=5,column=1,pady=(10,0))
        
        self.dpspin = customtkinter.CTkEntry(self.leftwindowFrame,text_font=(self.font),justify=tk.CENTER,width=250)
        self.dpspin.grid(row=6,column=0,columnspan=3)

        self.label = customtkinter.CTkLabel(self.leftwindowFrame,text="Interest Rate",text_font=(self.font))
        self.label.grid(row=7,column=1,pady=(10,0))

        self.irentry = customtkinter.CTkEntry(self.leftwindowFrame,text_font=self.font,width=100,justify=tk.CENTER)
        self.irentry.grid(row=8,column=1)

        self.label = customtkinter.CTkLabel(self.leftwindowFrame,text="Mortgage Length",text_font=self.font)
        self.label.grid(row=9,column=1,pady=(10,0))

        self.mlspinbox = customtkinter.CTkEntry(self.leftwindowFrame,text_font=self.font,justify=tk.CENTER)
        self.mlspinbox.grid(row=10,column=1)

        self.label = customtkinter.CTkLabel(self.leftwindowFrame,text="Units Rented",text_font=(self.font))
        self.label.grid(row=11,column=1,pady=(10,0))

        self.urspinbox = customtkinter.CTkEntry(self.leftwindowFrame,text_font=(self.font),justify=tk.CENTER,width=100)
        self.urspinbox.grid(row=12,column=1)

        self.label = customtkinter.CTkLabel(self.leftwindowFrame,text="Rent Pricing", text_font=self.font)
        self.label.grid(row=13,column=1,pady=(10,5))

        self.rentvar = tk.StringVar(value="Custom")

        def custom_rent():
            self.customentry.configure(state="normal")
        def selected_rent():
            self.customentry.configure(state="disabled")
        self.conservativerent = customtkinter.CTkRadioButton(self.leftwindowFrame,text="Conservative",text_font=("Helvetica",15),variable=self.rentvar,value="Conservative",command=selected_rent)
        self.conservativerent.grid(row=14,column=0,padx=(5,0))
        
        self.moderaterent = customtkinter.CTkRadioButton(self.leftwindowFrame,text="Moderate",text_font=("Helvetica",15),variable=self.rentvar,value="Moderate",command=selected_rent)
        self.moderaterent.grid(row=14,column=1)
        
        self.agressiverent = customtkinter.CTkRadioButton(self.leftwindowFrame,text="Agressive",text_font=("Helvetica",15),variable=self.rentvar,value="Agressive",command=selected_rent)
        self.agressiverent.grid(row=14,column=2,padx=(0,10))

        self.customrent = customtkinter.CTkRadioButton(self.leftwindowFrame,text="Custom",text_font=("Helvetica",15),variable=self.rentvar,value="Custom",command=custom_rent)
        self.customrent.grid(row=15,column=1,pady=(10,0))

        self.customentry = customtkinter.CTkEntry(self.leftwindowFrame,text_font=(self.font),justify=tk.CENTER,width=100)
        self.customentry.grid(row=16,column=1,pady=(5,0))

        self.button = customtkinter.CTkButton(self.leftwindowFrame,text="Analyze",text_font=("helvetica",20,"bold"),command=self.analyze)
        self.button.grid(row=17,column=1,pady=(25,50))

        # ============== Create Right Frame ============== #  
        self.rightwindowFrame = customtkinter.CTkFrame(self.windowFrame)
        self.rightwindowFrame.grid(column=1,row=0,padx=30,pady=70,sticky="n")

        self.a_title = customtkinter.CTkLabel(self.rightwindowFrame,text="Analysis Results",text_font=("helvetica",25,"bold"),justify=tk.CENTER)
        self.a_title.grid(row=0,column=0,padx=(365,325),columnspan=3,pady=(30,60))

        self.purchase_price = customtkinter.CTkLabel(self.rightwindowFrame,text=" ",text_font=(self.font))
        self.purchase_price.grid(row=1,column=0,padx=(30,0),columnspan=1)

        self.down_payment = customtkinter.CTkLabel(self.rightwindowFrame,text=" ",text_font=(self.font))
        self.down_payment.grid(row=1,column=1,padx=10,columnspan=1)

        self.interest_rate = customtkinter.CTkLabel(self.rightwindowFrame,text=" ",text_font=(self.font))
        self.interest_rate.grid(row=1,column=2,padx=(0,30),columnspan=1)

        self.mortgage_length = customtkinter.CTkLabel(self.rightwindowFrame,text=" ",text_font=(self.font))
        self.mortgage_length.grid(row=2,column=0,padx=(30,0))
        
        self.monthly_label = customtkinter.CTkLabel(self.rightwindowFrame,text=" ",text_font=(self.font))
        self.monthly_label.grid(row=2,pady=60,column=1,padx=10)

        self.units_rented = customtkinter.CTkLabel(self.rightwindowFrame,text=" ",text_font=(self.font))
        self.units_rented.grid(row=2,column=2,padx=(0,30))
        
        self.net_profit = customtkinter.CTkLabel(self.rightwindowFrame,text=" ",text_font=(self.font))
        self.net_profit.grid(row=3,column=0,padx=(30,0))

        self.gar_label = customtkinter.CTkLabel(self.rightwindowFrame,text=" ",text_font=(self.font))
        self.gar_label.grid(row=3,column=1,padx=10)

        self.roi_label = customtkinter.CTkLabel(self.rightwindowFrame,text=" ",text_font=(self.font))
        self.roi_label.grid(row=3,column=2,padx=(0,30))

        self.city_state = customtkinter.CTkLabel(self.rightwindowFrame,text=" ",text_font=(self.font))
        self.city_state.grid(row=4,column=1,pady=50)

def run():
    root = tk.Tk()
    app = MyGui(root)
    root.mainloop()

run()