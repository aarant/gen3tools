from io import BytesIO

from PIL import Image, ImageFont, ImageDraw

from seed_tools import wild_pids

grid = Image.open('grid.png')
blank = Image.open('spinda_blank.png')
top = Image.open('spinda_top.png')
mask = Image.open('spinda_mask.png')
spot_imgs = [Image.open('spot%s.png' % i) for i in range(4)]

OFFSETS = [(18, 19), (6, 18), (24, 1), (0, 0)]


def draw_pid(pid, f=None, is_image=False):
    body1, body2, ear_r, ear_l = pid >> 24, pid >> 16, pid >> 8, pid
    spots = (body1 & 0xff, body2 & 0xff, ear_r & 0xff, ear_l & 0xff)
    coords = [(s & 0xf, s >> 4) for s in spots]
    im = blank.copy()
    for i in range(4):
        im.paste(spot_imgs[i], (coords[i][0]+OFFSETS[i][0], coords[i][1]+OFFSETS[i][1]), spot_imgs[i])
    im.paste(top, (0, 0), mask)
    draw = ImageDraw.Draw(im)
    if (pid & 0xff) > 127:
        color, text = 'rgb(50, 40, 255)', 'M'
    else:
        color, text = 'rgb(255, 80, 150)', 'F'
    draw.text((2, 0), text, fill=color, size=8)
    if is_image:
        return im
    if f is None:
        f = BytesIO()
    im.save(f, format='PNG')
    return f


def center_on_frame(frame, f=None):
    pids = list(wild_pids(frame-7, 15))
    grid_im = grid.copy()
    draw = ImageDraw.Draw(grid_im)
    for i, pid in enumerate(pids):
        x = 53*(i % 5)
        y = 58*(i // 5)
        im = draw_pid(pid, is_image=True)
        grid_im.paste(im, (x, y), im)
        color = 'rgb(255, 0, 0)' if i == 7 else 'rgb(0, 0, 0)'
        draw.text((x+20, y), str(frame-7+i), fill=color, size=8)
    if f is None:
        f = BytesIO()
    grid_im.save(f, format='PNG')
    return f


with open('grid_test.png', 'wb') as f:
    center_on_frame(700, f)
