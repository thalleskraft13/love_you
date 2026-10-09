import tkinter as tk
import math

PINK = (255, 95, 168)
PINK_SOFT = "#ffb3d6"
PINK_DEEP = "#e0408a"
PINK_HEX = "#ff5fa8"

# (x, y, tamanho, duração, atraso, texto)
TEXTS = [
    (74.9, 34.8, 10.4, 4.2, -1.9, "I love you"),
    (165.1, 34.8, 10.4, 4.5, -3.4, "I love you"),
    (50.9, 51.3, 7.0, 4.2, -2.4, "I love you"),
    (98.4, 51.3, 7.0, 3.6, -3.1, "I love you"),
    (141.6, 51.3, 7.0, 3.1, -1.6, "I love you"),
    (189.1, 51.3, 7.0, 4.6, -3.3, "I love you"),
    (53.4, 67.8, 10.0, 3.1, -3.0, "I love you"),
    (186.6, 67.8, 10.0, 2.5, -0.8, "I love you"),
    (45.7, 84.3, 6.0, 2.4, -2.1, "I love you"),
    (194.3, 84.3, 6.0, 3.8, -1.8, "I love you"),
    (68.2, 100.8, 12.0, 3.6, -3.3, "I love you"),
    (171.8, 100.8, 12.0, 4.0, -1.7, "I love you"),
    (72.3, 117.3, 8.0, 4.0, -2.7, "I love you"),
    (167.7, 117.3, 8.0, 4.0, -3.7, "I love you"),
    (120.0, 133.8, 11.0, 3.8, -2.5, "I love you"),
    (120.0, 150.3, 6.0, 2.3, -2.3, "I love you"),
    (120.0, 166.8, 7.0, 3.4, -1.7, "♥"),
    (92.0, 77.3, 5.0, 3.3, -0.6, "♥"),
    (100.8, 105.1, 5.0, 2.5, -0.7, "♥"),
    (124.5, 118.7, 5.0, 2.3, -1.0, "♥"),
    (137.6, 102.1, 5.0, 2.9, -2.0, "♥"),
    (149.4, 88.3, 5.0, 3.3, -1.0, "♥"),
    (151.4, 77.0, 5.0, 3.2, -1.6, "♥")
]

# (x, y, escala, rotação, atraso do balanço)
HATS = [
    (18, 34, 0.40, -18, 0.0),
    (224, 34, 0.40, 16, -1.3),
    (222, 208, 0.35, 12, -2.6),
]


def mix(op, base=PINK):
    return "#%02x%02x%02x" % tuple(int(c * op) for c in base)


def twinkle(t, dur, delay):
    """Mesma curva do protótipo: apaga -> acende -> fica -> apaga."""
    p = ((t - delay) % dur) / dur
    if p < 0.35:
        k = p / 0.35
    elif p < 0.55:
        return 1.0
    else:
        k = 1 - (p - 0.55) / 0.45
    return k * k * (3 - 2 * k)  # suaviza


def bezier(p0, p1, p2, p3, n=10):
    pts = []
    for i in range(1, n + 1):
        t = i / n
        u = 1 - t
        pts.append((u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
                    u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1]))
    return pts


# Formas do chapéu (coordenadas locais; base do chapéu na origem)
BRIM = [(23 * math.cos(a * math.pi / 16), 5 * math.sin(a * math.pi / 16)) for a in range(32)]

_c = [(-14, -1)]
_c += bezier((-14, -1), (-12, -14), (-6, -30), (4, -40))
_c += bezier((4, -40), (10, -46), (18, -48), (23, -42))
_c += bezier((23, -42), (16, -42), (13, -38), (12, -30))
_c += bezier((12, -30), (11, -18), (13, -8), (14, -1))
CONE = _c

_b = [(-13.2, -7)]
_b += bezier((-13.2, -7), (-5, -4), (5, -4), (13, -7))
_b += [(14, -1)]
_b += bezier((14, -1), (5, 1), (-5, 1), (-14, -1))
BAND = _b

BUCKLE = [(-2.5, -6.5), (2.5, -6.5), (2.5, -1.5), (-2.5, -1.5)]


class App:
    def __init__(self, root):
        self.root = root
        root.title("I love you \u2665")
        root.geometry("820x760")
        root.minsize(360, 330)
        root.configure(bg="black")
        self.c = tk.Canvas(root, bg="black", highlightthickness=0)
        self.c.pack(fill="both", expand=True)
        root.bind("<F11>", lambda e: root.attributes("-fullscreen", not root.attributes("-fullscreen")))
        root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))
        self.t = 0.0
        self.tick()

    def view(self):
        w, h = self.c.winfo_width(), self.c.winfo_height()
        k = min(w / 240, h / 220) * 0.94
        return k, (w - 240 * k) / 2, (h - 220 * k) / 2

    def hat(self, k, ox, oy, x, y, scale, rot, delay):
        sway = math.sin((self.t - delay) / 4 * 2 * math.pi)
        a = math.radians(rot + 3 * sway)
        dy = -2 - 2 * sway
        ca, sa = math.cos(a), math.sin(a)

        def tr(pts):
            out = []
            for px, py in pts:
                px, py = px * scale, py * scale
                out += [ox + (x + px * ca - py * sa) * k,
                        oy + (y + dy + px * sa + py * ca) * k]
            return out

        lw = max(1, int(0.8 * k * scale * 2))
        c = self.c
        c.create_polygon(*tr(BRIM), fill=PINK_DEEP, outline=PINK_SOFT, width=lw)
        c.create_polygon(*tr(CONE), fill=PINK_HEX, outline=PINK_SOFT, width=lw)
        c.create_polygon(*tr(BAND), fill=PINK_SOFT, outline="")
        c.create_polygon(*tr(BUCKLE), fill="white", outline="")

    def tick(self):
        c = self.c
        c.delete("all")
        k, ox, oy = self.view()
        for x, y, s, dur, delay, txt in TEXTS:
            op = twinkle(self.t, dur, delay)
            if op < 0.02:
                continue
            font = ("Georgia", -max(6, int(s * k)), "bold italic")
            px, py = ox + x * k, oy + y * k
            glow = mix(op * 0.35)  # brilho suave ao redor
            for gx, gy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                c.create_text(px + gx, py + gy, text=txt, font=font, fill=glow)
            c.create_text(px, py, text=txt, font=font, fill=mix(op))
        for hx, hy, sc, rot, dl in HATS:
            self.hat(k, ox, oy, hx, hy, sc, rot, dl)
        self.t += 0.033
        self.root.after(33, self.tick)


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
