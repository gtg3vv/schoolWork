x=int(input('Think of a number between 1 and 100 and I will try to guess it: '))

guesses=int(input('How many guesses do I get? '))

guessesleft=guesses

options=list(range(1,100))

computerguess= str(((len(options)+1)//2))

y=input('Is the number higheer or lower or the same as: '+ computerguess+'?')

for i in range(0,guessesleft):
    if y=="same" :
        print('You win!')
        break
    elif y=="higher" :
        guessesleft-=1
        if guessesleft==0:
            print('Sorry you lose. The number was: ',x)
        else:
           newrange=list(range(50,100))
           newguess=str((+len(newrange)-1)//2)
           computerguess=newguess
           y = input('Is the number higheer or lower or the same as: ' + computerguess + '?')
    elif y=="lower":
        guessesleft -= 1
        if guessesleft == 0:
            print('Sorry you lose. The number was: ', x)
        else:
            max=int(computerguess)
            min=0
            newrange = list(range((min), max))
            newguess = str((len(newrange) + 1) // 2)
            computerguess = newguess
            y = input('Is the number higheer or lower or the same as: ' + computerguess + '?')
            if y=='higher':
                options = list(range(1, 25))
                newguess = str((len(newrange) + 1) // 2)
                computerguess = newguess
                y = input('Is the number higheer or lower or the same as: ' + computerguess + '?')