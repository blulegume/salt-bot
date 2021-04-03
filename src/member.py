class Member():
    def __init__(self, id, name, nick, **kwargs):
        self._id = id
        self._name = name
        self._nick = nick

    @property
    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'nick': self.nick
        }
    @property
    def id(self):
        return self._id
    @property
    def name(self):
        return self._name
    @property
    def nick(self):
        return self._nick if self._nick else self.name
