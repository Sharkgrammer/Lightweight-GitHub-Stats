from collections import OrderedDict

import io

import settings as s
import strings as strings
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont, ImageOps

from utils import get_linguist_colours


def create_big_image(data):
    w = s.OVERALL_WIDTH
    h = s.OVERALL_HEIGHT

    img = setup_background(w, h)
    draw = ImageDraw.Draw(img)

    # Font Prep
    font = ImageFont.load_default(s.ITEM_FONT_SIZE)
    fill = s.IMAGE_THEME["text_col"]

    # Title code
    title_height_adj = 0

    if s.SHOW_TITLE_TEXT:
        title_font = ImageFont.load_default(s.TITLE_FONT_SIZE)

        text = f"{data['name'] if s.TITLE_USE_REAL_NAME else data['username']}{strings.TITLE_POSTFIX}"
        text_len = title_font.getlength(text)

        y = 10
        x = (w / 2) - (text_len / 2)

        draw.text((x, y), text, fill=fill, font=title_font)

        y = y + s.TITLE_FONT_SIZE + s.TITLE_LINE_VADJ

        draw.line((x - s.TITLE_LINE_HADJ, y, x + text_len + s.TITLE_LINE_HADJ, y), fill=fill, width=s.TITLE_LINE_WIDTH)
    else:
        # If you don't display title, move the contents up to be centered
        title_height_adj = int((10 + s.TITLE_FONT_SIZE + s.TITLE_LINE_VADJ) / 2)

    # Create and add the language graph
    lan = data["languages"]

    if len(lan) > 0:
        graph_img = create_graph(lan, s.GRAPH_WIDTH, s.GRAPH_HEIGHT)
        img.paste(graph_img, (w - s.GRAPH_WIDTH - s.ITEM_STARTING_X, 0 - title_height_adj), graph_img)

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

    y = s.ITEM_STARTING_Y - title_height_adj
    x = s.ITEM_STARTING_X + s.ITEM_IMG_SIZE + s.ITEM_TEXT_HADJ

    item_text_adj = int((s.ITEM_FONT_SIZE / 2))

    icon_fill = s.IMAGE_THEME["icon_col"]

    for item in items:
        add_icon_to_image(img, item, (s.ITEM_STARTING_X, y), icon_fill)

        draw.text((x, y + item_text_adj), items[item], fill=fill, font=font)

        y += s.ITEM_VADJ

    img = add_rounded_corners(img, s.IMAGE_BORDER_RADIUS)

    img.save("data.png", "PNG", dpi=(300, 300))


def create_graph_image(data):
    w = s.OVERALL_WIDTH
    h = s.OVERALL_HEIGHT

    img = setup_background(w, h)

    lan = data["languages"]

    if len(lan) > 0:
        graph_height = s.GRAPH_HEIGHT
        graph_width = s.GRAPH_WIDTH

        if h < graph_height:
            graph_height = h
            graph_width = h

        graph_img = create_graph(lan, graph_height, graph_width)
        img.paste(graph_img, (int((w - graph_width) / 2), 0), graph_img)

    img = add_rounded_corners(img, s.IMAGE_BORDER_RADIUS)

    img.save("graph.png", "PNG", dpi=(300, 300))


