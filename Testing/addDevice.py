from numpy import isnan
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time 
from signIn import signIn
from logout import logout


driver = webdriver.Edge('C:/Users/moham/OneDrive/Desktop/edgedriver_win64/msedgedriver.exe')
driver.get("http://127.0.0.1:9000/dashboard")
driver.maximize_window()

headers = ['num','equipment','code','manufacturer','model', 'sn','prod_date','supp_date','del','del','del','del','del','del','location','terms','status','qrcode']
devices = pd.read_excel('./DB.xlsx',names=headers)
devices.drop(['del','del.1','del.2','del.3','del.4','del.5'], axis = 1, inplace = True) 

contracts = ["Warranty", "Local", "Contract of Maintenance"]
maintenances = ["Calibration","Inclusive","Excl","Calibration","Excl","Inclusive","Inclusive","Inclusive"]
countries = ["Egypt","Egypt","Egypt", "France", "Germany", "Greece", "United States", "Uruguay", "India", "Japan", "China","Japan"]
images = ["1.webp","2.jpg","3.jpg","4.jpg","5.jpg","6.jpg","7.jpg","8.jpg","9.jpg","10.jpg"]
def add_device():
    for i in range(1,len(devices)):    
        sn = driver.find_element(By.NAME, "sn")
        equipment = driver.find_element(By.NAME, 'equipment')
        category = driver.find_element(By.NAME, "category")
        model = driver.find_element(By.NAME, "model")
        manufacturer = driver.find_element(By.NAME, "manufacturer")

        prod_date = driver.find_element(By.NAME, "prod-date")
        supp_date = driver.find_element(By.NAME, "supp-date")
        location = driver.find_element(By.NAME, "location")
        country = driver.find_element(By.NAME, "country")
        image = driver.find_element(By.NAME, "image")
        
        contract = driver.find_element(By.NAME, "contract-type")
        maintenance_contract_type = driver.find_element(By.NAME, 'maintenance-contract-type')
        contract_start_date = driver.find_element(By.NAME, 'contract-start-date')
        contract_end_date = driver.find_element(By.NAME, 'contract-end-date')
        inspection_list = driver.find_element(By.NAME, 'inspection-list')
        inspection_checklist = driver.find_element(By.NAME, 'inspection-checklist')

        inspection_freq = driver.find_element(By.NAME, 'inspection-freq')
        inspection_start_date = driver.find_element(By.NAME, 'inspection-start-date')
        inspection_end_date = driver.find_element(By.NAME, 'inspection-end-date')

        ppm_list = driver.find_element(By.NAME, 'ppm-list')
        ppm_checklist = driver.find_element(By.NAME, 'ppm-checklist')
        ppm_external = driver.find_element(By.NAME, 'ppm-external')
        ppm_freq = driver.find_element(By.NAME, 'ppm-freq')
        ppm_start_date = driver.find_element(By.NAME, 'ppm-start-date')
        ppm_end_date = driver.find_element(By.NAME, 'ppm-end-date')
        
        calibration_list = driver.find_element(By.NAME, 'calibration-list')
        calibration_checklist = driver.find_element(By.NAME, 'calibration-checklist')
        calibration_external = driver.find_element(By.NAME, "calibration-external")
        calibration_freq = driver.find_element(By.NAME, "calibration-freq")
        calibration_start_date = driver.find_element(By.NAME, "calibration-start-date")
        calibration_end_date = driver.find_element(By.NAME, "calibration-end-date")
        if isnan(devices['status'].get(i)):
            technical_status = driver.find_element(By.XPATH, value=f"//input[@value='{devices['status'].get(i)}']")
        PF_problem = driver.find_element(By.NAME, "PF-problem")
        NF_problem = driver.find_element(By.NAME, "NF-problem")
        trc = driver.find_element(By.XPATH, value=f"//input[@value='{(i%3)+1}']")
        
        description = driver.find_element(By.NAME, "description")
        description_file = driver.find_element(By.NAME, "description-file")
        code = driver.find_element(By.NAME, "code")
        qrcode = driver.find_element(By.NAME, "qrcode")

        # Send Keys
        sn.send_keys(f"{devices['sn'].get(i)}")
        equipment.send_keys(f"{devices['equipment'].get(i)}")
        category.send_keys("BM")
        model.send_keys(f"{devices['model'].get(i)}")
        manufacturer.send_keys(f"{devices['manufacturer'].get(i)}")
        if not isnan(devices['prod_date'].get(i)):
            prod_date.send_keys(f"01/01/{int(devices['prod_date'].get(i))}")
        if not isnan(devices['supp_date'].get(i)):
            supp_date.send_keys(f"01/01/{int(devices['supp_date'].get(i))}")
        location.send_keys(f"{devices['location'].get(i)}")
        country.send_keys(f"{countries[i%len(countries)]}")
        image.send_keys(f"C:/Users\moham/OneDrive/Desktop/MohdAhmed/College/Summer-2022/Database Project/تجربة/devices img/{images[i%10]}")
        
        contract.send_keys(f"{contracts[i%len(contracts)]}")
        if contracts[i%len(contracts)] == "Contract of Maintenance":
            maintenance_contract_type.send_keys(f"{maintenances[i%len(maintenances)]}")
        if contracts[i%len(contracts)] != "Local":
            contract_start_date.send_keys("10/6/2022")
            contract_end_date.send_keys("10/6/2024")

        # inspection_list.send_keys("")
        # inspection_checklist.send_keys("")
        inspection_freq.send_keys("6 Months")
        inspection_start_date.send_keys("10/06/2021")
        inspection_end_date.send_keys("12/06/2024")

        # ppm_list.send_keys()
        # ppm_checklist.send_keys("")
        ppm_external.send_keys("")
        ppm_freq.send_keys("6 Months")
        ppm_start_date.send_keys("10/06/2022")
        ppm_end_date.send_keys("01/12/2025")

        # calibration_list.send_keys()
        # calibration_checklist.send_keys("")
        calibration_external.send_keys("")
        calibration_freq.send_keys("Annually")
        calibration_start_date.send_keys("10/06/2022")
        calibration_end_date.send_keys("01/12/2025")
    
        if isnan(devices['status'].get(i)):
            driver.execute_script("arguments[0].click();", technical_status)
        if devices['status'].get(i) == "NF":
            NF_problem.send_keys("Equipment cannot start")
        elif devices['status'].get(i) == "PF":
            PF_problem.send_keys("Need Calibration")
        driver.execute_script("arguments[0].click();", trc)
        
        if not isnan(devices['terms'].get(i)):
            description.send_keys(f"{devices['terms'].get(i)}")
        # description_file.send_keys("")
        code.send_keys(f"{devices['qrcode'].get(i)}")

        submit_button = driver.find_element(By.XPATH, value="//input[@value='ADD DEVICE']")
        submit_button.submit()

# Sign in
signIn(driver)

driver.get("http://127.0.0.1:9000/add-device")
add_device()

# Logout
logout(driver)
    
# Quit
driver.quit()
