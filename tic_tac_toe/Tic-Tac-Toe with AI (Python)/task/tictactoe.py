def main():


    initial_state = 9 * "_"
    board = generate_board(initial_state)
    print_board(board)

    game_state = GameState.GAME_NOT_FINISHED
    while game_state == GameState.GAME_NOT_FINISHED:
        player = player_in_turn(board)
        x, y = get_move(board) if player == 'X' else get_random_move(board)
        board[x][y] = player
        print_board(board)
        game_state = update_game_state(board, player)
    print_game_state(game_state)


main()
