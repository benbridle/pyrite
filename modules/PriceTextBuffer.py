import string
from swm.components import TextBuffer


class PriceTextBuffer(TextBuffer):
    def add(self, text: str):
        if not isinstance(text, str):
            raise TypeError("Text must be a string")
        for char in text:
            if char == "." and self.buffer.count(".") == 0:
                if len(self.buffer) == 0:
                    self.buffer += "0."
                else:
                    self.buffer += char
            if char in string.digits:
                if "." not in self.buffer:
                    self.buffer += char
                elif len(self.buffer.split(".")[-1]) < 2:  # if less than two digits after decimal place
                    self.buffer += char
