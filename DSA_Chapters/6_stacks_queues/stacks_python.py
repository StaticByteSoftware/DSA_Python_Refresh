# Implementing a stack using a Python List as storage

class ArrayStack:
    # LIFO stack implementation using python list for storage
    def __init__(self):
        # create an empty stack 
        self._data = [] #non public list instance

    def __len__(self):
        # return the number of elemetns in the stack 
        return len(self._data)

    def is_empty(self):
        # return True if the stack is empty 
        return len(self._data) == 0

    def push(self, e):
        # add element e to top of stack 
        self._data.append(e)    # new item stored at end of list

    def top(self):
        # return (but do not remove) element at top of stack
        if self.is_empty():
            raise Empty('Stack is empty')
        return self._data[-1]   # last item in the list 

    def pop(self):
        # remove and return elemetn from top of stack
        if self.is_empty():
            raise Empty('Stack is empty')
        return self._data.pop()     # remove last item from the list 
