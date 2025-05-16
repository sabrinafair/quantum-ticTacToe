from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler
# from qiskit_aer import AerSimulator

class Tiktactoe:
  def __init__(self):
    self.board = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    self.userToken = ''
    self.compToken = ''
    self.usersTurn = False

  def quantumNumberGenerator(self, circ, backend, sampler):
    transpiled_circuit = transpile(circ, backend=backend)

    job = sampler.run([transpiled_circuit])
    result = job.result()
    dist = result[0].data.c.get_counts().keys()
    binary = list(dist)[0]
    decimal = int(binary, 2)
    # counts = job.result().get_memory()
    # num = int(list(counts.keys())[0], 2)

    return decimal + 1

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
    self.userToken = input("would you like to be x's or o's? (enter x or o): ")
    self.compToken = 'o' if self.userToken == 'x' else 'x'
    self.usersTurn = (self.userToken == 'x')

  def main(self):
    """Main function to run the command-line program."""
    service = QiskitRuntimeService(channel="ibm_quantum", token="beea75a591e1c2a59371c780418fda3473317a37bc48a1f0b8197b5b0f999ffb68707fcf2c00dc052ef340b6d0cc32faff314cce420969aeeac8f0e3923480ac")
 
    # backend = service.least_busy(simulator=False, operational=True)
    backend = service.backend(name="ibm_brisbane")

    username = input("enter your username: ")
    self.reset_game()


    #define circuits for the quantum computer
    num_qubits = 3

    circ = QuantumCircuit(num_qubits, num_qubits)
    # added a Hadamard gate to all the qubits
    # this will create a superposition state
    circ.h(range(num_qubits))
    circ.measure(range(num_qubits), range(num_qubits))
    sampler = Sampler(mode=backend)

    # simulator = AerSimulator()

    # counts = quantumNumberGenerator(circ, simulator)

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
        #  location = self.quantumNumberGenerator(circ, simulator)
         location = self.quantumNumberGenerator(circ, backend, sampler)
         self.usersTurn = not self.usersTurn
         changed = self.updateLocation(location, token)
         while not changed:
          #  location = self.quantumNumberGenerator(circ, simulator)
           location = self.quantumNumberGenerator(circ, backend, sampler)
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
