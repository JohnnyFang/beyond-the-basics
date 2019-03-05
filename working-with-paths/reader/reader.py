class Reader:
    def __init__(self, filename):
        self.filename = filename

    def read(self):
        with open(self.filename) as file:
            data = file.read()
            return data
