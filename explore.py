import csv
n = 0
missing_values = 0
# course = {'Index', 'Hogwarts House', 'First Name', 'Last Name', 'Birthday', 'Best Hand', 'Arithmancy', 'Astronomy', 'Herbology', 'Defense Against the Dark Arts', 'Divination', 'Muggle Studies', 'Ancient Runes', 'History of Magic', 'Transfiguration', 'Potions', 'Care of Magical Creatures', 'Charms', 'Flying'}
count = {}
houses = {}
with open("datasets/dataset_train.csv", "r") as f:
	reader = csv.DictReader(f)
	for row in reader:
		for column, value in row.items():
			if column not in count:
				count[column] = 0
			if column == "Hogwarts House":
				if value not in houses:
					houses[value] = 0
				houses[value] += 1
			if value == "":
				count[column] += 1
				missing_values += 1
		# print(row)
		# break
		n += 1
for column, nb in count.items():
    print(column, nb)
for house, nb in houses.items():
	print(house, nb)
print(n)
print(missing_values)

