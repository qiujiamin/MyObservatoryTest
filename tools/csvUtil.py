import csv, random, os

class CSVUtil:
    """CSV util"""

    def __init__(self):
        self.writedataPath = r"data/result.csv"

    def readcsv(self, csv_path, colname):
        with open(csv_path, 'r', encoding='UTF-8') as csvfile:
            reader = csv.DictReader(csvfile)
            column = [row[colname] for row in reader]
            b = []
            for i in column:
                b.append("".join(i))
                c = random.choice(b)
            return c

    def writeCsv(self, csv_path, *row):
        if csv_path:
            if row:
                with open(csv_path, mode="a", encoding="utf-8") as f:
                    csv_writer = csv.writer(f, lineterminator='\n')
                    csv_writer.writerow(row)
            else:
                print("error")
        f.close()

if __name__ == '__main__':
    # cs = CSVUtil()
    # cs.writeCsv("../data/result.csv","11","ddd")
    pass

