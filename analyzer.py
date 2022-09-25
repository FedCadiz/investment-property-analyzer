from decimal import Decimal
from re import sub
from turtle import down
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

class Analyzer:
    def __init__(self,cityState,price,downPayment,interestRate,units,length):
        self.city = (cityState.split(","))[0]
        self.state = (cityState.split(","))[1]
        self.price = price
        self.downPayent = downPayment
        self.interestRate = interestRate
        self.units = units
        self.length = length
        self.loan = int(float(price) - (float(downPayment)*.01))
        self.homeInsurance = 0

        self.rentPrice = 1500
        self.totalmonthlyRent = self.rentPrice * int(self.units)

    def calculate(self):
        start = time.perf_counter()
        options = Options()
        options.headless = True
        PATH = "C:\Program Files (x86)\chromedriver.exe"
        driver = webdriver.Chrome(PATH,options=options)
        driver.get("https://www.rocketmortgage.com/learn/property-taxes-by-state")
        rows = driver.find_elements("tag name","tbody")
        index = -1
        for row in rows:
            columns = driver.find_elements("tag name","td")
            for column in columns:
                index += 1
                if str(column.text).lower() == str(self.state).lower():
                    self.propertyTax = (columns[index+1].text).replace("%","")
                else:
                    pass

        driver.get("https://www.calculator.net/mortgage-calculator.html")

        price = driver.find_element("id","chouseprice")
        price.clear()
        price.send_keys(self.price)

        downPayment = driver.find_element("id","cdownpayment")
        downPayment.clear()
        downPayment.send_keys(self.downPayent)

        length = driver.find_element("id","cloanterm")
        length.clear()
        length.send_keys(self.length)

        interestRate = driver.find_element("id","cinterestrate")
        interestRate.clear()
        interestRate.send_keys(self.interestRate)

        propertyTax = driver.find_element("id","cpropertytaxes")
        propertyTax.clear()
        propertyTax.send_keys(self.propertyTax)

        homeInsurance = driver.find_element("id","chomeins")
        homeInsurance.clear()
        homeInsurance.send_keys(2000)

        if self.downPayent < 20:
            pmi = driver.find_element("id","cpmi")
            pmi.clear()
            pmi.send_keys(int(self.loan*.01))
        else:
            pass

        otherCosts = driver.find_element("id","cothercost")
        otherCosts.clear()
        otherCosts.send_keys(int(.01*float(self.price)))
        otherCosts.send_keys(Keys.RETURN)

        self.monthlyPayment = driver.find_element("class name","h2result")
        self.monthlyPayment = (str(self.monthlyPayment.text).split(" ")[4])
        self.monthlyPayment = Decimal(sub(r'[^\d.]', '', self.monthlyPayment))
        print(f"Monthly Payment: {self.monthlyPayment}")

        principalBalance = driver.find_element("xpath", "//div[@id='camortizationschdis']/table/tbody/tr[2]/td[5]")
        self.principalBalance = principalBalance.text
        self.principalBalance = Decimal(sub(r'[^\d.]', '', self.principalBalance))

        self.totalRevenue = self.principalBalance + Decimal(self.totalmonthlyRent * 12)
        print(f"Total Revenue: {self.totalRevenue}")

        self.netProfit = self.totalRevenue - self.monthlyPayment

        self.totalReturn = self.netProfit / self.price
        print(f"ROI: {format(self.totalReturn,'.2%')}")

        if self.totalReturn >= .07:
            print("This rental property has a good return on investment")
        else:
            print("The return on investment is too low")


        driver.close()
        end = time.perf_counter()
        print(f"Finished in {round(end-start, 2)} seconds")





# test = Analyzer("Garden Grove,California",500000,10,5,2,30)
# test.calculate()
