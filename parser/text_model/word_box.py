def pretty_word(w):
    """
    capitablize first char and lowecase other chars
    """
    return w[0].upper() + w[1:].lower()


def is_price(s):
    """
    check if a string is a price (aka a float)
    """
    try:
        float(s)
        return True
    except ValueError:
        return False


class Word():
    """
    a word object for a detected text
    includes the position of the box, the text, and the recognition confidence
    """
    def __init__(self, a, b, c, d, text, confidence):
        """
        args: the 4 points of the box, and each point is a tuple (x, y)
                the box is like this:
                    d ---- c
                    |      |
                    a ---- b
        """
        # vars
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.text = pretty_word(text)
        self.confidence = confidence
        # price
        self.numeric = is_price(text)
        self.price = None
        if self.numeric:
            self.price = float(text)
        # calculate some stats
        self.width = self.b[0] - self.a[0]
        self.height = self.d[1] - self.a[1]
        self.center = ((self.a[0] + self.b[0]) / 2, (self.a[1] + self.d[1]) / 2)
    
    def print_stats(self):
        print(f"word: {self.text}, center: {self.center}, confidence: {self.confidence}")

    def get_center(self):
        return self.center

