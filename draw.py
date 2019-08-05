from io import BytesIO

from PIL import Image, ImageDraw

grid = Image.open('assets/grid.png')
blank = Image.open('assets/spinda_blank.png')
top = Image.open('assets/spinda_top.png')
mask = Image.open('assets/spinda_mask.png')
spot_imgs = [Image.open('assets/spot%s.png' % i) for i in range(4)]

OFFSETS = [(18, 19), (6, 18), (24, 1), (0, 0)]  # Pixel offsets for each spot

wild_pids = lambda *args, **kwargs: None


def draw_spinda(pid: int) -> Image:
    """ Draw a spinda with a specific PID.

    Args:
        pid (int): Integer PID. 0 <= pid < 2**32.

    Returns:
        Image: Spinda image
    """
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
    return im


def save_spinda(pid: int, f=None):
    """ Draw and save a spinda to a file.

    Args:
        pid (int): Integer PID. 0 <= pid < 2**32.
        f (IOBase): Either a file object, or None. Defaults to None.

    Returns:
        IOBase: File object to which the image was saved.
    """
    im = draw_spinda(pid)
    if f is None:
        f = BytesIO()
    im.save(f, format='PNG')
    return f


def save_spinda_grid(frame: int, f=None):
    """ Save a grid of spinda images centered on a frame to a file.

    Args:
        frame (int): Frame to center the grid around.
        f (IOBase): Either a file object, or None.

    Returns:
        IOBase: File object the grid was saved to.
    """
    grid_im = grid.copy()
    draw = ImageDraw.Draw(grid_im)
    for i, pid in enumerate(wild_pids(frame-7, 15)):
        x = 53*(i % 5)
        y = 58*(i // 5)
        im = draw_spinda(pid)
        grid_im.paste(im, (x, y), im)
        color = 'rgb(255, 0, 0)' if i == 7 else 'rgb(0, 0, 0)'
        draw.text((x+20, y), str(frame-7+i), fill=color, size=8)
    if f is None:
        f = BytesIO()
    grid_im.save(f, format='PNG')
    return f

if __name__ == '__main__':
    with open('grid_test.png', 'wb') as f:
        save_spinda_grid(700, f)
