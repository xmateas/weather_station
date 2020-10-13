import csv
def random_data(x):
    m = ''
    with open(x, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for k in reader:
            k = str(k)
            m = m + k
    return m

data = random_data('temp_data.csv')
print(data)
print(len(data))