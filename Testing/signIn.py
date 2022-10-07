from selenium.webdriver.common.by import By


def signIn(driver):
        username = driver.find_element(By.ID, "username")
        password = driver.find_element(By.ID, "password")
        username.send_keys("Admin")
        password.send_keys("Admin")
        sign_button = driver.find_element(By.XPATH, value="//input[@value='SIGN IN']")
        sign_button.click()


