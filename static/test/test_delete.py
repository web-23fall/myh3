from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import chromedriver_autoinstaller
import pytest
import inspect
import requests

chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
# and if it doesn't exist, download it automatically,
# then add chromedriver to path

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--no-gpu")
chrome_options.add_argument("--disable-setuid-sandbox")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_experimental_option("detach", True)


def login() -> webdriver.Chrome:
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://127.0.0.1:5000/login")
    driver.implicitly_wait(2)

    username = driver.find_element(by=By.ID, value="username")
    pwd = driver.find_element(by=By.ID, value="pwd")
    button = driver.find_element(by=By.ID, value="login")
    captcha_button = driver.find_element(by=By.ID, value="send-btn")

    username.send_keys("12345qwq!")
    pwd.send_keys("123abc!")
    button.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.ID, "send-btn"))
    )
    captcha_button.click()

    WebDriverWait(driver, 10).until(EC.title_is("show"))

    return driver


def get_func_name() -> str:
    function_name = inspect.currentframe().f_back.f_code.co_name
    if function_name.startswith("test_"):
        function_name = function_name[len("test_") :]
    return function_name


def query_fail(driver, name_str, stu_id_str, func: str):
    driver.get("http://127.0.0.1:5000")
    name = driver.find_element(by=By.ID, value="name")
    stu_id = driver.find_element(by=By.ID, value="id")
    submit = driver.find_element(by=By.ID, value="query")

    name.send_keys(name_str)
    stu_id.send_keys(stu_id_str)
    submit.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup2 > p"))
    )

    driver.save_screenshot(f"png/{func}_{get_func_name()}.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup2 > p")
    text = message.text

    assert text == "查询结果为空，请检查查询条件"

    table = driver.find_element(by=By.XPATH, value="//form[@id='deleteForm']/table")
    rows = table.find_elements(by=By.TAG_NAME, value="tr")

    assert len(rows) == 1


def query_suc(driver, name_str, stu_id_str, func: str):
    name = driver.find_element(by=By.ID, value="name")
    stu_id = driver.find_element(by=By.ID, value="id")
    submit = driver.find_element(by=By.ID, value="query")

    name.send_keys(name_str)
    stu_id.send_keys(stu_id_str)
    submit.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//form[@id='deleteForm']/table")
        )
    )

    driver.save_screenshot(f"png/{func}_{get_func_name()}.png")

    table = driver.find_element(by=By.XPATH, value="//form[@id='deleteForm']/table")
    rows = table.find_elements(by=By.TAG_NAME, value="tr")

    assert len(rows) == 2
    assert (
        driver.find_element(
            by=By.XPATH, value="//form[@id='deleteForm']/table/tbody/tr[2]/td[2]"
        ).text
        == stu_id_str
    )
    assert (
        driver.find_element(
            by=By.XPATH, value="//form[@id='deleteForm']/table/tbody/tr[2]/td[3]"
        ).text
        == name_str
    )


# 注意并发问题，强行取不同的数据
@pytest.mark.delete
def test_del_fail_0():
    driver = login()
    driver.get("http://127.0.0.1:5000")

    stu_id = driver.find_element(
        by=By.XPATH, value='//*[@id="deleteForm"]/table/tbody/tr[3]/td[2]'
    ).text
    name = driver.find_element(
        by=By.XPATH, value='//*[@id="deleteForm"]/table/tbody/tr[3]/td[3]'
    ).text

    driver.save_screenshot(f"png/{get_func_name()}.png")

    query_suc(driver, name, stu_id, get_func_name())

    driver.quit()


@pytest.mark.delete
def test_del_success_1():
    driver = login()
    driver.get("http://127.0.0.1:5000")

    stu_id = driver.find_element(
        by=By.XPATH, value='//*[@id="deleteForm"]/table/tbody/tr[2]/td[2]'
    ).text
    name = driver.find_element(
        by=By.XPATH, value='//*[@id="deleteForm"]/table/tbody/tr[2]/td[3]'
    ).text

    delete = driver.find_element(
        by=By.XPATH, value='//form[@id="deleteForm"]/table/tbody/tr[2]/td[9]/a'
    )
    delete.click()

    driver.save_screenshot(f"png/{get_func_name()}.png")

    query_fail(driver, name, stu_id, get_func_name())

    driver.quit()


@pytest.mark.delete
def test_del_success_link():
    driver = login()
    driver.get("http://127.0.0.1:5000")

    stu_id = driver.find_element(
        by=By.XPATH, value='//*[@id="deleteForm"]/table/tbody/tr[4]/td[2]'
    ).text
    name = driver.find_element(
        by=By.XPATH, value='//*[@id="deleteForm"]/table/tbody/tr[4]/td[3]'
    ).text

    driver.get(f"http://127.0.0.1:5000/delete/{stu_id}")

    driver.save_screenshot(f"png/{get_func_name()}.png")

    query_fail(driver, name, stu_id, get_func_name())

    driver.quit()


@pytest.mark.delete
def test_del_fail_link_non():
    driver = login()
    driver.get("http://127.0.0.1:5000/delete/11451")

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup2 > p"))
    )

    driver.save_screenshot(f"png/{get_func_name()}.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup2 > p")
    text = message.text

    assert text == "无效的学号，请检查"

    driver.quit()


@pytest.mark.delete
def test_del_fail_link_sql():
    driver = login()
    driver.get("http://127.0.0.1:5000/delete/abcd' or 1=1;--")

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".btn"))
    )

    driver.save_screenshot(f"png/{get_func_name()}.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value="p")
    text = message.text

    assert text == "你来到了没有内容的荒原，点击下方的“确定”返回主页。"

    response = requests.get("http://127.0.0.1:5000/delete/abcd' or 1=1;--")

    assert response.status_code == 404

    driver.quit()


@pytest.mark.delete
def test_del_fail_link_wrong_format():
    driver = login()
    driver.get("http://127.0.0.1:5000/delete/abcd")

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".btn"))
    )

    driver.save_screenshot(f"png/{get_func_name()}.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value="p")
    text = message.text

    assert text == "你来到了没有内容的荒原，点击下方的“确定”返回主页。"

    response = requests.get("http://127.0.0.1:5000/delete/abcd")

    assert response.status_code == 404

    driver.quit()
