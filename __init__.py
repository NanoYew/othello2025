# Generation ID: Hutch_1765784632459_7c7sj60p3 (前半)

class myai:
    def __init__(self):
        self.board = [[0] * 6 for _ in range(6)]
        # 初期配置: 6x6では中央4マスに配置
        self.board[2][2] = -1  # 白
        self.board[2][3] = 1   # 黒
        self.board[3][2] = 1   # 黒
        self.board[3][3] = -1  # 白
    
    def get_valid_moves(self, player):
        valid_moves = []
        for row in range(6):
            for col in range(6):
                if self.board[row][col] == 0 and self._is_valid_move(player, row, col):
                    valid_moves.append((row, col))
        return valid_moves
    
    def _is_valid_move(self, player, row, col):
        if self.board[row][col] != 0:
            return False
        
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
        for dr, dc in directions:
            if self._has_flips(player, row, col, dr, dc):
                return True
        
        return False
    
    def _has_flips(self, player, row, col, dr, dc):
        r, c = row + dr, col + dc
        opponent = -player
        found_opponent = False
        
        while 0 <= r < 6 and 0 <= c < 6:
            if self.board[r][c] == opponent:
                found_opponent = True
            elif self.board[r][c] == player:
                return found_opponent
            else:
                return False
            r += dr
            c += dc
        
        return False
    
    def make_move(self, player, row, col):
        if self.board[row][col] != 0:
            return False
        
        self.board[row][col] = player
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
        for dr, dc in directions:
            self._flip_stones(player, row, col, dr, dc)
        
        return True
    
    def _flip_stones(self, player, row, col, dr, dc):
        r, c = row + dr, col + dc
        opponent = -player
        to_flip = []
        
        while 0 <= r < 6 and 0 <= c < 6:
            if self.board[r][c] == opponent:
                to_flip.append((r, c))
            elif self.board[r][c] == player:
                for flip_r, flip_c in to_flip:
                    self.board[flip_r][flip_c] = player
                return
            else:
                return
            r += dr
            c += dc
    
    def is_game_over(self):
        return len(self.get_valid_moves(1)) == 0 and len(self.get_valid_moves(-1)) == 0
    
    def count_stones(self):
        black = sum(row.count(1) for row in self.board)
        white = sum(row.count(-1) for row in self.board)
        return (black, white)
    
    def copy(self):
        new_game = Othello6x6()
        new_game.board = [row[:] for row in self.board]
        return new_game


WEIGHT_MATRIX_6X6 = [
    [100, -5, 10, 10, -5, 100],
    [-5, -10, 1, 1, -10, -5],
    [10, 1, 5, 5, 1, 10],
    [10, 1, 5, 5, 1, 10],
    [-5, -10, 1, 1, -10, -5],
    [100, -5, 10, 10, -5, 100]
]


def evaluate_board(board, player):
    score = 0
    for row in range(6):
        for col in range(6):
            if board[row][col] == player:
                score += WEIGHT_MATRIX_6X6[row][col]
            elif board[row][col] == -player:
                score -= WEIGHT_MATRIX_6X6[row][col]
    return score


def minimax(board, depth, is_maximizing_player, player, game):
    if depth == 0 or game.is_game_over():
        return evaluate_board(board, player), None
    
    valid_moves = game.get_valid_moves(player if is_maximizing_player else -player)
    
    if not valid_moves:
        return minimax(board, depth - 1, not is_maximizing_player, player, game)
    
    best_move = None
    if is_maximizing_player:
        best_value = float('-inf')
        for move in valid_moves:
            temp_game = game.copy()
            temp_game.make_move(player, move[0], move[1])
            value, _ = minimax(temp_game.board, depth - 1, False, player, temp_game)
            if value > best_value:
                best_value = value
                best_move = move
        return best_value, best_move
    else:
        best_value = float('inf')
        for move in valid_moves:
            temp_game = game.copy()
            temp_game.make_move(-player, move[0], move[1])
            value, _ = minimax(temp_game.board, depth - 1, True, player, temp_game)
            if value < best_value:
                best_value = value
                best_move = move
        return best_value, best_move


def find_best_move_minimax(board, depth, player):
    game = Othello6x6()
    game.board = [row[:] for row in board]
    _, best_move = minimax(board, depth, True, player, game)
    return best_move


def alphabeta(board, depth, alpha, beta, is_maximizing_player, player, game):
    if depth == 0 or game.is_game_over():
        return evaluate_board(board, player), None
    
    valid_moves = game.get_valid_moves(player if is_maximizing_player else -player)
    
    if not valid_moves:
        return alphabeta(board, depth - 1, alpha, beta, not is_maximizing_player, player, game)
    
    best_move = None
    if is_maximizing_player:
        best_value = float('-inf')
        for move in valid_moves:
            temp_game = game.copy()
            temp_game.make_move(player, move[0], move[1])
            value, _ = alphabeta(temp_game.board, depth - 1, alpha, beta, False, player, temp_game)
            if value > best_value:
                best_value = value
                best_move = move
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
        return best_value, best_move
    else:
        best_value = float('inf')
        for move in valid_moves:
            temp_game = game.copy()
            temp_game.make_move(-player, move[0], move[1])
            value, _ = alphabeta(temp_game.board, depth - 1, alpha, beta, True, player, temp_game)
            if value < best_value:
                best_value = value
                best_move = move
            beta = min(beta, best_value)
            if beta <= alpha:
                break
        return best_value, best_move


def find_best_move_alphabeta(board, depth, player):
    game = Othello6x6()
    game.board = [row[:] for row in board]
    _, best_move = alphabeta(board, depth, float('-inf'), float('inf'), True, player, game)
    return best_move


def print_board(board):
    print("  0 1 2 3 4 5")
    for i, row in enumerate(board):
        print(f"{i} {' '.join(['○' if cell == 1 else '●' if cell == -1 else '·' for cell in row])}")


if __name__ == "__main__":
    game = Othello6x6()
    
    print("Initial board:")
    print_board(game.board)
    print()
    
    print("Valid moves for black (1):", game.get_valid_moves(1))
    print()
    
    print("Finding best move with Alpha-Beta pruning (depth=5)...")
    best_move = find_best_move_alphabeta(game.board, 5, 1)
    print(f"Best move for black: {best_move}")
    
    if best_move:
        game.make_move(1, best_move[0], best_move[1])
        print("\nBoard after AI move:")
        print_board(game.board)
        print(f"Stone count - Black: {game.count_stones()[0]}, White: {game.count_stones()[1]}")

# Generation ID: Hutch_1765784632459_7c7sj60p3 (後半)
