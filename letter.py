class Letter:
    def __init__(self, author, letter, image, drawn_in_free_mode, id=-1):
        self.id = id
        self.author = author
        self.letter = letter
        self.image = image
        self.drawn_in_free_mode = drawn_in_free_mode