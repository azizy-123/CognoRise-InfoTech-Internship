import os
import random

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

class Player:
    def __init__(self, name, symbol, is_ai=False):
        self.name = name
        self.symbol = symbol
        self.is_ai = is_ai

    def get_move(self, board):
        if self.is_ai:
            return self.get_ai_move(board)
        else:
            return self.get_human_move(board)

    def get_human_move(self, board):
        while True:
            try:
                move = int(input(f"{self.name}, enter your move (1-9): "))
                if 1 <= move <= 9 and board.is_valid_move(move):
                    return move
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Please enter a number between 1 and 9.")

    def get_ai_move(self, board):
        _, move = self.minimax(board, self.symbol, True)
        return move + 1  # Convert to 1-9 range

    def minimax(self, board, player, is_maximizing):
        if board.check_win(self.symbol):
            return 1, None
        if board.check_win('X' if self.symbol == 'O' else 'O'):
            return -1, None
        if board.is_full():
            return 0, None

        if is_maximizing:
            best_score = float('-inf')
            best_move = None
            for i in range(9):
                if board.board[i] == ' ':
                    board.board[i] = player
                    score, _ = self.minimax(board, 'O' if player == 'X' else 'X', False)
                    board.board[i] = ' '
                    if score > best_score:
                        best_score = score
                        best_move = i
            return best_score, best_move
        else:
            best_score = float('inf')
            best_move = None
            for i in range(9):
                if board.board[i] == ' ':
                    board.board[i] = player
                    score, _ = self.minimax(board, 'O' if player == 'X' else 'X', True)
                    board.board[i] = ' '
                    if score < best_score:
                        best_score = score
                        best_move = i
            return best_score, best_move

class Menu:
    def display_main_menu(self):
        print("\n=== Welcome to Tic Tac Toe ===")
        print("1. Play against AI")
        print("2. Play against another player")
        print("3. Exit Game")
        return input("Enter your choice (1, 2 or 3): ")

    def display_endgame_menu(self):
        print("\n=== Game Over! ===")
        print("1. Play Again")
        print("2. Exit Game")
        return input("Enter your choice (1 or 2): ")

class Board:
    def __init__(self):
        self.reset()

    def reset(self):
        self.board = [' ' for _ in range(9)]

    def display_board(self):
        print("\n")
        for i in range(0, 9, 3):
            print(" | ".join(self.board[i:i+3]))
            if i < 6:
                print("-" * 11)
        print("\n")

    def update_board(self, choice, symbol):
        if self.is_valid_move(choice):
            self.board[choice - 1] = symbol
            return True
        return False

    def is_valid_move(self, choice):
        return 1 <= choice <= 9 and self.board[choice - 1] == ' '

    def is_full(self):
        return ' ' not in self.board

    def check_win(self, symbol):
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]
        return any(all(self.board[i] == symbol for i in combo) for combo in win_combinations)

class Game:
    def __init__(self):
        self.board = Board()
        self.menu = Menu()

    def start_game(self):
        while True:
            choice = self.menu.display_main_menu()
            if choice == "1":
                self.play_game(ai_opponent=True)
            elif choice == "2":
                self.play_game(ai_opponent=False)
            elif choice == "3":
                self.quit_game()
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

    def play_game(self, ai_opponent):
        clear_screen()
        self.board.reset()  # Reset the board at the start of each game
        human_name = input("Enter your name: ")
        human_symbol = self.choose_symbol(human_name)
        ai_symbol = 'O' if human_symbol == 'X' else 'X'

        players = [
            Player(human_name, human_symbol),
            Player("AI", ai_symbol, is_ai=True) if ai_opponent else Player("Player 2", ai_symbol)
        ]

        current_player_index = 0 if human_symbol == 'X' else 1

        while True:
            self.play_turn(players[current_player_index])
            if self.check_game_over(players[current_player_index]):
                break
            current_player_index = 1 - current_player_index

        choice = self.menu.display_endgame_menu()
        if choice == "1":
            self.play_game(ai_opponent)
        else:
            self.quit_game()

    def play_turn(self, player):
        self.board.display_board()
        print(f"{player.name}'s turn ({player.symbol})")
        move = player.get_move(self.board)
        self.board.update_board(move, player.symbol)
        clear_screen()

    def check_game_over(self, player):
        if self.board.check_win(player.symbol):
            self.board.display_board()
            print(f"\nCongratulations! {player.name} ({player.symbol}) wins!")
            return True
        if self.board.is_full():
            self.board.display_board()
            print("\nIt's a draw!")
            return True
        return False

    def choose_symbol(self, name):
        while True:
            symbol = input(f"{name}, choose your symbol (X or O): ").upper()
            if symbol in ['X', 'O']:
                return symbol
            print("Invalid choice. Please enter X or O.")

    def quit_game(self):
        print("Thank you for playing Tic Tac Toe!")

if __name__ == "__main__":
    game = Game()
    game.start_game()