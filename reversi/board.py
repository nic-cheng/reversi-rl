type Board = list[list[int]]

class Piece:
    BLACK = 1
    EMPTY = 0
    WHITE = -1
    
    def __str__(self):
        if self == self.BLACK:
            return "◯"
        elif self == self.WHITE:
            return "⬤"
        else:
            return "⠶"

