
from tortoises.driver import start_chrome

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, \
    ElementNotInteractableException, ElementClickInterceptedException

from selenium.webdriver import ActionChains
import time
import json


base_url = 'https://www.d4j.cn'
driver = start_chrome(headless=True)

driver.get(base_url)
time.sleep(10)


book_infos = []

for index in range(3, 5):

    navigate_elements = driver.find_elements_by_xpath('//*[@id="kratos-primary-menu"]/li')
    navigate_element = navigate_elements[index]
    navigate_name = navigate_element.find_element_by_xpath('a').text.strip()
    ActionChains(driver).move_to_element(navigate_element).perform()
    time.sleep(2)
    num_menus = len(navigate_element.find_elements_by_xpath('ul/li'))

    for num in range(num_menus):

        navigate_element = driver.find_elements_by_xpath('//*[@id="kratos-primary-menu"]/li')[index]
        ActionChains(driver).move_to_element(navigate_element).perform()
        time.sleep(5)
        menu_elements = navigate_element.find_elements_by_xpath('ul/li')
        menu_element = menu_elements[num]
        menu_name = menu_element.find_element_by_xpath('a').text.strip()
        time.sleep(10)
        try:
            menu_element.click()
        except (ElementNotInteractableException, ElementClickInterceptedException):
            print(f'skip {navigate_name}/{menu_name}')
            continue
        WebDriverWait(driver=driver, timeout=60, poll_frequency=0.5).until(
            expected_conditions.presence_of_element_located((By.XPATH, "//div")))
        current_url = driver.current_url
        time.sleep(5)

        try:
            selector = driver.find_element_by_xpath("//a[@class='extend' and @title='尾页']")
            driver.execute_script('arguments[0].click()', selector)
            WebDriverWait(driver=driver, timeout=60, poll_frequency=0.5).until(
                expected_conditions.presence_of_element_located((By.XPATH, "//div")))
            time.sleep(5)
            max_page = int(driver.current_url.split('/')[-1])
        except NoSuchElementException:
            max_page = 1

        book_info = {
            'navigate_name': navigate_name,
            'menu_name': menu_name,
            'current_url': current_url,
            'max_page': max_page
        }
        print(book_info)
        book_infos.append(book_info)


with open('demo/d4j/book_infos.json', 'w') as f:
    json.dump(book_infos, f, ensure_ascii=False)


book_lists = []

for book_info in book_infos:
    for page in range(1, book_info.get('max_page') + 1):
        url = f"{book_info.get('current_url')}/page/{page}"
        path = f"{book_info.get('navigate_name')}/{book_info.get('menu_name')}"
        book_lists.append((url, path))

with open('demo/d4j/book_lists.json', 'w') as f:
    json.dump(book_lists, f, ensure_ascii=False)
