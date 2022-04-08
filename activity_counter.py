wordlist = ['laying', 'sit_on_the_floor']

def find_activity(activities: list) -> int:
    count_laying = activities.count('laying')
    count_sit = activities.count('sit_on_the_floor')

    return count_laying, count_sit


import time
import random

message_stack = list()
activity_list = list()

while True:
    msg = random.choice(['laying', 'sit_on_the_floor', 'a', 'b', 'c'])

    message_stack.append(msg)

    if len(message_stack) == 10:
        activity_list = message_stack.copy()
        message_stack.clear()

    print(f"message_stack = {message_stack}")
    print(f"stack = {activity_list} \n")

    laying, sit_on_the_floor = find_activity(activity_list)

    if laying >= 7 or sit_on_the_floor >= 7:
        print(f"\n laying = {laying}")
        print(f" sit on the floor = {sit_on_the_floor} \n")

        print("\n [Send!] \n")
        activity_list.clear()
        laying = 0
        sit_on_the_floor = 0
    else:
        if len(activity_list) == 10:
            print(f"\n laying = {laying}")
            print(f" sit on the floor = {sit_on_the_floor} \n")

            activity_list.clear()
            laying = 0
            sit_on_the_floor = 0

    time.sleep(1)