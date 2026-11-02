import csv
import math

def ft_count(values):
	n = 0
	for v in values:
		n += 1
	return n

def ft_mean(values):
	n = ft_count(values)
	if n == 0:
		return float("nan")
	total = 0
	for v in values:
		total += v
	return total / n

def ft_std(values):
	n = ft_count(values)
	if n == 0:
		return float("nan")
	mean = ft_mean(values)
	total = 0 
	#pour chaque v dans values:
	for v in values:
		total += (v - mean) **2
	return (total / (n - 1)) ** 0.5

def load_csv(path):
	rows = []
	with open(path, "r") as f:
		reader = csv.DictReader(f)
		for r in reader:
			clean = {}
			for column, value in r.items():
				if value == "":
					clean[column] = None
				else:
					try:
						x = float(value)
						if math.isnan(x) or math.isinf(x):
							clean[column] = value# "Nan", "inf" : on garde le texte
						else:
							clean[column] = x
					except ValueError:
						clean[column] = value
			rows.append(clean)
	#print(rows)
	return rows

def to_columns(rows):
	data = {}
	for row in rows:
		for column, value in row.items():
			if column not in data:
				data[column] = []
			if value is not None:
				data[column].append(value)
	return data

def group_by_house(rows):
	notes = {}
	for row in rows:
		house = row["Hogwarts House"]
		for column, value in row.items():
			if column == "Index" or not isinstance(value, float):
				continue
			if column not in notes:
				notes[column] = {}
			if house not in notes[column]:
				notes[column][house] = []
			notes[column][house].append(value)
	return notes

def pair_all(rows, a, b):
	xs = []
	ys = []
	for row in rows:
		x = row[a]
		y = row[b]
		if not isinstance(x, float) or not isinstance(y, float):
			continue
		xs.append(x)
		ys.append(y)
	return xs, ys

def ft_correlation(xs, ys):
	mx = ft_mean(xs)
	my = ft_mean(ys)
	num = 0
	sx = 0
	sy = 0
	for i in range(ft_count(xs)):
		num += (xs[i] - mx) * (ys[i] - my)
		sx += (xs[i] - mx) ** 2
		sy += (ys[i] - my) ** 2
	if sx == 0 or sy == 0:
		return float("nan")
	return num / (sx ** 0.5 * sy ** 0.5)

def pair_by_house(rows, a, b):
	points = {}
	for row in rows:
		x = row[a]
		y = row[b] #on lit les deux notes de l'élève.
		if not isinstance(x, float) or not isinstance(y, float):
			continue
		house = row["Hogwarts House"]
		if house not in points:
			points[house] = ([], [])
		points[house][0].append(x)
		points[house][1].append(y)
	return points
