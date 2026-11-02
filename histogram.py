import matplotlib.pyplot as plt
from utils import load_csv, to_columns, group_by_house
import sys
import os

os.makedirs("plots", exist_ok=True)

if len(sys.argv) != 2:
	print("Usage: python histogram.py <dataset.csv>")
	sys.exit(1)
rows = {}
data = {}
try:
	rows = load_csv(sys.argv[1])
	data = to_columns(rows)
	notes = group_by_house(rows)
except FileNotFoundError:
	print(f"File {sys.argv[1]} not found.")
	sys.exit(1)

def plot_histogram(notes):
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