#!/usr/bin/env python
# encoding: utf-8
# Généré par Mocodo 2.3.9 le Mon, 21 Mar 2022 16:14:09

from __future__ import division
from math import hypot

import time, codecs

(width,height) = (620,528)
cx = {
    u"Calendrier":  335,
    u"Paru"      :  335,
    u"Consoles"  :   61,
    u"Executer"  :  192,
    u"Jeux"      :  335,
    u"Avoir"     :  461,
    u"Genres"    :  567,
    u"Publier"   :  335,
    u"Editeurs"  :  335,
}
cy = {
    u"Calendrier":   39,
    u"Paru"      :  122,
    u"Consoles"  :  256,
    u"Executer"  :  256,
    u"Jeux"      :  256,
    u"Avoir"     :  256,
    u"Genres"    :  256,
    u"Publier"   :  390,
    u"Editeurs"  :  481,
}
shift = {
    u"Paru,Calendrier"  :    0,
    u"Paru,Jeux"        :    0,
    u"Executer,Consoles":    0,
    u"Executer,Jeux"    :    0,
    u"Avoir,Jeux"       :    0,
    u"Avoir,Genres"     :    0,
    u"Publier,Jeux"     :    0,
    u"Publier,Editeurs" :    0,
}
colors = {
    u"annotation_color"                : '#060707',
    u"annotation_text_color"           : '#E2EED0',
    u"association_attribute_text_color": '#607734',
    u"association_cartouche_color"     : '#b2bba4',
    u"association_cartouche_text_color": '#27360c',
    u"association_color"               : '#ccd6ba',
    u"association_stroke_color"        : '#85956b',
    u"background_color"                : 'none',
    u"card_text_color"                 : '#726f83',
    u"entity_attribute_text_color"     : '#3e3c42',
    u"entity_cartouche_color"          : '#97b8ff',
    u"entity_cartouche_text_color"     : '#131114',
    u"entity_color"                    : '#c0d4ff',
    u"entity_stroke_color"             : '#578dff',
    u"label_text_color"                : '#726f83',
    u"leg_stroke_color"                : '#726f83',
    u"transparent_color"               : 'none',
}
card_max_width = 19
card_max_height = 14
card_margin = 5
arrow_width = 12
arrow_half_height = 6
arrow_axis = 8
card_baseline = 3

def cmp(x, y):
    return (x > y) - (x < y)

def offset(x, y):
    return (x + card_margin, y - card_baseline - card_margin)

def line_intersection(ex, ey, w, h, ax, ay):
    if ax == ex:
        return (ax, ey + cmp(ay, ey) * h)
    if ay == ey:
        return (ex + cmp(ax, ex) * w, ay)
    x = ex + cmp(ax, ex) * w
    y = ey + (ay-ey) * (x-ex) / (ax-ex)
    if abs(y-ey) > h:
        y = ey + cmp(ay, ey) * h
        x = ex + (ax-ex) * (y-ey) / (ay-ey)
    return (x, y)

