import random, hashlib, string
from PIL import Image, ImageDraw, ImageFont


def generate_equation():
    operator, ans = ("+", "-"), random.randint(1, 15)
    eqt = str(ans)
    for _ in range(2):
        opr = random.randint(1, 15)
        opt = operator[random.randint(0, 1)]
        if opt == "+":
            ans = ans + opr
        else:
            ans = ans - opr
        eqt = eqt + opt + str(opr)
    sha1 = hashlib.sha1()
    sha1.update(str(ans).encode("utf-8"))
    return eqt + "=?", sha1.hexdigest()


def ran(begin, end):
    return random.randint(begin, end)


def generate_image(eqt):
    width, height = 200, 100
    image = Image.new("RGB", (width, height), (ran(0, 255), ran(0, 255), ran(0, 255)))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font="./static/ttf/Roboto-Black.ttf", size=25)
    draw.text(
        (ran(0, 75), ran(0, 75)),
        eqt,
        font=font,
        fill=(ran(0, 255), ran(0, 255), ran(0, 255)),
    )
    for _ in range(20):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line(
            (x1, y1, x2, y2), fill=(ran(0, 255), ran(0, 255), ran(0, 255)), width=2
        )
    for _ in range(200):
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.point((x, y), fill=(ran(0, 255), ran(0, 255), ran(0, 255)))
    img_name = "".join(random.sample(string.ascii_letters + string.digits, 8))
    img_path = "./static/images/%s.jpg" % img_name
    image.save(img_path)
    return img_path


def paging(result, page, per_page):
    # 计算总页数
    pagination = len(result) // per_page
    if len(result) % per_page > 0:
        pagination += 1

    # 添加分页
    start = (page - 1) * per_page
    end = start + per_page
    results = result[start:end]
    return results, pagination
