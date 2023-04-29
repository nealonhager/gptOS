import json


class Message:
    def __init__(self, role, content, name):
        self.role = role
        self.content = content
        self.name = name

    def to_dict(self):
        return {"role": self.role, "content": self.content, "name": self.name}

    def to_json(self):
        return json.dumps(self.to_dict())


class Prompt(Message):
    def __init__(self, content):
        super().__init__(role="user", content=content, name="Human")


class Response(Message):
    def __init__(self, content):
        super().__init__(role="assistant", content=content, name="AI")
