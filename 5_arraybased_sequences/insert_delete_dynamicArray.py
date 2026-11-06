from dynamicArray_example import DynamicArray   # base class from the other file


class InsertableDynamicArray(DynamicArray):
    # DynamicArray plus insert and remove

    # inserting into a Dynamic Array
    def insert(self, k, value):
        # insert value at index k, shifting other values right
        if self._n == self._capacity:
            self._resize(2 * self._capacity)
        for j in range(self._n, k, -1):
            self._A[j] = self._A[j-1]
        self._A[k] = value
        self._n += 1

    # remove from a dynamic array
    def remove(self, value):
        for k in range(self._n):
            if self._A[k] == value:
                for j in range(k, self._n - 1):  # found a match!
                    self._A[j] = self._A[j+1]
                self._A[self._n - 1] = None      # help garbage collection
                self._n -= 1                     # we have one less item
                return                           # exit immediately
        raise ValueError('value not found')      # only reached if no match



arr = InsertableDynamicArray()
arr.append('a')
arr.append('b')
arr.append('c')
print(list(arr), len(arr))   # ['a', 'b', 'c'] 3

arr.insert(1, 'X')           # put 'X' at index 1
print(list(arr), len(arr))   # ['a', 'X', 'b', 'c'] 4

arr.remove('b')              # remove the first 'b'
print(list(arr), len(arr))   # ['a', 'X', 'c'] 3
