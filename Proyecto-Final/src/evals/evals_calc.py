import chess

# Define standard material values
MATERIAL_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0
}

# Center squares for evaluation (central control is important)
CENTER_SQUARES = [chess.D4, chess.E4, chess.D5, chess.E5]

# Pawn Structure Considerations (pawn on 4th or 5th ranks are better)
PAWN_STRUCTURE_SCORES = {
    1: -0.5,  # Pawn on the 1st rank
    2: 0,     # Pawn on the 2nd rank
    3: 0.5,   # Pawn on the 3rd rank
    4: 1,     # Pawn on the 4th rank
    5: 1,     # Pawn on the 5th rank
    6: 0.5,   # Pawn on the 6th rank
    7: 0,     # Pawn on the 7th rank
    8: -0.5   # Pawn on the 8th rank
}

# Evaluate material: sum of piece values
def evaluate_material(board):
    white_material = 0
    black_material = 0

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            if piece.color == chess.WHITE:
                white_material += MATERIAL_VALUES.get(piece.piece_type, 0)
            else:
                black_material += MATERIAL_VALUES.get(piece.piece_type, 0)
    
    return white_material, black_material

# Evaluate piece activity: pieces closer to the center and developed pieces are better
def evaluate_piece_activity(board):
    white_activity = 0
    black_activity = 0

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is None:
            continue

        # Piece activity: prioritize central and developed squares
        if piece.color == chess.WHITE:
            if square in CENTER_SQUARES:
                white_activity += 1
            elif piece.piece_type in [chess.KNIGHT, chess.BISHOP] and square in [chess.C3, chess.F3, chess.C4, chess.F4]:
                white_activity += 0.5
        elif piece.color == chess.BLACK:
            if square in CENTER_SQUARES:
                black_activity += 1
            elif piece.piece_type in [chess.KNIGHT, chess.BISHOP] and square in [chess.C6, chess.F6, chess.C5, chess.F5]:
                black_activity += 0.5
    
    return white_activity, black_activity

# Evaluate pawn structure: Strong pawns are on the 4th/5th rank, weak pawns are on the 7th/8th rank
def evaluate_pawn_structure(board):
    white_pawn_score = 0
    black_pawn_score = 0

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is None or piece.piece_type != chess.PAWN:
            continue

        # Evaluate pawns based on their rank
        if piece.color == chess.WHITE:
            white_pawn_score += PAWN_STRUCTURE_SCORES.get(chess.square_rank(square), 0)
        elif piece.color == chess.BLACK:
            black_pawn_score += PAWN_STRUCTURE_SCORES.get(chess.square_rank(square), 0)
    
    return white_pawn_score, black_pawn_score

# Evaluate king safety: Castled kings are safer than non-castled
def evaluate_king_safety(board):
    white_king_safety = 0
    black_king_safety = 0

    if board.king(chess.WHITE) is not None:
        white_king_square = board.king(chess.WHITE)
        # If the white king is in a safe position (castled or tucked away)
        if chess.square_file(white_king_square) in [chess.C1, chess.G1] and chess.square_rank(white_king_square) == 1:
            white_king_safety += 1  # Castled kings are safer

    if board.king(chess.BLACK) is not None:
        black_king_square = board.king(chess.BLACK)
        # If the black king is in a safe position (castled or tucked away)
        if chess.square_file(black_king_square) in [chess.C8, chess.G8] and chess.square_rank(black_king_square) == 8:
            black_king_safety += 1  # Castled kings are safer

    return white_king_safety, black_king_safety

# Evaluate position: combines all the positional factors
def evaluate_position(board):
    white_activity, black_activity = evaluate_piece_activity(board)
    white_pawn_score, black_pawn_score = evaluate_pawn_structure(board)
    white_king_safety, black_king_safety = evaluate_king_safety(board)

    # Combine all the positional evaluations
    white_position = white_activity + white_pawn_score + white_king_safety
    black_position = black_activity + black_pawn_score + black_king_safety
    
    return white_position, black_position

# Main function to evaluate the performance based on both material and position
def evaluate_performance(game):
    # Get the final FEN from the game
    fen = game.end().board().fen()  # Use `game.board()` at the end of the game
    
    # Create a board object from the FEN string
    board = chess.Board(fen)
    
    # Evaluate the material and position
    white_material, black_material = evaluate_material(board)
    white_position, black_position = evaluate_position(board)
    
    # Combine material and positional evaluations
    white_score = white_material + white_position
    black_score = black_material + black_position
    
    # Normalize scores to get a percentage
    total_score = white_score + black_score
    if total_score == 0:
        return 50.0, 50.0  # In case of a draw, both players have equal performance
    
    white_performance = (white_score / total_score) * 100
    black_performance = (black_score / total_score) * 100
    
    return white_performance, black_performance