import logging
import threading
import time
import concurrent.futures
from random import randint
import pprint
from typing import Counter

watchCounter = 0
watchResults = {}
watchList = ["291 elgin", "303 elgin"]
workers = len(watchList)

testCounter = 0


def making_numbers(grade):
    global testCounter
    print(grade)
    with lock:
        print("\nAdding to Watch Results")
        watchResults[testCounter] = {"grade": grade, "results": randint(50, 200)}
        testCounter += 1
    return


def main(grade_list):
    global lock
    lock = threading.Lock()

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        for index in range(workers):
            executor.submit(making_numbers(grade_list[index]), index)
        return


main(watchList)

print("\nPrinting Watch Dictionary: ")
print(watchResults)

print("\nPrinting Results")
print(watchResults[0]["grade"])

print("\nStarting Loop: ")
printCounter = 0
while printCounter < len(watchResults):
    print(f"Grade : {watchResults[printCounter]['grade']}")
    print(f"Results {watchResults[printCounter]['results']}")
    printCounter += 1
