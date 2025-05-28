from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


edge_options = Options()
edge_options.add_experimental_option('excludeSwitches',['enable-logging']) #needed to remove extra debugging from displaying to the console
driver = webdriver.Edge(options=edge_options)
driver.set_page_load_timeout(30)

Color_Percent = []
BizhubList = {"Put Bizhub Url Here" : "Put Printer Name Here", "etc." : "etc."} #Is a key:value pair. Include all printers here 


def Color_P(Printer_Name,color,name): #Checks if printer level is low and adds it to a list
    Percent_Low = ["10","9","8","7","6","5","4","3","2","1","0"]
    for percent in Percent_Low:
        if color == f"{percent}" + "%":
            Color_Percent.append(Printer_Name + ": " + name + " " + percent + "%")

def Bizhub_Percent(Url,Printer_Name): #Traverses through bizhub portal and finds the toner percentage
    wait = WebDriverWait(driver, 5)
    try:                              
        driver.get(Url)
        wait.until(ec.element_to_be_clickable((By.XPATH,'//*[@id="ID_Menu_System"]'))).click()
        time.sleep(.5)
        wait.until(ec.element_to_be_clickable((By.XPATH,'//*[@id="ID_SubMenu_System_DeviceInfo"]'))).click()
        time.sleep(.5)
        wait.until(ec.element_to_be_clickable((By.XPATH,'//*[@id="ID_SpareSubMenu_System_Consumables"]'))).click()
        Iframe = wait.until(ec.visibility_of_element_located((By.XPATH,'//*[@id="SPA-contents-body"]')))
        driver.switch_to.frame(Iframe) #Needed to move to the Iframe within the bizhub portal
        Yellow = wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="CSM_DETAILLIST1"]/div/div/table/tbody/tr[2]/td[2]/div[2]'))).text
        Magenta = wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="CSM_DETAILLIST1"]/div/div/table/tbody/tr[3]/td[2]/div[2]'))).text
        Cyan = wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="CSM_DETAILLIST1"]/div/div/table/tbody/tr[4]/td[2]/div[2]'))).text
        Black = wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="CSM_DETAILLIST1"]/div/div/table/tbody/tr[5]/td[2]/div[2]'))).text
        Color_P(Printer_Name,Yellow,"Yellow")
        Color_P(Printer_Name,Magenta,"Magenta")
        Color_P(Printer_Name,Cyan,"Cyan")
        Color_P(Printer_Name,Black,"Black")
        print(Printer_Name)
        print("Yellow  " + Yellow)
        print("Magenta  " + Magenta)
        print("Cyan  " + Cyan)
        print("Black  " + Black + "\n")
        return True
    except TimeoutException or NoSuchElementException:  # This one handles that dumb "omg the site is unsafe!! Thank you edge for saving me" page
        try:
            advanced_button = driver.find_element(By.XPATH, '//*[@id="details-button"]')
            advanced_button.click()
            proceed_link = driver.find_element(By.XPATH, '//*[@id="proceed-link"]')
            proceed_link.click()
            time.sleep(1)
            wait.until(ec.element_to_be_clickable((By.XPATH,'//*[@id="ID_Menu_System"]'))).click()
            time.sleep(.5)
            wait.until(ec.element_to_be_clickable((By.XPATH,'//*[@id="ID_SubMenu_System_DeviceInfo"]'))).click()
            time.sleep(.5)
            wait.until(ec.element_to_be_clickable((By.XPATH,'//*[@id="ID_SpareSubMenu_System_Consumables"]'))).click()
            Iframe = wait.until(ec.visibility_of_element_located((By.XPATH,'//*[@id="SPA-contents-body"]')))
            driver.switch_to.frame(Iframe)
            Yellow = wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="CSM_DETAILLIST1"]/div/div/table/tbody/tr[2]/td[2]/div[2]'))).text
            Magenta = wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="CSM_DETAILLIST1"]/div/div/table/tbody/tr[3]/td[2]/div[2]'))).text
            Cyan = wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="CSM_DETAILLIST1"]/div/div/table/tbody/tr[4]/td[2]/div[2]'))).text
            Black = wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="CSM_DETAILLIST1"]/div/div/table/tbody/tr[5]/td[2]/div[2]'))).text
            Color_P(Printer_Name,Yellow,"Yellow")
            Color_P(Printer_Name,Magenta,"Magenta")
            Color_P(Printer_Name,Cyan,"Cyan")
            Color_P(Printer_Name,Black,"Black")
            print(Printer_Name)
            print("Yellow  " + Yellow)
            print("Magenta  " + Magenta)
            print("Cyan  " + Cyan)
            print("Black  " + Black + "\n")
            if NoSuchElementException:
                pass
        except TimeoutException or NoSuchElementException:
            print("timeout")


def ProgramWait():
    UserInput = 0
    while (UserInput == 0):
        UserInput = input("Press enter to exit ")

def Biz_Run():
    
    for Url,PrinterName in BizhubList.items():
        Bizhub_Percent(Url,PrinterName)
        
    if Color_Percent == []:
        print("No low toner")
    else:
        print(Color_Percent)
    ProgramWait()
    quit()


if __name__ == "__main__":
    Biz_Run()
