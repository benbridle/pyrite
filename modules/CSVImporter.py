import csv


class CSVImporter:
    def __init__(self, file_path, ignore_header=True):
        self.ignore_header = ignore_header
        self.file_path = file_path
        self.importFromFile(file_path)

    def importFromFile(self, file_path):
        self.contents = []
        with open(file_path, "r") as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            if self.ignore_header:
                reader.__next__()
            for line in reader:
                self.contents.append(line)

    def getContents(self):
        return(self.contents)
