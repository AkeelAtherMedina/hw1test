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


class Node: #separate class for Node
    def __init__(self, value):
        self.value = value
        self.next = None  # points to nothing


class PointerList(MyList):
    def __init__(self, size, value=None):
        MyList.__init__(self, size, value)

        self.head = None
        self.count = 0

        # make a linked list since since the list is static and fill it with values
        if value is not None:
            self.head = Node(value)
            current = self.head #current points to head node

            for x in range(int(self.size)):
                current.next = Node(value)
                current = current.next
        else:
            self.head = Node((None, None, None))
            current = self.head

            for x in range(int(self.size)):
                current.next = Node((None, None, None))
                current = current.next

    def __len__(self):
        # since the list is static, the length would be the size specified by the user
        return self.size

    def __getitem__(self, i: int):
        current = self.head #set current to the first node which is the head node 
        if i > self.size: #index provided should not be greater than the size of the list
            return "Index out of range"
        else:
            for x in range(self.size):
                if x == i:
                    return current.value
                else:
                    current = current.next
        return None

    def __setitem__(self, i: int, value) -> None:
        current = self.head #set current to the first node which is the head node
        if i > self.size: #index provided should not be greater than the size of the list
            return "Index out of range"
        else:
            for x in range(self.size):
                if x == i:
                    current.value = value
                else:
                    current = current.next


class ArrayList(MyList):

    def __init__(self, size, value=None):
        """
        Creates a list of the given size, optionally intializing elements to value.

        The list is static. It only has space for size elements.

        Args:
        - size: size of the list; space is reserved for these many elements.
        - value: the optional initial value of the created elements.

        Returns:
        none
        """
        MyList.__init__(self, size, value)  # initialise parent class

        self.rgb = arr.array('i', [])  # empty array of integers

        # we extend the array by 3 pixels, r, g, b, for every iteration.
        # this means our array is overall length of 3*self.size
        if value is not None:
            for i in range(int(self.size)):
                self.rgb.extend([value[0], value[1], value[2]])
        else:
            for i in range(int(self.size)):
                # no value given so any integer can be used
                self.rgb.extend([0, 0, 0])

    def __getitem__(self, i: int):
        '''
        Returns the value at index, i. 

        Args:
        - i: the index from which to retrieve the value.

        Returns:
        the value at index i.
        '''
        # we can retrieve an array element by index, and we must return the rgb values in a tuple
        # when we initialised the array, we gave 3 times the amount of entries than the size, so the ith element of the image is at 3*i for this implementation
        return (self.rgb[i*3], self.rgb[(i*3)+1], self.rgb[(i*3)+2])

    def __setitem__(self, i: int, value) -> None:
        '''
        Sets the element at index, i, to value. 

        Args:
        - i: the index of the elemnent to be set
        - value: the value to be set

        Returns:
        none
        '''
        # when we initialised the array, we gave 3 times the amount of entries than the size, so the ith element of the image is at 3*i for this implementation
        # the red, green and blue values are next to each other in index so we must add 1 to the index in this order
        self.rgb[(i*3)] = value[0]
        self.rgb[(i*3)+1] = value[1]
        self.rgb[(i*3)+2] = value[2]

    def __len__(self) -> int:
        '''
        Returns the size of the list.

        Args:

        Returns:
        the size of the list.
        '''
        return self.size