def create_stats_image(data):
    w = s.OVERALL_WIDTH
    h = s.OVERALL_HEIGHT

    img = setup_background(w, h)
    draw = ImageDraw.Draw(img)

    # Font Prep
    font = ImageFont.load_default(s.STAT_ITEM_FONT_SIZE)
    fill = s.IMAGE_THEME["text_col"]
    icon_fill = s.IMAGE_THEME["icon_col"]

    # Code for each of the displayed items
    items = {}
    items_contrib = {}

    if s.DISPLAY_STARS:
        items["star.png"] = parse_text(data['stars'], strings.ITEM_STAR)

    if s.DISPLAY_REPOS:
        items["repo.png"] = parse_text(data['repos'], strings.ITEM_REPO)

    if s.DISPLAY_COMMITS:
        items_contrib["commit.png"] = parse_text(data['commits'], strings.ITEM_COMMIT)

    if s.DISPLAY_REQUESTS:
        items_contrib["request.png"] = parse_text(data['requests'], strings.ITEM_REQUEST)

    if s.DISPLAY_REVIEWS:
        items_contrib["review.png"] = parse_text(data['reviews'], strings.ITEM_REVIEW)

    if s.DISPLAY_ISSUES:
        items_contrib["issue.png"] = parse_text(data['issues'], strings.ITEM_ISSUE)

    y = 200

    box_size = s.STAT_ITEM_IMG_SIZE * 4
    item_count = len(items_contrib)
    total_width = (box_size * item_count) + (s.STAT_LINE_SIZE * item_count - 1)

    x = int((w - total_width) / 2)

    text = strings.STAT_TITLE_TEXT

    title_font = ImageFont.load_default(s.STAT_TITLE_FONT_SIZE)
    text_len = title_font.getlength(text)

    draw.text(((w / 2) - (text_len / 2), y), text, fill=fill, font=title_font)
    y += s.STAT_TITLE_FONT_SIZE + s.STAT_TITLE_LINE_VADJ

    draw.line((x, y, x + total_width, y), fill=fill, width=s.STAT_LINE_SIZE)

    y += int(s.STAT_TITLE_LINE_VADJ * 2.5)
    item_text_adj = int(s.STAT_ITEM_FONT_SIZE / 4)

    counter = 0

    for item in items_contrib:
        temp_y = y
        text = items_contrib[item]
        text_pos = text.index(" ")

        add_icon_to_image(img, item, (x + int((box_size - s.STAT_ITEM_IMG_SIZE) / 2), temp_y), icon_fill,
                          s.STAT_ITEM_IMG_SIZE)

        temp_y += s.STAT_ITEM_IMG_SIZE + item_text_adj

        draw_stats_text_data(draw, text[0:text_pos], x, temp_y, box_size, fill, font)
        temp_y += s.STAT_ITEM_FONT_SIZE + item_text_adj

        draw_stats_text_data(draw, text[text_pos:len(text)], x, temp_y, box_size, fill, font)

        x += box_size

        if counter < item_count - 1:
            draw.line((x, y - s.STAT_LINE_ADJ, x, temp_y + s.STAT_ITEM_FONT_SIZE + item_text_adj + s.STAT_LINE_ADJ),
                      fill=fill, width=s.STAT_LINE_SIZE)

        counter += 1

    img = add_rounded_corners(img, s.IMAGE_BORDER_RADIUS)

    img.save("stats.png", "PNG", dpi=(300, 300))


def draw_stats_text_data(draw, text, x, y, box_size, fill, font):
    size = font.getlength(text)

    draw.text((x + int(abs(box_size - size) / 2), y), text, fill=fill, font=font)


def add_rounded_corners(img, radius):
    if "background_col" in s.IMAGE_THEME:
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
    else:
        return img


def setup_background(w, h):
    if "background_col" in s.IMAGE_THEME:
        return Image.new('RGB', (w, h), color=s.IMAGE_THEME["background_col"])
    else:
        return Image.new('RGBA', (w, h), color=(255, 255, 255, 0))


def add_icon_to_image(img, icon, xy, fill, size=s.ITEM_IMG_SIZE):
    path = f"./app/img/{icon}"

    img_icon = Image.open(path).convert("RGBA")

    icon_data = img_icon.getdata()

    changed_img = []
    for p in icon_data:

        if p[0] == 255 and p[3] != 0:
            changed_img.append(fill)

        else:
            changed_img.append(p)

    img_icon.putdata(changed_img)

    img_icon = img_icon.resize((size, size))

    img.paste(img_icon, xy, img_icon)

    return img


def parse_text(amount, text, yearly=False):
    return (f"{amount if amount > 0 else strings.ZERO_TEXT} {text}"
            f"{strings.PLURAL_POSTFIX if (amount > 1 or amount == 0) else ''} "
            f"{strings.ITEM_YEAR if yearly else ''}")


def create_graph(lan, w, h):
    lan = OrderedDict(sorted(lan.items(), key=lambda item: item[1], reverse=True))

    colours = []
    if not s.USE_LINGUIST_COLOURS:
        colours = plt.cm.tab10.colors
    else:
        all_colours = get_linguist_colours()

        for key in lan:
            colours.append(all_colours[key]["color"])

    labels = list(lan.keys())
    values = list(lan.values())

    fig, ax = plt.subplots(figsize=(6, 6))

    if s.SHOW_TOP_LANGUAGES:
        max_len = min(3, len(lan))

        text = (f"{strings.LAN_PREFIX} {str(max_len) + ' ' if max_len > 1 else ''}{strings.LAN_POSTFIX}"
                f"{strings.PLURAL_POSTFIX if max_len > 1 else ''}\n") if s.SHOW_TOP_LANGUAGES_TEXT else ""

        for x in range(0, max_len):
            text += f"{str(labels[x])}\n"

        text = text[:-1]

        ax.text(0, 0, text, fontsize=s.GRAPH_FONT_SIZE, ha='center', va='center', color=s.IMAGE_THEME["text_col"])

    plt.pie(values, labels=labels, textprops={'color': s.IMAGE_THEME["text_col"], 'fontsize': s.GRAPH_FONT_SIZE},
            wedgeprops={'width': 0.4}, colors=colours)

    # Finally, convert the figure to a pillow image
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=200, transparent=True)

    buf.seek(0)
    img = Image.open(buf).resize((w, h)).convert("RGBA")

    return img
