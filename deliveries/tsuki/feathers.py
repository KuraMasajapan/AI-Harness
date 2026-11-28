"""Bake the orthographic reference colors onto the sculpt's ring UVs."""
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
WORK = HERE / "work"
HEIGHT = 3.027
EYE_X = .237
EYE_Z = 2.503

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


def facial_disc(x, z):
    dx = abs(x) - .252
    dz = z - 2.49 + .14 * dx
    r = np.hypot(dx / .347, dz / .324)
    angle = np.arctan2(dz / .324, dx / .347)
    return r, angle


def socket_profile(x, z):
    dx = abs(x) - .270
    dz = z - EYE_Z
    brow = dz - .115 + .042 * np.clip(dx/.140, -1.45, 1.45)**2
    return dx, dz, brow


def bristle_crest(x, z):
    branch = .017 + .44 * np.maximum(0, z - 2.345)
    length = smooth(2.326, 2.398, z) * (1 - smooth(2.501, 2.610, z))
    return np.exp(-((abs(x) - branch)/.045)**2) * length


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
    dx, dz, brow = socket_profile(x, z)
    socket = np.exp(-(dx / .151)**2 - (dz / .112)**2) * smooth(.35, .80, c)
    powers = np.where(c > 0, .78 + .13 * smooth(1.8, 2.4, z), .85)
    y = (798 - center - depth * np.sign(c) * abs(c)**powers + 53 * socket) / 220
    y -= .054 * np.exp(-(brow/.030)**2 - (dx/.146)**4) * smooth(.45, .85, c)
    y += .075 * np.exp(-((abs(x)-.457)/.104)**2 - (dz/.116)**2) * smooth(.42, .74, c)
    y -= .041 * np.exp(-((abs(x)-.054)/.048)**2 - ((z-2.368)/.079)**2) * smooth(.71, .97, c)
    r, _ = facial_disc(x, z)
    face = smooth(.44, .80, c)
    y -= .036 * bristle_crest(x, z) * face
    y -= face * (.023 * np.exp(-((r - .90) / .16)**2)
                 - .013 * np.exp(-((r - 1.085) / .10)**2))
    aperture = np.hypot(abs(x) - EYE_X, dz)
    socket_floor = -.438 - .176*smooth(.091, .117, aperture)
    y += np.maximum(0, socket_floor - y) * (1 - smooth(.117, .130, aperture)) * face
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
    for feature in [(215, 339, 29, 24), (332, 340, 29, 24), (274, 390, 27, 42),
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
    r, a = facial_disc(x, z)
    grain = np.sin(101*a + r*11) + .52*np.sin(173*a - r*14) + .30*np.sin(227*a + r*19)
    below = (1 - np.sin(a)) / 2
    outer = np.exp(-((r - 1.01 - .025*np.sin(5*a))/.105)**2)
    edge = smooth(.48, .85, c) * smooth(.045, .22, abs(x))
    feather = smooth(.40, .67, r) * (1 - smooth(.94, 1.22, r))
    result += (edge * (-outer * (12 + 12*below) + grain*feather*3.25))[..., None] * [1, 1.04, 1.12]
    dx, dz, brow = socket_profile(x, z)
    around = np.hypot(dx/.116, dz/.086)
    orbit = (36 + 20*smooth(-.026, .078, dz)) * np.exp(-((around - .94)/.47)**2)
    brow_shadow = 87 * np.exp(-((brow + .031)/.028)**2 - (dx/.129)**4)
    bill_root = 28 * np.exp(-(x/.085)**2 - ((z - 2.375)/.083)**2)
    fibers = np.abs(np.sin(336*x + np.sign(x)*34*(z-2.350) + .54*np.sin(217*z)))**7
    bill_root += 44 * fibers * np.exp(-((abs(x)-.034)/.037)**2 - ((z-2.374)/.065)**2)
    shading = smooth(.42, .89, c) * (orbit + brow_shadow + bill_root)
    result *= 1 - shading[..., None] / 305 * np.array([.91, 1, 1.14])
    crest = bristle_crest(x, z) * smooth(.71, .96, c)
    direction = abs(x) - .46*(z - 2.35)
    barbs = np.sin(390*direction + .65*np.sin(130*z)) + .43*np.sin(707*direction - 61*z)
    result = result * (1 - .61*crest[..., None]) + crest[..., None] * (
        .61*np.array([237, 234, 227]) + 8*barbs[..., None])
    Image.fromarray(result.clip(0, 255).astype("uint8")).save(
        WORK / "plumage.jpg", quality=93, subsampling=0)

    # The iris color is a radial amber field with dark limbus and fine spokes.
    size = 384
    coord = (np.arange(size) + .5) * 2 / size - 1
    x, y = np.meshgrid(coord, coord)
    r, a = np.hypot(x, y), np.arctan2(y, x)
    spokes = np.sin(a * 83 + np.sin(r * 24) * 1.3) + .42 * np.sin(a * 131 + r * 31)
    gold = (.80 + .23 * np.clip(y, -1, 1) + .11 * spokes
            + .075 * np.sin(r * 23 + np.sin(a * 13)))[..., None]
    inner = smooth(.375, .655, r)[..., None]
    iris = (np.array([102, 60, 23]) * (1 - inner) + np.array([177, 113, 40]) * inner) * gold
    rim = (1 - smooth(.78, .965, r))[..., None]
    pupil = smooth(.393, .423, np.hypot(x + .015, y + .027))[..., None]
    eye = (iris * rim + np.array([20, 13, 9]) * (1 - rim)) * pupil
    eye += np.array([8, 6, 5]) * (1 - pupil)
    eye *= (.52 + .48 * smooth(-.79, -.08, y))[..., None]
    light_x, light_y = x + .240, y + .267 + .40*(x + .240)
    catchlight = np.exp(-((light_x/.130)**4 + (light_y/.062)**2))[..., None] * .59
    eye = eye * (1 - catchlight) + np.array([171, 174, 168]) * catchlight
    Image.fromarray(eye.clip(0, 255).astype("uint8")).save(WORK / "iris.png")

    v, u = np.mgrid[0:1:160j, 0:2*np.pi:128j]
    striae = np.sin(27*u + np.sin(v*8)*.42) + .4*np.sin(49*u - v*3)
    ridge = 15*np.maximum(0, np.sin(u))**22
    cutting_edge = 10*np.cos(u)**36 * smooth(.16, .55, v)
    keratin = 33 + 40*smooth(.04, .76, v) + ridge + cutting_edge + 2.4*striae
    slate = smooth(0, .31, v)
    Image.fromarray(np.stack((keratin - 6*slate, keratin + 3*slate, keratin + 13*slate), axis=-1)
                    .clip(0, 255).astype("uint8")).save(WORK / "bill-keratin.jpg", quality=93)

    v, u = np.mgrid[0:1:320j, -1:1:192j]
    fibers = np.sin(175*u + 7*np.sin(v*6 + u*3)) + .64*np.sin(283*u - v*17)
    wisps = np.sin(69*u + 5*np.sin(v*11 + u*4))
    clumps = np.sin(27*u + 2.5*np.sin(v*8 + u*3))
    ivory = 224 - 29*u*u + 5*fibers + 7*wisps + 7*clumps - 16*smooth(.72, 1, v)
    foot = np.stack((ivory + 5, ivory + 1, ivory - 7), axis=-1)
    Image.fromarray(foot.clip(0, 255).astype("uint8")).save(WORK / "toe-feather.jpg", quality=91)

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
