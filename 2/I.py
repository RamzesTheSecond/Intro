#1
class Logger:
    def __enter__(self):
        print('Start sekcji logowania')

    def __exit__(self, *args):
        print('Koniec sekcji logowania')

with Logger() as logger:
    print('Środek')

#2
class FileWriter:
    def __init__(self, path):
        self.path = path
        self.handle = None

    def __enter__(self):
        self.handle = open(self.path, 'w')
        return self.handle

    def __exit__(self, exc_type, exc_value, traceback):
        self.handle.close()
        return True

with FileWriter('text.txt') as f:
    f.write('Tomek')
    raise ValueError("Błąd")

#3
class FileWriter2:
    def __init__(self, path):
        self.path = path
        self.handle = None

    def __enter__(self):
        self.handle = open(self.path, 'w')
        return self.handle

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            print(f"Błąd podczas zapisu: {exc_value}")
        self.handle.close()
        return False

with FileWriter2('text.txt') as f:
    f.write('Tomek')
    # raise ValueError("Błąd")

#4
class SafeDivision:
    def __enter__(self):
        return self
    def divide(self, a, b):
        return a/b
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is ZeroDivisionError:
            print("Niemożna dzielić przez zero")
            return True
        return False

with SafeDivision() as sd:
    sd.divide(5, 0)