class MemoryWindow:
    def __init__(self, size=3):
        self.size = size
        self.buffer = []

    def add(self, exchange):
        """Add an exchange dict: {"user": ..., "assistant": ...}"""
        self.buffer.append(exchange)
        if len(self.buffer) > self.size:
            self.buffer.pop(0)

    def get_texts(self):
        return list(self.buffer)

    def clear(self):
        self.buffer = []