def straight_leg_factory(ex, ey, ew, eh, ax, ay, aw, ah, cw, ch):
    
    def card_pos(twist, shift):
        compare = (lambda x1_y1: x1_y1[0] < x1_y1[1]) if twist else (lambda x1_y1: x1_y1[0] <= x1_y1[1])
        diagonal = hypot(ax-ex, ay-ey)
        correction = card_margin * 1.4142 * (1 - abs(abs(ax-ex) - abs(ay-ey)) / diagonal) - shift
        (xg, yg) = line_intersection(ex, ey, ew, eh + ch, ax, ay)
        (xb, yb) = line_intersection(ex, ey, ew + cw, eh, ax, ay)
        if compare((xg, xb)):
            if compare((xg, ex)):
                if compare((yb, ey)):
                    return (xb - correction, yb)
                return (xb - correction, yb + ch)
            if compare((yb, ey)):
                return (xg, yg + ch - correction)
            return (xg, yg + correction)
        if compare((xb, ex)):
            if compare((yb, ey)):
                return (xg - cw, yg + ch - correction)
            return (xg - cw, yg + correction)
        if compare((yb, ey)):
            return (xb - cw + correction, yb)
        return (xb - cw + correction, yb + ch)
    
    def arrow_pos(direction, ratio):
        (x0, y0) = line_intersection(ex, ey, ew, eh, ax, ay)
        (x1, y1) = line_intersection(ax, ay, aw, ah, ex, ey)
        if direction == "<":
            (x0, y0, x1, y1) = (x1, y1, x0, y0)
        (x, y) = (ratio * x0 + (1 - ratio) * x1, ratio * y0 + (1 - ratio) * y1)
        return (x, y, x1 - x0, y0 - y1)
    
    straight_leg_factory.card_pos = card_pos
    straight_leg_factory.arrow_pos = arrow_pos
    return straight_leg_factory


def curved_leg_factory(ex, ey, ew, eh, ax, ay, aw, ah, cw, ch, spin):
    
    def bisection(predicate):
        (a, b) = (0, 1)
        while abs(b - a) > 0.0001:
            m = (a + b) / 2
            if predicate(bezier(m)):
                a = m
            else:
                b = m
        return m
    
    def intersection(left, top, right, bottom):
       (x, y) = bezier(bisection(lambda p: left <= p[0] <= right and top <= p[1] <= bottom))
       return (int(round(x)), int(round(y)))
    
    def card_pos(shift):
        diagonal = hypot(ax-ex, ay-ey)
        correction = card_margin * 1.4142 * (1 - abs(abs(ax-ex) - abs(ay-ey)) / diagonal)
        (top, bot) = (ey - eh, ey + eh)
        (TOP, BOT) = (top - ch, bot + ch)
        (lef, rig) = (ex - ew, ex + ew)
        (LEF, RIG) = (lef - cw, rig + cw)
        (xr, yr) = intersection(LEF, TOP, RIG, BOT)
        (xg, yg) = intersection(lef, TOP, rig, BOT)
        (xb, yb) = intersection(LEF, top, RIG, bot)
        if spin > 0:
            if (yr == BOT and xr <= rig) or (xr == LEF and yr >= bot):
                return (max(x for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if y >= bot) - correction + shift, bot + ch)
            if (xr == RIG and yr >= top) or yr == BOT:
                return (rig, min(y for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if x >= rig) + correction + shift)
            if (yr == TOP and xr >= lef) or xr == RIG:
                return (min(x for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if y <= top) + correction + shift - cw, TOP + ch)
            return (LEF, max(y for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if x <= lef) - correction + shift + ch)
        if (yr == BOT and xr >= lef) or (xr == RIG and yr >= bot):
            return (min(x for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if y >= bot) + correction + shift - cw, bot + ch)
        if xr == RIG or (yr == TOP and xr >= rig):
            return (rig, max(y for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if x >= rig) - correction + shift + ch)
        if yr == TOP or (xr == LEF and yr <= top):
            return (max(x for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if y <= top) - correction + shift, TOP + ch)
        return (LEF, min(y for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if x <= lef) + correction + shift)
    
    def arrow_pos(direction, ratio):
        t0 = bisection(lambda p: abs(p[0] - ax) > aw or abs(p[1] - ay) > ah)
        t3 = bisection(lambda p: abs(p[0] - ex) < ew and abs(p[1] - ey) < eh)
        if direction == "<":
            (t0, t3) = (t3, t0)
        tc = t0 + (t3 - t0) * ratio
        (xc, yc) = bezier(tc)
        (x, y) = derivate(tc)
        if direction == "<":
            (x, y) = (-x, -y)
        return (xc, yc, x, -y)
    
    diagonal = hypot(ax - ex, ay - ey)
    (x, y) = line_intersection(ex, ey, ew + cw / 2, eh + ch / 2, ax, ay)
    k = (cw *  abs((ay - ey) / diagonal) + ch * abs((ax - ex) / diagonal))
    (x, y) = (x - spin * k * (ay - ey) / diagonal, y + spin * k * (ax - ex) / diagonal)
    (hx, hy) = (2 * x - (ex + ax) / 2, 2 * y - (ey + ay) / 2)
    (x1, y1) = (ex + (hx - ex) * 2 / 3, ey + (hy - ey) * 2 / 3)
    (x2, y2) = (ax + (hx - ax) * 2 / 3, ay + (hy - ay) * 2 / 3)
    (kax, kay) = (ex - 2 * hx + ax, ey - 2 * hy + ay)
    (kbx, kby) = (2 * hx - 2 * ex, 2 * hy - 2 * ey)
    bezier = lambda t: (kax*t*t + kbx*t + ex, kay*t*t + kby*t + ey)
    derivate = lambda t: (2*kax*t + kbx, 2*kay*t + kby)
    
    curved_leg_factory.points = (ex, ey, x1, y1, x2, y2, ax, ay)
    curved_leg_factory.card_pos = card_pos
    curved_leg_factory.arrow_pos = arrow_pos
    return curved_leg_factory


