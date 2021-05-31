from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from steampy.guard import generate_one_time_code
import steam.webauth

from time import sleep
from sys import exit

#gun_type = ['CZ75-Auto', 'Desert Eagle', 'Dual Berettas', 'Five-SeveN', 'Glock-18', 'P2000', 'R8 Revolver', 'Tec-9', 'USP-S', 'AK-47', 'AUG', 'AWP', 'FAMAS', 'G3SG1', 'Galil AR', 'M4A1-S', 'M4A4', 'SCAR-20', 'SG 553', 'SSG 08', 'MAC-10', 'MP5-SD', 'MP7', 'MP9', 'PP-Bizon', 'P90', 'UMP-45', 'MAG-7', 'Nova', 'Sawed-Off', 'XM1014', 'M249', 'Negev']
gun_type = ['M4A4', 'M4A4']

login = ""
password = ""
shared_secret = ""

'''options = webdriver.ChromeOptions()
options.add_argument("headless")'''
driver = webdriver.Chrome(executable_path='chromedriver.exe')#, chrome_options=options)
driver.get('https://csgetto.bet/?login')
driver.find_element_by_id("steamAccountName").send_keys(login)
driver.find_element_by_id("steamPassword").send_keys(password)
driver.find_element_by_id("steamPassword").submit()
while True:
    try:
        WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.ID, "twofactorcode_entry"))).send_keys(generate_one_time_code(shared_secret))
        break
    except:
        pass
driver.find_element_by_id("twofactorcode_entry").submit()
while True:
    try:
        WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.CLASS_NAME, "modal-start-cross"))).click()
        break
    except:
        pass

