class Logger:
    def __enter__(self):
        print('Start sekcji logowania')

    def __exit__(self, *args):
        print('Koniec sekcji logowania')


with Logger() as logger:
    print('Środek')