def upper_round_rect(x, y, w, h, r):
    return " ".join([str(x) for x in ["M", x + w - r, y, "a", r, r, 90, 0, 1, r, r, "V", y + h, "h", -w, "V", y + r, "a", r, r, 90, 0, 1, r, -r]])

def lower_round_rect(x, y, w, h, r):
    return " ".join([str(x) for x in ["M", x + w, y, "v", h - r, "a", r, r, 90, 0, 1, -r, r, "H", x + r, "a", r, r, 90, 0, 1, -r, -r, "V", y, "H", w]])

def arrow(x, y, a, b):
    c = hypot(a, b)
    (cos, sin) = (a / c, b / c)
    return " ".join([str(x) for x in [ "M", x, y, "L", x + arrow_width * cos - arrow_half_height * sin, y - arrow_half_height * cos - arrow_width * sin, "L", x + arrow_axis * cos, y - arrow_axis * sin, "L", x + arrow_width * cos + arrow_half_height * sin, y + arrow_half_height * cos - arrow_width * sin, "Z"]])

def safe_print_for_PHP(s):
    try:
        print(s)
    except UnicodeEncodeError:
        print(s.encode("utf8"))


lines = '<?xml version="1.0" standalone="no"?>\n<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"\n"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">'
lines += '\n\n<svg width="%s" height="%s" view_box="0 0 %s %s"\nxmlns="http://www.w3.org/2000/svg"\nxmlns:link="http://www.w3.org/1999/xlink">' % (width,height,width,height)
lines += u'\\n\\n<desc>Généré par Mocodo 2.3.9 le %s</desc>' % time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
lines += '\n\n<rect id="frame" x="0" y="0" width="%s" height="%s" fill="%s" stroke="none" stroke-width="0"/>' % (width,height,colors['background_color'] if colors['background_color'] else "none")

