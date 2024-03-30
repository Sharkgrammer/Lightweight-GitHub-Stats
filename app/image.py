from collections import OrderedDict

import io

import settings as s
import strings as strings
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont, ImageOps


def create_image(data):
    w = 600
    h = 350

    if "background_col" in s.IMAGE_THEME:
        img = Image.new('RGB', (w, h), color=s.IMAGE_THEME["background_col"])
    else:
        img = Image.new('RGBA', (w, h), color=(255, 255, 255, 0))

    draw = ImageDraw.Draw(img)

    # Create and add the language graph
    lan = data["languages"]

    if len(lan) > 0:
        graph_img = create_graph(data["languages"])
        img.paste(graph_img, (200, 0), graph_img)

    title_font = ImageFont.load_default(s.TITLE_FONT_SIZE)
    font = ImageFont.load_default(s.ITEM_FONT_SIZE)
    fill = s.IMAGE_THEME["text_col"]

    # Title code
    text = f"{data['name'] if s.TITLE_USE_REAL_NAME else data['username']}{strings.TITLE_POSTFIX}"

    text_len = title_font.getlength(text)

    y = 10
    x = (w / 2) - (text_len / 2)

    draw.text((x, y), text, fill=fill, font=title_font)

    y = y + s.TITLE_FONT_SIZE + s.TITLE_LINE_VADJ

    draw.line((x - s.TITLE_LINE_HADJ, y, x + text_len + s.TITLE_LINE_HADJ, y), fill=fill, width=s.TITLE_LINE_WIDTH)

    # Code for each of the displayed items
    items = {}

    if s.DISPLAY_STARS:
        items["star.png"] = parse_text(data['stars'], strings.ITEM_STAR)

    if s.DISPLAY_REPOS:
        items["repo.png"] = parse_text(data['repos'], strings.ITEM_REPO)

    if s.DISPLAY_COMMITS:
        items["commit.png"] = parse_text(data['commits'], strings.ITEM_COMMIT, True)

    if s.DISPLAY_REQUESTS:
        items["request.png"] = parse_text(data['requests'], strings.ITEM_REQUEST, True)

    if s.DISPLAY_REVIEWS:
        items["review.png"] = parse_text(data['reviews'], strings.ITEM_REVIEW, True)

    if s.DISPLAY_ISSUES:
        items["issue.png"] = parse_text(data['issues'], strings.ITEM_ISSUE, True)

    y = s.ITEM_STARTING_Y
    x = s.ITEM_STARTING_X + s.ITEM_IMG_SIZE + s.ITEM_TEXT_HADJ

    item_text_adj = int((s.ITEM_FONT_SIZE / 2))

    icon_fill = s.IMAGE_THEME["icon_col"]

    for item in items:
        add_icon_to_image(img, item, (s.ITEM_STARTING_X, y), icon_fill)

        draw.text((x, y + item_text_adj), items[item], fill=fill, font=font)

        y += s.ITEM_VADJ

    if "background_col" in s.IMAGE_THEME:
        img = add_rounded_corners(img, s.IMAGE_BORDER_RADIUS)

    img.save("data.png", "PNG", dpi=(300, 300))
    # img.show()


def add_rounded_corners(img, radius):
    fill = 255
    double_radius = radius * 2
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    width, height = img.size

    draw.pieslice((width - double_radius, height - double_radius, width, height), 0, 90, fill=fill)
    draw.pieslice((0, height - double_radius, double_radius, height), 90, 180, fill=fill)
    draw.pieslice((0, 0, double_radius, double_radius), 180, 270, fill=fill)
    draw.pieslice((width - double_radius, 0, width, double_radius), 270, 360, fill=fill)

    draw.rectangle((radius, 0, width - radius, height), fill=fill)
    draw.rectangle((0, radius, width, height - radius), fill=fill)

    rounded_image = ImageOps.fit(img, mask.size, method=0, bleed=0.0, centering=(0.5, 0.5))
    rounded_image.putalpha(mask)

    return rounded_image


def add_icon_to_image(img, icon, xy, fill):
    img_icon = Image.open(f"./app/img/{icon}").convert("RGBA")

    icon_data = img_icon.getdata()

    changed_img = []
    for p in icon_data:

        if p[0] == 255 and p[3] != 0:
            changed_img.append(fill)

        else:
            changed_img.append(p)

    img_icon.putdata(changed_img)

    img_icon = img_icon.resize((s.ITEM_IMG_SIZE, s.ITEM_IMG_SIZE))

    img.paste(img_icon, xy, img_icon)

    return img


def parse_text(amount, text, yearly=False):
    return (f"{amount if amount > 0 else strings.ZERO_TEXT} {text}"
            f"{strings.PLURAL_POSTFIX if (amount > 1 or amount == 0) else ''} "
            f"{strings.ITEM_YEAR if yearly else ''}")


def create_graph(lan):
    lan = OrderedDict(sorted(lan.items(), key=lambda item: item[1], reverse=True))

    labels = list(lan.keys())
    values = list(lan.values())

    fig, ax = plt.subplots(figsize=(6, 6))

    if s.SHOW_TOP_LANGUAGES:
        max_len = min(3, len(lan))

        text = (f"{strings.LAN_PREFIX} {str(max_len) + ' ' if max_len > 1 else ''}{strings.LAN_POSTFIX}"
                f"{strings.PLURAL_POSTFIX if max_len > 1 else ''}\n")

        for x in range(0, max_len):
            text += f"{str(labels[x])}\n"

        text = text[:-1]

        ax.text(0, 0, text, size="x-large", ha='center', va='center', color=s.IMAGE_THEME["text_col"])

    plt.pie(values, labels=labels, textprops={'color': s.IMAGE_THEME["text_col"], 'size': 'medium'},
            wedgeprops={'width': 0.4})

    # Finally, convert the figure to a pillow image
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=200, transparent=True)

    buf.seek(0)
    img = Image.open(buf).resize((400, 400)).convert("RGBA")

    return img
