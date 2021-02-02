from myimage import MyImage
from copy import deepcopy


def remove_channel(src: MyImage, red: bool = False, green: bool = False,
                   blue: bool = False) -> MyImage:
    """Returns a copy of src in which the indicated channels are suppressed.

    Suppresses the red channel if no channel is indicated. src is not modified.

    Args:
    - src: the image whose copy the indicated channels have to be suppressed.
    - red: suppress the red channel if this is True.
    - green: suppress the green channel if this is True.
    - blue: suppress the blue channel if this is True.

    Returns:
    a copy of src with the indicated channels suppressed.
    """
    newsrc = deepcopy(src)
    if red == True or (red == False and green == False and blue == False):
        for i in range(src.width):
            for j in range(src.height):
                r, g, b = src.get(i, j)
                newsrc.set(i, j, (0, g, b))
    if green == True:
        for i in range(src.width):
            for j in range(src.height):
                r, g, b = src.get(i, j)
                newsrc.set(i, j, (r, 0, b))
    if blue == True:
        for i in range(src.width):
            for j in range(src.height):
                r, g, b = src.get(i, j)
                newsrc.set(i, j, (r, g, 0))
    return newsrc


def rotations(src: MyImage) -> MyImage:
    """Returns an image containing the 4 rotations of src.

    The new image has twice the dimensions of src. src is not modified.

    Args:
    - src: the image whose rotations have to be stored and returned.

    Returns:
    an image twice the size of src and containing the 4 rotations of src.
    """
    # my logic is to create 4 images and append them all together to one larger image
    newsrc1 = deepcopy(src)  # sideways left
    newsrc2 = deepcopy(src)  # original
    newsrc3 = deepcopy(src)  # upside down
    newsrc4 = deepcopy(src)  # sideways right

    i = 0
    j = 0

    while (i <= src.width):
        while (j <= src.height):
            r, g, b = src.get(j, i)
            newsrc1.set(i, j, (r, g, b))
            j += 1
        i += 1

    i = src.width
    j = src.height

    while (i >= 0):
        while (j >= 0):
            r, g, b = src.get(i, j)
            newsrc3.set(i, j, (r, g, b))
            j -= 1
        i -= 1

    i = src.width
    j = src.height

    while (i >= 0):
        while (j >= 0):
            r, g, b = src.get(j, i)
            newsrc4.set(i, j, (r, g, b))
            j -= 1
        i -= 1

    # final image with 2 times the dimensions
    finalimg = MyImage((2*src.width, 2*src.height), False)

    for x in range(src.width):
        for y in range(src.height):
            r, g, b = newsrc1.get(x, y)
            finalimg.set(x, y, (r, g, b))

    for x in range(src.width):
        for y in range(src.height):
            r, g, b = newsrc2.get(x, y)
            finalimg.set(x+src.width, y, (r, g, b))

    for x in range(src.width):
        for y in range(src.height):
            r, g, b = newsrc3.get(x, y)
            finalimg.set(x, y+src.height, (r, g, b))

    for x in range(src.width):
        for y in range(src.height):
            r, g, b = newsrc4.get(x, y)
            finalimg.set(x+src.width, y+src.height, (r, g, b))

    return finalimg


def apply_mask(src: MyImage, maskfile: str, average: bool = True) -> MyImage:
    """Returns an copy of src with the mask from maskfile applied to it.

    maskfile specifies a text file which contains an n by n mask. It has the
    following format:
    - the first line contains n
    - the next n^2 lines contain 1 element each of the flattened mask

    Args:
    - src: the image on which the mask is to be applied
    - maskfile: path to a file specifying the mask to be applied
    - average: if True, averaging should to be done when applying the mask

    Returns:
    an image which the result of applying the specified mask to src.
    """
    file1 = open(maskfile, 'r')

    n = file1.readline()
    file1.seek(1)

    mask = {}
    masktotal = 0

    for i in range(n):
        for j in range(n):
            temp = file1.readline()
            mask[(i, j)] = temp
            # dictionary to save mask value by index
            masktotal += temp
            # to use for final pixel value

    file1.close()

    newsrc = deepcopy(src)
    mid = (n-1)/2
    # distance between center and top and side of nxn matrix

    for i in range(src.width):
        for j in range(src.height):
            sum = 0
            k = i - mid
            l = j - mid
            # loop for the first position of matrix n if it is put ontop of pixel on image
            for x in range(n):
                for y in range(n):
                    try:
                        # try so that if the pixel is out of bounds i dont have to deal with it
                        sum += mask[(x, y)] * ((src.get(k, l)[0] +
                                                src.get(k, l)[1] + src.get(k, l)[2]) / 3)
                        # i want to average the pixel values (assuming the index returns a part of the tuple)
                    except:
                        sum += 0
                    l += 1
                k += 1
            sum = sum/masktotal
            newsrc.set(i, j, (sum, sum, sum))
