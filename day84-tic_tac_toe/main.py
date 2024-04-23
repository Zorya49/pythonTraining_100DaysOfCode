import os

# Game board
board = [" "] * 9

# Player markers
PLAYER_1 = "X"
PLAYER_2 = "O"

# Game state
current_player = PLAYER_1
game_over = False
winner = None


def print_board():
    print(f" {board[0]} | {board[1]} | {board[2]} \n"
          f"-----------\n"
          f" {board[3]} | {board[4]} | {board[5]} \n"
          f"-----------\n"
          f" {board[6]} | {board[7]} | {board[8]} \n")


def start_game():
    global board, current_player, game_over, winner
    board = [" "] * 9
    current_player = PLAYER_1
    game_over = False
    winner = None
    os.system("cls")
    print("Tic Tac Toe game.")
    print("Positions on the board:")
    print(f" 1 | 2 | 3 \n"
          f"-----------\n"
          f" 4 | 5 | 6 \n"
          f"-----------\n"
          f" 7 | 8 | 9 \n")
    print("Let the game begin!")


def get_player_move(player):
    move = int(input(f"{player}'s turn. Enter a position (1-9): ")) - 1
    while move < 0 or move > 8 or board[move] != " ":
        move = int(input("Invalid move. Enter a position (1-9): ")) - 1
    return move


def check_winner(mark):
    # Check rows
    for i in [0, 3, 6]:
        if board[i] == board[i+1] == board[i+2] == mark:
            return True
    # Check columns
    for i in [0, 1, 2]:
        if board[i] == board[i+3] == board[i+6] == mark:
            return True
    # Check diagonals
    if board[0] == board[4] == board[8] == mark:
        return True
    if board[2] == board[4] == board[6] == mark:
        return True
    return False


def play_game():
    global current_player, game_over, winner
    start_game()
    while not game_over:
        print_board()

        position = get_player_move(current_player)
        board[position] = current_player

        if check_winner(current_player):
            game_over = True
            winner = current_player
        elif " " not in board:
            game_over = True

        if current_player == PLAYER_1:
            current_player = PLAYER_2
        else:
            current_player = PLAYER_1


def main():
    while True:
        play_game()
        print_board()

        if winner:
            print(f"{winner} wins!")
        else:
            print("It's a tie!")

        if input("\n\n\nDo you want to play again? Type 'y' or 'n': ") != "y":
            break


if __name__ == '__main__':
    main()