while True:

    driver.get('https://csgetto.bet/exchanger#sortdef')

    while True:
        if len(driver.find_elements_by_xpath("//div[@class='items']/div[@class='item']"))>0:
            break
        else:
            sleep(1)
            if len(driver.find_elements_by_xpath("//div[@class='items']/div[@class='item']"))>0:
                break
            else:
                driver.get('https://csgetto.bet/exchanger')
                sleep(1)
                driver.get('https://csgetto.bet/exchanger#sortdef')
                sleep(3)
    while True:
        try:
            Select(driver.find_element_by_id("exSelectTradeban")).select_by_visible_text("7 дней")
            driver.find_element_by_id("exSelectName").send_keys("M4A4")
            break
        except ConnectionAbortedError:
            pass
    sleep(0.33)
    while True:
        try:
            WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.ID, "exSearchAccept"))).click()
            break
        except:
            pass
    while True:
        try:
            WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.ID, "exSearchAccept")))
            break
        except:
            pass

    balance = float(driver.find_element_by_id("pointsCount").text.replace(' ', ''))

    while True:
        try:
            WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.ID, "exSearchAccept")))
            break
        except:
            pass

    while True:
        try:
            num_of_skins = driver.find_elements_by_xpath("//div[@class='items']/div[@class='item']/div[@class='smallButton']/input")
            skin_names = []
            for elem in driver.find_elements_by_xpath("//div[@class='items']/div[@class='item']/div[@class='image']/div[@class='itemName']"):
                skin_names.append(elem.text)
            buy_buttons = driver.find_elements_by_xpath("//div[@class='items']/div[@class='item']/div[@class='smallButton']/button")
            skin_count = []
            for elem in driver.find_elements_by_xpath("//div[@class='items']/div[@class='item']/div[@class='image']/div[@class='countItems']"):
                skin_count.append(int(elem.text.replace('x', '')))
            skin_price = []
            for elem in driver.find_elements_by_xpath("//div[@class='items']/div[@class='item']/div[@class='pointPrice']"):
                skin_price.append(float(elem.text))
            break
        except:
            WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.ID, "exSearchAccept")))
            sleep(1)

    current_num_of_skins = []
    current_skin_names = []
    current_buy_buttons = []
    current_skin_count = []
    current_skin_price = []

    for i in range(len(skin_names)-1, -1, -1):
        while True:
            try:
                if skin_names[i].split(' | ')[0] in gun_type:
                    current_skin_names.append(skin_names[i])
                    current_num_of_skins.append(num_of_skins[i])
                    current_buy_buttons.append(buy_buttons[i])
                    current_skin_count.append(skin_count[i])
                    current_skin_price.append(skin_price[i])
                break
            except:
                pass
    total_count = int(balance*100)//int(current_skin_price[0]*100)
    if total_count==0:
        driver.refresh()
        while True:
            try:
                WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.ID, "exSearchAccept")))
                break
            except:
                pass
        balance = float(driver.find_element_by_id("pointsCount").text.replace(' ', ''))
        total_count = int(balance*100)//int(current_skin_price[0]*100)
        if total_count==0:
            print('У тебя закончились деньги!')
            exit(0)
    if total_count > int(float(current_skin_count[0])):
        total_count = int(float(current_skin_count[0]))
    for _ in range(total_count):
        while True:
            try:
                skin_names = []
                for elem in driver.find_elements_by_xpath("//div[@class='items']/div[@class='item']/div[@class='image']/div[@class='itemName']"):
                    skin_names.append(elem.text)
                buy_buttons = driver.find_elements_by_xpath("//div[@class='items']/div[@class='item']/div[@class='smallButton']/button")
                current_skin_names = []
                current_buy_buttons = []
                for i in range(len(skin_names)-1, -1, -1):
                    while True:
                        try:
                            if skin_names[i].split(' | ')[0] in gun_type:
                                current_skin_names.append(skin_names[i])
                                current_buy_buttons.append(buy_buttons[i])
                            break
                        except:
                            pass
                current_buy_buttons[0].click()
                sleep(0.2)
                if driver.find_element_by_xpath("//div[@id='alerts']/div[@class='alert success']").text == "ВЫ КУПИЛИ ПРЕДМЕТ":
                    break
                else:
                    sleep(0.1)
            except:
                sleep(0.1)
    sleep(0.25)
    driver.get('https://csgetto.bet/inventory')
    sum_of_stickers = []
    while True:
        try:
            labels = driver.find_elements_by_xpath("//div[@id='inventoryLocal']/div/div[@class='intentoryitems']/div/label")
            stickers_web = driver.find_elements_by_xpath("//div[@id='inventoryLocal']/div/div[@class='intentoryitems']/div/label/div[@class='stickers']")
            if len(stickers_web)>=total_count:
                break
            else:
                raise ConnectionAbortedError
        except:
            sleep(0.1)
    stickers = []
    for i in range(len(stickers_web)):
        stickers.append(stickers_web[i].find_elements_by_class_name("sticker"))
    for i in range(len(stickers)):
        if len(stickers[i])>1:
            print('===================================================')
            sum_of_current_stickers = float(0)
            for j in range(len(stickers[i])-1):
                print(stickers[i][j].get_attribute("title"))
                try:
                    sum_of_current_stickers+=float(stickers[i][j].get_attribute("title").split(' ')[-1].replace('(', '').replace('$)', ''))
                except:
                    sum_of_current_stickers+=float(0)
            sum_of_stickers.append(sum_of_current_stickers)
        else:
            sum_of_stickers.append(float(0))
    good_skin = []
    for i in range(len(sum_of_stickers)):
        if sum_of_stickers[i]>3:
            good_skin.append(1)
        else:
            good_skin.append(0)
    if sum(good_skin)>0:
        exit(0)
        i=0
        while sum(good_skin)>0:
            if good_skin[i]>0:
                labels[i].click()
                good_skin[i] = 0
            i+=1

        driver.find_element_by_id("slideSendUser").click()
        sleep(1)
        name = driver.find_element_by_id("inputProfileLink")
        name.click()
        sleep(0.5)
        name.send_keys("https://csgetto.bet/user/Un4avcIc0p9EENqx")

        driver.find_element_by_id("inventorySend").click()
    else:
        driver.get('https://csgetto.bet/exchanger')
        while True:
            try:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "exSearchAccept")))
                driver.find_element_by_xpath("//div[@idtype='sell']").click()
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "sendExchange")))
                try:
                    total_count = int(driver.find_element_by_xpath("//div[@class='items']/div[@class='item']/div[@class='image']/div[@class='countItems']").text.replace('x', ''))
                    driver.find_element_by_class_name('countItemsInput').send_keys(Keys.BACKSPACE, total_count)
                except:
                    total_count = 1  
                sleep(0.25)
                driver.find_element_by_id('sendExchange').click()
                sleep(0.25)
                if driver.find_element_by_xpath("//div[@id='alerts']/div[@class='alert success']").text == "ВЫ ПРОДАЛИ ПРЕДМЕТ":
                    driver.get('https://csgetto.bet/exchanger#sortdef')
                    break
            except:
                balance = float(driver.find_element_by_id("pointsCount").text.replace(' ', ''))
                if int(balance*100)//int(current_skin_price[0]*100)>0:
                    break
                driver.refresh()
                sleep(2)
        continue
