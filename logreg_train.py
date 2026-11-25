import argparse
import csv
import random

from utils import load_csv, predict, FEATURES, ft_mean, ft_std, student_features

parser = argparse.ArgumentParser(description="Train the Hogwarts house classifier and write weights.csv.")
parser.add_argument("dataset", help="Path to the labeled training CSV")
parser.add_argument("--sgd", action="store_true", help="Use stochastic gradient descent. Cannot be combined with --mini-batch.")
parser.add_argument("--mini-batch", action="store_true", help="Use mini-batch gradient descent. Cannot be combined with --sgd.")
parser.add_argument("--batch-size", type=int, help="Students per mini-batch (default: 32)")
args = parser.parse_args()
if args.sgd and args.mini_batch:
	parser.error("Cannot combine --sgd and --mini-batch. Choose one optimizer flag, or omit both to use full-batch gradient descent.")
if args.batch_size is not None:
	if not args.mini_batch:
		parser.error("--batch-size requires --mini-batch.")
	if args.batch_size < 1:
		parser.error("--batch-size must be a positive integer.")
batch_size = 32 if args.batch_size is None else args.batch_size
try:
	rows = load_csv(args.dataset)
except FileNotFoundError:
	parser.error(f"File {args.dataset} not found.")

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

def train_sgd(training_features, house_labels, initial_learning_rate, epochs, seed):
	weights = [0.0] * (len(training_features[0]) + 1)
	student_indices = list(range(len(training_features)))
	random_generator = random.Random(seed)
	for epoch in range(epochs):
		random_generator.shuffle(student_indices)
		# Take smaller steps as training progresses.
		learning_rate = initial_learning_rate / (1 + epoch / 10)
		for student_index in student_indices:
			student_scores = training_features[student_index]
			prediction_error = predict(student_scores, weights) - house_labels[student_index]
			scaled_error = learning_rate * prediction_error
			weights[0] -= scaled_error
			for weight_index, score in enumerate(student_scores, start=1):
				weights[weight_index] -= scaled_error * score
	return weights

def train_mini_batch(training_features, house_labels, initial_learning_rate, epochs, batch_size, seed):
	weights = [0.0] * (len(training_features[0]) + 1)
	student_indices = list(range(len(training_features)))
	random_generator = random.Random(seed)
	for epoch in range(epochs):
		random_generator.shuffle(student_indices)
		learning_rate = initial_learning_rate / (1 + epoch / 10)
		for batch_start in range(0, len(student_indices), batch_size):
			batch = student_indices[batch_start:batch_start + batch_size]
			gradient = [0.0] * len(weights)
			for student_index in batch:
				student_scores = training_features[student_index]
				prediction_error = predict(student_scores, weights) - house_labels[student_index]
				gradient[0] += prediction_error
				for weight_index, score in enumerate(student_scores, start=1):
					gradient[weight_index] += prediction_error * score
			# Average over the actual batch, including a shorter final batch.
			for weight_index, gradient_sum in enumerate(gradient):
				weights[weight_index] -= learning_rate * gradient_sum / len(batch)
	return weights

HOUSES = ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]
weights = {}
with open("weights.csv", "w", newline="") as f:
	writer = csv.writer(f)
	writer.writerow(["name"] + [f"w{k}" for k in range(len(FEATURES) + 1)])
	for house in HOUSES:
		y = [1 if h == house else 0 for h in houses]
		if args.sgd:
			weights[house] = train_sgd(X, y, initial_learning_rate=0.02, epochs=100, seed=42)
		elif args.mini_batch:
			weights[house] = train_mini_batch(X, y, initial_learning_rate=0.2,
				epochs=100, batch_size=batch_size, seed=42)
		else:
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
