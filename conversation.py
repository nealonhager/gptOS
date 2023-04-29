from collections import MutableSequence
from message import Message, Prompt, Response


class Conversation(MutableSequence):
    def __init__(self, *args):
        self.oktypes = ( Message, Prompt, Response )
        self.history = list()
        self.extend(list(args))

    def check(self, v):
        if not isinstance(v, self.oktypes):
            raise TypeError

    def __len__(self): return len(self.history)

    def __getitem__(self, i): return self.history[i]

    def __delitem__(self, i): del self.history[i]

    def __setitem__(self, i, v):
        self.check(v)
        self.history[i] = v

    def insert(self, i, v):
        self.check(v)
        self.history.insert(i, v)

    def __str__(self):
        return str(self.history)

    def export(self, filename, human_readable=False):
        """
        Exports the conversation to a file
        """
        with open(filename, "w") as f:
            if human_readable:
                f.write("\n".join([f"{str.upper(x.name)} - ({str.upper(x.role)})\n\t{x.content}\n" for x in self.history]))
            else:
                f.write("\n".join([x.to_json() for x in self.history]))