from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

class Tiktactoe:
  def __init__(self):
    self.board = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    self.userToken = ''
    self.compToken = ''
    self.usersTurn = False

  def quantumNumberGenerator(self, circ, simulator):
    result = simulator.run(circ, shots=1).result()
    counts = result.get_counts()
    num = int(list(counts.keys())[0], 2)
    return num + 1

  def updateLocation(self, value, token):
    changed = False
    for i in range(len(self.board)):
        for j in range(len(self.board[i])):
            if self.board[i][j] == value:
                self.board[i][j] = token
                changed = True
    # print_board(arr)
    return changed

  def checkTie(self):
    hasAvailable = 'tie'
    for i in range(len(self.board)):
        for j in range(len(self.board[i])):
            if self.board[i][j] != 'x' and self.board[i][j] != 'o':
                hasAvailable = 'open'
    # print_board(arr)
    return hasAvailable

  # Example usage:
  def print_board(self):
    for row in self.board:
        print(row)

  def checkWinner(self):
    if self.board[0][0] == self.board[1][1] == self.board[2][2]:
      return self.board[0][0]
    if self.board[0][2] == self.board[1][1] == self.board[2][0]:
      return self.board[0][2]
    # Check rows and columns
    for i in range(3):
      if self.board[i][0] == self.board[i][1] == self.board[i][2]:
        return self.board[i][0]
      if self.board[0][i] == self.board[1][i] == self.board[2][i]:
        return self.board[0][i]

    return 'none'

  def reset_game(self):
    self.board = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    self.userToken = input("would you like to be x's or O's? (enter x or O): ")
    self.compToken = 'o' if self.userToken == 'x' else 'x'
    self.usersTurn = (self.userToken == 'x')

  def main(self):
    """Main function to run the command-line program."""

    username = input("enter your username: ")
    self.reset_game()


    #define circuits for the quantum computer
    num_qubits = 3

    circ = QuantumCircuit(num_qubits, num_qubits)
    circ.h(range(num_qubits))
    circ.measure(range(num_qubits), range(num_qubits))

    simulator = AerSimulator()

    # counts = quantumNumberGenerator(circ, simulator)
    # print(counts)

    self.print_board()
    playGame = True
    while playGame:
      token = self.userToken if self.usersTurn else self.compToken
      if self.usersTurn:
        print("TURN OF: " + username)
        location = int(input("enter the number where you would like to place your token: "))
        changed = self.updateLocation(location, token)
        while not changed:
           location = int(input("Sorry, location already taken. Please enter the available number where you would like to place your token: "))
           changed = self.updateLocation(location, token)
        self.usersTurn = not self.usersTurn
      else:
         print("TURN OF: QUANTUM COMPUTER")
         location = self.quantumNumberGenerator(circ, simulator)
         self.usersTurn = not self.usersTurn
         changed = self.updateLocation(location, token)
         while not changed:
           location = self.quantumNumberGenerator(circ, simulator)
           changed = self.updateLocation(location, token)
      self.print_board()
      winner = self.checkTie()
      winner = winner if winner == 'tie' else self.checkWinner()
      if winner == 'tie':
        print("This Game is a TIE!")
        userInput = input("Would you like to play again? (y/n): ")
        if userInput == 'y':
          self.reset_game()
        else:
          playGame = False
          break
      elif winner != 'none':
         winner = username if winner == self.userToken else 'Quantum Computer'
         print(winner + " is the winner!!!")
         userInput = input("Would you like to play again? (y/n): ")
         if userInput == 'y':
            self.reset_game()
         else:
          playGame = False
          break

        
    print("Thanks for Playing!")


if __name__ == "__main__":
  TicTacToeGame = Tiktactoe()
  TicTacToeGame.main()
