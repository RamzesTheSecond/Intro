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
        if self.handle:
            self.handle.close()

with FileWriter('text.txt') as f:
    f.write('Tomek')