
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException

import time
import json
import re

# import sys
# sys.path.append('/remote-home/my/Projects/pycloud')

from pycloud.netdisk import NetDisk
from multiprocessing import Process, Queue


book_lists_queue = Queue()

with open('demo/d4j/book_lists.json', 'r') as f:
    book_lists = json.load(f)

for book_list in book_lists:
    book_lists_queue.put(book_list)

share_url_pool = set()


def save_d4j(queue, url_pool):

    nd = NetDisk()
    nd.login_with_cookie()

    while True:
        if queue.empty():
            return
        else:
            url, path = queue.get()
            try:
                try:
                    nd.driver.get(url)
                    WebDriverWait(driver=nd.driver, timeout=60, poll_frequency=0.5).until(
                        expected_conditions.presence_of_element_located((By.XPATH, "//div")))
                except TimeoutException:
                    continue

                time.sleep(2)
                hrefs = [element.get_attribute('href') for element in nd.driver.find_elements_by_xpath(
                    "//article//h2[@class='kratos-entry-title-new']//a")]

                for href in hrefs:
                    try:
                        nd.driver.get(href)
                        WebDriverWait(driver=nd.driver, timeout=60, poll_frequency=0.5).until(
                            expected_conditions.presence_of_element_located((By.XPATH, "//div")))
                    except TimeoutException:
                        continue
                    time.sleep(2)
                    try:
                        extra_link = nd.driver.find_element_by_class_name('downbtn').get_attribute('href')
                    except NoSuchElementException:
                        continue

                    share_url, vc = None, None
                    if extra_link.startswith('https://pan.baidu.com'):
                        share_url = extra_link
                        try:
                            vc = re.findall(r'提取码[:：]\s+([a-zA-Z0-9]{4})', nd.driver.page_source)[0]
                        except Exception as e:
                            print(e)
                    else:
                        try:
                            nd.driver.get(extra_link)
                            WebDriverWait(driver=nd.driver, timeout=60, poll_frequency=0.5).until(
                                expected_conditions.presence_of_element_located((By.XPATH, "//div")))
                        except TimeoutException:
                            continue
                        for element in nd.driver.find_elements_by_xpath("//div[@class='plus_l']//li"):
                            if '百度网盘提取码 ：' in element.text:
                                vc = element.text.replace('百度网盘提取码 ：', '').strip()
                        share_url = nd.driver.find_element_by_xpath("//div[@class='panel-body']/span/a").get_attribute('href')

                    if share_url and vc and share_url not in url_pool:
                        print(f'百度网盘链接: {share_url}, 验证码: {vc}')
                        nd.save(url=share_url, pwd=vc, verbose=False, save_path=path)
                        share_url_pool.add(share_url)

            except Exception as e:
                print(e)


start = time.time()
num_workers = 8
processes = []

for _ in range(num_workers):
    processes.append(Process(target=save_d4j, args=(book_lists_queue, share_url_pool)))

for p in processes:
    p.start()

for p in processes:
    p.join()

end = time.time()
print(f'done. {round(end - start, 4)} seconds used.')
