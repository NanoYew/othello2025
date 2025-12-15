# Generation ID: Hutch_1763363898192_thz8gnz7l (前半)

from collections import deque

BLACK = 1
WHITE = 2

def othello(board, color):
    """
    オセロの最適な手を返す関数
    """
    size = len(board)
    opponent = WHITE if color == BLACK else BLACK
    
    # コーナー位置と辺の位置を定義
    corners = [(0, 0), (0, size-1), (size-1, 0), (size-1, size-1)]
    
    def is_valid_move(b, col, row, c):
        """指定位置が有効な手かチェック"""
        if b[row][col] != 0:
            return False
        
        directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        
        for dr, dc in directions:
            r, c_pos = row + dr, col + dc
            if 0 <= r < size and 0 <= c_pos < size and b[r][c_pos] == opponent:
                r += dr
                c_pos += dc
                while 0 <= r < size and 0 <= c_pos < size and b[r][c_pos] == opponent:
                    r += dr
                    c_pos += dc
                if 0 <= r < size and 0 <= c_pos < size and b[r][c_pos] == c:
                    return True
        return False
    
    def count_flips(b, col, row, c):
        """指定位置で取れる石の数をカウント"""
        if b[row][col] != 0:
            return 0
        
        flips = 0
        directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        
        for dr, dc in directions:
            count = 0
            r, c_pos = row + dr, col + dc
            while 0 <= r < size and 0 <= c_pos < size and b[r][c_pos] == opponent:
                count += 1
                r += dr
                c_pos += dc
            if count > 0 and 0 <= r < size and 0 <= c_pos < size and b[r][c_pos] == c:
                flips += count
        
        return flips
    
    def is_corner(col, row):
        return (col, row) in corners
    
    def is_edge(col, row):
        return col == 0 or col == size-1 or row == 0 or row == size-1
    
    # BFSで有効な手を探索
    valid_moves = []
    
    for row in range(size):
        for col in range(size):
            if is_valid_move(board, col, row, color):
                flips = count_flips(board, col, row, color)
                valid_moves.append((col, row, flips))
    
    if not valid_moves:
        return None
    
    # コーナーを取る手を優先
    corner_moves = [m for m in valid_moves if is_corner(m[0], m[1])]
    if corner_moves:
        return max(corner_moves, key=lambda x: x[2])[:2]
    
    # 辺を取る手を優先
    edge_moves = [m for m in valid_moves if is_edge(m[0], m[1])]
    if edge_moves:
        return max(edge_moves, key=lambda x: x[2])[:2]
    
    # その他の手から最も石が取れる位置を選択
    best_move = max(valid_moves, key=lambda x: x[2])
    return (best_move[0], best_move[1])

# Generation ID: Hutch_1763363898192_thz8gnz7l (後半)
