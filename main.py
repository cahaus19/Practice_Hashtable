items_ = """
Write a hash table data structure.

Must contain the following methods:
    __getitem__
    __setitem__
    __delitem__
    __eq__
    __bool__
    __contains__
    __len__
    __iter__

    clear
    copy
    setdefault (if it's in the dictionary, returns what's there.  Otherwise, sets the entry in the dictionary)
    popitem (pops a random key/value pair from the dictionary)
    pop (pops a specific item from the dictionary or a random item if no parameters are added)

    keys
    values
    items
"""
from enum import Enum
from sympy import *


class BucketStatus(Enum):
    FULL = 1
    EMPTY = 2
    DUMMY = 3


class HashTableStructure:
    MIN_BUCKETS = 11

    def __init__(self):
        self._keys = [None for _ in range(self.MIN_BUCKETS)]
        self._values = [None for _ in range(self.MIN_BUCKETS)]
        self._bucketstatus = [BucketStatus.EMPTY for _ in range(self.MIN_BUCKETS)]
        self._len = 0

    def _numberofbuckets(self):
         return len(self._bucketstatus)

    def _getindex(self, key):
        k = 0
        # this will throw an error if item is not hashable
        hash_item = hash(key)
        while True:
            index = (hash_item + k ** 2) % self._numberofbuckets()
            k += 1
            if self._bucketstatus[index] is BucketStatus.EMPTY:
                raise KeyError('Nope, not in here')
            if self._bucketstatus[index] is BucketStatus.DUMMY:
                continue
            if key is self._keys[index] or (key == self._keys[index] and hash(key) == hash(self._keys[index])):
                return index
            # TODO: update and add counter to make sure no infinite cycles

    def _resize(self):
        if self._len >= .49*self._numberofbuckets():
            desired_length = nextprime(2*self._numberofbuckets())
            #number_of_buckets_to_add = desired_length - len(self._bucketstatus) + 1
            old_keys = self._keys
            old_values = self._values
            old_bucket_status = self._bucketstatus
            self._keys = [None for _ in range(desired_length)]
            self._values = [None for _ in range(desired_length)]
            self._bucketstatus = [BucketStatus.EMPTY for _ in range(desired_length)]
            self._len = 0
            for i in range(len(old_keys)):
                if old_bucket_status[i] is BucketStatus.FULL:
                    self.__setitem__(old_keys[i], old_values[i])

    def __getitem__(self, key):
        index = self._getindex(key)
        return self._values[index]

    def __setitem__(self, key, value):
        k = 0
        hash_item = hash(key)
        dummy_waiting_room = None
        while True:
            index = (hash_item + k ** 2) % self._numberofbuckets()
            k += 1
            if self._bucketstatus[index] is BucketStatus.EMPTY:
                if dummy_waiting_room is not None:
                    index = dummy_waiting_room

                self._keys[index] = key
                self._values[index] = value
                self._bucketstatus[index] = BucketStatus.FULL
                self._len += 1
                # now resize
                self._resize()

                return
            if self._bucketstatus[index] is BucketStatus.DUMMY:
                if dummy_waiting_room is None:
                    dummy_waiting_room = index
                continue
            if self._keys[index] is key or (key == self._keys[index] and hash(key) == hash(self._keys[index])):
                self._values[index] = value


    def  __delitem__(self, key):
        index = self._getindex(key)
        self._bucketstatus[index] = BucketStatus.DUMMY

    def __iter__(self):
        yield from self._iter_any_list(self._keys)

    def _iter_any_list(self, input_list):
        for i in range(len(input_list)):
            if self._bucketstatus is BucketStatus.FULL:
                yield input_list[i]

    def keys(self):
        #functions the same as [x for x in self.__iter__()]
        return [x for x in self]

    def values(self):
        return [x for x in self._iter_any_list(self._values)]

    def items(self):
        return [(k,v) for k,v in zip(self, self._iter_any_list(self._values))]

    def __eq__(self, other):
        # type() matches if the class of one is the exact same as the type of the other (no inheritance)
        # isinstance() matches if you inherit from original type
        if not isinstance(self, other):
            return False
        if len(self) != len(other):
            return False
        for k in self:
            if k not in other:
                return False
            if self.__getitem__(k) != other.__getitem__(k):
                return False
        return True

    def __len__(self):
        return self._len

    def __contains__(self, item):
        try:
            self._getindex(item)
            return True
        except KeyError:
            return False

    def __bool__(self):
        #shorthand: return if len(self) > 0
        if len(self) > 0:
            return True
        return False

    def clear(self):
        self._keys = [None for _ in range(self.MIN_BUCKETS)]
        self._values = [None for _ in range(self.MIN_BUCKETS)]
        self._bucketstatus = [BucketStatus.EMPTY for _ in range(self.MIN_BUCKETS)]
        self._len = 0

    def copy(self):
        #shallow copy: pointer to the same place in memory as the other
        #deep copy: have to go into every single object in your dictionary and go recursively to recopy every single item
        copied_instance = type(self)()
        for k,v in self.items():
            copied_instance.__setitem__(k,v)
        return copied_instance

    def pop(self, key=None):
        if not self:
            raise TypeError('Nothing in Dictionary')
        if key is not None:
            returned_value = self.__getitem__(key)
            del self[key]
            return returned_value
        for item in self:
            key = item
            returned_value = self.__getitem__(key)
            break
        del self[key]
        return returned_value

    def popitem(self):
        if not self:
            raise TypeError('Nothing in Dictionary')
        for item in self:
            key = item
            returned_value =self.__getitem__(key)
            break
        del self[key]
        return key, returned_value

    def setdefault(self, key, value):
        try:
            return self.__getitem__(key)
        except KeyError:
            self.__setitem__(key, value)
            return value