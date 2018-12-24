print('You will never win the game, Camelot is my name.')
answer = input("Guess my name: ")
while answer != 'Camelot':
    print("Ha! you'll never guess")
    answer = input("Guess my name: ")

print('No! How did you guess', answer, 'Congrats')