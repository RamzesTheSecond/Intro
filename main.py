import requests
import time
from datetime import datetime
from functools import wraps

# 1
class NotFoundError(Exception):
    def __init__(self, message="Resource not found!"):
        self.message = message
        super().__init__(f"{message}.")

class AccessDeniedError(Exception):
    def __init__(self, message="Access denied!"):
        self.message = message
        super().__init__(f"{message}.")

def saveFile(source, filename="latest.txt"):
    response = requests.get(source)
    if response.status_code == 404:
        raise NotFoundError()
    if response.status_code == 403:
        raise AccessDeniedError()
    data = response.text
    with open(filename, "w") as file:
        file.write(data)

saveFile('https://oleksandr-fedoruk.com/wp-content/uploads/2025/10/sample.csv')

#2 #3

def logujCzas(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        startTime = datetime.now()
        print(f"[START] {startTime.strftime('%Y-%m-%d %H:%M:%S')}")
        wynik = func(*args, **kwargs)
        endTime = datetime.now()
        print(f"[END]   {endTime.strftime('%Y-%m-%d %H:%M:%S')}")
        return wynik
    return wrapper

class AnalyseFile:
    def __init__(self, filepath):
        self.filepath = filepath
    def readLines(self):
        with open(self.filepath, 'r', encoding='utf-8') as file:
            for line in file:
                yield line.rstrip('\n')
    @logujCzas
    def do(self):
        sumString = ''
        indexesString = ''
        for line in self.readLines():
            index, *numbers = line.strip().split(',')
            suma = sum([float(x) for x in numbers if x != '-'])
            indexes = [ind for ind, x in enumerate(numbers) if x == '-']
            avg = suma / (len(numbers) - len(indexes))
            sumString = sumString + index +';'+ str(suma) +';' + str(avg) + '\n'
            indexesString = indexesString + index + ';' + ','.join(str(x) for x in indexes) + '\n'
            with open("values.csv", "w") as textFile:
                textFile.write(sumString)
            with open("missing_values.csv", "w") as textFile:
                textFile.write(indexesString)

AnalyseFile("latest.txt").do()