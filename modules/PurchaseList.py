import csv
from datetime import datetime
from . import datetime_tools


class PurchaseList:
    TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"

    def __init__(self, purchases):
        self.purchases = purchases

    @classmethod
    def from_csv(cls, purchases_file_path):
        """
        Constructs a PurchaseList from a csv file
        """
        purchases = []
        with open(purchases_file_path, "r") as csv_file:
            reader = csv.reader(csv_file, delimiter=",")
            reader.__next__()
            for line in reader:
                time_created = datetime.strptime(line[0], PurchaseList.TIMESTAMP_FORMAT)
                category = line[1]
                cost = line[2]
                new_purchase = Purchase(category, cost, time_created)
                purchases.append(new_purchase)
        purchase_list = PurchaseList(purchases)
        purchase_list.purchases_file_path = purchases_file_path
        return purchase_list

    def to_csv(self, purchases_file_path):
        output_spreadsheet = ["Timestamp,Category,Cost"]
        for purchase in self.purchases:
            line = ",".join(
                [
                    purchase.time_created.strftime(PurchaseList.TIMESTAMP_FORMAT),
                    purchase.category_name,
                    str(float(purchase.cost)),
                ]
            )
            output_spreadsheet.append(line)
        with open(purchases_file_path, "w") as purchases_file:
            for line in output_spreadsheet:
                purchases_file.write(line + "\n")

    def save(self):
        try:
            self.to_csv(self.purchases_file_path)
        except AttributeError:
            raise AttributeError("Can only be used on a PurchaseList loaded from a file")

    def get_purchases_within_time_period(self, start_time, end_time):
        selected_purchases = []
        for purchase in self.purchases:
            if start_time <= purchase.time_created <= end_time:
                selected_purchases.append(purchase)
        return PurchaseList(selected_purchases)

    def group_purchases_by_category(self):
        category_totals = {}
        for purchase in self.purchases:
            category_name = purchase.category_name
            cost = purchase.cost
            if category_name in category_totals:
                category_totals[category_name] += cost
            else:
                category_totals[category_name] = cost
        purchase_groups = [Purchase(category_name, cost) for category_name, cost in category_totals.items()]
        return purchase_groups

    def add_purchase(self, *args, **kwargs):
        self.purchases.append(Purchase(*args, **kwargs))


class Purchase:
    def __init__(self, category_name: str, cost, time_created=None):
        if time_created is None:
            time_created = datetime_tools.now()
        if not isinstance(time_created, datetime):
            raise ValueError("time_created must be a datetime object")
        self.time_created = time_created
        self.category_name = category_name
        self.cost = Price(cost)


class Price:
    def __init__(self, value):
        self._value = float(value)

    def __str__(self):
        return "$" + "{0:.2f}".format(self._value)

    def __float__(self):
        return float(self._value)

    def __add__(self, other):
        return Price(float(self) + float(other))

    def formatted(self):
        return self.__str__()

    @property
    def value(self):
        return self._value

    @value.setter
    def _set_value(self, new_value):
        self._value = float(new_value)
