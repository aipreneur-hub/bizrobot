# bizrobot/core/memory/memory.py
class Memory:
    """In-memory store for episodes, plans, and tool logs."""
    def __init__(self):
        self.history = []

    def add(self, event):
        self.history.append(event)

    def recall(self, query=None):
        return self.history[-5:]
