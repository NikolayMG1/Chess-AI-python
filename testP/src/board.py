from const import *
from square import Square
from piece import *
from move import Move
import copy
from ai import AI

class Board:

    def __init__(self):
        self.squares = [[0,0,0,0,0,0,0,0] for col in range(COLS)]
        self.last_move = None
        self.create()
        self.add_pieces('white')
        self.add_pieces('black')
        self.counter_white = 0
        self.counter_black = 0
        
    def move(self, piece, move):
        initial = move.initial
        final = move.final
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        if isinstance(piece, Pawn):
            self.pawn_prom(piece, final)

        if isinstance(piece, King):
            if self.castling(initial, final):
                diff = final.col - initial.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                # print(rook.moves.final.row, rook.moves.final.col, rook.name, rook.color)
                if rook.moves and len(rook.moves) > 0:  # Check if moves list is not empty and has elements
                    self.move(rook, rook.moves[-1])


        piece.moved = True
        piece.clear_moves()
        self.last_move = move

    def pawn_prom(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)      

    def castling(self,initial, final):
        return abs(initial.col - final.col) == 2

    def valid_move(self, piece, move):
        return move in piece.moves

    def calc_moves(self, piece, row, col, bool=True):

        def knight_moves():
            possible_moves = [
                (row+2, col+1),
                (row+2, col-1),
                (row-2, col+1),
                (row-2, col-1),
                (row+1, col+2),
                (row+1, col-2),
                (row-1, col-2),
                (row-1, col+2)
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move
                
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].is_empty_or_other_colored_taken(piece.color):
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        move = Move(initial, final)

                        if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                        else:
                            piece.add_move(move)

        def pawn_moves():      
            steps = 1 if piece.moved else 2
            start = row + piece.dir 
            end = row + (piece.dir * (1 + steps))

            for move_row in range(start, end, piece.dir):
                if Square.in_range(move_row):
                    
                    if self.squares[move_row][col].is_empty():

                        initial = Square(row,col)
                        final = Square(move_row, col)
                        move = Move(initial, final)
                        
                        if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                        else:
                            piece.add_move(move)
                    else:
                        break 
                else:
                    break
            move_row = row + piece.dir
            possible_move_cols = [col - 1, col + 1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(move_row, possible_move_col):
                    if self.squares[move_row][possible_move_col].other_colored_taken(piece.color):
                        initial = Square(row,col)
                        final_piece = self.squares[move_row][possible_move_col].piece
                        final = Square(move_row, possible_move_col, final_piece)
                        move = Move(initial, final)

                        if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                        else:
                            piece.add_move(move)
            
        def bishop_moves():
            possible_moves = []
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

            for dx, dy in directions:
                for i in range(1,8):
                    x, y = i*dx + row, i*dy + col
                    if Square.in_range(x, y) and self.squares[x][y].other_colored_taken(piece.color) :
                        possible_moves.append((x, y))
                        break
                    elif Square.in_range(x, y) and self.squares[x][y].my_colored_taken(piece.color):
                        break
                    else :possible_moves.append((x, y))
                    # print(x, y)

            for possible_move in possible_moves: 
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    # print(possible_move_row, possible_move_col)
                    if self.squares[possible_move_row][possible_move_col].is_empty_or_other_colored_taken(piece.color):  
                            initial = Square(row, col)
                            final_piece = self.squares[possible_move_row][possible_move_col].piece
                            final = Square(possible_move_row, possible_move_col, final_piece)
                            move = Move(initial, final)
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)

        def rook_moves():

            possible_moves = []
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

            for dx, dy in directions:
                for i in range(1,8):
                        x, y = i*dx + row, i*dy + col
                        if Square.in_range(x, y) and self.squares[x][y].other_colored_taken(piece.color) :
                            possible_moves.append((x, y))
                            break
                        elif Square.in_range(x, y) and self.squares[x][y].my_colored_taken(piece.color):
                            break
                        else :possible_moves.append((x, y))

            for possible_move in possible_moves: 
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    # print(possible_move_row, possible_move_col)
                    if self.squares[possible_move_row][possible_move_col].is_empty_or_other_colored_taken(piece.color):  
                            initial = Square(row, col)
                            final_piece = self.squares[possible_move_row][possible_move_col].piece
                            final = Square(possible_move_row, possible_move_col, final_piece)
                            move = Move(initial, final)
                            
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                            
        def queen_moves():

            directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
            possible_moves = []
            
            for dx, dy in directions:
                for i in range(1,8):
                    x, y = i*dx + row, i*dy + col
                    if Square.in_range(x, y) and self.squares[x][y].other_colored_taken(piece.color) :
                        possible_moves.append((x, y))
                        break
                    elif Square.in_range(x, y) and self.squares[x][y].my_colored_taken(piece.color):
                        break
                    else :possible_moves.append((x, y))

            for possible_move in possible_moves: 
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    # print(possible_move_row, possible_move_col)
                    if self.squares[possible_move_row][possible_move_col].is_empty_or_other_colored_taken(piece.color):  
                            initial = Square(row, col)
                            final_piece = self.squares[possible_move_row][possible_move_col].piece
                            final = Square(possible_move_row, possible_move_col, final_piece)
                            move = Move(initial, final)
                            
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)

        def king_moves():
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
            possible_moves = []

            for dx, dy in directions:
                    x, y = dx + row, dy + col
                    # print(x, y)
                    if Square.in_range(x, y) and self.squares[x][y].is_empty_or_other_colored_taken(piece.color) :
                        possible_moves.append((x, y))
                    # print(x, y)

            for possible_move in possible_moves: 
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    # print(possible_move_row, possible_move_col)
                    if self.squares[possible_move_row][possible_move_col].is_empty_or_other_colored_taken(piece.color):  
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
            
            if piece.moved == False:
                
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if right_rook.moved == False:
                        breaker = True
                        for i in range(5, 7):
                            if self.squares[row][i].has_piece():
                                breaker = False
                        if breaker:
                            piece.right_rook = right_rook

                            initialK = Square(row, col)
                            finalK = Square(row, 6)
                            moveK = Move(initialK, finalK)

                            initialR = Square(row, 7)
                            finalR = Square(row, 5)
                            moveR = Move(initialR, finalR)

                            if bool:
                                if not self.in_check(piece, moveK) and not self.in_check(right_rook, moveR):
                                    piece.right_rook.add_move(moveR)
                                    piece.add_move(moveK)
                            else:   
                                print(initialR.row, initialR.col, finalR.row, finalR.col)                        
                                piece.right_rook.add_move(moveR)
                                piece.add_move(moveK)

                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if left_rook.moved == False:
                        for i in range(1, 4):
                            if self.squares[row][i].has_piece():
                                return
                        piece.left_rook = left_rook

                        initialK = Square(row, col)
                        finalK = Square(row, 2)
                        moveK = Move(initialK, finalK)

                        initialR = Square(row, 0)
                        finalR = Square(row, 3)
                        moveR = Move(initialR, finalR)
                        
                        if bool:
                            if not self.in_check(piece, moveK) and not self.in_check(left_rook, moveR):
                                piece.left_rook.add_move(moveR)
                                piece.add_move(moveK)
                        else:
                            piece.left_rook.add_move(moveR)
                            piece.add_move(moveK)


        if isinstance(piece, Pawn):
            pawn_moves()

        elif isinstance(piece, King):
            king_moves()

        elif isinstance(piece, Rook):
            rook_moves()

        elif isinstance(piece, Bishop):
            bishop_moves()

        elif isinstance(piece, Knight):
            knight_moves()

        elif isinstance(piece, Queen):
            queen_moves()

    def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move)

        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].other_colored_taken(piece.color):
                    # print(temp_board.squares[row][col].piece)
                    
                    p = temp_board.squares[row][col].piece
                    temp_board.calc_moves(p, row, col, bool=False)
                    for m in p.moves:
                        
                        if isinstance(m.final.piece, King):
                            return True 

        return False

    def create(self):
        
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        # pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # king
        self.squares[row_other][4] = Square(row_other, 4, King(color))
        
    def is_game_over(self, board):
        current_color = self.color  # Assuming self.color is the current player's color
        opponent_color = 'white' if current_color == 'black' else 'black'

        # Get all legal moves for the current player
        all_legal_moves = []
        for row in range(ROWS):
            for col in range(COLS):
                square = board.squares[row][col]
                if square.has_piece() and square.piece.color == current_color:
                    self.calc_moves(square.piece, row, col)
                    all_legal_moves.extend(square.piece.moves)

        # Check if the current player is in check
        in_check = self.is_player_in_check(board, current_color)

        if not all_legal_moves:
            if in_check:
                return True  # Checkmate
            else:
                return True  # Stalemate (no legal moves, but not in check)

        return False  # Game is not over

    def is_player_in_check(self, board, color):
        for row in range(ROWS):
            for col in range(COLS):
                square = board.squares[row][col]
                if square.has_piece() and square.piece.color == color:
                    if isinstance(square.piece, King):
                        return self.is_king_in_check(board, color, row, col)
        return False

    def is_king_in_check(self, board, color, row, col):
        opponent_color = 'white' if color == 'black' else 'black'

        # Check if any opponent's piece threatens the king's position
        for i in range(ROWS):
            for j in range(COLS):
                square = board.squares[i][j]
                if square.has_piece() and square.piece.color == opponent_color:
                    self.calc_moves(square.piece, i, j)
                    for move in square.piece.moves:
                        if isinstance(move.final.piece, King) and move.final.piece.color == color:
                            return True  # King is in check

        return False
