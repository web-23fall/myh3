from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
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
    captcha_button.click()

    WebDriverWait(driver, 10).until(EC.title_is("show"))

    return driver


def get_func_name() -> str:
    function_name = inspect.currentframe().f_back.f_code.co_name
    if function_name.startswith("test_"):
        function_name = function_name[len("test_") :]
    return function_name


def query_suc(driver, stu_id_str, name_str, age: str, func: str):
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
    assert (
        driver.find_element(
            by=By.XPATH, value="//form[@id='deleteForm']/table/tbody/tr[5]/td[3]"
        ).text
        == age
    )


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


def get_ids(length: int, num: int) -> list:
    ids = [i for i in range(length)]
    random.shuffle(ids)
    return ids[:num]


def xyny(num: int, func: str):
    driver = login()
    driver.get("http://127.0.0.1:5000/updateAge")

    age = driver.find_element(by=By.ID, value="age")

    checkbox_elements = driver.find_elements(
        by=By.CSS_SELECTOR, value="input[type='checkbox']"
    )

    ids = get_ids(len(checkbox_elements), num)
    i = 0

    for checkbox in checkbox_elements:
        if checkbox.is_selected():
            checkbox.click()
        if i in ids:
            checkbox.click()
        i += 1

    nextpage = driver.find_element(by=By.ID, value="nextpage")
    nextpage.click()

    submit = driver.find_element(by=By.CSS_SELECTOR, value="#updateAge > button")
    submit.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    checkbox_elements = driver.find_elements(
        by=By.CSS_SELECTOR, value="input[type='checkbox']"
    )

    selected = 0
    for checkbox in checkbox_elements:
        if checkbox.is_selected():
            selected += 1

    driver.save_screenshot(f"png/{func}.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert selected == 0 and text == "请至少选中一项，否则无法修改"
    driver.quit()


def xynn(num: int, func: str):
    driver = login()
    driver.get("http://127.0.0.1:5000/updateAge")

    age = driver.find_element(by=By.ID, value="age")

    checkbox_elements = driver.find_elements(
        by=By.CSS_SELECTOR, value="input[type='checkbox']"
    )

    ids = get_ids(len(checkbox_elements), num)
    i = 0

    for checkbox in checkbox_elements:
        if checkbox.is_selected():
            checkbox.click()
        if i in ids:
            checkbox.click()
        i += 1

    nextpage = driver.find_element(by=By.ID, value="nextpage")
    nextpage.click()

    checkbox_elements = driver.find_elements(
        by=By.CSS_SELECTOR, value="input[type='checkbox']"
    )

    selected = 0
    for checkbox in checkbox_elements:
        if checkbox.is_selected():
            selected += 1

    driver.save_screenshot(f"png/{func}.png")

    assert selected == 0
    driver.quit()


def xyyy(num: int, func: str):
    driver = login()
    driver.get("http://127.0.0.1:5000/updateAge")

    age = driver.find_element(by=By.ID, value="age")
    age.send_keys("24")

    checkbox_elements = driver.find_elements(
        by=By.CSS_SELECTOR, value="input[type='checkbox']"
    )

    ids = get_ids(len(checkbox_elements), num)
    i = 0

    for checkbox in checkbox_elements:
        if checkbox.is_selected():
            checkbox.click()
        if i in ids:
            checkbox.click()
        i += 1

    nextpage = driver.find_element(by=By.ID, value="nextpage")
    nextpage.click()

    submit = driver.find_element(by=By.CSS_SELECTOR, value="#updateAge > button")
    submit.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    checkbox_elements = driver.find_elements(
        by=By.CSS_SELECTOR, value="input[type='checkbox']"
    )

    selected = 0
    for checkbox in checkbox_elements:
        if checkbox.is_selected():
            selected += 1

    driver.save_screenshot(f"png/{func}.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert selected == 0 and text == "请至少选中一项，否则无法修改"
    driver.quit()


def xyyn(num: int, func: str):
    driver = login()
    driver.get("http://127.0.0.1:5000/updateAge")

    age = driver.find_element(by=By.ID, value="age")
    age.send_keys("24")

    checkbox_elements = driver.find_elements(
        by=By.CSS_SELECTOR, value="input[type='checkbox']"
    )

    ids = get_ids(len(checkbox_elements), num)
    i = 0

    for checkbox in checkbox_elements:
        if checkbox.is_selected():
            checkbox.click()
        if i in ids:
            checkbox.click()
        i += 1

    nextpage = driver.find_element(by=By.ID, value="nextpage")
    nextpage.click()

    checkbox_elements = driver.find_elements(
        by=By.CSS_SELECTOR, value="input[type='checkbox']"
    )

    selected = 0
    for checkbox in checkbox_elements:
        if checkbox.is_selected():
            selected += 1

    driver.save_screenshot(f"png/{func}.png")

    assert selected == 0
    driver.quit()


def xnny(num: int, func: str):
    driver = login()
    driver.get("http://127.0.0.1:5000/updateAge")

    age = driver.find_element(by=By.ID, value="age")

    checkbox_elements = driver.find_elements(
        by=By.CSS_SELECTOR, value="input[type='checkbox']"
    )

    ids = get_ids(len(checkbox_elements), num)
    i = 0

    for checkbox in checkbox_elements:
        if checkbox.is_selected():
            checkbox.click()
        if i in ids:
            checkbox.click()
        i += 1

    submit = driver.find_element(by=By.CSS_SELECTOR, value="#updateAge > button")
    submit.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    checkbox_elements = driver.find_elements(
        by=By.CSS_SELECTOR, value="input[type='checkbox']"
    )

    selected = 0
    for checkbox in checkbox_elements:
        if checkbox.is_selected():
            selected += 1

    driver.save_screenshot(f"png/{func}.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert selected == num
    if num == 0:
        assert text == "请至少选中一项，否则无法修改"
    else:
        assert text.startswith("年龄不合法")
    driver.quit()


def xnnn(num: int, func: str):
    driver = login()
    driver.get("http://127.0.0.1:5000/updateAge")

    age = driver.find_element(by=By.ID, value="age")

    checkbox_elements = driver.find_elements(
        by=By.CSS_SELECTOR, value="input[type='checkbox']"
    )

    ids = get_ids(len(checkbox_elements), num)
    i = 0

    for checkbox in checkbox_elements:
        if checkbox.is_selected():
            checkbox.click()
        if i in ids:
            checkbox.click()
        i += 1

    checkbox_elements = driver.find_elements(
        by=By.CSS_SELECTOR, value="input[type='checkbox']"
    )

    selected = 0
    for checkbox in checkbox_elements:
        if checkbox.is_selected():
            selected += 1

    driver.save_screenshot(f"png/{func}.png")

    assert selected == num
    driver.quit()


def xnyy(num: int, func: str):
    driver = login()
    driver.get("http://127.0.0.1:5000/updateAge")

    age = driver.find_element(by=By.ID, value="age")
    age.send_keys("24")

    checkbox_elements = driver.find_elements(
        by=By.CSS_SELECTOR, value="input[type='checkbox']"
    )

    ids = get_ids(len(checkbox_elements), num)
    name = []
    stu_id = []
    i = 0

    driver.save_screenshot(f"png/{func}_1.png")

    for checkbox in checkbox_elements:
        if i in ids:
            # TODO: ?
            stu_id.append(
                driver.find_element(
                    by=By.CSS_SELECTOR,
                    value=f'tr:nth-child({i}) > td:nth-child(2)',
                ).text
            )
            name.append(
                driver.find_element(
                    by=By.CSS_SELECTOR,
                    value=f'tr:nth-child({i}) > td:nth-child(3)',
                ).text
            )
            checkbox.click()
        i += 1

    submit = driver.find_element(by=By.CSS_SELECTOR, value="#updateAge > button")
    submit.click()

    if num == 0:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
        )
        checkbox_elements = driver.find_elements(
            by=By.CSS_SELECTOR, value="input[type='checkbox']"
        )

        selected = 0
        for checkbox in checkbox_elements:
            if checkbox.is_selected():
                selected += 1

        driver.save_screenshot(f"png/{func}.png")

        message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
        text = message.text

        assert selected == 0 and text == "请至少选中一项，否则无法修改"
    else:
        WebDriverWait(driver, 10).until(EC.title_is("show"))
        driver.save_screenshot(f"png/{func}.png")
        for i in range(len(stu_id)):
            query_suc(driver, stu_id[i], name[i], "24", func)

    driver.quit()


@pytest.mark.multi_upd_age
def test_multi_upd_age_fail_0yny():
    xyny(0, get_func_name())


@pytest.mark.multi_upd_age
def test_multi_upd_age_fail_1yny():
    xyny(1, get_func_name())


@pytest.mark.multi_upd_age
def test_multi_upd_age_fail_20yny():
    xyny(20, get_func_name())


@pytest.mark.multi_upd_age
def test_multi_upd_age_fail_0ynn():
    xynn(0, get_func_name())


@pytest.mark.multi_upd_age
def test_multi_upd_age_fail_1ynn():
    xynn(1, get_func_name())


@pytest.mark.multi_upd_age
def test_multi_upd_age_fail_20ynn():
    xynn(20, get_func_name())


@pytest.mark.multi_upd_age
def test_multi_upd_age_fail_0yyy():
    xyyy(0, get_func_name())


@pytest.mark.multi_upd_age
def test_multi_upd_age_fail_1yyy():
    xyyy(1, get_func_name())


@pytest.mark.multi_upd_age
def test_multi_upd_age_fail_20yyy():
    xyyy(20, get_func_name())


@pytest.mark.multi_upd_age
def test_multi_upd_age_fail_0yyn():
    xyyn(0, get_func_name())


@pytest.mark.multi_upd_age
def test_multi_upd_age_fail_1yyn():
    xyyn(1, get_func_name())


@pytest.mark.multi_upd_age
def test_multi_upd_age_fail_20yyn():
    xyyn(20, get_func_name())


@pytest.mark.multi_upd_age
def test_multi_upd_age_fail_0nny():
    xnny(0, get_func_name())


@pytest.mark.multi_upd_age
def test_multi_upd_age_fail_1nny():
    xnny(1, get_func_name())


@pytest.mark.multi_upd_age
def test_multi_upd_age_fail_20nny():
    xnny(20, get_func_name())


@pytest.mark.multi_upd_age
def test_multi_upd_age_fail_0nnn():
    xnnn(0, get_func_name())


@pytest.mark.multi_upd_age
def test_multi_upd_age_fail_1nnn():
    xnnn(1, get_func_name())


@pytest.mark.multi_upd_age
def test_multi_upd_age_fail_20nnn():
    xnnn(20, get_func_name())


@pytest.mark.multi_upd_age
def test_multi_upd_age_fail_0nyy():
    xnyy(0, get_func_name())


@pytest.mark.multi_upd_age
def test_multi_upd_age_fail_1nyy():
    xnyy(1, get_func_name())


@pytest.mark.multi_upd_age
def test_multi_upd_age_fail_20nyy():
    xnyy(20, get_func_name())
