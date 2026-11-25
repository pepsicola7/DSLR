import argparse
import os

from utils import ft_count, load_csv, group_by_house, pair_by_house

parser = argparse.ArgumentParser(description="Compare all course pairs and save a scatter plot matrix to plots/pair_plot.png.")
parser.add_argument("dataset", help="Path to the labeled student CSV")
args = parser.parse_args()
try:
	rows = load_csv(args.dataset)
	notes = group_by_house(rows)
except FileNotFoundError:
	parser.error(f"File {args.dataset} not found.")

def pair_plot(rows, notes):
	import matplotlib.pyplot as plt

	subjects = list(notes.keys())
	n = ft_count(subjects)
	fig, axes = plt.subplots(n, n, figsize=(40,40))
	for i in range(n) :
		for j in range(n):
			ax = axes[i][j]
			if i == j:
				for house, values in notes[subjects[i]].items():
					ax.hist(values, bins=20, alpha=0.5)
			else:
				points = pair_by_house(rows, subjects[j], subjects[i])
				for house, (xs, ys) in points.items():
					ax.scatter(xs, ys, s=2, alpha=0.5)
			ax.set_xticks([])
			ax.set_yticks([])
			if i == 0:
				ax.set_title(subjects[j][:12], fontsize=8)
			if j == 0:
				ax.set_ylabel(subjects[i][:12], fontsize=8)
	os.makedirs("plots", exist_ok=True)
	plt.savefig("plots/pair_plot.png")

pair_plot(rows, notes)
