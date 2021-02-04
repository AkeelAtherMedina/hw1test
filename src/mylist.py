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
        pass

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
        pass

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
    def __init__(self, value):
        self.value = value
        self.next = None  # points to nothing


class PointerList(MyList):

    def __init__(self):
        self.head = None

    def insert(self, value):
        new_node = Node(value)  # new node created
        if self.head == None:  # if the list is empty
            self.head = new_node
            current_node = self.head  # head becomes current node

        else:
            while current_node != None:  # iterates over the list till we reach the end
                current_node = current_node.next
            current_node.next = new_node


class ArrayList(MyList):

    def __init__(self):
        MyList.__init__(self, self.size)

        temp = [self.value for i in range(self.size)]

        self.r = arr.array('i', [])
        self.r.extend(temp)
        self.g = arr.array('i', [])
        self.g.extend(temp)
        self.b = arr.array('i', [])
        self.b.extend(temp)

    def __getitem__(self, i: int):
        return (self.r[i], self.g[i], self.b[i])

    def __setitem__(self, i: int, value) -> None:
        self.r[i] = value[0]
        self.g[i] = value[1]
        self.b[i] = value[2]

    def __len__(self):
        return len(self.r)
