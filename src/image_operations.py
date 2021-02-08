from myimage import MyImage
from mylist import *
from PIL import Image
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
    # if red == True or ((red == False) and (green == False) and (blue == False)):
    #     for i in range(src.size[0]):
    #         for j in range(src.size[1]):
    #             r, g, b = src.get(i, j)
    #             newsrc.set(i, j, (255, g, b))
    # if green == True:
    #     for i in range(src.size[0]):
    #         for j in range(src.size[1]):
    #             r, g, b = src.get(i, j)
    #             newsrc.set(i, j, (r, 255, b))
    # if blue == True:
    #     for i in range(src.size[0]):
    #         for j in range(src.size[1]):
    #             r, g, b = src.get(i, j)
    #             newsrc.set(i, j, (r, g, 255))
    if not (red == True and blue == True and green == True):
        if red == True:
            for i in range(src.size[0]):
                for j in range(src.size[1]):
                    r, g, b = src.get(i, j)
                    if (green == False) and (blue == False):
                        newsrc.set(i, j, (0, g, b))
                    elif green == True and blue == False:
                        newsrc.set(i, j, (0, 0, b))
                    elif blue == True and green == False:
                        newsrc.set(i, j, (0, g, 0))
        elif green == True:
            for i in range(src.size[0]):
                for j in range(src.size[1]):
                    r, g, b = src.get(i, j)
                    if (red == False) and (blue == False):
                        newsrc.set(i, j, (r, 0, b))
                    elif blue == True:
                        newsrc.set(i, j, (r, 0, 0))
        elif blue == True and ((green == False) and (red == False)):
            for i in range(src.size[0]):
                for j in range(src.size[1]):
                    r, g, b = src.get(i, j)
                    newsrc.set(i, j, (r, g, 0))
        elif red == False and blue == False and green == False:
            for i in range(src.size[0]):
                for j in range(src.size[1]):
                    r, g, b = src.get(i, j)
                    newsrc.set(i, j, (0, g, b))
    else:
        for i in range(src.size[0]):
            for j in range(src.size[1]):
                r, g, b = src.get(i, j)
                newsrc.set(i, j, (0, 0, 0))
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
    newsrc1 = MyImage((src.size[0], src.size[1]), False)  # sideways left
    newsrc2 = deepcopy(src)  # original
    newsrc3 = MyImage((src.size[0], src.size[1]), False)  # upside down
    newsrc4 = MyImage((src.size[0], src.size[1]), False)  # sideways right

    for i in range(src.size[0]):
        for j in range(src.size[1]):
            r, g, b = src.get(j, (src.size[0]-1)-i)
            newsrc1.set(i, j, (r, g, b))

    for i in range(src.size[0]):
        for j in range(src.size[1]):
            r, g, b = src.get((src.size[0]-1) - i, (src.size[0]-1)-j)
            newsrc3.set(i, j, (r, g, b))

    for i in range(src.size[0]):
        for j in range(src.size[1]):
            r, g, b = src.get((src.size[0]-1) - j, i)
            newsrc4.set(i, j, (r, g, b))

    # final image with 2 times the dimensions
    finalimg = MyImage((2*src.size[0], 2*src.size[1]), False)

    for x in range(src.size[0]):
        for y in range(src.size[1]):
            r, g, b = newsrc1.get(x, y)
            finalimg.set(x, y, (r, g, b))

    for x in range(src.size[0]):
        for y in range(src.size[1]):
            r, g, b = newsrc2.get(x, y)
            finalimg.set(x, y+src.size[0], (r, g, b))

    for x in range(src.size[0]):
        for y in range(src.size[1]):
            r, g, b = newsrc3.get(x, y)
            finalimg.set(x+src.size[0], y, (r, g, b))

    for x in range(src.size[0]):
        for y in range(src.size[1]):
            r, g, b = newsrc4.get(x, y)
            finalimg.set(x+src.size[0], y+src.size[1], (r, g, b))

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
    if src is not None:
        file1 = open(maskfile, 'r')
        # print(src.size[0])
        n = int(file1.readline())
        # file1.seek(1)

        mask = {}
        masktotal = 0

        for i in range(n):
            for j in range(n):
                temp = file1.readline()
                try:
                    mask[(j, i)] = int(temp)
                    # dictionary to save mask value by index
                except:
                    pass
        file1.close()
        newsrc = deepcopy(src)
        mid = int((n-1)/2)
        # distance between center and top and side of nxn matrix
        for j in range(int(src.size[0])):
            for i in range(int(src.size[1])):
                sumo = 0
                # loop for the first position of matrix n if it is put ontop of pixel on image
                l = j - mid
                for x in range(n):
                    k = i - mid
                    for y in range(n):
                        try:
                            r, g, b = src.get(k, l)
                            rgb = ((r + g + b) // 3)
                            temp = mask[(x, y)] * rgb
                            # try so that if the pixel is out of bounds i dont have to deal with it
                            # sum += (r + g + b) // 3
                            sumo += temp
                            masktotal += mask[(x, y)]
                            if i == 10 and j == 10:
                                print((x, y))
                            # i want to average the pixel values (assuming the index returns a part of the tuple)
                        except:
                            pass
                        k += 1
                    l += 1
                if masktotal != 0 and average == True:
                    sumo = int(sumo/masktotal)
                if sumo < 0:
                    sumo = 0
                elif sumo > 255:
                    sumo = 255
                newsrc.set(i, j, (sumo, sumo, sumo))
                masktotal = 0
                sumo = 0
        return newsrc
    else:
        return
