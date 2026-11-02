import sys
from utils import load_csv, to_columns, ft_count, ft_mean, ft_std 

def describe (data):
	#filter numeric columns
	numeric = {}
	for column, values in data.items():
		if ft_count(values) > 0 and isinstance(values[0], float):
			numeric[column] = values
	#calcul
	stats = {}
	for column, values in numeric.items():
		stats[column] = {
			"count": ft_count(values),
			"mean": ft_mean(values),
			"std": ft_std(values),
			"min": ft_min(values),
			"25%": ft_quantile(values, 0.25),
			"50%": ft_quantile(values, 0.5),
			"75%": ft_quantile(values, 0.75),
			"max": ft_max(values)
		}
	#print
	header = f"{'':<8}" # 8 espaces vides pour la colonne des noms de stats
	for column in stats:
		header += f"{column[:14]:>15}"# chaque nom cadré à droite sur 12
	print(header)

	lignes = ["count", "mean", "std", "min", "25%", "50%", "75%", "max"]
	for stat in lignes:
		ligne = f"{stat:<8}"
		for column in stats:
			ligne += f"{stats[column][stat]:>15.6f}"
		print(ligne)

def ft_min(values):
	if ft_count(values) == 0:
		return float("nan")
	smallest = float("inf")
	for v in values:
		if v < smallest:
			smallest = v
	return smallest

def ft_max(values):
	if ft_count(values) == 0:
		return float("nan")
	largest = float("-inf")
	for v in values:
		if v > largest:
			largest = v
	return largest

def ft_quantile(values, q):
	s = sorted(values)
	n = ft_count(values)
	if n == 0:
		return float("nan")
	position = (n - 1) * q
	i = int(position)
	f = position - i
	if f == 0:
		return s[i]
	return s[i] + f * (s[i + 1] - s[i])

data = {}
if len(sys.argv) != 2:
	print("Usage: python describe.py <dataset.csv>")
	sys.exit(1)

try:
	rows = load_csv(sys.argv[1])
except FileNotFoundError:
	print(f"File {sys.argv[1]} not found.")
	sys.exit(1)
data = to_columns(rows)
describe(data)

