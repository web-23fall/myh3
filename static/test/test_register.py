from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import chromedriver_autoinstaller
import pytest

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


@pytest.mark.register
def test_register_username_fail_none():
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://127.0.0.1:5000/register")
    driver.implicitly_wait(2)

    pwd = driver.find_element(by=By.NAME, value="pwd")
    pwdagain = driver.find_element(by=By.NAME, value="pwdagain")
    button = driver.find_element(by=By.ID, value="reg")

    pwd.send_keys("123abcABC")
    pwdagain.send_keys("123abcABC")
    button.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.save_screenshot("png/register_username_fail_none.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text == "用户名或密码不能为空"

    driver.quit()


@pytest.mark.register
def test_register_username_fail_short():
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://127.0.0.1:5000/register")
    driver.implicitly_wait(2)

    username = driver.find_element(by=By.NAME, value="username")
    pwd = driver.find_element(by=By.NAME, value="pwd")
    pwdagain = driver.find_element(by=By.NAME, value="pwdagain")
    button = driver.find_element(by=By.ID, value="reg")

    username.send_keys("1234")
    pwd.send_keys("123abcABC")
    pwdagain.send_keys("123abcABC")
    button.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.get_screenshot_as_file("png/register_username_fail_short.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert (
        text
        == "用户名不合法，应当为一个长度为 6-16 的，以大小写字母或数字或下划线开头的，包含大小写字母、数字和特殊字符的其中三种的字符串，且不包含任何 SQL 关键字"
    )

    driver.quit()


@pytest.mark.register
def test_register_username_fail_long():
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://127.0.0.1:5000/register")
    driver.implicitly_wait(2)

    username = driver.find_element(by=By.NAME, value="username")
    pwd = driver.find_element(by=By.NAME, value="pwd")
    pwdagain = driver.find_element(by=By.NAME, value="pwdagain")
    button = driver.find_element(by=By.ID, value="reg")

    username.send_keys("asdfghjklqwert;457")
    pwd.send_keys("123abcABC")
    pwdagain.send_keys("123abcABC")
    button.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.get_screenshot_as_file("png/register_username_fail_long.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert (
        text
        == "用户名不合法，应当为一个长度为 6-16 的，以大小写字母或数字或下划线开头的，包含大小写字母、数字和特殊字符的其中三种的字符串，且不包含任何 SQL 关键字"
    )

    driver.quit()


@pytest.mark.register
def test_register_username_fail_only1():
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://127.0.0.1:5000/register")
    driver.implicitly_wait(2)

    username = driver.find_element(by=By.NAME, value="username")
    pwd = driver.find_element(by=By.NAME, value="pwd")
    pwdagain = driver.find_element(by=By.NAME, value="pwdagain")
    button = driver.find_element(by=By.ID, value="reg")

    username.send_keys("123456789")
    pwd.send_keys("123abcABC")
    pwdagain.send_keys("123abcABC")
    button.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.get_screenshot_as_file("png/register_username_fail_only1.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert (
        text
        == "用户名不合法，应当为一个长度为 6-16 的，以大小写字母或数字或下划线开头的，包含大小写字母、数字和特殊字符的其中三种的字符串，且不包含任何 SQL 关键字"
    )

    driver.quit()


@pytest.mark.register
def test_register_username_fail_only2():
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://127.0.0.1:5000/register")
    driver.implicitly_wait(2)

    username = driver.find_element(by=By.NAME, value="username")
    pwd = driver.find_element(by=By.NAME, value="pwd")
    pwdagain = driver.find_element(by=By.NAME, value="pwdagain")
    button = driver.find_element(by=By.ID, value="reg")

    username.send_keys("123456789ab")
    pwd.send_keys("123abcABC")
    pwdagain.send_keys("123abcABC")
    button.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.get_screenshot_as_file("png/register_username_fail_only2.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert (
        text
        == "用户名不合法，应当为一个长度为 6-16 的，以大小写字母或数字或下划线开头的，包含大小写字母、数字和特殊字符的其中三种的字符串，且不包含任何 SQL 关键字"
    )

    driver.quit()


@pytest.mark.register
def test_register_username_fail_with_space():
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://127.0.0.1:5000/register")
    driver.implicitly_wait(2)

    username = driver.find_element(by=By.NAME, value="username")
    pwd = driver.find_element(by=By.NAME, value="pwd")
    pwdagain = driver.find_element(by=By.NAME, value="pwdagain")
    button = driver.find_element(by=By.ID, value="reg")

    username.send_keys("abcdef1 ")
    pwd.send_keys("123abcABC")
    pwdagain.send_keys("123abcABC")
    button.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.get_screenshot_as_file("png/register_username_fail_with_space.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert (
        text
        == "用户名不合法，应当为一个长度为 6-16 的，以大小写字母或数字或下划线开头的，包含大小写字母、数字和特殊字符的其中三种的字符串，且不包含任何 SQL 关键字"
    )

    driver.quit()


@pytest.mark.register
def test_register_username_fail_sql():
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://127.0.0.1:5000/register")
    driver.implicitly_wait(2)

    username = driver.find_element(by=By.NAME, value="username")
    pwd = driver.find_element(by=By.NAME, value="pwd")
    pwdagain = driver.find_element(by=By.NAME, value="pwdagain")
    button = driver.find_element(by=By.ID, value="reg")

    username.send_keys("abcd' or 1=1;--")
    pwd.send_keys("123abcABC")
    pwdagain.send_keys("123abcABC")
    button.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.get_screenshot_as_file("png/register_username_fail_sql.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert (
        text
        == "用户名不合法，应当为一个长度为 6-16 的，以大小写字母或数字或下划线开头的，包含大小写字母、数字和特殊字符的其中三种的字符串，且不包含任何 SQL 关键字"
    )

    driver.quit()


@pytest.mark.register
def test_register_username_fail_nonstart():
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://127.0.0.1:5000/register")
    driver.implicitly_wait(2)

    username = driver.find_element(by=By.NAME, value="username")
    pwd = driver.find_element(by=By.NAME, value="pwd")
    pwdagain = driver.find_element(by=By.NAME, value="pwdagain")
    button = driver.find_element(by=By.ID, value="reg")

    username.send_keys("-123ab_q")
    pwd.send_keys("123abcABC")
    pwdagain.send_keys("123abcABC")
    button.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.get_screenshot_as_file("png/register_username_fail_nonstart.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert (
        text
        == "用户名不合法，应当为一个长度为 6-16 的，以大小写字母或数字或下划线开头的，包含大小写字母、数字和特殊字符的其中三种的字符串，且不包含任何 SQL 关键字"
    )

    driver.quit()


@pytest.mark.register
def test_register_username_fail_same():
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://127.0.0.1:5000/register")
    driver.implicitly_wait(2)

    username = driver.find_element(by=By.NAME, value="username")
    pwd = driver.find_element(by=By.NAME, value="pwd")
    pwdagain = driver.find_element(by=By.NAME, value="pwdagain")
    button = driver.find_element(by=By.ID, value="reg")

    username.send_keys("12345qwq!")
    pwd.send_keys("asd123A!")
    pwdagain.send_keys("asd123A!")
    button.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup2 > p"))
    )

    driver.get_screenshot_as_file("png/register_username_fail_same.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup2 > p")
    text = message.text

    assert text == "用户名已被注册，请选择不同的用户名。"

    driver.quit()


