import array as arr


class MyListIterator:
    ''' Iterator class to make MyList iterable.
    https://thispointer.com/python-how-to-make-a-class-iterable-create-iterator-class-for-it/
    '''

    def __init__(self, lst):
        # MyList object reference
        self._lst: MyList = lst
        # member variable to keep track of current index
        self._index: int = 0

    def __next__(self):
        ''''Returns the next value from the stored MyList instance.'''
        if self._index < len(self._lst):
            value = self._lst[self._index]
            self._index += 1
            return value
        # End of Iteration
        raise StopIteration


class MyList:
    '''A list interface.'''

    def __init__(self, size: int, value=None) -> None:
        """Creates a list of the given size, optionally intializing elements to value.

        The list is static. It only has space for size elements.

        Args:
        - size: size of the list; space is reserved for these many elements.
        - value: the optional initial value of the created elements.

        Returns:
        none
        """
        self.size = size
        self.value = value

    def __len__(self) -> int:
        '''Returns the size of the list. Allows len() to be called on it.

        Ref: https://stackoverflow.com/q/7642434/1382487

        Args:

        Returns:
        the size of the list.
        '''
        # return len(self)  # do i use metaclass? idk # len(self) isnt valid -akeel
        pass

    def __getitem__(self, i: int):
        '''Returns the value at index, i. Allows indexing syntax.

        Ref: https://stackoverflow.com/a/33882066/1382487

        Args:
        - i: the index from which to retrieve the value.

        Returns:
        the value at index i.
        '''
        # Ensure bounds.
        assert 0 <= i < len(self),\
            f'Getting invalid list index {i} from list of size {len(self)}'
        return self[i]

    def __setitem__(self, i: int, value) -> None:
        '''Sets the element at index, i, to value. Allows indexing syntax.

        Ref: https://stackoverflow.com/a/33882066/1382487

        Args:
        - i: the index of the elemnent to be set
        - value: the value to be set

        Returns:
        none
        '''
        # Ensure bounds.
        assert 0 <= i < len(self),\
            f'Setting invalid list index {i} in list of size {self.size()}'
        self[i] = value

    def __iter__(self) -> MyListIterator:
        '''Returns an iterator that allows iteration over this list.

        Ref: https://thispointer.com/python-how-to-make-a-class-iterable-create-iterator-class-for-it/

        Args:

        Returns:
        an iterator that allows iteration over this list.
        '''
        return MyListIterator(self)

    def get(self, i: int):
        '''Returns the value at index, i.

        Alternate to use of indexing syntax.

        Args:
        - i: the index from which to retrieve the value.

        Returns:
        the value at index i.
        '''
        return self[i]

    def set(self, i: int, value) -> None:
        '''Sets the element at index, i, to value.

        Alternate to use of indexing syntax.

        Args:
        - i: the index of the elemnent to be set
        - value: the value to be set

        Returns:
        none
        '''
        self[i] = value


class Node:
    def _init_(self, value):
        self.value = value
        self.next = None  # points to nothing


class PointerList(MyList):
    def _init_(self, size, value=None):
        MyList.__init__(self, size, value)

        self.head = None
        self.count = 0

        # make a linked list since since the list is static and fill it with dummy values
        # if self.head == None:  # if list is empty
        self.head = Node(value)
        current = self.head

        for x in range(int(self.size)):
            current.next = Node(value)
            current = current.next

    def _len_(self):
        # since the list is static, the length would be the size specified by the user
        return self.size

    def _getitem_(self, i: int):
        current = self.head
        if i > self.size:
            return "Index out of range"
        else:
            for x in range(self.size):
                if x == i:
                    return current.value
                else:
                    current = current.next
        return None

    def _setitem_(self, i: int, value) -> None:
        current = self.head
        if i > self.size:
            return "Index out of range"
        else:
            for x in range(self.size):
                if x == i:
                    current.value = value
                else:
                    current = current.next


# class ArrayList(MyList):

#     def __init__(self, size, value=None):
#         MyList.__init__(self, size, value)

#         self.r = arr.array('i', [])
#         self.g = arr.array('i', [])
#         self.b = arr.array('i', [])

#         for i in range(self.size):
#             self.r.extend(value)
#             self.g.extend(value)
#             self.b.extend(value)

#     def __getitem__(self, i: int):
#         assert 0 <= i < len(self),\
#             f'Getting invalid list index {i} from list of size {len(self)}'
#         return (self.r[i], self.g[i], self.b[i])

#     def __setitem__(self, i: int, value) -> None:
#         assert 0 <= i < len(self),\
#             f'Setting invalid list index {i} in list of size {self.size()}'
#         self.r[i] = value[0]
#         self.g[i] = value[1]
#         self.b[i] = value[2]

#     def __len__(self):
#         return len(self.r)
# class ArrayList(MyList):

#     def __init__(self, size, value=None):
#         MyList.__init__(self, size, value)

#         self.rgb = arr.array('I', [])

#         for i in range(self.size):
#             for j in range(3):
#                 if value[j] < 10:
#                     temp = "0"+"0"+str(value[j])
#                     self.rgb.append(int(temp))
#                 elif value[j] < 100:
#                     temp = '0'+str(value[j])
#                     self.rgb.append(int(temp))
#                 elif value[j] < 1000:
#                     self.rgb.append(int(str(value[j])))

#     def __getitem__(self, i: int):

#         assert 0 <= i < len(self),\
#             f'Getting invalid list index {i} from list of size {len(self)}'

#         temp = str(self.rgb[i])
#         while len(temp) <= 9:
#             temp = "0" + temp

#         return (int(temp[0:3]), int(temp[3:6]), int(temp[6:9]))

#     def __setitem__(self, i: int, value) -> None:

#         assert 0 <= i < len(self),\
#             f'Setting invalid list index {i} in list of size {self.size()}'

#         a = str(value[0])
#         while len(a) <= 3:
#             a = "0" + a
#         b = str(value[1])
#         while len(b) <= 3:
#             b = "0" + b
#         c = str(value[2])
#         while len(c) <= 3:
#             c = "0" + c

#         self.rgb[i] = int(a + b + c)

#     def __len__(self):
#         return len(self.rgb)
class ArrayList(MyList):

    def __init__(self, size, value=None):
        MyList.__init__(self, size, value)

        self.rgb = arr.array('i', [])

        if value is not None:
            for i in range(int(self.size)):
                self.rgb.extend([value[0], value[1], value[2]])
        else:
            for i in range(int(self.size)):
                self.rgb.extend([0, 0, 0])

    def __getitem__(self, i: int):
        return (self.rgb[i*3], self.rgb[(i*3)+1], self.rgb[(i*3)+2])

    def __setitem__(self, i: int, value) -> None:
        self.rgb[(i*3)] = value[0]
        self.rgb[(i*3)+1] = value[1]
        self.rgb[(i*3)+2] = value[2]

    def __len__(self):
        return self.size
