from myimage import MyImage
from mylist import *
from PIL import Image


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
    # 9 possible combinations of channels we can remove
    newsrc = MyImage(((src.size)[0], (src.size)[1]))  # initialise copy of src
    if not (red == True and blue == True and green == True):
        if red == True:
            for i in range(src.size[0]):
                for j in range(src.size[1]):
                    # traverse through image and get every pixel
                    r, g, b = src.get(i, j)
                    if (green == False) and (blue == False):
                        # our new image is the same as the src file, with red channel removed
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
                    # when all are false, it is the same as red channel being removed
                    newsrc.set(i, j, (0, g, b))
    else:  # if red green and blue are all True, everything channel is removed
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
    newsrc1 = MyImage((src.size[0], src.size[1]))  # sideways left
    newsrc2 = MyImage((src.size[0], src.size[1]))  # original
    newsrc3 = MyImage((src.size[0], src.size[1]))  # upside down
    newsrc4 = MyImage((src.size[0], src.size[1]))  # sideways right

    for i in range(src.size[0]):
        for j in range(src.size[1]):
            r, g, b = src.get(i, (src.size[0]-1)-j)  # sideways left
            newsrc1.set(j, i, (r, g, b))

            r, g, b = src.get(j, i)
            newsrc2.set(j, i, (r, g, b))  # original

            r, g, b = src.get((src.size[0]-1) - j,
                              (src.size[0]-1)-i)  # upside down
            newsrc3.set(j, i, (r, g, b))

            r, g, b = src.get((src.size[0]-1) - i, j)  # sideways right
            newsrc4.set(j, i, (r, g, b))

    # final image with 2 times the dimensions
    finalimg = MyImage((2*src.size[0], 2*src.size[1]), False)

    for x in range(src.size[0]):
        for y in range(src.size[1]):
            r, g, b = newsrc1.get(y, x)
            finalimg.set(y, x, (r, g, b))  # starting point is 0,0

            r, g, b = newsrc2.get(y, x)
            # starting point is 0,src.size[0]
            finalimg.set(y, x+src.size[0], (r, g, b))

            r, g, b = newsrc3.get(y, x)
            # starting point is src.size[0], 0
            finalimg.set(y+src.size[0], x, (r, g, b))

            r, g, b = newsrc4.get(y, x)
            # starting point is src.size[0], src.size[1]
            finalimg.set(y+src.size[0], x+src.size[1], (r, g, b))

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
        n = int(file1.readline())  # n^2 is the size of the mask

        # I will store mask values in a dictionary to map the row and column.
        mask = {}
        masktotal = 0  # if we need to average the mask, we must divide by the total mask weights applied to each pixel

        for i in range(n):
            for j in range(n):
                temp = file1.readline()
                try:
                    mask[(j, i)] = int(temp)
                    # dictionary to save mask value by index, must be an integer
                except:
                    pass
        file1.close()

        newsrc = MyImage((src.size[0], src.size[1]))  # initialise new image

        # distance between center pixel of image and top and side of nxn matrix
        mid = int((n-1)/2)

        for j in range(int(src.size[0])):
            for i in range(int(src.size[1])):

                sumo = 0  # new pixel value after mask, sum of weights
                # loop for the first position of matrix n if it is put ontop of pixel on image
                l = j - mid  # the pixel index column iterating over the mask mapped ontop of the image pixel j,i
                for x in range(n):  # iterating over the mask
                    k = i - mid  # the pixel index row iterating over the mask mapped ontop of the image pixel j,i
                    for y in range(n):  # iterating over the mask

                        try:  # try so that if the pixel is out of bounds it isnt considered
                            r, g, b = src.get(k, l)
                            # averaging of channels is always done, results in grayscale
                            rgb = ((r + g + b) // 3)
                            # multiplying with relevant mask weights
                            temp = mask[(x, y)] * rgb
                            sumo += temp
                            masktotal += mask[(x, y)]
                        except:
                            pass

                        k += 1
                    l += 1

                # we take average if bool passed is true, but we also cannot do zerodivision
                if masktotal != 0 and average == True:
                    sumo = int(sumo/masktotal)

                # this sum cannot be negative or over 255
                if sumo < 0:
                    sumo = 0
                elif sumo > 255:
                    sumo = 255

                newsrc.set(i, j, (sumo, sumo, sumo))  # apply sum to new images

                # set masktotal and sum to 0 for next iteration
                masktotal = 0
                sumo = 0
        return newsrc
    else:
        return  # in case there is no src image passed
