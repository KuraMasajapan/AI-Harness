"""Bake the orthographic reference colors onto the sculpt's ring UVs."""
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
WORK = HERE / "work"
HEIGHT = 3.027

# Rows: reference height in pixels, front half width, profile back and front.
PROFILE = np.array([
    (223, 1, 813, 819), (228, 50, 782, 862), (248, 91, 737, 898),
    (273, 119, 712, 924), (302, 137, 692, 943), (337, 148, 678, 952),
    (368, 153, 672, 956), (405, 154, 666, 950), (442, 158, 667, 951),
    (474, 174, 649, 960), (512, 187, 623, 965), (558, 195, 605, 962),
    (601, 197, 595, 955), (657, 193, 585, 939), (708, 179, 587, 914),
    (756, 155, 579, 879), (788, 137, 595, 849), (813, 118, 621, 830),
    (836, 91, 644, 823), (850, 73, 674, 817), (856, 46, 703, 790),
    (865, 1, 749, 754),
], dtype=float)
BOTTOM = (889 - 865) / 220


def smooth(start, end, value):
    t = np.clip((value - start) / (end - start), 0, 1)
    return t * t * (3 - 2 * t)


def interpolate(xs, ys, sample):
    slopes = np.gradient(ys, xs)
    i = np.clip(np.searchsorted(xs, sample) - 1, 0, len(xs) - 2)
    dx = xs[i + 1] - xs[i]
    t = np.clip((sample - xs[i]) / dx, 0, 1)
    return ((2*t**3 - 3*t**2 + 1)*ys[i] + (t**3 - 2*t**2 + t)*dx*slopes[i]
            + (-2*t**3 + 3*t**2)*ys[i + 1] + (t**3 - t**2)*dx*slopes[i + 1])


def ring(theta, z):
    py = 889 - 220 * z
    width, back, front = (interpolate(PROFILE[:, 0], PROFILE[:, i], py) for i in (1, 2, 3))
    crown = smooth(233, 265, py)
    dome = np.sqrt(np.maximum(.035, py - 223))
    width = crown * width + (1 - crown) * 18.2 * dome
    s, c = np.sin(theta), np.cos(theta)
    x = width * np.sign(s) * abs(s)**0.92 / 220
    center = (front + back) / 2
    depth = crown * (front - back) / 2 + (1 - crown) * 16.4 * dome
    socket = (np.exp(-((abs(x) - .266) / .135)**2 - ((z - 2.505) / .129)**2)
              * smooth(.35, .82, c))
    powers = np.where(c > 0, .78 + .13 * smooth(1.8, 2.4, z), .85)
    y = (798 - center - depth * np.sign(c) * abs(c)**powers + 31 * socket) / 220
    # Raised scapulars and the groove between the folded wings.
    mantle = smooth(.47, .9, z) * (1 - smooth(1.48, 1.99, z))
    y += .054 * mantle * smooth(.1, .55, abs(s)) * smooth(.15, .85, -c)
    return x, y


def sample(pixels, x, y):
    x = np.clip(x, 0, pixels.shape[1] - 1.01)
    y = np.clip(y, 0, pixels.shape[0] - 1.01)
    ix, iy = x.astype(int), y.astype(int)
    fx, fy = (x - ix)[..., None], (y - iy)[..., None]
    return ((pixels[iy, ix] * (1 - fx) + pixels[iy, ix + 1] * fx) * (1 - fy)
            + (pixels[iy + 1, ix] * (1 - fx) + pixels[iy + 1, ix + 1] * fx) * fy)


def erase(pixels, cx, cy, rx, ry):
    y, x = np.mgrid[cy-ry:cy+ry+1, cx-rx:cx+rx+1]
    u, v = (x - cx) / rx, (y - cy) / ry
    angle = np.arctan2(v, u)
    weight = (1 - smooth(.7, 1, np.hypot(u, v)))[..., None]
    fill = sample(pixels, cx + rx * 1.07 * np.cos(angle), cy + ry * 1.07 * np.sin(angle))
    pixels[y, x] = pixels[y, x] * (1 - weight) + fill * weight


