#!/usr/bin/env python3
"""The Daily Compass — Tuesday 24 November 2026.

Renders the front page for the make.fun news-image-20261124 entry: the
International Court of Justice's ruling that Myanmar committed genocide
against the Rohingya, NATO's pledge to defend space, the COP31 recriminations
and the United States losing its measles-free status. Drawn with PIL only;
writes entry.png next to itself.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 960, 1024
PAPER = (247, 243, 233)
INK = (26, 23, 18)
ACCENT = (140, 43, 29)
FAINT = (110, 102, 88)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = w if not cur else cur + " " + w
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, xy, text, fnt, width, leading, fill=INK):
    x, y = xy
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def centred(draw, y, text, fnt, fill=INK):
    draw.text(((W - draw.textlength(text, font=fnt)) / 2, y), text, font=fnt, fill=fill)
    return y


def rule(draw, y, weight=2):
    draw.line([(36, y), (W - 36, y)], fill=INK, width=weight)
    return y


def scales(draw, cx, cy):
    """A simple scales-of-justice mark: pillar, beam and two pans."""
    draw.line([(cx, cy - 74), (cx, cy + 74)], fill=INK, width=3)
    draw.line([(cx - 30, cy + 74), (cx + 30, cy + 74)], fill=INK, width=3)
    draw.line([(cx - 66, cy - 52), (cx + 66, cy - 52)], fill=INK, width=3)
    draw.ellipse([cx - 7, cy - 79, cx + 7, cy - 65], fill=INK)
    for sx in (cx - 66, cx + 66):
        draw.line([(sx, cy - 52), (sx, cy - 8)], fill=INK, width=2)
        draw.arc([sx - 26, cy - 12, sx + 26, cy + 28], 0, 180, fill=INK, width=3)
        draw.line([(sx - 26, cy + 8), (sx + 26, cy + 8)], fill=INK, width=3)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- top strip -------------------------------------------------------
    d.text((36, 14), "Vol. V — No. 328", font=font(SANS, 17), fill=FAINT)
    right = "THE HAGUE • BRUSSELS • ANTALYA"
    d.text((W - 36 - d.textlength(right, font=font(SANS, 17)), 14), right,
           font=font(SANS, 17), fill=FAINT)
    rule(d, 42, 1)

    # --- masthead --------------------------------------------------------
    size = 84
    while d.textlength("THE DAILY COMPASS", font=font(SERIF_B, size)) > W - 72:
        size -= 2
    centred(d, 52, "THE DAILY COMPASS", font(SERIF_B, size))
    rule(d, 146, 4)
    rule(d, 154, 1)
    centred(d, 162, "TUESDAY, 24 NOVEMBER 2026", font(SANS_B, 25))
    centred(d, 192, "The day's news, on one page", font(SERIF_I, 19), fill=FAINT)
    rule(d, 222, 2)

    # --- lead ------------------------------------------------------------
    d.text((36, 236), "THE HAGUE  •  WORLD COURT", font=font(SANS_B, 19), fill=ACCENT)
    y = para(d, (36, 262), "WORLD COURT: MYANMAR COMMITTED GENOCIDE",
             font(SERIF_B, 49), W - 72, 52)
    y = para(d, (36, y + 4),
             "The ICJ's verdict on the Rohingya wins backing from fourteen nations — "
             "and a reckoning for the world's courts",
             font(SERIF_I, 21), W - 72, 26, fill=(60, 54, 44))

    scales(d, 140, y + 100)
    lead = ("THE HAGUE — The International Court of Justice has ruled that Myanmar "
            "committed genocide against the Rohingya, in a judgment that drew backing "
            "on Monday from fourteen countries — the United Kingdom, Spain, Canada "
            "and Australia among them — which affirmed they recognise the decision. "
            "The court found the military's campaign against the minority amounted "
            "to genocide, the gravest crime under international law, and its ruling "
            "is binding on Myanmar. Campaigners called it a landmark for "
            "accountability; the focus now turns to whether the world will enforce it.")
    y = para(d, (248, y + 22), lead, font(SERIF, 17), W - 248 - 36, 22)
    rule(d, y + 14, 1)

    # --- three panels ------------------------------------------------------
    top = y + 28
    colw = (W - 72 - 2 * 24) // 3
    panels = [
        ("NATO VOWS TO DEFEND SPACE",
         "BRUSSELS — Nato chief Mark Rutte said the alliance will defend against "
         "any threat in space, after reports that Russia may place a nuclear "
         "weapon in orbit as soon as next month."),
        ("“HELD HOSTAGE BY THE PETROLEUM MAFIA”",
         "ANTALYA — The recriminations over COP31's collapse spread on Tuesday: "
         "Panama's environment minister said his country was “being held hostage "
         "by the petroleum mafia”. Focus shifts to COP32 in Addis Ababa."),
        ("US LOSES MEASLES-FREE STATUS",
         "WASHINGTON — The United States has lost its measles elimination status "
         "after more than 25 years, as the virus spreads again — Pennsylvania "
         "recorded a ninth death in an epidemic spanning 46 counties."),
    ]
    bottom = top
    for idx, (head, body) in enumerate(panels):
        x = 36 + idx * (colw + 24)
        hy = para(d, (x, top), head, font(SERIF_B, 18), colw, 22, fill=ACCENT)
        by = para(d, (x, hy + 6), body, font(SERIF, 14), colw, 19)
        bottom = max(bottom, by)
        if idx:
            d.line([(x - 12, top), (x - 12, bottom)], fill=FAINT, width=1)

    # --- briefs ------------------------------------------------------------
    by = bottom + 14
    rule(d, by, 2)
    d.text((36, by + 10), "THE DAY IN BRIEF", font=font(SANS_B, 19), fill=ACCENT)
    briefs = ("Israeli strikes in Gaza kill at least six, including a Hamas security "
              "chief  •  Iraq orders takeover of oilfields in Kurdish-controlled "
              "areas  •  Russian jets enter South Korea's air defence zone  •  Seoul "
              "stocks jump 6% as the Nvidia rebound lifts markets")
    by = para(d, (36, by + 36), briefs, font(SERIF, 15), W - 72, 20)
    rule(d, by + 10, 1)
    centred(d, by + 18, "The Daily Compass — Tuesday 24 November 2026 — Page 1 of 1",
            font(SANS, 15), fill=FAINT)

    img.save("entry.png", optimize=True)
    print("final y:", by + 44)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
