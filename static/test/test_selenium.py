from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
# and if it doesn't exist, download it automatically,
# then add chromedriver to path


def test_register_username_fail_none():
    driver = webdriver.Chrome()
    driver.get("http://localhost:5000/register")
    driver.implicitly_wait(0.5)
    username = driver.find_element(by=By.NAME, value="username")
    pwd = driver.find_element(by=By.NAME, value="pwd")
    pwdagain = driver.find_element(by=By.NAME, value="pwdagain")
    button = driver.find_element(by=By.ID, value="reg")

    pwd.send_keys("123abcABC")
    pwdagain.send_keys("123abcABC")
    button.click()

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text == "用户名或密码不能为空"

    time.sleep(3)
    driver.quit()


def test_register_username_fail_short():
    driver = webdriver.Chrome()
    driver.get("http://localhost:5000/register")
    driver.implicitly_wait(0.5)
    username = driver.find_element(by=By.NAME, value="username")
    pwd = driver.find_element(by=By.NAME, value="pwd")
    pwdagain = driver.find_element(by=By.NAME, value="pwdagain")
    button = driver.find_element(by=By.ID, value="reg")

    username.send_keys("1234")
    pwd.send_keys("123abcABC")
    pwdagain.send_keys("123abcABC")
    button.click()

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert (
        text
        == "用户名不合法，应当为一个长度为 6-16 的，以大小写字母或数字或下划线开头的，包含大小写字母、数字和特殊字符的其中三种的字符串，且不包含任何 SQL 关键字"
    )

    time.sleep(3)
    driver.quit()


def test_register_username_fail_only1():
    driver = webdriver.Chrome()
    driver.get("http://localhost:5000/register")
    driver.implicitly_wait(0.5)
    username = driver.find_element(by=By.NAME, value="username")
    pwd = driver.find_element(by=By.NAME, value="pwd")
    pwdagain = driver.find_element(by=By.NAME, value="pwdagain")
    button = driver.find_element(by=By.ID, value="reg")

    username.send_keys("123456789")
    pwd.send_keys("123abcABC")
    pwdagain.send_keys("123abcABC")
    button.click()

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert (
        text
        == "用户名不合法，应当为一个长度为 6-16 的，以大小写字母或数字或下划线开头的，包含大小写字母、数字和特殊字符的其中三种的字符串，且不包含任何 SQL 关键字"
    )

    time.sleep(3)
    driver.quit()


def test_register_username_fail_only2():
    driver = webdriver.Chrome()
    driver.get("http://localhost:5000/register")
    driver.implicitly_wait(0.5)
    username = driver.find_element(by=By.NAME, value="username")
    pwd = driver.find_element(by=By.NAME, value="pwd")
    pwdagain = driver.find_element(by=By.NAME, value="pwdagain")
    button = driver.find_element(by=By.ID, value="reg")

    username.send_keys("123456789ab")
    pwd.send_keys("123abcABC")
    pwdagain.send_keys("123abcABC")
    button.click()

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert (
        text
        == "用户名不合法，应当为一个长度为 6-16 的，以大小写字母或数字或下划线开头的，包含大小写字母、数字和特殊字符的其中三种的字符串，且不包含任何 SQL 关键字"
    )

    time.sleep(3)
    driver.quit()


def test_register_username_fail_with_space():
    driver = webdriver.Chrome()
    driver.get("http://localhost:5000/register")
    driver.implicitly_wait(0.5)
    username = driver.find_element(by=By.NAME, value="username")
    pwd = driver.find_element(by=By.NAME, value="pwd")
    pwdagain = driver.find_element(by=By.NAME, value="pwdagain")
    button = driver.find_element(by=By.ID, value="reg")

    username.send_keys("abcdef1 ")
    pwd.send_keys("123abcABC")
    pwdagain.send_keys("123abcABC")
    button.click()

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert (
        text
        == "用户名不合法，应当为一个长度为 6-16 的，以大小写字母或数字或下划线开头的，包含大小写字母、数字和特殊字符的其中三种的字符串，且不包含任何 SQL 关键字"
    )

    time.sleep(3)
    driver.quit()


