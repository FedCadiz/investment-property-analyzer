from decimal import Decimal
from re import sub
from unicodedata import decimal
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import chromedriver_autoinstaller as chromedriver
chromedriver.install()

class Analyzer:
    def __init__(self,cityState,price,downPayment,interestRate,units,length,rent):
        if ", " in cityState:
            self.city = (cityState.split(", "))[0]
            self.state = (cityState.split(", "))[1]
        elif "," in cityState:
            self.city = (cityState.split(","))[0]
            self.state = (cityState.split(","))[1]
        self.price = price
        self.downPayment = downPayment
        self.interestRate = interestRate
        self.units = units
        self.length = length
        self.loan = int(float(price) - (float(downPayment)*.01))
        

        self.rentPrice = rent
        self.totalmonthlyRent = self.rentPrice * int(self.units)

    def calculate(self):
        start = time.perf_counter()
        options = Options()
        options.headless = True
        chromedriver.install()
        driver = webdriver.Chrome(options=options)
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
        downPayment.send_keys(self.downPayment)

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

        if self.downPayment < 20:
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

        self.netProfit = self.totalRevenue - (self.monthlyPayment*12)

        self.roi = self.netProfit / Decimal((self.downPayment * .01) * self.price)
        print(Decimal((self.downPayment * .01) * self.price))
        print(f"ROI: {format(self.roi,'.2%')}")

        if self.roi >= .07:
            print("This rental property has a good return on investment")
        else:
            print("The return on investment is too low")

        self.monthlyPayment = "${:0,.2f}".format(self.monthlyPayment)
        self.totalRevenue = "${:0,.2f}".format(self.totalRevenue)
        self.price = "${:0,.2f}".format(self.price)
        self.netProfit = "${:0,.2f}".format(self.netProfit)
        print(self.netProfit)

        driver.close()
        end = time.perf_counter()
        print(f"Finished in {round(end-start, 2)} seconds")





# test = Analyzer("Garden Grove,California",500000,20,7,3,30)
# test.calculate()
