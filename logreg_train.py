import sys, csv
from utils import load_csv, predict, FEATURES, ft_mean, ft_std, student_features

if len(sys.argv) != 2:
	print("Usage: python logreg_train.py <dataset.csv>")
	sys.exit(1)
try:
	rows = load_csv(sys.argv[1])
except FileNotFoundError:
	print(f"File {sys.argv[1]} not found.")
	sys.exit(1)

def prepare_data(rows):
	means = []
	stds = []
	for f in FEATURES:
		values = [row[f] for row in rows if row[f] is not None]
		means.append(ft_mean(values))
		stds.append(ft_std(values))
	X = []
	houses = []
	for row in rows:
		X.append(student_features(row, means, stds))
		houses.append(row["Hogwarts House"])
	return means, stds, X, houses

means, stds, X, houses = prepare_data(rows)

def train(X, y, alpha, iterations):
	m = len(X)
	n = len(X[0])
	w = []
	for j in range(n + 1):
		w.append(0)
	for it in range(iterations):
		grad = [0] *(n + 1) #initialise grad
		for i in range(m):
			p = predict(X[i], w) 
			error = p - y[i]
			grad[0] += error
			for j in range(n):
				grad[j + 1] += error *X[i][j]
		for k in range(n + 1):
			w[k] -= alpha * grad[k]/m
	return w

HOUSES = ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]
weights = {}
with open("weights.csv", "w", newline="") as f:
	writer = csv.writer(f)
	writer.writerow(["name"] + [f"w{k}" for k in range(len(FEATURES) + 1)])
	for house in HOUSES:
		y = [1 if h == house else 0 for h in houses]
		weights[house] = train(X, y, 0.5, 1000)
		writer.writerow([house] + weights[house])
	writer.writerow(["mean"] + means)
	writer.writerow(["std"] + stds)

bons = 0
for i in range(len(X)):
	best_house = None
	best_proba = -1
	for house in HOUSES:
		p = predict(X[i], weights[house])
		if p > best_proba:
			best_proba = p
			best_house = house
	if best_house == houses[i]:
		bons += 1
print(f"Accuracy: {bons / len(X):.4f}")




#trois choses a faire
#1.Parcourir les éléves
#2.calculer z
#3.recalculer w0
#L'idee est predict calcule une proba pour un seul élève
#x, la liste des 9 notes normalisées d'un élève, dans l'ordre de FEATURES
