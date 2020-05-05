from collections import namedtuple
import re
TableEntry = namedtuple("Element",'hash key value')

class NotFoundException(Exception):
    def __init__(self,exception):
        self.__exception = exception

    def getException(self):
        return self.__exception

class HashTable(object):
    DEFAULT_SIZE = 8
    EMPTY_VALUE = TableEntry(None, None, None)
    DELETED_VALUE = TableEntry(None, None, None)
    LOAD_FACTOR = 2 / 3
    MIN_FACTOR = 1 / 3

    def __init__(self):
        self.container = [self.EMPTY_VALUE]*self.DEFAULT_SIZE
        self.size = 0
        self.deleted_size = 0
        self.container_size = self.DEFAULT_SIZE

    def __len__(self):
        return self.size

    def __contains__(self, item):
        try:
            _ = self.get(item)
            return True
        except KeyError:
            return False

    def _resize(self):
        oldTable = self.container
        oldSize = self.size
        self.container_size = int(oldSize//self.MIN_FACTOR)
        self.container = [self.EMPTY_VALUE]*self.container_size
        self.size = 0
        self.deleted_size = 0
        for element in oldTable:
            if element is not self.EMPTY_VALUE and element is not self.DELETED_VALUE:
                self.set(element.key, element.value)

    def __repr__(self):
        tokens = []
        for element in self.container:
            if element is not self.EMPTY_VALUE and element  is not self.DELETED_VALUE:
                tokens.append("{0} : {1}".format(element.key, element.value))
        return "{" + "\n".join(tokens) + "}"

    def _getElement(self, key):
        """
        :param key: index
        :return: (V,I )
            V : value or EMPTY_VALUE
            I : index where it was found or if V is EMPTY_VALUE
            then it returns the nest insert index for the given key
        """
        keyHash = hash(key)
        rootindex = keyHash
        for off in range(self.container_size):
            index = (rootindex + off)%self.container_size
            element = self.container[index]
            if element is self.EMPTY_VALUE or element.hash == keyHash and element.key == key:
                return (element, index)
        raise KeyError

    def set(self, key, value):
        entry, index = self._getElement(key)
        self.container[index] = TableEntry(hash(key),key, value)
        if entry is self.EMPTY_VALUE:
            self.size += 1
        if (self.deleted_size + self.size) / self.container_size >self.LOAD_FACTOR:
            self._resize()

    def __setitem__(self, key, value):
        self.set(key,value)

    def get(self, key):
        entry, _ = self._getElement(key)
        if entry is self.EMPTY_VALUE:
            raise KeyError('Key {0} not in hash table'.format(key))
        else:
            return entry.value

    def __getitem__(self, key):
        return self.get(key)

    def delete(self, key):
        entry, index = self._getElement(key)
        if entry is self.EMPTY_VALUE:
            raise KeyError('Key {0} not in hashtable'.format(key))
        else:
            self.container[index] = self.DELETED_VALUE
            self.size -= 1
            self.deleted_size +=1

    def __delitem__(self, key):
        self.delete(key)


class Analizor:
    def __init__(self,preTable, inputFile):
        self.__preTable = preTable
        self.__inputFile = inputFile
        self.__FIP = []
        self.__idTable = HashTable()
        self.__ctTable = HashTable()

    def parsare(self):
        with open(self.__inputFile) as f:
            line = f.readline()
            while line:
                line = line.strip()
                elems = line.split(" ")
                for elem in elems:
                    if len(elem) > 0 and elem != "\n":
                        if elem in self.__preTable:
                            self.__FIP.append([self.__preTable[elem],None])
                        else:
                            is_identificator_or_constanta = self.__verificare(elem)
                            if not is_identificator_or_constanta:
                                raise NotFoundException("Atom is not a valid identificator  or constant")
                    else:
                        if len(elem) > 8:
                            raise NotFoundException("Literal length is longer than 8")
                line = f.readline()

    def __verificare(self,elem):
        is_id = self.__verifID(elem)
        if is_id is True:
            self.__idTable.set(sum(map(ord, elem)),elem)
            self.__FIP.append([self.__preTable['ID'],sum(map(ord,elem))])
            return True
        is_const = self.__verifConst(elem)
        if is_const is True:
            self.__ctTable.set(sum(map(ord,elem)),elem)
            self.__FIP.append([self.__preTable['CONST'],sum(map(ord,elem))])
            return True
        return False

    def __verifID(self,elem):
        pattern = re.compile('^[a-zA-Z]([a-zA-Z0-9])*$')
        return pattern.match(elem) is not None

    def __verifConst(self,elem):
        if len(elem) == 1 and elem[0] == '0':
            return True
        patternInt = re.compile('^[1-9]([0-9])*$')
        patternFloat = re.compile('^[0-9]([0-9])*.[0-9]([0-9])*$')

        if patternInt.match(elem) is not None:
            return True
        if patternFloat.match(elem):
            return True
        return False

    def getPredefTable(self):
        return self.__preTable

    def getIDTable(self):
        return self.__idTable

    def getConstTable(self):
        return self.__ctTable

    def getFip(self):
        return  self.__FIP