class Square:

    def __init__(self,row,col, piece= None):
        self.row = row
        self.col = col
        self.piece = piece
   
    def __eq__(self, other):
        return self.row == other.row and self.col == other.col
    
    def has_piece(self):
        return self.piece != None
    
    def is_empty(self):
        return not self.has_piece()
    
    def my_colored_taken(self,color):
        return self.has_piece() and self.piece.color == color

    def other_colored_taken(self,color):
        return self.has_piece() and self.piece.color != color

    def is_empty_or_other_colored_taken(self, color):
        return self.is_empty() or self.other_colored_taken(color)

    def has_behind(self, color):
        return self.other_colored_taken(color) 

    @staticmethod
    def in_range(*args):
        for arg in args:
            if arg < 0 or arg > 7:
                return False
        return True
    