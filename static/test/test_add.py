from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
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


courses = [
    "计算机科学与技术",
    "软件工程",
    "网络工程",
    "物联网工程",
    "数据科学与大数据",
    "信息安全",
    "数字媒体技术",
    "智能科学与技术",
    "空间信息与数字技术",
    "电子与计算机工程",
    "数据科学与大数据技术",
    "网络空间安全",
]

cnt = 0


@pytest.mark.add
def test_add_stuid_fail_none():
    global cnt
    driver = login()

    driver.get("http://127.0.0.1:5000/add")

    name = driver.find_element(by=By.ID, value="stu_name")
    stu_id = driver.find_element(by=By.ID, value="stu_id")
    male = driver.find_element(by=By.ID, value="male")
    female = driver.find_element(by=By.ID, value="female")
    age = driver.find_element(by=By.ID, value="stu_age")
    origin = driver.find_element(by=By.ID, value="stu_origin")
    pro = Select(driver.find_element(by=By.ID, value="stu_profession"))
    add = driver.find_element(by=By.ID, value="add")

    name.send_keys("William Thompson")
    if cnt & 1:
        female.click()
    else:
        male.click()
    age.send_keys("24")
    origin.send_keys("New York")
    pro.select_by_value(courses[cnt % len(courses)])
    add.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.save_screenshot(f"png/{get_func_name()}.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text == "学号不合法，应为一个长度为 1-16 的正整数"

    driver.quit()
    cnt += 1


@pytest.mark.add
def test_add_stuid_fail_long():
    global cnt
    driver = login()

    driver.get("http://127.0.0.1:5000/add")

    name = driver.find_element(by=By.ID, value="stu_name")
    stu_id = driver.find_element(by=By.ID, value="stu_id")
    male = driver.find_element(by=By.ID, value="male")
    female = driver.find_element(by=By.ID, value="female")
    age = driver.find_element(by=By.ID, value="stu_age")
    origin = driver.find_element(by=By.ID, value="stu_origin")
    pro = Select(driver.find_element(by=By.ID, value="stu_profession"))
    add = driver.find_element(by=By.ID, value="add")

    stu_id.send_keys("1" * 20)
    name.send_keys("William Thompson")
    if cnt & 1:
        female.click()
    else:
        male.click()
    age.send_keys("24")
    origin.send_keys("New York")
    pro.select_by_value(courses[cnt % len(courses)])
    add.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.save_screenshot(f"png/{get_func_name()}.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text == "学号不合法，应为一个长度为 1-16 的正整数"

    driver.quit()
    cnt += 1


@pytest.mark.add
def test_add_stuid_fail_not_num():
    global cnt
    driver = login()

    driver.get("http://127.0.0.1:5000/add")

    name = driver.find_element(by=By.ID, value="stu_name")
    stu_id = driver.find_element(by=By.ID, value="stu_id")
    male = driver.find_element(by=By.ID, value="male")
    female = driver.find_element(by=By.ID, value="female")
    age = driver.find_element(by=By.ID, value="stu_age")
    origin = driver.find_element(by=By.ID, value="stu_origin")
    pro = Select(driver.find_element(by=By.ID, value="stu_profession"))
    add = driver.find_element(by=By.ID, value="add")

    stu_id.send_keys("12345abc!")
    name.send_keys("William Thompson")
    if cnt & 1:
        female.click()
    else:
        male.click()
    age.send_keys("24")
    origin.send_keys("New York")
    pro.select_by_value(courses[cnt % len(courses)])
    add.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.save_screenshot(f"png/{get_func_name()}.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text == "学号不合法，应为一个长度为 1-16 的正整数"

    driver.quit()
    cnt += 1


@pytest.mark.add
def test_add_stuid_fail_zero():
    global cnt
    driver = login()

    driver.get("http://127.0.0.1:5000/add")

    name = driver.find_element(by=By.ID, value="stu_name")
    stu_id = driver.find_element(by=By.ID, value="stu_id")
    male = driver.find_element(by=By.ID, value="male")
    female = driver.find_element(by=By.ID, value="female")
    age = driver.find_element(by=By.ID, value="stu_age")
    origin = driver.find_element(by=By.ID, value="stu_origin")
    pro = Select(driver.find_element(by=By.ID, value="stu_profession"))
    add = driver.find_element(by=By.ID, value="add")

    stu_id.send_keys("0")
    name.send_keys("William Thompson")
    if cnt & 1:
        female.click()
    else:
        male.click()
    age.send_keys("24")
    origin.send_keys("New York")
    pro.select_by_value(courses[cnt % len(courses)])
    add.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.save_screenshot(f"png/{get_func_name()}.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text == "学号不合法，应为一个长度为 1-16 的正整数"

    driver.quit()
    cnt += 1


@pytest.mark.add
def test_add_stuid_fail_neg():
    global cnt
    driver = login()

    driver.get("http://127.0.0.1:5000/add")

    name = driver.find_element(by=By.ID, value="stu_name")
    stu_id = driver.find_element(by=By.ID, value="stu_id")
    male = driver.find_element(by=By.ID, value="male")
    female = driver.find_element(by=By.ID, value="female")
    age = driver.find_element(by=By.ID, value="stu_age")
    origin = driver.find_element(by=By.ID, value="stu_origin")
    pro = Select(driver.find_element(by=By.ID, value="stu_profession"))
    add = driver.find_element(by=By.ID, value="add")

    stu_id.send_keys("-114514")
    name.send_keys("William Thompson")
    if cnt & 1:
        female.click()
    else:
        male.click()
    age.send_keys("24")
    origin.send_keys("New York")
    pro.select_by_value(courses[cnt % len(courses)])
    add.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.save_screenshot(f"png/{get_func_name()}.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text == "学号不合法，应为一个长度为 1-16 的正整数"

    driver.quit()
    cnt += 1


@pytest.mark.add
def test_add_stuid_fail_same():
    global cnt
    driver = login()

    driver.get("http://127.0.0.1:5000/add")

    name = driver.find_element(by=By.ID, value="stu_name")
    stu_id = driver.find_element(by=By.ID, value="stu_id")
    male = driver.find_element(by=By.ID, value="male")
    female = driver.find_element(by=By.ID, value="female")
    age = driver.find_element(by=By.ID, value="stu_age")
    origin = driver.find_element(by=By.ID, value="stu_origin")
    pro = Select(driver.find_element(by=By.ID, value="stu_profession"))
    add = driver.find_element(by=By.ID, value="add")

    stu_id.send_keys("24")
    name.send_keys("William Thompson")
    if cnt & 1:
        female.click()
    else:
        male.click()
    age.send_keys("24")
    origin.send_keys("New York")
    pro.select_by_value(courses[cnt % len(courses)])
    add.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup2 > p"))
    )

    driver.save_screenshot(f"png/{get_func_name()}.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup2 > p")
    text = message.text

    assert text == "学号重复，请修改输入"

    driver.quit()
    cnt += 1


@pytest.mark.add
def test_add_name_fail_none():
    global cnt
    driver = login()

    driver.get("http://127.0.0.1:5000/add")

    name = driver.find_element(by=By.ID, value="stu_name")
    stu_id = driver.find_element(by=By.ID, value="stu_id")
    male = driver.find_element(by=By.ID, value="male")
    female = driver.find_element(by=By.ID, value="female")
    age = driver.find_element(by=By.ID, value="stu_age")
    origin = driver.find_element(by=By.ID, value="stu_origin")
    pro = Select(driver.find_element(by=By.ID, value="stu_profession"))
    add = driver.find_element(by=By.ID, value="add")

    stu_id.send_keys("114")
    if cnt & 1:
        female.click()
    else:
        male.click()
    age.send_keys("24")
    origin.send_keys("New York")
    pro.select_by_value(courses[cnt % len(courses)])
    add.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.save_screenshot(f"png/{get_func_name()}.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text.startswith("姓名不合法")

    driver.quit()
    cnt += 1


@pytest.mark.add
def test_add_name_fail_long():
    global cnt
    driver = login()

    driver.get("http://127.0.0.1:5000/add")

    name = driver.find_element(by=By.ID, value="stu_name")
    stu_id = driver.find_element(by=By.ID, value="stu_id")
    male = driver.find_element(by=By.ID, value="male")
    female = driver.find_element(by=By.ID, value="female")
    age = driver.find_element(by=By.ID, value="stu_age")
    origin = driver.find_element(by=By.ID, value="stu_origin")
    pro = Select(driver.find_element(by=By.ID, value="stu_profession"))
    add = driver.find_element(by=By.ID, value="add")

    stu_id.send_keys("114")
    name.send_keys("abcdefghijklmnopqrs")
    if cnt & 1:
        female.click()
    else:
        male.click()
    age.send_keys("24")
    origin.send_keys("New York")
    pro.select_by_value(courses[cnt % len(courses)])
    add.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.save_screenshot(f"png/{get_func_name()}.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text.startswith("姓名不合法")

    driver.quit()
    cnt += 1


@pytest.mark.add
def test_add_name_fail_num():
    global cnt
    driver = login()

    driver.get("http://127.0.0.1:5000/add")

    name = driver.find_element(by=By.ID, value="stu_name")
    stu_id = driver.find_element(by=By.ID, value="stu_id")
    male = driver.find_element(by=By.ID, value="male")
    female = driver.find_element(by=By.ID, value="female")
    age = driver.find_element(by=By.ID, value="stu_age")
    origin = driver.find_element(by=By.ID, value="stu_origin")
    pro = Select(driver.find_element(by=By.ID, value="stu_profession"))
    add = driver.find_element(by=By.ID, value="add")

    stu_id.send_keys("114")
    name.send_keys("cdef23")
    if cnt & 1:
        female.click()
    else:
        male.click()
    age.send_keys("24")
    origin.send_keys("New York")
    pro.select_by_value(courses[cnt % len(courses)])
    add.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.save_screenshot(f"png/{get_func_name()}.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text.startswith("姓名不合法")

    driver.quit()
    cnt += 1


@pytest.mark.add
def test_add_name_fail_special():
    global cnt
    driver = login()

    driver.get("http://127.0.0.1:5000/add")

    name = driver.find_element(by=By.ID, value="stu_name")
    stu_id = driver.find_element(by=By.ID, value="stu_id")
    male = driver.find_element(by=By.ID, value="male")
    female = driver.find_element(by=By.ID, value="female")
    age = driver.find_element(by=By.ID, value="stu_age")
    origin = driver.find_element(by=By.ID, value="stu_origin")
    pro = Select(driver.find_element(by=By.ID, value="stu_profession"))
    add = driver.find_element(by=By.ID, value="add")

    stu_id.send_keys("114")
    name.send_keys("cdefghij,sa")
    if cnt & 1:
        female.click()
    else:
        male.click()
    age.send_keys("24")
    origin.send_keys("New York")
    pro.select_by_value(courses[cnt % len(courses)])
    add.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.save_screenshot(f"png/{get_func_name()}.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text.startswith("姓名不合法")

    driver.quit()
    cnt += 1


@pytest.mark.add
def test_add_name_fail_sql():
    global cnt
    driver = login()

    driver.get("http://127.0.0.1:5000/add")

    name = driver.find_element(by=By.ID, value="stu_name")
    stu_id = driver.find_element(by=By.ID, value="stu_id")
    male = driver.find_element(by=By.ID, value="male")
    female = driver.find_element(by=By.ID, value="female")
    age = driver.find_element(by=By.ID, value="stu_age")
    origin = driver.find_element(by=By.ID, value="stu_origin")
    pro = Select(driver.find_element(by=By.ID, value="stu_profession"))
    add = driver.find_element(by=By.ID, value="add")

    stu_id.send_keys("114")
    name.send_keys("cdef and qq")
    if cnt & 1:
        female.click()
    else:
        male.click()
    age.send_keys("24")
    origin.send_keys("New York")
    pro.select_by_value(courses[cnt % len(courses)])
    add.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.save_screenshot(f"png/{get_func_name()}.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text.startswith("姓名不合法")

    driver.quit()
    cnt += 1


@pytest.mark.add
def test_add_sex_fail_none():
    global cnt
    driver = login()

    driver.get("http://127.0.0.1:5000/add")

    name = driver.find_element(by=By.ID, value="stu_name")
    stu_id = driver.find_element(by=By.ID, value="stu_id")
    male = driver.find_element(by=By.ID, value="male")
    female = driver.find_element(by=By.ID, value="female")
    age = driver.find_element(by=By.ID, value="stu_age")
    origin = driver.find_element(by=By.ID, value="stu_origin")
    pro = Select(driver.find_element(by=By.ID, value="stu_profession"))
    add = driver.find_element(by=By.ID, value="add")

    stu_id.send_keys("114")
    name.send_keys("William Thompson")
    age.send_keys("24")
    origin.send_keys("New York")
    pro.select_by_value(courses[cnt % len(courses)])
    add.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.save_screenshot(f"png/{get_func_name()}.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text == "请选择性别"

    driver.quit()
    cnt += 1


@pytest.mark.add
def test_add_age_fail_none():
    global cnt
    driver = login()

    driver.get("http://127.0.0.1:5000/add")

    name = driver.find_element(by=By.ID, value="stu_name")
    stu_id = driver.find_element(by=By.ID, value="stu_id")
    male = driver.find_element(by=By.ID, value="male")
    female = driver.find_element(by=By.ID, value="female")
    age = driver.find_element(by=By.ID, value="stu_age")
    origin = driver.find_element(by=By.ID, value="stu_origin")
    pro = Select(driver.find_element(by=By.ID, value="stu_profession"))
    add = driver.find_element(by=By.ID, value="add")

    stu_id.send_keys("114")
    name.send_keys("William Thompson")
    if cnt & 1:
        female.click()
    else:
        male.click()
    origin.send_keys("New York")
    pro.select_by_value(courses[cnt % len(courses)])
    add.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.save_screenshot(f"png/{get_func_name()}.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text.startswith("年龄不合法")

    driver.quit()
    cnt += 1


@pytest.mark.add
def test_add_age_fail_zero():
    global cnt
    driver = login()

    driver.get("http://127.0.0.1:5000/add")

    name = driver.find_element(by=By.ID, value="stu_name")
    stu_id = driver.find_element(by=By.ID, value="stu_id")
    male = driver.find_element(by=By.ID, value="male")
    female = driver.find_element(by=By.ID, value="female")
    age = driver.find_element(by=By.ID, value="stu_age")
    origin = driver.find_element(by=By.ID, value="stu_origin")
    pro = Select(driver.find_element(by=By.ID, value="stu_profession"))
    add = driver.find_element(by=By.ID, value="add")

    stu_id.send_keys("114")
    name.send_keys("William Thompson")
    if cnt & 1:
        female.click()
    else:
        male.click()
    age.send_keys("0")
    origin.send_keys("New York")
    pro.select_by_value(courses[cnt % len(courses)])
    add.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.save_screenshot(f"png/{get_func_name()}.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text.startswith("年龄不合法")

    driver.quit()
    cnt += 1


@pytest.mark.add
def test_add_age_fail_neg():
    global cnt
    driver = login()

    driver.get("http://127.0.0.1:5000/add")

    name = driver.find_element(by=By.ID, value="stu_name")
    stu_id = driver.find_element(by=By.ID, value="stu_id")
    male = driver.find_element(by=By.ID, value="male")
    female = driver.find_element(by=By.ID, value="female")
    age = driver.find_element(by=By.ID, value="stu_age")
    origin = driver.find_element(by=By.ID, value="stu_origin")
    pro = Select(driver.find_element(by=By.ID, value="stu_profession"))
    add = driver.find_element(by=By.ID, value="add")

    stu_id.send_keys("114")
    name.send_keys("William Thompson")
    if cnt & 1:
        female.click()
    else:
        male.click()
    age.send_keys("-114514")
    origin.send_keys("New York")
    pro.select_by_value(courses[cnt % len(courses)])
    add.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.save_screenshot(f"png/{get_func_name()}.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text.startswith("年龄不合法")

    driver.quit()
    cnt += 1


@pytest.mark.add
def test_add_age_fail_en():
    global cnt
    driver = login()

    driver.get("http://127.0.0.1:5000/add")

    name = driver.find_element(by=By.ID, value="stu_name")
    stu_id = driver.find_element(by=By.ID, value="stu_id")
    male = driver.find_element(by=By.ID, value="male")
    female = driver.find_element(by=By.ID, value="female")
    age = driver.find_element(by=By.ID, value="stu_age")
    origin = driver.find_element(by=By.ID, value="stu_origin")
    pro = Select(driver.find_element(by=By.ID, value="stu_profession"))
    add = driver.find_element(by=By.ID, value="add")

    stu_id.send_keys("114")
    name.send_keys("William Thompson")
    if cnt & 1:
        female.click()
    else:
        male.click()
    age.send_keys("114cda")
    origin.send_keys("New York")
    pro.select_by_value(courses[cnt % len(courses)])
    add.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.save_screenshot(f"png/{get_func_name()}.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text.startswith("年龄不合法")

    driver.quit()
    cnt += 1


@pytest.mark.add
def test_add_age_fail_special():
    global cnt
    driver = login()

    driver.get("http://127.0.0.1:5000/add")

    name = driver.find_element(by=By.ID, value="stu_name")
    stu_id = driver.find_element(by=By.ID, value="stu_id")
    male = driver.find_element(by=By.ID, value="male")
    female = driver.find_element(by=By.ID, value="female")
    age = driver.find_element(by=By.ID, value="stu_age")
    origin = driver.find_element(by=By.ID, value="stu_origin")
    pro = Select(driver.find_element(by=By.ID, value="stu_profession"))
    add = driver.find_element(by=By.ID, value="add")

    stu_id.send_keys("114")
    name.send_keys("William Thompson")
    if cnt & 1:
        female.click()
    else:
        male.click()
    age.send_keys("114!!!")
    origin.send_keys("New York")
    pro.select_by_value(courses[cnt % len(courses)])
    add.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.save_screenshot(f"png/{get_func_name()}.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text.startswith("年龄不合法")

    driver.quit()
    cnt += 1


@pytest.mark.add
def test_add_ht_fail_none():
    global cnt
    driver = login()

    driver.get("http://127.0.0.1:5000/add")

    name = driver.find_element(by=By.ID, value="stu_name")
    stu_id = driver.find_element(by=By.ID, value="stu_id")
    male = driver.find_element(by=By.ID, value="male")
    female = driver.find_element(by=By.ID, value="female")
    age = driver.find_element(by=By.ID, value="stu_age")
    origin = driver.find_element(by=By.ID, value="stu_origin")
    pro = Select(driver.find_element(by=By.ID, value="stu_profession"))
    add = driver.find_element(by=By.ID, value="add")

    stu_id.send_keys("114")
    name.send_keys("William Thompson")
    if cnt & 1:
        female.click()
    else:
        male.click()
    age.send_keys("24")
    pro.select_by_value(courses[cnt % len(courses)])
    add.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.save_screenshot(f"png/{get_func_name()}.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text.startswith("籍贯不合法")

    driver.quit()
    cnt += 1


@pytest.mark.add
def test_add_ht_fail_long():
    global cnt
    driver = login()

    driver.get("http://127.0.0.1:5000/add")

    name = driver.find_element(by=By.ID, value="stu_name")
    stu_id = driver.find_element(by=By.ID, value="stu_id")
    male = driver.find_element(by=By.ID, value="male")
    female = driver.find_element(by=By.ID, value="female")
    age = driver.find_element(by=By.ID, value="stu_age")
    origin = driver.find_element(by=By.ID, value="stu_origin")
    pro = Select(driver.find_element(by=By.ID, value="stu_profession"))
    add = driver.find_element(by=By.ID, value="add")

    stu_id.send_keys("114")
    name.send_keys("William Thompson")
    if cnt & 1:
        female.click()
    else:
        male.click()
    age.send_keys("24")
    origin.send_keys("abcdefghijklmnopqrs")
    pro.select_by_value(courses[cnt % len(courses)])
    add.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.save_screenshot(f"png/{get_func_name()}.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text.startswith("籍贯不合法")

    driver.quit()
    cnt += 1


@pytest.mark.add
def test_add_ht_fail_num():
    global cnt
    driver = login()

    driver.get("http://127.0.0.1:5000/add")

    name = driver.find_element(by=By.ID, value="stu_name")
    stu_id = driver.find_element(by=By.ID, value="stu_id")
    male = driver.find_element(by=By.ID, value="male")
    female = driver.find_element(by=By.ID, value="female")
    age = driver.find_element(by=By.ID, value="stu_age")
    origin = driver.find_element(by=By.ID, value="stu_origin")
    pro = Select(driver.find_element(by=By.ID, value="stu_profession"))
    add = driver.find_element(by=By.ID, value="add")

    stu_id.send_keys("114")
    name.send_keys("William Thompson")
    if cnt & 1:
        female.click()
    else:
        male.click()
    age.send_keys("24")
    origin.send_keys("cdef23")
    pro.select_by_value(courses[cnt % len(courses)])
    add.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.save_screenshot(f"png/{get_func_name()}.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text.startswith("籍贯不合法")

    driver.quit()
    cnt += 1


@pytest.mark.add
def test_add_ht_fail_special():
    global cnt
    driver = login()

    driver.get("http://127.0.0.1:5000/add")

    name = driver.find_element(by=By.ID, value="stu_name")
    stu_id = driver.find_element(by=By.ID, value="stu_id")
    male = driver.find_element(by=By.ID, value="male")
    female = driver.find_element(by=By.ID, value="female")
    age = driver.find_element(by=By.ID, value="stu_age")
    origin = driver.find_element(by=By.ID, value="stu_origin")
    pro = Select(driver.find_element(by=By.ID, value="stu_profession"))
    add = driver.find_element(by=By.ID, value="add")

    stu_id.send_keys("114")
    name.send_keys("William Thompson")
    if cnt & 1:
        female.click()
    else:
        male.click()
    age.send_keys("24")
    origin.send_keys("cdefghij,sa")
    pro.select_by_value(courses[cnt % len(courses)])
    add.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".popup1 > p"))
    )

    driver.save_screenshot(f"png/{get_func_name()}.png")

    message = driver.find_element(by=By.CSS_SELECTOR, value=".popup1 > p")
    text = message.text

    assert text.startswith("籍贯不合法")

    driver.quit()
    cnt += 1


@pytest.mark.add
def test_add_success_en_en():
    global cnt
    driver = login()

    driver.get("http://127.0.0.1:5000/add")

    name = driver.find_element(by=By.ID, value="stu_name")
    stu_id = driver.find_element(by=By.ID, value="stu_id")
    male = driver.find_element(by=By.ID, value="male")
    female = driver.find_element(by=By.ID, value="female")
    age = driver.find_element(by=By.ID, value="stu_age")
    origin = driver.find_element(by=By.ID, value="stu_origin")
    pro = Select(driver.find_element(by=By.ID, value="stu_profession"))
    add = driver.find_element(by=By.ID, value="add")

    stu_id.send_keys("114")
    name.send_keys("William Thompson")
    if cnt & 1:
        female.click()
    else:
        male.click()
    age.send_keys("24")
    origin.send_keys("New York")
    pro.select_by_value(courses[cnt % len(courses)])
    add.click()

    WebDriverWait(driver, 10).until(EC.title_is("show"))

    driver.save_screenshot(f"png/{get_func_name()}_1.png")

    query_suc(driver, "William Thompson", "114", get_func_name())

    driver.quit()
    cnt += 1


@pytest.mark.add
def test_add_success_szh_en():
    global cnt
    driver = login()

    driver.get("http://127.0.0.1:5000/add")

    name = driver.find_element(by=By.ID, value="stu_name")
    stu_id = driver.find_element(by=By.ID, value="stu_id")
    male = driver.find_element(by=By.ID, value="male")
    female = driver.find_element(by=By.ID, value="female")
    age = driver.find_element(by=By.ID, value="stu_age")
    origin = driver.find_element(by=By.ID, value="stu_origin")
    pro = Select(driver.find_element(by=By.ID, value="stu_profession"))
    add = driver.find_element(by=By.ID, value="add")

    stu_id.send_keys("115")
    name.send_keys("田所浩二")
    if cnt & 1:
        female.click()
    else:
        male.click()
    age.send_keys("24")
    origin.send_keys("New York")
    pro.select_by_value(courses[cnt % len(courses)])
    add.click()

    WebDriverWait(driver, 10).until(EC.title_is("show"))

    driver.save_screenshot(f"png/{get_func_name()}_1.png")

    query_suc(driver, "田所浩二", "115", get_func_name())

    driver.quit()
    cnt += 1


@pytest.mark.add
def test_add_success_tzh_en():
    global cnt
    driver = login()

    driver.get("http://127.0.0.1:5000/add")

    name = driver.find_element(by=By.ID, value="stu_name")
    stu_id = driver.find_element(by=By.ID, value="stu_id")
    male = driver.find_element(by=By.ID, value="male")
    female = driver.find_element(by=By.ID, value="female")
    age = driver.find_element(by=By.ID, value="stu_age")
    origin = driver.find_element(by=By.ID, value="stu_origin")
    pro = Select(driver.find_element(by=By.ID, value="stu_profession"))
    add = driver.find_element(by=By.ID, value="add")

    stu_id.send_keys("116")
    name.send_keys("胡圖圖")
    if cnt & 1:
        female.click()
    else:
        male.click()
    age.send_keys("24")
    origin.send_keys("New York")
    pro.select_by_value(courses[cnt % len(courses)])
    add.click()

    WebDriverWait(driver, 10).until(EC.title_is("show"))

    driver.save_screenshot(f"png/{get_func_name()}_1.png")

    query_suc(driver, "胡圖圖", "116", get_func_name())

    driver.quit()
    cnt += 1


@pytest.mark.add
def test_add_success_en_szh():
    global cnt
    driver = login()

    driver.get("http://127.0.0.1:5000/add")

    name = driver.find_element(by=By.ID, value="stu_name")
    stu_id = driver.find_element(by=By.ID, value="stu_id")
    male = driver.find_element(by=By.ID, value="male")
    female = driver.find_element(by=By.ID, value="female")
    age = driver.find_element(by=By.ID, value="stu_age")
    origin = driver.find_element(by=By.ID, value="stu_origin")
    pro = Select(driver.find_element(by=By.ID, value="stu_profession"))
    add = driver.find_element(by=By.ID, value="add")

    stu_id.send_keys("117")
    name.send_keys("William Thompson")
    if cnt & 1:
        female.click()
    else:
        male.click()
    age.send_keys("24")
    origin.send_keys("威海")
    pro.select_by_value(courses[cnt % len(courses)])
    add.click()

    WebDriverWait(driver, 10).until(EC.title_is("show"))

    driver.save_screenshot(f"png/{get_func_name()}_1.png")

    query_suc(driver, "William Thompson", "117", get_func_name())

    driver.quit()
    cnt += 1


@pytest.mark.add
def test_add_success_szh_szh():
    global cnt
    driver = login()

    driver.get("http://127.0.0.1:5000/add")

    name = driver.find_element(by=By.ID, value="stu_name")
    stu_id = driver.find_element(by=By.ID, value="stu_id")
    male = driver.find_element(by=By.ID, value="male")
    female = driver.find_element(by=By.ID, value="female")
    age = driver.find_element(by=By.ID, value="stu_age")
    origin = driver.find_element(by=By.ID, value="stu_origin")
    pro = Select(driver.find_element(by=By.ID, value="stu_profession"))
    add = driver.find_element(by=By.ID, value="add")

    stu_id.send_keys("118")
    name.send_keys("田所浩二")
    if cnt & 1:
        female.click()
    else:
        male.click()
    age.send_keys("24")
    origin.send_keys("威海")
    pro.select_by_value(courses[cnt % len(courses)])
    add.click()

    WebDriverWait(driver, 10).until(EC.title_is("show"))

    driver.save_screenshot(f"png/{get_func_name()}_1.png")

    query_suc(driver, "田所浩二", "118", get_func_name())

    driver.quit()
    cnt += 1


@pytest.mark.add
def test_add_success_tzh_szh():
    global cnt
    driver = login()

    driver.get("http://127.0.0.1:5000/add")

    name = driver.find_element(by=By.ID, value="stu_name")
    stu_id = driver.find_element(by=By.ID, value="stu_id")
    male = driver.find_element(by=By.ID, value="male")
    female = driver.find_element(by=By.ID, value="female")
    age = driver.find_element(by=By.ID, value="stu_age")
    origin = driver.find_element(by=By.ID, value="stu_origin")
    pro = Select(driver.find_element(by=By.ID, value="stu_profession"))
    add = driver.find_element(by=By.ID, value="add")

    stu_id.send_keys("119")
    name.send_keys("胡圖圖")
    if cnt & 1:
        female.click()
    else:
        male.click()
    age.send_keys("24")
    origin.send_keys("威海")
    pro.select_by_value(courses[cnt % len(courses)])
    add.click()

    WebDriverWait(driver, 10).until(EC.title_is("show"))

    driver.save_screenshot(f"png/{get_func_name()}_1.png")

    query_suc(driver, "胡圖圖", "119", get_func_name())

    driver.quit()
    cnt += 1


@pytest.mark.add
def test_add_success_en_tzh():
    global cnt
    driver = login()

    driver.get("http://127.0.0.1:5000/add")

    name = driver.find_element(by=By.ID, value="stu_name")
    stu_id = driver.find_element(by=By.ID, value="stu_id")
    male = driver.find_element(by=By.ID, value="male")
    female = driver.find_element(by=By.ID, value="female")
    age = driver.find_element(by=By.ID, value="stu_age")
    origin = driver.find_element(by=By.ID, value="stu_origin")
    pro = Select(driver.find_element(by=By.ID, value="stu_profession"))
    add = driver.find_element(by=By.ID, value="add")

    stu_id.send_keys("120")
    name.send_keys("William Thompson")
    if cnt & 1:
        female.click()
    else:
        male.click()
    age.send_keys("24")
    origin.send_keys("下北澤")
    pro.select_by_value(courses[cnt % len(courses)])
    add.click()

    WebDriverWait(driver, 10).until(EC.title_is("show"))

    driver.save_screenshot(f"png/{get_func_name()}_1.png")

    query_suc(driver, "William Thompson", "120", get_func_name())

    driver.quit()
    cnt += 1


@pytest.mark.add
def test_add_success_szh_tzh():
    global cnt
    driver = login()

    driver.get("http://127.0.0.1:5000/add")

    name = driver.find_element(by=By.ID, value="stu_name")
    stu_id = driver.find_element(by=By.ID, value="stu_id")
    male = driver.find_element(by=By.ID, value="male")
    female = driver.find_element(by=By.ID, value="female")
    age = driver.find_element(by=By.ID, value="stu_age")
    origin = driver.find_element(by=By.ID, value="stu_origin")
    pro = Select(driver.find_element(by=By.ID, value="stu_profession"))
    add = driver.find_element(by=By.ID, value="add")

    stu_id.send_keys("121")
    name.send_keys("田所浩二")
    if cnt & 1:
        female.click()
    else:
        male.click()
    age.send_keys("24")
    origin.send_keys("下北澤")
    pro.select_by_value(courses[cnt % len(courses)])
    add.click()

    WebDriverWait(driver, 10).until(EC.title_is("show"))

    driver.save_screenshot(f"png/{get_func_name()}_1.png")

    query_suc(driver, "田所浩二", "121", get_func_name())

    driver.quit()
    cnt += 1


@pytest.mark.add
def test_add_success_tzh_tzh():
    global cnt
    driver = login()

    driver.get("http://127.0.0.1:5000/add")

    name = driver.find_element(by=By.ID, value="stu_name")
    stu_id = driver.find_element(by=By.ID, value="stu_id")
    male = driver.find_element(by=By.ID, value="male")
    female = driver.find_element(by=By.ID, value="female")
    age = driver.find_element(by=By.ID, value="stu_age")
    origin = driver.find_element(by=By.ID, value="stu_origin")
    pro = Select(driver.find_element(by=By.ID, value="stu_profession"))
    add = driver.find_element(by=By.ID, value="add")

    stu_id.send_keys("122")
    name.send_keys("胡圖圖")
    if cnt & 1:
        female.click()
    else:
        male.click()
    age.send_keys("24")
    origin.send_keys("下北澤")
    pro.select_by_value(courses[cnt % len(courses)])
    add.click()

    WebDriverWait(driver, 10).until(EC.title_is("show"))

    driver.save_screenshot(f"png/{get_func_name()}_1.png")

    query_suc(driver, "胡圖圖", "122", get_func_name())

    driver.quit()
    cnt += 1
