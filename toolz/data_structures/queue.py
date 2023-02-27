from collections import deque

# Note on deque (pronounced "deck") vs list:
# dequeue allows for O(1) insertion and removal from both ends
# whereas a list only allows for O(1) insertion and removal from the end


class Queue:
    def __init__(self):
        self.nodes = deque()

    def is_empty(self, nodes):
        return len(nodes) == 0

    def enqueue(self, node):
        self.nodes.append(node)

    def dequeue(self):
        if not self.is_empty(self.nodes):
            return self.nodes.popleft()
        else:
            return None

    def peek(self):
        if not self.is_empty(self.nodes):
            return self.nodes[0]
        else:
            return None

    def get_len(self):
        return len(self.nodes)

    def print_queue(self):
        print(self.nodes)
