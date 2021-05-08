class Category:

    @classmethod
    def from_rows(cls, rows):
        items = []
        for row in rows:
            items.append(cls(row))
        return items

    @property
    def to_dict(self):
        as_dict = {}
        for name, value in self.__dict__.items():
            if not name.startswith('_') and not callable(value):
                as_dict[name] = value
        return as_dict

    def __init__(self, row: tuple):
        self.id = row[0]
        self.name = row[1]