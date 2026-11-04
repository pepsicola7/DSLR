import csv,sys
from utils import load_csv, predict, student_features

if len(sys.argv) != 3:
	print("Usage: python logreg_predict.py <dataset.csv> <weights.csv>")
	sys.exit(1)
try:
	rows = load_csv(sys.argv[1])
except FileNotFoundError:
	print(f"File {sys.argv[1]} not found.")
	sys.exit(1)

weights = {}
means = []
stds = []
with open(sys.argv[2]) as f:
	reader = csv.reader(f)
	next(reader)
	for line in reader:
		name = line[0]# "Gryffindor", "mean", "std"...
		values = [float(v) for v in line[1:]]
		if name == "mean":
			means = values
		elif name == "std":
			stds = values
		else:
			weights[name] = values

HOUSES = ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]
with open("houses.csv", "w", newline="") as f:
	writer = csv.writer(f)
	writer.writerow(["Index", "Hogwarts House"])
	for i in range(len(rows)):
		x = student_features(rows[i], means, stds)
		best_house = None
		best_proba = -1
		for house in HOUSES:
			p = predict(x, weights[house])
			if p > best_proba:
				best_proba = p
				best_house = house
		writer.writerow([int(rows[i]["Index"]), best_house])