@pytest.mark.register
def test_register_password_fail_none():
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://127.0.0.1:5000/register")
    driver.implicitly_wait(2)

    username = driver.find_element(by=By.NAME, value="username")
    pwdagain = driver.find_element(by=By.NAME, value="pwdagain")
    button = driver.find_element(by=By.ID, value="reg")

    username.send_keys("123abcqwq!")
    pwdagain.send_keys("123aA")
    button.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.get_screenshot_as_file("png/register_password_fail_none.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text == "用户名或密码不能为空"

    driver.quit()


@pytest.mark.register
def test_register_password_fail_short():
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://127.0.0.1:5000/register")
    driver.implicitly_wait(2)

    username = driver.find_element(by=By.NAME, value="username")
    pwd = driver.find_element(by=By.NAME, value="pwd")
    pwdagain = driver.find_element(by=By.NAME, value="pwdagain")
    button = driver.find_element(by=By.ID, value="reg")

    username.send_keys("123abcqwq!")
    pwd.send_keys("123aA")
    pwdagain.send_keys("123aA")
    button.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.get_screenshot_as_file("png/register_password_fail_short.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text == "密码不合法，应当为一个长度为 6-16 的，同时具有大写、小写、数字、特殊字符其中三种的字符串，且不包含任何 SQL 关键字"

    driver.quit()


@pytest.mark.register
def test_register_password_fail_long():
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://127.0.0.1:5000/register")
    driver.implicitly_wait(2)

    username = driver.find_element(by=By.NAME, value="username")
    pwd = driver.find_element(by=By.NAME, value="pwd")
    pwdagain = driver.find_element(by=By.NAME, value="pwdagain")
    button = driver.find_element(by=By.ID, value="reg")

    username.send_keys("123abcqwq!")
    pwd.send_keys("123aAa12345678jkm.")
    pwdagain.send_keys("123aAa12345678jkm.")
    button.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.get_screenshot_as_file("png/register_password_fail_long.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text == "密码不合法，应当为一个长度为 6-16 的，同时具有大写、小写、数字、特殊字符其中三种的字符串，且不包含任何 SQL 关键字"

    driver.quit()


@pytest.mark.register
def test_register_password_fail_only1():
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://127.0.0.1:5000/register")
    driver.implicitly_wait(2)

    username = driver.find_element(by=By.NAME, value="username")
    pwd = driver.find_element(by=By.NAME, value="pwd")
    pwdagain = driver.find_element(by=By.NAME, value="pwdagain")
    button = driver.find_element(by=By.ID, value="reg")

    username.send_keys("123abcqwq!")
    pwd.send_keys("12345678")
    pwdagain.send_keys("12345678")
    button.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.get_screenshot_as_file("png/register_password_fail_only1.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text == "密码不合法，应当为一个长度为 6-16 的，同时具有大写、小写、数字、特殊字符其中三种的字符串，且不包含任何 SQL 关键字"

    driver.quit()


@pytest.mark.register
def test_register_password_fail_only2():
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://127.0.0.1:5000/register")
    driver.implicitly_wait(2)

    username = driver.find_element(by=By.NAME, value="username")
    pwd = driver.find_element(by=By.NAME, value="pwd")
    pwdagain = driver.find_element(by=By.NAME, value="pwdagain")
    button = driver.find_element(by=By.ID, value="reg")

    username.send_keys("123abcqwq!")
    pwd.send_keys("12345678abc")
    pwdagain.send_keys("12345678abc")
    button.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.get_screenshot_as_file("png/register_password_fail_only2.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text == "密码不合法，应当为一个长度为 6-16 的，同时具有大写、小写、数字、特殊字符其中三种的字符串，且不包含任何 SQL 关键字"

    driver.quit()


@pytest.mark.register
def test_register_password_fail_sql():
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://127.0.0.1:5000/register")
    driver.implicitly_wait(2)

    username = driver.find_element(by=By.NAME, value="username")
    pwd = driver.find_element(by=By.NAME, value="pwd")
    pwdagain = driver.find_element(by=By.NAME, value="pwdagain")
    button = driver.find_element(by=By.ID, value="reg")

    username.send_keys("123abcqwq!")
    pwd.send_keys("1234 and ")
    pwdagain.send_keys("1234 and ")
    button.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.get_screenshot_as_file("png/register_password_fail_sql.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text == "密码不合法，应当为一个长度为 6-16 的，同时具有大写、小写、数字、特殊字符其中三种的字符串，且不包含任何 SQL 关键字"

    driver.quit()


@pytest.mark.register
def test_register_password_fail_same_username():
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://127.0.0.1:5000/register")
    driver.implicitly_wait(2)

    username = driver.find_element(by=By.NAME, value="username")
    pwd = driver.find_element(by=By.NAME, value="pwd")
    pwdagain = driver.find_element(by=By.NAME, value="pwdagain")
    button = driver.find_element(by=By.ID, value="reg")

    username.send_keys("123abcqwq!")
    pwd.send_keys("123abcqwq!")
    pwdagain.send_keys("123abcqwq!")
    button.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.get_screenshot_as_file("png/test_register_password_fail_same_username.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text == "用户名和密码不能相同"

    driver.quit()


@pytest.mark.register
def test_register_passwordagain_fail_none():
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://127.0.0.1:5000/register")
    driver.implicitly_wait(2)

    username = driver.find_element(by=By.NAME, value="username")
    pwd = driver.find_element(by=By.NAME, value="pwd")
    button = driver.find_element(by=By.ID, value="reg")

    username.send_keys("123abcqwq!")
    pwd.send_keys("123abcqwq?!")
    button.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.get_screenshot_as_file("png/register_passwordagain_fail_none.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text == "请确认密码"

    driver.quit()


@pytest.mark.register
def test_register_passwordagain_fail_not_equal():
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://127.0.0.1:5000/register")
    driver.implicitly_wait(2)

    username = driver.find_element(by=By.NAME, value="username")
    pwd = driver.find_element(by=By.NAME, value="pwd")
    pwdagain = driver.find_element(by=By.NAME, value="pwdagain")
    button = driver.find_element(by=By.ID, value="reg")

    username.send_keys("123abcqwq!")
    pwd.send_keys("123abcqwq?!")
    pwdagain.send_keys("1abcqwq?!")
    button.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.save_screenshot("png/register_passwordagain_fail_not_equal.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text == "两次输入的密码不一致"

    driver.quit()


@pytest.mark.register
def test_register_success():
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://127.0.0.1:5000/register")
    driver.implicitly_wait(2)

    username = driver.find_element(by=By.NAME, value="username")
    pwd = driver.find_element(by=By.NAME, value="pwd")
    pwdagain = driver.find_element(by=By.NAME, value="pwdagain")
    button = driver.find_element(by=By.ID, value="reg")

    username.send_keys("123ABCqwq!_")
    pwd.send_keys("asd123A!")
    pwdagain.send_keys("asd123A!")
    button.click()

    WebDriverWait(driver, 10).until(EC.title_is("login"))

    driver.save_screenshot("png/register_success.png")

    result = EC.title_is("login")
    assert result

    driver.quit()
