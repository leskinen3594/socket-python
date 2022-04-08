wordlist = ['laying', 'sit_on_the_floor']

def find_activity(activities: list) -> int:
    count_laying = activities.count('laying')
    count_sit = activities.count('sit_on_the_floor')

    return count_laying, count_sit


import time
import random

q = list()
word_stack = list()
success = False

while True:
    msg = random.choice(['laying', 'sit_on_the_floor'])

    q.append(msg)

    if len(q) == 10:
        word_stack = q.copy()
        q.clear()

    print(f"q = {q}")
    print(f"stack = {word_stack} \n")

    laying, sit_on_the_floor = find_activity(word_stack)

    if laying >= 7 or sit_on_the_floor >= 7:
        print(f"\n laying = {laying}")
        print(f" sit on the floor = {sit_on_the_floor} \n")

        print("\n [Send!] \n")
        word_stack.clear()
        laying = 0
        sit_on_the_floor = 0
    else:
        if len(word_stack) == 10:
            print(f"\n laying = {laying}")
            print(f" sit on the floor = {sit_on_the_floor} \n")

            word_stack.clear()
            laying = 0
            sit_on_the_floor = 0

    time.sleep(1)