def test_register_username_fail_long():
    driver = webdriver.Chrome()
    driver.get("http://localhost:5000/register")
    driver.implicitly_wait(0.5)
    username = driver.find_element(by=By.NAME, value="username")
    pwd = driver.find_element(by=By.NAME, value="pwd")
    pwdagain = driver.find_element(by=By.NAME, value="pwdagain")
    button = driver.find_element(by=By.ID, value="reg")

    username.send_keys("asdfghjklqwert;457")
    pwd.send_keys("123abcABC")
    pwdagain.send_keys("123abcABC")
    button.click()

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert (
        text
        == "用户名不合法，应当为一个长度为 6-16 的，以大小写字母或数字或下划线开头的，包含大小写字母、数字和特殊字符的其中三种的字符串，且不包含任何 SQL 关键字"
    )

    time.sleep(3)
    driver.quit()


def test_register_username_fail_SQL():
    driver = webdriver.Chrome()
    driver.get("http://localhost:5000/register")
    driver.implicitly_wait(0.5)
    username = driver.find_element(by=By.NAME, value="username")
    pwd = driver.find_element(by=By.NAME, value="pwd")
    pwdagain = driver.find_element(by=By.NAME, value="pwdagain")
    button = driver.find_element(by=By.ID, value="reg")

    username.send_keys("123 and -")
    pwd.send_keys("123abcABC")
    pwdagain.send_keys("123abcABC")
    button.click()

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert (
        text
        == "用户名不合法，应当为一个长度为 6-16 的，以大小写字母或数字或下划线开头的，包含大小写字母、数字和特殊字符的其中三种的字符串，且不包含任何 SQL 关键字"
    )

    time.sleep(3)
    driver.quit()


def test_register_username_fail_nonstart():
    driver = webdriver.Chrome()
    driver.get("http://localhost:5000/register")
    driver.implicitly_wait(0.5)
    username = driver.find_element(by=By.NAME, value="username")
    pwd = driver.find_element(by=By.NAME, value="pwd")
    pwdagain = driver.find_element(by=By.NAME, value="pwdagain")
    button = driver.find_element(by=By.ID, value="reg")

    username.send_keys("-123ab_q")
    pwd.send_keys("123abcABC")
    pwdagain.send_keys("123abcABC")
    button.click()

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert (
        text
        == "用户名不合法，应当为一个长度为 6-16 的，以大小写字母或数字或下划线开头的，包含大小写字母、数字和特殊字符的其中三种的字符串，且不包含任何 SQL 关键字"
    )

    time.sleep(3)
    driver.quit()


def test_register_password_fail_none():
    driver = webdriver.Chrome()
    driver.get("http://localhost:5000/register")
    driver.implicitly_wait(0.5)
    username = driver.find_element(by=By.NAME, value="username")
    pwd = driver.find_element(by=By.NAME, value="pwd")
    pwdagain = driver.find_element(by=By.NAME, value="pwdagain")
    button = driver.find_element(by=By.ID, value="reg")

    username.send_keys("123abcqwq!")
    pwdagain.send_keys("123aA")
    button.click()

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text == "用户名或密码不能为空"

    time.sleep(3)
    driver.quit()


def test_register_password_fail_short():
    driver = webdriver.Chrome()
    driver.get("http://localhost:5000/register")
    driver.implicitly_wait(0.5)
    username = driver.find_element(by=By.NAME, value="username")
    pwd = driver.find_element(by=By.NAME, value="pwd")
    pwdagain = driver.find_element(by=By.NAME, value="pwdagain")
    button = driver.find_element(by=By.ID, value="reg")

    username.send_keys("123abcqwq!")
    pwd.send_keys("123aA")
    pwdagain.send_keys("123aA")
    button.click()

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text == "密码不合法，应当为一个长度为 6-16 的，同时具有大写、小写、数字、特殊字符其中三种的字符串，且不包含任何 SQL 关键字"

    time.sleep(3)
    driver.quit()


def test_register_password_fail_long():
    driver = webdriver.Chrome()
    driver.get("http://localhost:5000/register")
    driver.implicitly_wait(0.5)
    username = driver.find_element(by=By.NAME, value="username")
    pwd = driver.find_element(by=By.NAME, value="pwd")
    pwdagain = driver.find_element(by=By.NAME, value="pwdagain")
    button = driver.find_element(by=By.ID, value="reg")

    username.send_keys("123abcqwq!")
    pwd.send_keys("123aAa12345678jkm.")
    pwdagain.send_keys("123aAa12345678jkm.")
    button.click()

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text == "密码不合法，应当为一个长度为 6-16 的，同时具有大写、小写、数字、特殊字符其中三种的字符串，且不包含任何 SQL 关键字"

    time.sleep(3)
    driver.quit()


