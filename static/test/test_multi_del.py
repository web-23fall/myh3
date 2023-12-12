from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import chromedriver_autoinstaller
import pytest
import inspect
import random

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
    captcha = driver.find_element(by=By.NAME, value="code")
    captcha.send_keys("AUTO")
    captcha_button.click()

    WebDriverWait(driver, 10).until(EC.title_is("show"))

    return driver


def get_func_name() -> str:
    function_name = inspect.currentframe().f_back.f_code.co_name
    if function_name.startswith("test_"):
        function_name = function_name[len("test_") :]
    return function_name


def query_fail(driver, stu_id_str, name_str, func: str):
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


@pytest.mark.multi_del
def test_multi_del_fail_0nn():
    driver = login()
    driver.get("http://127.0.0.1:5000")

    deleteButton = driver.find_element(by=By.CSS_SELECTOR, value="#deleteForm > button")
    checkbox_elements = driver.find_elements(
        by=By.CSS_SELECTOR, value="input[type=checkbox]"
    )
    for checkbox in checkbox_elements:
        if checkbox.is_selected():
            checkbox.click()

    selected = 0
    for checkbox in checkbox_elements:
        if checkbox.is_selected():
            selected += 1

    driver.save_screenshot(f"png/{get_func_name()}.png")

    assert selected == 0


@pytest.mark.multi_del
def test_multi_del_fail_1nn():
    driver = login()
    driver.get("http://127.0.0.1:5000")

    deleteButton = driver.find_element(by=By.CSS_SELECTOR, value="#deleteForm > button")
    checkbox_elements = driver.find_elements(
        by=By.CSS_SELECTOR, value="input[type=checkbox]"
    )
    for checkbox in checkbox_elements:
        if checkbox.is_selected():
            checkbox.click()
    checkbox_elements[0].click()

    selected = 0
    for checkbox in checkbox_elements:
        if checkbox.is_selected():
            selected += 1

    driver.save_screenshot(f"png/{get_func_name()}.png")

    assert selected == 1


@pytest.mark.multi_del
def test_multi_del_fail_20nn():
    driver = login()
    driver.get("http://127.0.0.1:5000")

    deleteButton = driver.find_element(by=By.CSS_SELECTOR, value="#deleteForm > button")
    checkbox_elements = driver.find_elements(
        by=By.CSS_SELECTOR, value="input[type=checkbox]"
    )
    for checkbox in checkbox_elements:
        if not checkbox.is_selected():
            checkbox.click()

    selected = 0
    for checkbox in checkbox_elements:
        if checkbox.is_selected():
            selected += 1

    driver.save_screenshot(f"png/{get_func_name()}.png")

    assert selected == len(checkbox_elements)


@pytest.mark.multi_del
def test_multi_del_fail_20yy():
    # 页面重新加载后所有元素需要重新 find
    driver = login()
    driver.get("http://127.0.0.1:5000")

    checkbox_elements = driver.find_elements(
        by=By.CSS_SELECTOR, value="input[type=checkbox]"
    )
    for checkbox in checkbox_elements:
        if not checkbox.is_selected():
            checkbox.click()

    nextPage = driver.find_element(by=By.ID, value="nextpage")
    nextPage.click()

    deleteButton = driver.find_element(by=By.ID, value="multi_del")
    deleteButton.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )
    driver.save_screenshot(f"png/{get_func_name()}.png")
    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    checkbox_elements = driver.find_elements(
        by=By.CSS_SELECTOR, value="input[type=checkbox]"
    )
    selected = 0
    for checkbox in checkbox_elements:
        if checkbox.is_selected():
            selected += 1

    assert text == "请至少选中一项，否则无法删除" and selected == 0


