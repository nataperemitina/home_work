
class Node(object):
    __slots__ = ('__data', '__next')

    def __init__(self, data):
        self.__data = data
        self.__next = None

    def set_next(self, next):
        self.__next = next

    def get_next(self):
        return self.__next

    def get_data(self):
        return self.__data

    def __repr__(self):
        return "[data:{0}, next:{1}]".format(self.__data, self.__next)


class LinkedList(object):
    __slots__ = ('__head', '__tail', '__size', '__current')

    def __init__(self, *args):
        self.__head = None
        self.__tail = None
        self.__current = None
        self.__size = 0
        for i in args:
            self.add(i)

    def __repr__(self):
        node = self.__head
        sstr = str()
        while node:
            sstr += (" {},".format(node.get_data()))
            node = node.get_next()

        return ("{}({})".format(self.__class__.__name__, sstr.strip().rstrip(',')))

    def add(self, data):
        node = Node(data)
        if not self.__head:
            self.__head = node
            self.__current = node
        else:
            self.__tail.set_next(node)

        self.__tail = node
        self.__size += 1

    def len(self):
        return self.__size

    def contains(self, data):
        node = self.__head
        while node:
            if node.get_data() == data:
                return True
            node = node.get_next()
        return False

    def remove(self, data):
        node = self.__head
        prev_node = None
        while node:
            if node.get_data() == data:
                if prev_node:
                    prev_node.set_next(node.get_next())
                    if not node.get_next():
                        self.__tail = prev_node
                elif not node.get_next():
                    self.__head = None
                    self.__tail = None
                    self.__current = self.__head
                else:
                    self.__head = node.get_next()
                    self.__current = self.__head

                self.__size -= 1
                break

            prev_node = node
            node = node.get_next()

    def remove_at(self, index):
        if index >= self.__size:
            raise IndexError

        node = self.__head
        prev_node = None
        cur_index = 0
        while cur_index < index:
            prev_node = node
            node = node.get_next()
            cur_index += 1

        if prev_node:
            prev_node.set_next(node.get_next())
            if not node.get_next():
                self.__tail = prev_node
        elif not node.get_next():
            self.__head = None
            self.__tail = None
            self.__current = self.__head
        else:
            self.__head = node.get_next()
            self.__current = self.__head

        self.__size -= 1
        return node.get_data()

    def insert(self, index, data):
        new_node = Node(data)

        if not self.__head:
            self.__head = new_node
            self.__tail = new_node
            self.__current = self.__head
        elif index == 0:
            new_node.set_next(self.__head)
            self.__head = new_node
            self.__current = self.__head
        elif index >= self.__size:
            self.__tail.set_next(new_node)
            self.__tail = new_node
        else:
            node = self.__head
            cur_index = 0
            while cur_index != index - 1:
                node = node.get_next()
                cur_index += 1

            new_node.set_next(node.get_next())
            node.set_next(new_node)

        self.__size += 1

    def get(self, index):
        if index >= self.__size:
            raise IndexError

        node = self.__head
        cur_index = 0
        while node:
            if cur_index == index:
                return node.get_data()
            node = node.get_next()
            cur_index += 1

    def clear(self):
        self.__head = None
        self.__tail = None
        self.__size = 0

    def is_empty(self):
        if self.__size == 0:
            return True
        else:
            return False

    def __iter__(self):
        return self

    def __next__(self):
        if self.__current:
            data = self.__current.get_data()
            self.__current = self.__current.get_next()
            return data
        else:
            self.__current = self.__head
            raise StopIteration

