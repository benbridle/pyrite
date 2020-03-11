from .CSVImporter import CSVImporter
import csv
from .Category import Category

class CategoryList:
    """
    A container to hold categories.
    """
    def __init__(self, categories):
        for category in categories:
            if not isinstance(category, Category):
                raise TypeError("Categories must be given an iterable containing Category instances")
        self.categories = categories


    @staticmethod
    def from_csv(csv_file_path):
        """
        Constructs a CategoryList from a csv file
        """
        categories = []
        with open(csv_file_path, "r") as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            reader.__next__()
            for line in reader:
                new_category = Category(line[0], line[1])
                categories.append(new_category)
        return CategoryList(categories)

    def __iter__(self):
        yield from self.categories

    def get_names(self):
        return [cat.name for cat in self.categories]

    def get_hint_from_category(self, category_name):
        for category in self.categories:
            if category.name == category_name:
                return(category.hint)