class Line():
    """
    just a line of words
    We process in into an item name and a price (if there is one)
    """
    def __init__(self, words):
        self.words = words
        self.process()
    
    def process(self):
        """
        process the line into an item name and a price
        NOTE: this method is HARDCODED, it assumes:
            - the last word is the price
            - the price only confuses . with ,
        """
        if len(self.words) <= 1:
            self.price = None
            self.item_name = " ".join([word.text for word in self.words])
        else:
            self.item_name = " ".join([word.text for word in self.words[:-1]])
            # check if the last word is a price
            if self.words[-1].numeric:
                self.price = self.words[-1].price
            else:
                self.price = float(self.words[-1].text.replace(",", "."))
    
    def print_line(self):
        print(self.item_name, self.price)


class TextCorpus():
    """
    a text corpus is just a collection of BoundingBox
    and includes methods to process the words
    """
    def __init__(self, words_list, y_delta=40, min_confidence=0.5):
        """
        args:
            words_list: a list of BoundingBox
            y_delta: the max distance between two words to be considered in the same line
        """
        self.words_list = words_list
        self.y_delta = y_delta
        self.min_confidence = min_confidence
    
    def filter_by_confidence(self):
        """
        filters out the words with low confidence
        """
        self.words_list = [word for word in self.words_list if word.confidence > self.min_confidence]
    
    def get_lines(self):
        """
        returns a list of lines, where each line is a list of BoundingBox that we think are in the same y position
        """
        # sort the words by y coordinate
        self.words_list.sort(key=lambda word: word.get_center()[1])
        # create the lines
        lines = []
        for word in self.words_list:
            # check if the word is in the same line as the last word
            if len(lines) == 0 or abs(lines[-1][-1].get_center()[1] - word.get_center()[1]) > self.y_delta:
                # create a new line
                lines.append([word])
            else:
                # add to the last line
                lines[-1].append(word)
        # order lines
        lines = self._order_lines(lines)
        # create the Lines objects
        lines = [Line(line) for line in lines]
        return lines

    def get_info_dict(self, lines):
        """
        given a list of lines, return a list of dict that maps item name to price
        """
        info = {}
        for line in lines:
            if line.price is not None:
                info[line.item_name] = line.price
        return info

    def _order_lines(self, lines):
        """
        order lines of words by their x coordinate
        """
        for line in lines:
            line.sort(key=lambda word: word.get_center()[0])
        return lines
    
    def print_lines(self, lines):
        """
        prints the lines
        """
        for line in lines:
            line.print_line()
