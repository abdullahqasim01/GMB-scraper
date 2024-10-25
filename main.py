import time
import pyap
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def google_scraper(niche, location):
    driver  = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://www.google.com/maps/search/?hl=en_US")

    driver.implicitly_wait(2)
    try:
        driver.find_element(By.XPATH, '//span[@class="VfPpkd-vQzf8d" and contains(text(), "Accept all")]').click()
    except:
        pass

    search = driver.find_element(By.XPATH, '//input[@id="searchboxinput"]')
    search.send_keys(f"{niche} in {location}")
    search.send_keys(Keys.RETURN)

    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="m6QErb DxyBCb kA9KIf dS8AEf ecceSd"]')))
    side_bar = driver.find_element(By.XPATH, '//div[@class="m6QErb DxyBCb kA9KIf dS8AEf ecceSd"]')
    
    exit_flag = True
    names = []

    while exit_flag:
        driver.implicitly_wait(3)
        side_bar.send_keys(Keys.END)

        try:
            if side_bar.find_element(By.XPATH, '//span[@class="HlvSq"]') != "None":
                exit_flag = False
        except:
            pass

    cards  = driver.find_elements(By.XPATH, '//a[@class="hfpxzc"]')
    
    for i in cards:
        driver.execute_script("link = arguments[0];", i)
        driver.execute_script("link.scrollIntoView();")
        driver.execute_script("link.click();")
        try:
            wait = WebDriverWait(driver, 20)
            wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="bJzME Hu9e2e tTVLSc"]')))
            details_card = driver.find_element(By.XPATH, '//div[@class="bJzME Hu9e2e tTVLSc"]')
        except:
            driver.execute_script("link.click();")
            wait = WebDriverWait(driver, 20)
            wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="bJzME Hu9e2e tTVLSc"]')))
            details_card = driver.find_element(By.XPATH, '//div[@class="bJzME Hu9e2e tTVLSc"]')


        time.sleep(3)

        name = details_card.find_element(By.XPATH, '//h1[@class="DUwDvf lfPIob"]').text

        try:
            web = details_card.find_element(By.XPATH, '//div[@class="rogA2c ITvuef"]/div').text
        except:
            web = "NOT AVAILABLE"

        try:
            number = details_card.find_element(By.XPATH, '//button[@data-tooltip="Copy phone number"]/div/div/div[@class="Io6YTe fontBodyMedium kR99db "]').text 
        except:
            number = "NOT AVAILABLE"

        try:
            address = details_card.find_element(By.XPATH, '//button[@data-tooltip="Copy address"]/div/div/div[@class="Io6YTe fontBodyMedium kR99db "]').text 
        except:
            address = "NOT AVAILABLE"

        street, city, state, zip_code = "", "", "", ""

        if address != "NOT AVAILABLE":
            addresses = pyap.parse(address, country='US')
            for address in addresses:
                a = address.as_dict()
                street = a['full_street']
                city = a['city']
                state = a['region1']
                zip_code = a['postal_code']
        else:
            street = "NOT AVAILABLE"
            city = "NOT AVAILABLE"
            state = "NOT AVAILABLE"
            zip_code = "NOT AVAILABLE"
            

        scrape_url = driver.current_url
        names.append({"name": name,
                        "niche": niche,
                        "web": web,
                        "number": number,
                        "address": address,
                        "street": street,
                        "city": city,
                        "state": state,
                        "zip_code": zip_code,
                        "scrape_url": scrape_url})


    df = pd.DataFrame(names)
    df.set_index("name", inplace=True)
    df.to_csv(f"{niche}_{location}.csv")
    driver.quit()

if __name__ == "__main__":
    niches = []
    locations = []

    with open("niches.txt", "r") as f:
        niches = f.read().splitlines()

    with open("zip_codes.txt", "r") as f:
        locations = f.read().splitlines()
    
    for loc in locations:
        for niche in niches:

                google_scraper(niche, loc)
