#!/usr/bin/env python3
"""Build-time renderer for the 27 November 2026 front page.

Draws a one-page newspaper front page (1024x1024 PNG) with PIL and saves
it as entry.png next to this script. Run once at build time; main.py only
copies the finished image, so the graded program needs no PIL and no
network. All six stories were first reported on Friday 27 November 2026.
"""
import os

from PIL import Image, ImageDraw, ImageFont

CANVAS_W, CANVAS_H = 1024, 1024
SAVE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "entry.png")

PAPER = (250, 246, 236)
INK = (18, 18, 20)
SOFT_INK = (64, 61, 55)
MID_GREY = (96, 93, 86)
HAIRLINE = (168, 162, 150)
CRIMSON = (172, 28, 28)
SKY = (196, 214, 226)
SLATE = (52, 68, 92)
AMBER = (226, 138, 24)
LEAF = (24, 108, 78)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def load_font(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(canvas, text, fnt, max_width):
    """Greedy word wrap: lines of `text` that fit inside max_width."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = (current + " " + word).strip()
        if canvas.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def para(canvas, origin, text, fnt, max_width, fill, leading=4):
    """Draw wrapped text at origin; return the y below the last line."""
    x, y = origin
    for line in wrap_text(canvas, text, fnt, max_width):
        canvas.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + leading
    return y


def hrule(canvas, x0, y, x1, width=2, colour=HAIRLINE):
    canvas.line([(x0, y), (x1, y)], fill=colour, width=width)


def kicker(canvas, x, y, text):
    fnt = load_font(SANS_BOLD, 18)
    canvas.text((x, y), text, font=fnt, fill=CRIMSON)
    return y + 25


def icon_drone(canvas, x, y, w, h):
    """Quadcopter drone over a blast star, for the Kuwait strike."""
    canvas.rectangle([x, y, x + w, y + h], fill=SKY, outline=SLATE, width=2)
    cx, cy = x + w // 2, y + h // 2 - 8
    burst = []
    for i in range(12):
        ang = 3.14159 * 2 * i / 12
        r = 52 if i % 2 == 0 else 26
        import math
        burst.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    canvas.polygon(burst, fill=(240, 196, 60), outline=AMBER)
    canvas.ellipse([cx - 26, cy - 14, cx + 26, cy + 14], fill=INK)
    canvas.ellipse([cx - 7, cy - 5, cx + 7, cy + 5], fill=CRIMSON)
    for dx, dy in [(-38, -22), (38, -22), (-38, 22), (38, 22)]:
        canvas.line([(cx, cy), (cx + dx, cy + dy)], fill=INK, width=4)
        canvas.line([(cx + dx - 16, cy + dy), (cx + dx + 16, cy + dy)],
                    fill=INK, width=5)
    canvas.line([(x, y + h - 14), (x + w, y + h - 14)], fill=LEAF, width=3)


def icon_rubble(canvas, x, y, w, h):
    """Toppled concrete blocks and dust, for the Gaza strikes."""
    canvas.rectangle([x, y, x + w, y + h], fill=(232, 226, 214),
                     outline=MID_GREY, width=2)
    blocks = [(x + 18, y + h - 34, 74, 22, -6), (x + 96, y + h - 30, 66, 20, 8),
              (x + 52, y + h - 58, 70, 22, -3), (x + 120, y + h - 62, 58, 20, 12),
              (x + 84, y + h - 86, 60, 20, -9)]
    for bx, by, bw, bh, tilt in blocks:
        canvas.rectangle([bx, by, bx + bw, by + bh], fill=(120, 116, 106),
                         outline=INK, width=2)
    for dx, dy, r in [(x + 30, y + 22, 4), (x + 70, y + 14, 3),
                      (x + 150, y + 26, 4), (x + 110, y + 34, 3)]:
        canvas.ellipse([dx - r, dy - r, dx + r, dy + r], fill=MID_GREY)


def icon_tanker(canvas, x, y, w, h):
    """A capsized tanker hull with waves and an oil drop, for Ibiza."""
    canvas.rectangle([x, y, x + w, y + h], fill=SKY, outline=SLATE, width=2)
    canvas.polygon([(x + 22, y + 52), (x + w - 26, y + 52),
                    (x + w - 52, y + 92), (x + 48, y + 92)], fill=INK)
    canvas.rectangle([x + 60, y + 30, x + 96, y + 52], fill=CRIMSON)
    canvas.line([(x + 14, y + 108), (x + w - 14, y + 108)], fill=SLATE, width=4)
    canvas.line([(x + 30, y + 122), (x + w - 40, y + 122)], fill=SLATE, width=3)
    dx, dy = x + w - 44, y + 26
    canvas.ellipse([dx - 12, dy - 4, dx + 12, dy + 14], fill=INK)
    canvas.polygon([(dx, dy - 18), (dx - 11, dy + 2), (dx + 11, dy + 2)],
                   fill=INK)


def icon_bars_down(canvas, x, y, w, h):
    """Falling bars for the UK migration chart."""
    canvas.rectangle([x, y, x + w, y + h], fill=(255, 255, 255),
                     outline=MID_GREY, width=2)
    canvas.line([(x + 12, y + h - 14), (x + w - 10, y + h - 14)],
                fill=INK, width=2)
    heights = [62, 50, 38, 24]
    for i, bh in enumerate(heights):
        bx = x + 18 + i * 34
        canvas.rectangle([bx, y + h - 14 - bh, bx + 24, y + h - 14],
                         fill=SLATE if i < 3 else CRIMSON)
    canvas.text((x + 12, y + 6), "LOWEST SINCE 1997",
                font=load_font(SANS_BOLD, 15), fill=CRIMSON)


def icon_rook(canvas, x, y, w, h):
    """A chess rook, for the World Championship match."""
    canvas.rectangle([x, y, x + w, y + h], fill=(232, 226, 214),
                     outline=MID_GREY, width=2)
    cx = x + w // 2
    canvas.rectangle([cx - 34, y + 22, cx + 34, y + 46], fill=INK)
    for notch in (-22, 0, 22):
        canvas.rectangle([cx + notch - 8, y + 12, cx + notch + 8, y + 24],
                         fill=INK)
    canvas.polygon([(cx - 26, y + 46), (cx + 26, y + 46),
                    (cx + 40, y + 96), (cx - 40, y + 96)], fill=INK)
    canvas.rectangle([cx - 46, y + 96, cx + 46, y + 110], fill=INK)


def icon_gavel(canvas, x, y, w, h):
    """A judge's gavel over a sound block, for the Depardieu trial."""
    canvas.rectangle([x, y, x + w, y + h], fill=(232, 226, 214),
                     outline=MID_GREY, width=2)
    canvas.line([(x + 30, y + 88), (x + w - 30, y + 30)], fill=(120, 74, 30),
                width=10)
    canvas.rectangle([x + w - 78, y + 12, x + w - 30, y + 40], fill=INK)
    canvas.rectangle([x + 28, y + 96, x + 92, y + 110], fill=SLATE)


def story(canvas, x, y, w, icon, tag, headline, body, head_size=25):
    """One secondary story: icon box, kicker, headline, body. Returns the
    y just below the block."""
    icon(canvas, x, y, 190, 108)
    yy = y + 118
    yy = kicker(canvas, x, yy, tag)
    yy = para(canvas, (x, yy), headline, load_font(SERIF_BOLD, head_size),
              w, INK, leading=2)
    yy = para(canvas, (x, yy + 5), body, load_font(SANS, 18), w, SOFT_INK,
              leading=3)
    return yy


def render():
    img = Image.new("RGB", (CANVAS_W, CANVAS_H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([8, 8, CANVAS_W - 9, CANVAS_H - 9], outline=INK, width=2)

    # ---- Masthead ----
    d.rectangle([0, 0, CANVAS_W, 96], fill=INK)
    d.text((512, 8), "THE WORLD", font=load_font(SERIF_BOLD, 62),
           fill=PAPER, anchor="ma")
    d.rectangle([0, 96, CANVAS_W, 132], fill=CRIMSON)
    d.text((512, 103),
           "FRIDAY  •  27 NOVEMBER 2026  •  THE DAY'S WORLD NEWS IN ONE PAGE",
           font=load_font(SANS_BOLD, 20), fill=PAPER, anchor="ma")

    # ---- Hero: Kuwait drone strike ----
    hy = 150
    kicker(d, 24, hy, "MIDDLE EAST  •  KUWAIT")
    y = para(d, (24, hy + 28),
             "Iranian drones kill two Italians in Kuwait",
             load_font(SERIF_BOLD, 46), 640, INK, leading=2)
    para(d, (24, y + 10),
         "Italy and Kuwait blame Iran for the strike on an air-defence "
         "station, where two Rheinmetall technicians died and two more "
         "people were hurt. Tehran denies any role.",
         load_font(SANS, 22), 640, SOFT_INK, leading=4)
    icon_drone(d, 700, 168, 300, 210)
    d.text((700, 384), "Drones hit a Kuwaiti air-defence site.",
           font=load_font(SANS, 16), fill=MID_GREY)
    hrule(d, 24, 428, 1000, width=2, colour=INK)

    # ---- Row A: Gaza | Ibiza ----
    ya = 444
    story(d, 24, ya, 460, icon_rubble, "GAZA",
          "Israel kills 10 in Gaza as Hamas weighs reply",
          "Ten people are killed in Israeli strikes, and Hamas weighs its "
          "response to the latest escalation.")
    d.line([(512, ya), (512, ya + 236)], fill=HAIRLINE, width=2)
    story(d, 540, ya, 460, icon_tanker, "SPAIN  •  IBIZA",
          "Tanker capsizes off Ibiza; one dead, oil spill feared",
          "A diesel tanker carrying up to 7,000 tonnes capsizes. Spain "
          "races to stop the spill.")
    hrule(d, 24, 700, 1000, width=2)

    # ---- Row B: three columns ----
    yb = 710
    col_w, gap = 306, 24
    story(d, 24, yb, col_w, icon_bars_down, "BRITAIN",
          "UK net migration falls to lowest since 1997",
          "Net migration falls to its lowest in nearly three decades.",
          head_size=22)
    d.line([(354, yb), (354, yb + 220)], fill=HAIRLINE, width=2)
    story(d, 360, yb, col_w, icon_rook, "CHESS  •  WORLD TITLE",
          "Gukesh, Sindarov draw marathon Game 3",
          "Nothing separates the two after three games.",
          head_size=22)
    d.line([(690, yb), (690, yb + 220)], fill=HAIRLINE, width=2)
    story(d, 696, yb, col_w, icon_gavel, "FRANCE  •  COURT",
          "Depardieu to stand trial for alleged rape",
          "A French court orders the actor to face trial over a 2018 "
          "allegation.", head_size=22)
    hrule(d, 24, 956, 1000, width=2, colour=INK)

    # ---- Footer strip ----
    fy = 962
    d.text((24, fy), "ALSO TODAY:", font=load_font(SANS_BOLD, 17),
           fill=CRIMSON)
    d.text((150, fy),
           "Ebola in Congo passes 12,000 cases  •  Nepal declares 4,000 "
           "missing dead  •  Trump seeks GDP probe",
           font=load_font(SANS, 16), fill=MID_GREY)
    d.text((512, 992), "All stories first reported Friday 27 November 2026",
           font=load_font(SANS, 14), fill=MID_GREY, anchor="ma")

    img.save(SAVE_PATH, format="PNG", optimize=True)
    print("wrote", SAVE_PATH, os.path.getsize(SAVE_PATH), "bytes")


if __name__ == "__main__":
    render()
