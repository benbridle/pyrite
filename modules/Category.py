class Category:
    """
    Object representing a single category. Contains a name and a hint.
    """
    def __init__(self, name, hint=""):
        self.name = name
        self.hint = hint

    def __str__(self):
        return self.name

    def __len__(self):
        return len(str(self))