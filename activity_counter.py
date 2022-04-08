def find_activity(activities: list):
    wordlist = ['laying', 'sit_on_the_floor']
    n = 0

    for act in activities:
        if act in wordlist:
            n += 1
            print(n)
            if n >= 7:
                print("\n [Send!] \n")
                return True


import time
import random

q = list()
word_stack = list()
success = False

while True:
    msg = random.choice(['laying', 'a', 'b', 'c'])

    q.append(msg)

    if len(q) == 10:
        word_stack = q.copy()
        success = find_activity(word_stack)
        q.clear()

    print("q = ", q)
    print("stack = ", word_stack)
    
    if success:
        word_stack.clear()
        print("stack clear = ", word_stack)
    else:
        if len(word_stack) == 10:
            word_stack.clear()
            print("stack clear = ", word_stack)

    time.sleep(1)