@pytest.mark.multi_del
def test_multi_del_fail_1yn():
    driver = login()
    driver.get("http://127.0.0.1:5000")

    checkbox_elements = driver.find_elements(
        by=By.CSS_SELECTOR, value="input[type=checkbox]"
    )
    for checkbox in checkbox_elements:
        if checkbox.is_selected():
            checkbox.click()
    checkbox_elements[0].click()

    nextPage = driver.find_element(by=By.ID, value="nextpage")
    nextPage.click()

    driver.save_screenshot(f"png/{get_func_name()}.png")

    checkbox_elements = driver.find_elements(
        by=By.CSS_SELECTOR, value="input[type=checkbox]"
    )
    selected = 0
    for checkbox in checkbox_elements:
        if checkbox.is_selected():
            selected += 1

    assert selected == 0


@pytest.mark.multi_del
def test_multi_del_fail_0ny():
    driver = login()
    driver.get("http://127.0.0.1:5000")

    checkbox_elements = driver.find_elements(
        by=By.CSS_SELECTOR, value="input[type=checkbox]"
    )
    for checkbox in checkbox_elements:
        if checkbox.is_selected():
            checkbox.click()

    deleteButton = driver.find_element(by=By.ID, value="multi_del")
    deleteButton.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )
    driver.save_screenshot(f"png/{get_func_name()}.png")
    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text == "请至少选中一项，否则无法删除"


@pytest.mark.multi_del
def test_multi_del_success_1ny():
    driver = login()
    driver.get("http://127.0.0.1:5000")

    checkbox_elements = driver.find_elements(
        by=By.CSS_SELECTOR, value="input[type=checkbox]"
    )
    for checkbox in checkbox_elements:
        if checkbox.is_selected():
            checkbox.click()
    checkbox_elements[0].click()

    stu_id = driver.find_element(
        by=By.XPATH, value='//*[@id="deleteForm"]/table/tbody/tr[2]/td[2]'
    ).text
    name = driver.find_element(
        by=By.XPATH, value='//*[@id="deleteForm"]/table/tbody/tr[2]/td[3]'
    ).text

    deleteButton = driver.find_element(by=By.ID, value="multi_del")
    deleteButton.click()

    driver.save_screenshot(f"png/{get_func_name()}.png")

    query_fail(driver, stu_id, name, get_func_name())

    driver.quit()


@pytest.mark.multi_del
def test_multi_del_success_20ny():
    driver = login()
    driver.get("http://127.0.0.1:5000")

    checkbox_elements = driver.find_elements(
        by=By.CSS_SELECTOR, value="input[type=checkbox]"
    )
    for checkbox in checkbox_elements:
        if not checkbox.is_selected():
            checkbox.click()

    stu_id = []
    name = []
    for i in range(2, len(checkbox_elements) + 2):
        stu_id.append(
            driver.find_element(
                by=By.XPATH, value=f'//*[@id="deleteForm"]/table/tbody/tr[{i}]/td[2]'
            ).text
        )
        name.append(
            driver.find_element(
                by=By.XPATH, value=f'//*[@id="deleteForm"]/table/tbody/tr[{i}]/td[3]'
            ).text
        )

    deleteButton = driver.find_element(by=By.ID, value="multi_del")
    deleteButton.click()

    driver.save_screenshot(f"png/{get_func_name()}.png")

    for i in range(len(stu_id)):
        query_fail(driver, stu_id[i], name[i], get_func_name())

    driver.quit()


@pytest.mark.multi_del
def test_multi_del_fail_0yn():
    driver = login()
    driver.get("http://127.0.0.1:5000")

    checkbox_elements = driver.find_elements(
        by=By.CSS_SELECTOR, value="input[type=checkbox]"
    )
    for checkbox in checkbox_elements:
        if checkbox.is_selected():
            checkbox.click()

    nextPage = driver.find_element(by=By.ID, value="nextpage")
    nextPage.click()

    driver.save_screenshot(f"png/{get_func_name()}.png")

    checkbox_elements = driver.find_elements(
        by=By.CSS_SELECTOR, value="input[type=checkbox]"
    )
    selected = 0
    for checkbox in checkbox_elements:
        if checkbox.is_selected():
            selected += 1

    assert selected == 0


