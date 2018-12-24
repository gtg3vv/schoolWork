number = input("What should the answer be? ")
number = int(number)
if number == -1:
    import random
    number = random.randrange(0, 100)

numguess = input("How many guesses? ")
numguess = int(numguess)



for element in range(numguess):
    guess = input("Guess a number: ")
    guess = int(guess)
    if guess == number:
        print("You win!")
        break
    elif element == numguess - 1:
        print("You lose; the number is", str(number)+".")
        break
    elif element < numguess and guess > number:
        print('The number is lower than that.')
    elif element < numguess and guess < number:
        print('The number is higher than that.')
