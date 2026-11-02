from utils import load_csv, group_by_house, ft_correlation, pair_all
import sys
import os
import matplotlib.pyplot as plt

if len(sys.argv) != 2:
	print("Usage: python scatter_plot.py <dataset.csv>")
	sys.exit(1)
try:
	rows = load_csv(sys.argv[1])
	notes = group_by_house(rows)
except FileNotFoundError:
	print(f"File {sys.argv[1]} not found.")
	sys.exit(1)

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

def  plot_scatter(rows, a, b):
	points = pair_by_house(rows, a, b)
	for house, (xs, ys) in points.items():
		plt.scatter(xs, ys, alpha= 0.5, label=house)
	plt.xlabel(a)
	plt.ylabel(b)
	plt.title(f"Scatter plot of {a} vs {b}")
	plt.legend()
	plt.savefig(f"plots/scatter_{a}_vs_{b}.png")
	plt.clf() #Dessine dans une nouvelle table pour le prochain sujet

def compare_scatter(rows, notes):
	subjects = list(notes.keys())        # les 13 matières
	best_a = None
	best_b = None
	best_r = 0
	for i in range(len(subjects)):
			for j in range(i + 1, len(subjects)):
				a = subjects[i]
				b = subjects[j]
				xs, ys = pair_all(rows, a, b)        # les deux listes, toutes maisons confondues
				r = ft_correlation(xs, ys)
				if abs(r) > abs(best_r):
					best_r = r
					best_a = a
					best_b = b
	print(f"Most similar: {best_a} and {best_b} (r = {best_r:.4f})")
	plot_scatter(rows, best_a, best_b)

compare_scatter(rows, notes)

# subjects = list(notes.keys())
# results = []
# for i in range(len(subjects)):
# 		for j in range(i + 1, len(subjects)):
# 				a = subjects[i]
# 				b = subjects[j]
# 				xs, ys = pair_all(rows, a, b)
# 				r = ft_correlation(xs, ys)
# 				results.append((abs(r), a, b))
# results = sorted(results, reverse=True)
# print("Top 5 most correlated pairs:")
# for r, a, b in results[:5]:
# 		print(f"  {r:.3f}  {a} / {b}")
# best_r, best_a, best_b = results[0]
# print(f"Most similar: {best_a} and {best_b} (r = {best_r:.4f})")
# plot_scatter(rows, best_a, best_b)