def bake():
    from PIL import Image

    WORK.mkdir(exist_ok=True)
    source = np.array(Image.open(HERE / "references/three-view.webp").convert("RGB")
                      .resize((1550, 1033), Image.Resampling.LANCZOS), dtype=float)
    for feature in [(216, 339, 35, 30), (334, 340, 35, 30), (274, 390, 27, 42),
                    (887, 338, 26, 30), (951, 390, 18, 26)]:
        erase(source, *feature)

    width, height = 2048, 1280
    theta = -np.pi + 2 * np.pi * ((np.arange(width)[None, :] + .5) / width)
    z = HEIGHT - (HEIGHT - BOTTOM) * ((np.arange(height)[:, None] + .5) / height)
    x, y = ring(theta, z)
    py = np.broadcast_to(889 - z * 220, x.shape)
    front = sample(source, 274 + 220 * x * .98, py)
    side_x = 798 - 220 * y
    # Follow the outline rather than sampling background just outside it.
    back_edge = interpolate(PROFILE[:, 0], PROFILE[:, 2], py)
    front_edge = interpolate(PROFILE[:, 0], PROFILE[:, 3], py)
    side_x = np.clip(side_x, back_edge + 4, np.maximum(back_edge + 4, front_edge - 4))
    side = sample(source, side_x, py)
    rear = sample(source, 1276 - 220 * x * .96, py)
    c = np.cos(theta)
    irregular = .052 * np.sin(theta * 21 + py * .21) * np.sin(py * .137 - theta * 12)
    weight = smooth(.29, .78, abs(c) + irregular)[..., None]
    result = side * (1 - weight) + np.where((c > 0)[..., None], front, rear) * weight
    result -= 12 * (1 - smooth(78, 185, result))
    Image.fromarray(result.clip(0, 255).astype("uint8")).save(
        WORK / "plumage.jpg", quality=93, subsampling=0)

    # The iris color is a radial amber field with dark limbus and fine spokes.
    size = 384
    coord = (np.arange(size) + .5) * 2 / size - 1
    x, y = np.meshgrid(coord, coord)
    r, a = np.hypot(x, y), np.arctan2(y, x)
    spokes = np.sin(a * 83 + np.sin(r * 24) * 1.3) + .42 * np.sin(a * 131 + r * 31)
    gold = (.92 + .16 * np.clip(y, -1, 1) + .12 * spokes
            + .15 * np.sin(r * 17 + np.sin(a * 13)))[..., None]
    iris = np.array([176, 115, 37]) * gold
    rim = (1 - smooth(.73, .99, r))[..., None]
    pupil = smooth(.48, .535, np.hypot(x + .018, y - .018))[..., None]
    eye = (iris * rim + np.array([37, 24, 11]) * (1 - rim)) * pupil
    eye += np.array([12, 9, 8]) * (1 - pupil)
    Image.fromarray(eye.clip(0, 255).astype("uint8")).save(WORK / "iris.png")

    y, x = np.mgrid[0:1:384j, -1:1:144j]
    tip = smooth(.28, .53, y)
    stripe = np.sin(2*np.pi*(3.15*y + .074*x*x + .012*np.sin(y*31 + x*8)))
    edge = np.sin(x*77 + y*48) * .025 + np.sin(x*196 - y*37) * .022
    ink = smooth(.29, .64, stripe + edge) * tip * (1 - smooth(.84, .98, y))
    shaft = np.exp(-abs(x)*52) * .22
    paper = (238 - 17*x*x + 3*np.sin(x*114 + y*49) + 2*np.sin(x*196 - y*92))
    base = np.stack([paper, paper-4, paper-10], axis=2)
    result = base * (1 - ink[..., None]*.73) + shaft[..., None]*30
    Image.fromarray(result.clip(0, 255).astype("uint8")).save(WORK / "tail.jpg", quality=94)


if __name__ == "__main__":
    bake()