lines += u"""\n\n<!-- Association Paru -->"""
(x,y) = (cx[u"Paru"],cy[u"Paru"])
(ex,ey) = (cx[u"Calendrier"],cy[u"Calendrier"])
leg=straight_leg_factory(ex,ey,61,30,x,y,30,29,19+2*card_margin,14+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"Paru,Calendrier"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Futura" font-size="11">1,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
(ex,ey) = (cx[u"Jeux"],cy[u"Jeux"])
leg=straight_leg_factory(ex,ey,64,81,x,y,30,29,18+2*card_margin,14+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"Paru,Jeux"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Futura" font-size="11">1,1</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
lines += u"""\n<g id="association-Paru">""" % {}
path = upper_round_rect(-30+x,-29+y,60,28,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_cartouche_color'], 'stroke_color': colors['association_cartouche_color']}
path = lower_round_rect(-30+x,-1.0+y,60,30,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_color'], 'stroke_color': colors['association_color']}
lines += u"""\n	<rect x="%(x)s" y="%(y)s" width="60" height="58" fill="%(color)s" rx="14" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -30+x, 'y': -29+y, 'color': colors['transparent_color'], 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x0': -30+x, 'y0': -1+y, 'x1': 30+x, 'y1': -1+y, 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Copperplate" font-size="18">Paru</text>""" % {'x': -23+x, 'y': -7.7+y, 'text_color': colors['association_cartouche_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Association Executer -->"""
(x,y) = (cx[u"Executer"],cy[u"Executer"])
(ex,ey) = (cx[u"Consoles"],cy[u"Consoles"])
leg=straight_leg_factory(ex,ey,52,38,x,y,50,29,19+2*card_margin,14+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"Executer,Consoles"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Futura" font-size="11">1,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
(ex,ey) = (cx[u"Jeux"],cy[u"Jeux"])
leg=straight_leg_factory(ex,ey,64,81,x,y,50,29,18+2*card_margin,14+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"Executer,Jeux"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Futura" font-size="11">1,1</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
lines += u"""\n<g id="association-Executer">""" % {}
path = upper_round_rect(-50+x,-29+y,100,28,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_cartouche_color'], 'stroke_color': colors['association_cartouche_color']}
path = lower_round_rect(-50+x,-1.0+y,100,30,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_color'], 'stroke_color': colors['association_color']}
lines += u"""\n	<rect x="%(x)s" y="%(y)s" width="100" height="58" fill="%(color)s" rx="14" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -50+x, 'y': -29+y, 'color': colors['transparent_color'], 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x0': -50+x, 'y0': -1+y, 'x1': 50+x, 'y1': -1+y, 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Copperplate" font-size="18">Executer</text>""" % {'x': -43+x, 'y': -7.7+y, 'text_color': colors['association_cartouche_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Association Avoir -->"""
(x,y) = (cx[u"Avoir"],cy[u"Avoir"])
(ex,ey) = (cx[u"Jeux"],cy[u"Jeux"])
leg=straight_leg_factory(ex,ey,64,81,x,y,33,29,18+2*card_margin,14+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"Avoir,Jeux"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Futura" font-size="11">1,1</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
(ex,ey) = (cx[u"Genres"],cy[u"Genres"])
leg=straight_leg_factory(ex,ey,44,38,x,y,33,29,19+2*card_margin,14+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"Avoir,Genres"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Futura" font-size="11">1,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
lines += u"""\n<g id="association-Avoir">""" % {}
path = upper_round_rect(-33+x,-29+y,66,28,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_cartouche_color'], 'stroke_color': colors['association_cartouche_color']}
path = lower_round_rect(-33+x,-1.0+y,66,30,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_color'], 'stroke_color': colors['association_color']}
lines += u"""\n	<rect x="%(x)s" y="%(y)s" width="66" height="58" fill="%(color)s" rx="14" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -33+x, 'y': -29+y, 'color': colors['transparent_color'], 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x0': -33+x, 'y0': -1+y, 'x1': 33+x, 'y1': -1+y, 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Copperplate" font-size="18">Avoir</text>""" % {'x': -26+x, 'y': -7.7+y, 'text_color': colors['association_cartouche_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Association Publier -->"""
(x,y) = (cx[u"Publier"],cy[u"Publier"])
(ex,ey) = (cx[u"Jeux"],cy[u"Jeux"])
leg=straight_leg_factory(ex,ey,64,81,x,y,44,29,18+2*card_margin,14+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"Publier,Jeux"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Futura" font-size="11">1,1</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
(ex,ey) = (cx[u"Editeurs"],cy[u"Editeurs"])
leg=straight_leg_factory(ex,ey,49,38,x,y,44,29,19+2*card_margin,14+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"Publier,Editeurs"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Futura" font-size="11">1,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
lines += u"""\n<g id="association-Publier">""" % {}
path = upper_round_rect(-44+x,-29+y,88,28,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_cartouche_color'], 'stroke_color': colors['association_cartouche_color']}
path = lower_round_rect(-44+x,-1.0+y,88,30,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_color'], 'stroke_color': colors['association_color']}
lines += u"""\n	<rect x="%(x)s" y="%(y)s" width="88" height="58" fill="%(color)s" rx="14" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -44+x, 'y': -29+y, 'color': colors['transparent_color'], 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x0': -44+x, 'y0': -1+y, 'x1': 44+x, 'y1': -1+y, 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Copperplate" font-size="18">Publier</text>""" % {'x': -37+x, 'y': -7.7+y, 'text_color': colors['association_cartouche_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Entity Calendrier -->"""
(x,y) = (cx[u"Calendrier"],cy[u"Calendrier"])
lines += u"""\n<g id="entity-Calendrier">""" % {}
lines += u"""\n	<g id="frame-Calendrier">""" % {}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="122" height="30" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -61+x, 'y': -30+y, 'color': colors['entity_cartouche_color'], 'stroke_color': colors['entity_cartouche_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="122" height="30" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -61+x, 'y': 0.0+y, 'color': colors['entity_color'], 'stroke_color': colors['entity_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="122" height="60" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -61+x, 'y': -30+y, 'color': colors['transparent_color'], 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n		<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x0': -61+x, 'y0': 0+y, 'x1': 61+x, 'y1': 0+y, 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n	</g>""" % {}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Copperplate" font-size="18">Calendrier</text>""" % {'x': -53+x, 'y': -8.7+y, 'text_color': colors['entity_cartouche_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Gill Sans" font-size="15">id_calendrier</text>""" % {'x': -53+x, 'y': 17.1+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -53+x, 'y0': 20+y, 'x1': 30+x, 'y1': 20+y, 'stroke_color': colors['entity_attribute_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Entity Consoles -->"""
(x,y) = (cx[u"Consoles"],cy[u"Consoles"])
lines += u"""\n<g id="entity-Consoles">""" % {}
lines += u"""\n	<g id="frame-Consoles">""" % {}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="104" height="30" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -52+x, 'y': -38+y, 'color': colors['entity_cartouche_color'], 'stroke_color': colors['entity_cartouche_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="104" height="46" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -52+x, 'y': -8.0+y, 'color': colors['entity_color'], 'stroke_color': colors['entity_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="104" height="76" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -52+x, 'y': -38+y, 'color': colors['transparent_color'], 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n		<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x0': -52+x, 'y0': -8+y, 'x1': 52+x, 'y1': -8+y, 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n	</g>""" % {}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Copperplate" font-size="18">Consoles</text>""" % {'x': -44+x, 'y': -16.7+y, 'text_color': colors['entity_cartouche_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Gill Sans" font-size="15">id_console</text>""" % {'x': -44+x, 'y': 9.1+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -44+x, 'y0': 12+y, 'x1': 24+x, 'y1': 12+y, 'stroke_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Gill Sans" font-size="15">nom_console</text>""" % {'x': -44+x, 'y': 26.1+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Entity Jeux -->"""
(x,y) = (cx[u"Jeux"],cy[u"Jeux"])
lines += u"""\n<g id="entity-Jeux">""" % {}
lines += u"""\n	<g id="frame-Jeux">""" % {}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="128" height="30" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -64+x, 'y': -81+y, 'color': colors['entity_cartouche_color'], 'stroke_color': colors['entity_cartouche_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="128" height="132" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -64+x, 'y': -51.0+y, 'color': colors['entity_color'], 'stroke_color': colors['entity_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="128" height="162" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -64+x, 'y': -81+y, 'color': colors['transparent_color'], 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n		<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x0': -64+x, 'y0': -51+y, 'x1': 64+x, 'y1': -51+y, 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n	</g>""" % {}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Copperplate" font-size="18">Jeux</text>""" % {'x': -21+x, 'y': -59.7+y, 'text_color': colors['entity_cartouche_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Gill Sans" font-size="15">id_jeu</text>""" % {'x': -56+x, 'y': -34.0+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -56+x, 'y0': -31+y, 'x1': -17+x, 'y1': -31+y, 'stroke_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Gill Sans" font-size="15">nom_jeu</text>""" % {'x': -56+x, 'y': -16.9+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Gill Sans" font-size="15">NA_vente_jeu</text>""" % {'x': -56+x, 'y': 0.1+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Gill Sans" font-size="15">EU_vente_jeu</text>""" % {'x': -56+x, 'y': 17.1+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Gill Sans" font-size="15">JP_vente_jeu</text>""" % {'x': -56+x, 'y': 34.0+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Gill Sans" font-size="15">Autre_vente_jeu</text>""" % {'x': -56+x, 'y': 51.0+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Gill Sans" font-size="15">Global_vente_jeu</text>""" % {'x': -56+x, 'y': 68.0+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Entity Genres -->"""
(x,y) = (cx[u"Genres"],cy[u"Genres"])
lines += u"""\n<g id="entity-Genres">""" % {}
lines += u"""\n	<g id="frame-Genres">""" % {}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="88" height="30" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -44+x, 'y': -38+y, 'color': colors['entity_cartouche_color'], 'stroke_color': colors['entity_cartouche_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="88" height="46" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -44+x, 'y': -8.0+y, 'color': colors['entity_color'], 'stroke_color': colors['entity_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="88" height="76" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -44+x, 'y': -38+y, 'color': colors['transparent_color'], 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n		<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x0': -44+x, 'y0': -8+y, 'x1': 44+x, 'y1': -8+y, 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n	</g>""" % {}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Copperplate" font-size="18">Genres</text>""" % {'x': -34+x, 'y': -16.7+y, 'text_color': colors['entity_cartouche_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Gill Sans" font-size="15">id_genre</text>""" % {'x': -36+x, 'y': 9.1+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -36+x, 'y0': 12+y, 'x1': 20+x, 'y1': 12+y, 'stroke_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Gill Sans" font-size="15">nom_genre</text>""" % {'x': -36+x, 'y': 26.1+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Entity Editeurs -->"""
(x,y) = (cx[u"Editeurs"],cy[u"Editeurs"])
lines += u"""\n<g id="entity-Editeurs">""" % {}
lines += u"""\n	<g id="frame-Editeurs">""" % {}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="98" height="30" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -49+x, 'y': -38+y, 'color': colors['entity_cartouche_color'], 'stroke_color': colors['entity_cartouche_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="98" height="46" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -49+x, 'y': -8.0+y, 'color': colors['entity_color'], 'stroke_color': colors['entity_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="98" height="76" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -49+x, 'y': -38+y, 'color': colors['transparent_color'], 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n		<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x0': -49+x, 'y0': -8+y, 'x1': 49+x, 'y1': -8+y, 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n	</g>""" % {}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Copperplate" font-size="18">Editeurs</text>""" % {'x': -41+x, 'y': -16.7+y, 'text_color': colors['entity_cartouche_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Gill Sans" font-size="15">id_editeur</text>""" % {'x': -41+x, 'y': 9.1+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -41+x, 'y0': 12+y, 'x1': 24+x, 'y1': 12+y, 'stroke_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Gill Sans" font-size="15">nom_editeur</text>""" % {'x': -41+x, 'y': 26.1+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n</g>""" % {}
lines += u'\n</svg>'

with codecs.open(r"mocodo_notebook\sandbox.svg", "w", "utf8") as f:
    f.write(lines)
safe_print_for_PHP(u'Fichier de sortie "mocodo_notebook\sandbox.svg" généré avec succès.')