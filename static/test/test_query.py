from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import chromedriver_autoinstaller
import pytest
import inspect

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


def get_func_name() -> str:
    function_name = inspect.currentframe().f_back.f_code.co_name
    if function_name.startswith("test_"):
        function_name = function_name[len("test_") :]
    return function_name


@pytest.mark.query
def test_query_username_fail_none():
    driver = login()

    # name = driver.find_element(by=By.ID, value="name")
    stu_id = driver.find_element(by=By.ID, value="id")
    submit = driver.find_element(by=By.ID, value="query")

    stu_id.send_keys("24")
    submit.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.save_screenshot(f"png/{get_func_name()}.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text == "请输入完整的查询条件"

    driver.quit()


@pytest.mark.query
def test_query_username_fail_long():
    driver = login()

    name = driver.find_element(by=By.ID, value="name")
    stu_id = driver.find_element(by=By.ID, value="id")
    submit = driver.find_element(by=By.ID, value="query")

    name.send_keys("abcdefghijklmnopqrs")
    stu_id.send_keys("24")
    submit.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.save_screenshot(f"png/{get_func_name()}.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text == "姓名不合法，应当为一个长度为 1-16 的，可包含空格，中文，英文，但不包含数字和特殊字符的字符串，且不包含任何 SQL 关键字"

    driver.quit()


@pytest.mark.query
def test_query_username_fail_special():
    driver = login()

    name = driver.find_element(by=By.ID, value="name")
    stu_id = driver.find_element(by=By.ID, value="id")
    submit = driver.find_element(by=By.ID, value="query")

    name.send_keys("cdefghij,sa")
    stu_id.send_keys("24")
    submit.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.save_screenshot(f"png/{get_func_name()}.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text == "姓名不合法，应当为一个长度为 1-16 的，可包含空格，中文，英文，但不包含数字和特殊字符的字符串，且不包含任何 SQL 关键字"

    driver.quit()


@pytest.mark.query
def test_query_username_fail_sql():
    driver = login()

    name = driver.find_element(by=By.ID, value="name")
    stu_id = driver.find_element(by=By.ID, value="id")
    submit = driver.find_element(by=By.ID, value="query")

    name.send_keys("cdef and qq")
    stu_id.send_keys("24")
    submit.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.save_screenshot(f"png/{get_func_name()}.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text == "姓名不合法，应当为一个长度为 1-16 的，可包含空格，中文，英文，但不包含数字和特殊字符的字符串，且不包含任何 SQL 关键字"

    driver.quit()


@pytest.mark.query
def test_query_username_fail_num():
    driver = login()

    name = driver.find_element(by=By.ID, value="name")
    stu_id = driver.find_element(by=By.ID, value="id")
    submit = driver.find_element(by=By.ID, value="query")

    name.send_keys("cdef23")
    stu_id.send_keys("24")
    submit.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.save_screenshot(f"png/{get_func_name()}.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text == "姓名不合法，应当为一个长度为 1-16 的，可包含空格，中文，英文，但不包含数字和特殊字符的字符串，且不包含任何 SQL 关键字"

    driver.quit()


@pytest.mark.query
def test_query_stuid_fail_none():
    driver = login()

    name = driver.find_element(by=By.ID, value="name")
    stu_id = driver.find_element(by=By.ID, value="id")
    submit = driver.find_element(by=By.ID, value="query")

    name.send_keys("Maruyama Rin")
    submit.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.save_screenshot(f"png/{get_func_name()}.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text == "请输入完整的查询条件"

    driver.quit()


@pytest.mark.query
def test_query_stuid_fail_long():
    driver = login()

    name = driver.find_element(by=By.ID, value="name")
    stu_id = driver.find_element(by=By.ID, value="id")
    submit = driver.find_element(by=By.ID, value="query")

    name.send_keys("Maruyama Rin")
    stu_id.send_keys("1234567890123456789")
    submit.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.save_screenshot(f"png/{get_func_name()}.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text == "学号不合法，应为一个长度为 1-16 的正整数"

    driver.quit()


@pytest.mark.query
def test_query_stuid_fail_not_num():
    driver = login()

    name = driver.find_element(by=By.ID, value="name")
    stu_id = driver.find_element(by=By.ID, value="id")
    submit = driver.find_element(by=By.ID, value="query")

    name.send_keys("Maruyama Rin")
    stu_id.send_keys("12345abc!")
    submit.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.save_screenshot(f"png/{get_func_name()}.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text == "学号不合法，应为一个长度为 1-16 的正整数"

    driver.quit()


@pytest.mark.query
def test_query_stuid_fail_zero():
    driver = login()

    name = driver.find_element(by=By.ID, value="name")
    stu_id = driver.find_element(by=By.ID, value="id")
    submit = driver.find_element(by=By.ID, value="query")

    name.send_keys("Maruyama Rin")
    stu_id.send_keys("0")
    submit.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.save_screenshot(f"png/{get_func_name()}.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text == "学号不合法，应为一个长度为 1-16 的正整数"

    driver.quit()


@pytest.mark.query
def test_query_stuid_fail_neg():
    driver = login()

    name = driver.find_element(by=By.ID, value="name")
    stu_id = driver.find_element(by=By.ID, value="id")
    submit = driver.find_element(by=By.ID, value="query")

    name.send_keys("Maruyama Rin")
    stu_id.send_keys("-114514")
    submit.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.save_screenshot(f"png/{get_func_name()}.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text == "学号不合法，应为一个长度为 1-16 的正整数"

    driver.quit()


@pytest.mark.query
def test_query_stuid_username_fail_not_crspnd():
    driver = login()

    name = driver.find_element(by=By.ID, value="name")
    stu_id = driver.find_element(by=By.ID, value="id")
    submit = driver.find_element(by=By.ID, value="query")

    name.send_keys("Maruyama Rin")
    stu_id.send_keys("23")
    submit.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup2 > p"))
    )

    driver.save_screenshot(f"png/{get_func_name()}.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup2 > p")
    text = message.text

    assert text == "查询结果为空，请检查查询条件"

    driver.quit()


@pytest.mark.query
def test_query_success_en():
    driver = login()

    query_suc(driver, "Maruyama Rin", "24", get_func_name())

    driver.quit()


@pytest.mark.query
def test_query_success_s_zh():
    driver = login()

    query_suc(driver, "姚子异", "25", get_func_name())

    driver.quit()


@pytest.mark.query
def test_query_success_t_zh():
    driver = login()

    query_suc(driver, "鈴木架純", "34", get_func_name())

    driver.quit()