def test_register_password_fail_only1():
    driver = webdriver.Chrome()
    driver.get("http://localhost:5000/register")
    driver.implicitly_wait(0.5)
    username = driver.find_element(by=By.NAME, value="username")
    pwd = driver.find_element(by=By.NAME, value="pwd")
    pwdagain = driver.find_element(by=By.NAME, value="pwdagain")
    button = driver.find_element(by=By.ID, value="reg")

    username.send_keys("123abcqwq!")
    pwd.send_keys("12345678")
    pwdagain.send_keys("12345678")
    button.click()

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text == "密码不合法，应当为一个长度为 6-16 的，同时具有大写、小写、数字、特殊字符其中三种的字符串，且不包含任何 SQL 关键字"

    time.sleep(3)
    driver.quit()


def test_register_password_fail_only2():
    driver = webdriver.Chrome()
    driver.get("http://localhost:5000/register")
    driver.implicitly_wait(0.5)
    username = driver.find_element(by=By.NAME, value="username")
    pwd = driver.find_element(by=By.NAME, value="pwd")
    pwdagain = driver.find_element(by=By.NAME, value="pwdagain")
    button = driver.find_element(by=By.ID, value="reg")

    username.send_keys("123abcqwq!")
    pwd.send_keys("12345678abc")
    pwdagain.send_keys("12345678abc")
    button.click()

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text == "密码不合法，应当为一个长度为 6-16 的，同时具有大写、小写、数字、特殊字符其中三种的字符串，且不包含任何 SQL 关键字"

    time.sleep(3)
    driver.quit()


def test_register_password_fail_SQL():
    driver = webdriver.Chrome()
    driver.get("http://localhost:5000/register")
    driver.implicitly_wait(0.5)
    username = driver.find_element(by=By.NAME, value="username")
    pwd = driver.find_element(by=By.NAME, value="pwd")
    pwdagain = driver.find_element(by=By.NAME, value="pwdagain")
    button = driver.find_element(by=By.ID, value="reg")

    username.send_keys("123abcqwq!")
    pwd.send_keys("1234 and ")
    pwdagain.send_keys("1234 and ")
    button.click()

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text == "密码不合法，应当为一个长度为 6-16 的，同时具有大写、小写、数字、特殊字符其中三种的字符串，且不包含任何 SQL 关键字"

    time.sleep(3)
    driver.quit()


def test_register_password_fail_same_username():
    driver = webdriver.Chrome()
    driver.get("http://localhost:5000/register")
    driver.implicitly_wait(0.5)
    username = driver.find_element(by=By.NAME, value="username")
    pwd = driver.find_element(by=By.NAME, value="pwd")
    pwdagain = driver.find_element(by=By.NAME, value="pwdagain")
    button = driver.find_element(by=By.ID, value="reg")

    username.send_keys("123abcqwq!")
    pwd.send_keys("123abcqwq!")
    pwdagain.send_keys("123abcqwq!")
    button.click()

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text == "用户名和密码不能相同"

    time.sleep(3)
    driver.quit()


def test_register_passwordagain_fail_none():
    driver = webdriver.Chrome()
    driver.get("http://localhost:5000/register")
    driver.implicitly_wait(0.5)
    username = driver.find_element(by=By.NAME, value="username")
    pwd = driver.find_element(by=By.NAME, value="pwd")
    pwdagain = driver.find_element(by=By.NAME, value="pwdagain")
    button = driver.find_element(by=By.ID, value="reg")

    username.send_keys("123abcqwq!")
    pwd.send_keys("123abcqwq?!")
    button.click()

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text == "请确认密码"

    time.sleep(3)
    driver.quit()


def test_register_passwordagain_fail_none():
    driver = webdriver.Chrome()
    driver.get("http://localhost:5000/register")
    driver.implicitly_wait(0.5)
    username = driver.find_element(by=By.NAME, value="username")
    pwd = driver.find_element(by=By.NAME, value="pwd")
    pwdagain = driver.find_element(by=By.NAME, value="pwdagain")
    button = driver.find_element(by=By.ID, value="reg")

    username.send_keys("123abcqwq!")
    pwd.send_keys("123abcqwq?!")
    pwdagain.send_keys("1abcqwq?!")
    button.click()

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text == "两次输入的密码不一致"

    time.sleep(3)
    driver.quit()
