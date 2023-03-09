from time import sleep

from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.relative_locator import *
from selenium.webdriver.support.wait import WebDriverWait
from loguru import logger

chrome_op = Options()
chrome_op.add_experimental_option("debuggerAddress", "127.0.0.1:5003")
driver = webdriver.Chrome(options=chrome_op)

already_find_region = []


def find_region() -> list[WebElement]:
    all_unready_region: set[WebElement] = set()
    all_mask_region = driver.find_elements(By.XPATH, '//*[contains(@class,"mask")]')
    logger.info("待探索区域数：{0}", len(all_mask_region))
    for mask_region in all_mask_region:
        try:
            region = driver.find_element(locate_with(By.XPATH, '//*[contains(@class,"public")]').near(mask_region))
            all_unready_region.add(region)
        except NoSuchElementException:
            pass
    logger.info("剩余可探索区域数：{0}", len(all_unready_region))
    return list(all_unready_region)


def reset():
    reset_button = driver.find_element(By.XPATH, '//*[normalize-space(text())="重置"]')
    reset_button.click()
    try:
        WebDriverWait(driver, timeout=2).until(
            lambda d: d.find_element(By.XPATH, '//*[normalize-space(text())="确认"]'))
        driver.find_element(By.XPATH, '//button[@class="btn btn-primary btn-xs confirm-ok"]').click()
        logger.info("重置地图")
    except TimeoutException:
        pass


def wait_kill():
    try:
        time = WebDriverWait(driver, timeout=0.2).until(
            lambda d: d.find_element(By.XPATH, '//*[@id="time"]')).text
        logger.info("等待杀死怪物，预计等待时间{0}", float(time))
        sleep(float(time))
    except TimeoutException:
        pass


def kill_monster():
    monster = driver.find_element(By.XPATH, '//a[contains(@class,"monster")]')
    monster.click()
    logger.info("开始杀怪")
    try:
        wait_kill()
        back_to_map()
    except TimeoutException:
        pass


def back_to_map():
    WebDriverWait(driver, timeout=0.2).until(
        lambda d: d.find_element(By.XPATH, '//*[normalize-space(text())="战斗双方"]'))
    back_button = driver.find_element(By.XPATH, '//*[normalize-space(text())="返回"]')
    back_button.click()
    logger.info("返回地图")


def move(regions):
    if len(regions) <= 0:
        logger.info("当前地图无可搜索区域")
        reset()
        return

    for region in regions:
        region_id = region.get_attribute("id")
        if region_id not in already_find_region:
            region.click()
            logger.info("移动到未知区域")
            already_find_region.append(region_id)
        else:
            logger.info("已知区域")
            pass

        try:
            back_to_map()
            break
        except TimeoutException:
            pass


if __name__ == '__main__':
    while True:
        try:
            kill_monster()
        except NoSuchElementException:
            move(find_region())
