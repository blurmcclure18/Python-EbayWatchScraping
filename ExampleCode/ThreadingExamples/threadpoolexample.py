import logging
import threading
import time
import concurrent.futures
from random import randint

# [rest of code]

someNumbers = {}
name_list = ["(303) elgin", "(291) elgin"]

new_list = []

for n in name_list:
    new_list.append(n.split("(")[1].split(")")[0])

print(new_list)


def making_numbers():
    counter = 1
    while counter < 6:
        print("Creating Price List")
        someNumbers[counter] = {f"price{counter}": randint(10, 20)}
        counter += 1


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(making_numbers(), range(3))

print("\nNumber of entries: " + str(len(someNumbers)))
