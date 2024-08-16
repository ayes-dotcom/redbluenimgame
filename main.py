import argparse
class RedBlueNimGame:
    def __init__(self, num_red, num_blue, version, first_player='computer', depth=9):
        self.num_red = num_red
        self.num_blue = num_blue
        self.version = version
        self.current_player = first_player
        self.depth = depth

    def turn_over(self):
        while True:
            color, amount = None, None
            if self.current_player == "human":
                color, amount = self.human_move()
                while not self.validate_move(color, amount):
                    print("Invalid move, try again!")
                    color, amount = self.human_move()
            else:
                color, amount = self.computer_move()
                while not self.validate_move(color, amount):
                    print("Computer made an invalid move, try again!")
                    color, amount = self.computer_move()
            self.move(color, amount)
            print(f"Red marbles remaining: {self.num_red}")
            print(f"Blue marbles remaining: {self.num_blue}")
            if self.game_over():
                if self.version == "standard":
                    if self.num_red == 0:
                        print("human wins!")
                    else:
                        print("com wins!")
                    break
                if self.version == "misere":
                    if self.num_red == 0:
                        print("com wins!")
                    else:
                        print("human wins!")
                    break
            self.current_player = "human" if self.current_player == "computer" else "computer"

    def game_over(self):
        if self.version == "standard":
            if self.num_red == 0 or self.num_blue == 0:
                return True
            return False
        if self.version == "misere":
            if self.num_red > 0 or self.num_blue > 0:
                return False
            return True

    def move(self, color, amount):
        if color == "red":
            if amount == 3:
                self.num_red -= 3
            if amount == 2:
                self.num_red -= 2
            elif amount == 1:
                self.num_red -= 1
        elif color == "blue":
            if amount == 3:
                self.num_blue -= 3
            if amount == 2:
                self.num_blue -= 2
            elif amount == 1:
                self.num_blue -= 1

    def validate_move(self, color, amount):
        if color not in ['red', 'blue']:
            return False
        if amount not in [1, 2, 3]:
            return False
        if color == 'red' and self.num_red < amount:
            return False
        if color == 'blue' and self.num_blue < amount:
            return False
        return True

    def human_move(self):
        print("Human's turn")
        while True:
            try:
                color = input("Enter color (red/blue): ")
                amount = int(input("Enter amount (1/3): "))
                if color in ['red', 'blue'] and amount in [1, 2, 3]:
                    return color, amount
                else:
                    print("Invalid input. Please enter 'red' or 'blue' for color and 1, 2, or 3 for amount.")
            except ValueError:
                print("Invalid input. Please enter a number for amount.")

    def computer_move(self):
        print("Computer's turn")
        best_score = float('-inf')
        best_move = None
        for move in self.get_possible_moves():
            if self.version == "standard":
                score = self.maximize(self.depth - 1, float('-inf'), float('inf'), False)
            elif self.version == "misere":
                score = self.minimize(self.depth - 1, float('-inf'), float('inf'), False)
            if score is not None and score > best_score:
                best_score = score
                best_move = move
        if best_move is None:
            best_move = self.get_possible_moves()[0]  # default to first move if none found
        return best_move[0], best_move[1]

    def maximize(self, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.game_over():
            return self.calculate_score()
        if maximizing_player:
            best_score = -float('inf')
            for move in self.get_possible_moves():
                self.move(move[0], move[1])  # Simulate the move
                score = self.maximize(depth - 1, alpha, beta, False)
                self.undo_move(move[0], move[1])  # Undo the move
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            return best_score

    def minimize(self, depth, alpha, beta, minimizing_player):
        if depth == 0 or self.game_over():
            return self.calculate_score()
        if minimizing_player:
            least_score = float('inf')
            for move in self.get_possible_moves():
                self.move(move[0], move[1])  # Simulate the move
                score = self.minimize(depth - 1, alpha, beta, False)
                self.undo_move(move[0], move[1])  # Undo the move
                least_score = min(least_score, score)
                alpha = min(alpha, least_score)
                if beta >= alpha:
                    break
            return least_score

    def undo_move(self, color, amount):
        if color == "red":
            self.num_red += amount
        elif color == "blue":
            self.num_blue += amount

    def get_possible_moves(self):
        moves = []
        if self.num_red > 0:
            moves.append(("red", 1))
            if self.num_red > 1:
                moves.append(("red", 2))
            if self.num_red > 2:
                moves.append(("red", 3))
        if self.num_blue > 0:
            moves.append(("blue", 1))
            if self.num_blue > 1:
                moves.append(("blue", 2))
            if self.num_blue > 2:
                moves.append(("blue", 3))
        return moves

    def calculate_score(self):
        if self.version == 'standard':
            if self.num_red == 0:
                return 1  # Computer wins
            elif self.num_blue == 0:
                return -1  # Human wins
            else:
                return 0  # Game is not over yet
        elif self.version == 'misere':
            if self.num_red == 0:
                return -1  # Human wins
            elif self.num_blue == 0:
                return 1  # Computer wins
            else:
                return 0  # Game is not over yet


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Red-Blue Nim Game')
    parser.add_argument('--red', type=int, help='Initial number of red marbles', default=5)
    parser.add_argument('--blue', type=int, help='Initial number of blue marbles', default=5)
    parser.add_argument('--version', choices=['standard', 'misere'], help='Game version')
    parser.add_argument('--player', choices=['human', 'computer'], help='Starting player', default='computer')
    args = parser.parse_args()
    if not args.version:
        print("Please select a game version:")
        print("1. Standard")
        print("2. Misere")
        choice = input("Enter your choice (1/2): ")
        if choice == "1":
            args.version = "standard"
        elif choice == "2":
            args.version = "misere"
        else:
            print("Invalid choice. Defaulting to standard version.")
            args.version = "standard"
    print(f"Initial number of red marbles: {args.red}")
    print(f"Initial number of blue marbles: {args.blue}")
    game = RedBlueNimGame(args.red, args.blue, args.version, args.player)
    game.turn_over()