@pytest.mark.multi_del
def test_multi_del_fail_0yy():
    # 页面重新加载后所有元素需要重新 find
    driver = login()
    driver.get("http://127.0.0.1:5000")

    checkbox_elements = driver.find_elements(
        by=By.CSS_SELECTOR, value="input[type=checkbox]"
    )
    for checkbox in checkbox_elements:
        if checkbox.is_selected():
            checkbox.click()

    nextPage = driver.find_element(by=By.ID, value="nextpage")
    nextPage.click()

    deleteButton = driver.find_element(by=By.ID, value="multi_del")
    deleteButton.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )
    driver.save_screenshot(f"png/{get_func_name()}.png")
    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    checkbox_elements = driver.find_elements(
        by=By.CSS_SELECTOR, value="input[type=checkbox]"
    )
    selected = 0
    for checkbox in checkbox_elements:
        if checkbox.is_selected():
            selected += 1

    assert text == "请至少选中一项，否则无法删除" and selected == 0


@pytest.mark.multi_del
def test_multi_del_fail_1yy():
    # 页面重新加载后所有元素需要重新 find
    driver = login()
    driver.get("http://127.0.0.1:5000")

    checkbox_elements = driver.find_elements(
        by=By.CSS_SELECTOR, value="input[type=checkbox]"
    )
    for checkbox in checkbox_elements:
        if checkbox.is_selected():
            checkbox.click()
    checkbox_elements[0].click()

    nextPage = driver.find_element(by=By.ID, value="nextpage")
    nextPage.click()

    deleteButton = driver.find_element(by=By.ID, value="multi_del")
    deleteButton.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )
    driver.save_screenshot(f"png/{get_func_name()}.png")
    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    checkbox_elements = driver.find_elements(
        by=By.CSS_SELECTOR, value="input[type=checkbox]"
    )
    selected = 0
    for checkbox in checkbox_elements:
        if checkbox.is_selected():
            selected += 1

    assert text == "请至少选中一项，否则无法删除" and selected == 0


@pytest.mark.multi_del
def test_multi_del_fail_20yn():
    driver = login()
    driver.get("http://127.0.0.1:5000")

    checkbox_elements = driver.find_elements(
        by=By.CSS_SELECTOR, value="input[type=checkbox]"
    )
    for checkbox in checkbox_elements:
        if not checkbox.is_selected():
            checkbox.click()

    nextPage = driver.find_element(by=By.ID, value="nextpage")
    nextPage.click()

    driver.save_screenshot(f"png/{get_func_name()}.png")

    checkbox_elements = driver.find_elements(
        by=By.CSS_SELECTOR, value="input[type=checkbox]"
    )
    selected = 0
    for checkbox in checkbox_elements:
        if checkbox.is_selected():
            selected += 1

    assert selected == 0


@pytest.mark.multi_del
def test_multi_del_success_random_ny():
    driver = login()
    driver.get("http://127.0.0.1:5000")

    checkbox_elements = driver.find_elements(
        by=By.CSS_SELECTOR, value="input[type=checkbox]"
    )

    stu_id = []
    name = []
    i = 2

    for checkbox in checkbox_elements:
        if not checkbox.is_selected() and random.randint(0, 1) == 1:
            checkbox.click()
            stu_id.append(
                driver.find_element(
                    by=By.XPATH,
                    value=f'//*[@id="deleteForm"]/table/tbody/tr[{i}]/td[2]',
                ).text
            )
            name.append(
                driver.find_element(
                    by=By.XPATH,
                    value=f'//*[@id="deleteForm"]/table/tbody/tr[{i}]/td[3]',
                ).text
            )
        i += 1

    deleteButton = driver.find_element(by=By.ID, value="multi_del")
    deleteButton.click()

    driver.save_screenshot(f"png/{get_func_name()}.png")

    for i in range(len(stu_id)):
        query_fail(driver, stu_id[i], name[i], get_func_name())

    driver.quit()
