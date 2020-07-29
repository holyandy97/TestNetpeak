import os
from selenium import webdriver
from selenium.webdriver.support.select import Select
import time
import random
import string


class ChromeDriverTest:
    @staticmethod
    def sample_test():
        driver = webdriver.Chrome(executable_path='chromedriver.exe')
        driver.maximize_window()
        # Go to the main page of Netpeak site.
        driver.get('https://netpeak.ua/')
        driver.find_element_by_css_selector('#main-menu li.blog a').click()
        # Go to the "Work in Netpeak" page, clicking "Career" button
        driver.implicitly_wait(3)
        # Click "I want to work in Netpeak" button
        driver.find_element_by_xpath('//*[@id="header"]/div[2]/div/div/div[1]/a').click()
        # Upload file with invalid format in "Resume" block (.png in this case)
        driver.find_element_by_css_selector('input[type=file]').send_keys(os.getcwd() + '/1.png')
        time.sleep(5)

        # Verify that message about invalid format is appeared
        error_message = driver.find_element_by_xpath('//form/div[1]/div/div[1]/div[8]/div[2]/label')
        assert error_message.text == "Ошибка: неверный формат файла (разрешённые форматы: doc, docx, pdf, txt, odt, " \
                                     "rtf).", "Error: File data was not transferred or file format is correct"

        # Fill with random data "3. Personal data" block
        random_name = ''.join(random.choice(string.ascii_lowercase) for _ in range(random.randint(5, 12)))
        random_phone = ''.join(random.choice(string.digits) for _ in range(8))
        fields, data = ["name", "lastname", "hiringe", "phone"], [random_name, random_name, random_name + '@gmail.com',
                                                                 '380' + random_phone]

        for field, dat in zip(fields, data):
            driver.find_element_by_name(field).send_keys(dat)

        year = random.randint(1951, 2002)
        month = ''.join(random.sample(['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'], 1))
        day = random.randint(10, 27)

        for date, value in zip(['by', 'bm', 'bd'], [f'{year}', f'{month}', f'{day}']):
            Select(driver.find_element_by_name(date)).select_by_value(value)
        # Press "Send resume" button
        driver.find_element_by_id('submit').click()

        # Verify that "Все поля являются обязательными для заполнения" message is highlighted in red
        is_warning_message_red = driver.find_element_by_xpath('/html/body/div[2]/div/p').value_of_css_property('color')
        assert is_warning_message_red == 'rgba(255, 0, 0, 1)', 'The warning message is not red or absent'
        # Click to logo and verify that navigation to the main page is implemented
        driver.find_element_by_class_name('logo-block').click()
        time.sleep(4)
        assert driver.current_url == 'https://netpeak.ua/', 'Navigation to the main page was not implemented'

        driver.quit()


test_run = ChromeDriverTest()
test_run.sample_test()
