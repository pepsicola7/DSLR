import argparse
import os

from utils import load_csv, to_columns, group_by_house

parser = argparse.ArgumentParser(description="Compare course score distributions by house. Saves one plots/hist_<course>.png per course.")
parser.add_argument("dataset", help="Path to the labeled student CSV")
args = parser.parse_args()
rows = {}
data = {}
try:
	rows = load_csv(args.dataset)
	data = to_columns(rows)
	notes = group_by_house(rows)
except FileNotFoundError:
	parser.error(f"File {args.dataset} not found.")

def plot_histogram(notes):
	import matplotlib.pyplot as plt

	os.makedirs("plots", exist_ok=True)
	for sujet in notes:
		for house, values in notes[sujet].items():
			plt.hist(values, bins=10, edgecolor='black', label=house, alpha=0.5)
		plt.title(f"Histogram of {sujet}")
		plt.xlabel("Score")
		plt.ylabel("Students")
		plt.legend()
		plt.savefig(f"plots/hist_{sujet}.png")
		plt.clf() #Dessine dans une bouvelle table pour le prochain sujet


plot_histogram(notes)
