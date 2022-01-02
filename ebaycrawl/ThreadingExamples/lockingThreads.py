import logging
import threading
import time
import concurrent.futures
from random import randint

someNumbers = []
testList = [1, 2, 3, 4, 5, 6]
workers = len(testList)


def making_numbers():
    counter = 1
    while counter < 6:
        with lock:
            print("Creating Price List")
            someNumbers.append(randint(10, 20))
            counter += 1


def main():
    global lock
    lock = threading.Lock()
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        for index in range(workers):
            executor.submit(making_numbers(), index)


main()

average = sum(someNumbers) / len(someNumbers)
print("\nNumber of entries: " + str(len(someNumbers)))
print(average)
