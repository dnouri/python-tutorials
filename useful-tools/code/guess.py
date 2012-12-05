import random
import time

def main():
    number = random.randint(1, 100)
    guess = None
    count = 0
    start_time = time.time()

    while guess != number:
        guess = int(
            raw_input('Guess a number between 1 and 100: '))
        count += 1

        if guess == number:
            print 'You guessed it!'
        elif guess < number:
            print 'Too small'
        else:
            print 'Too big'

    print 'It took you %s guesses and %.2f seconds.' % (
        count, time.time() - start_time)

main()
