import argparse
from pathlib import Path
from utils import load_csv, to_columns, ft_count, ft_mean, ft_std 

def describe(data, row_count):
	#filter numeric columns
	numeric = {}
	for column, values in data.items():
		if ft_count(values) > 0 and isinstance(values[0], float):
			numeric[column] = values
	#calcul
	stats = {}
	for column, values in numeric.items():
		count = ft_count(values)
		minimum = ft_min(values)
		maximum = ft_max(values)
		first_quartile = ft_quantile(values, 0.25)
		third_quartile = ft_quantile(values, 0.75)
		stats[column] = {
				"count": count,
			"mean": ft_mean(values),
			"std": ft_std(values),
				"min": minimum,
				"25%": first_quartile,
			"50%": ft_quantile(values, 0.5),
				"75%": third_quartile,
				"max": maximum,
				"Missing %": 100 * (row_count - count) / row_count,
				"Range": maximum - minimum,
				"IQR": third_quartile - first_quartile,
		}
	return stats

SUMMARY_FIELDS = ("count", "mean", "std", "min", "25%", "50%", "75%", "max", "Missing %", "Range", "IQR")

def print_summary(stats):
	header = f"{'':<10}"
	for column in stats:
		header += f"{column[:14]:>15}"# chaque nom cadré à droite sur 12
	print(header)

	for stat in SUMMARY_FIELDS:
		ligne = f"{stat:<10}"
		for column in stats:
			ligne += f"{stats[column][stat]:>15.6f}"
		print(ligne)

def format_sheet_value(field, value):
	if field == "count":
		return f"{value:,}"
	if field == "Missing %":
		return f"{value:.2f}%"
	return f"{value:,.6f}".rstrip("0").rstrip(".")

def plot_summary(stats, dataset_name, row_count):
	import matplotlib.pyplot as plt

	headings = ["Numeric field"] + [field.title() for field in SUMMARY_FIELDS]
	sheet_rows = [
		[feature] + [format_sheet_value(field, values[field]) for field in SUMMARY_FIELDS]
		for feature, values in stats.items()
	]
	field_width = max(3.0, max(len(feature) for feature in stats) * 0.10 + 0.5)
	number_width = 1.25
	sheet_width = field_width + number_width * len(SUMMARY_FIELDS)
	height = 1.65 + 0.36 * (len(sheet_rows) + 1)
	fig = plt.figure(figsize=(sheet_width + 0.6, height), facecolor="#f1f5f9")
	left = 0.3 / fig.get_figwidth()
	fig.text(left, 1 - 0.28 / height, "Dataset summary", fontsize=22,
		fontweight="bold", color="#14283a", va="top")
	fig.text(left, 1 - 0.74 / height,
		f"{dataset_name}  ·  {row_count:,} rows  ·  {len(stats)} numeric columns",
		fontsize=11, color="#526678", va="top")

	axis = fig.add_axes([left, 0.55 / height, 1 - 2 * left, 1 - 1.65 / height])
	axis.set_axis_off()
	widths = [field_width / sheet_width] + [number_width / sheet_width] * len(SUMMARY_FIELDS)
	table = axis.table(cellText=sheet_rows, colLabels=headings, colWidths=widths,
		cellLoc="right", colLoc="right", bbox=[0, 0, 1, 1])
	table.auto_set_font_size(False)
	table.set_fontsize(10)
	for (row_index, column_index), cell in table.get_celld().items():
		cell.set_edgecolor("#dde6ee")
		cell.set_linewidth(0.5)
		cell.PAD = 0.06
		label = cell.get_text()
		if column_index == 0:
			label.set_ha("left")
		if row_index == 0:
			cell.set_facecolor("#16445a")
			label.set_color("white")
			label.set_fontweight("bold")
		else:
			cell.set_facecolor("#ffffff" if row_index % 2 else "#edf4f8")
			label.set_color("#14283a")
			if column_index == 0:
				label.set_fontweight("bold")

	fig.text(left, 0.22 / height,
		"Std = sample standard deviation   ·   50% = median   ·   IQR = 75% − 25%",
		fontsize=10, color="#526678")
	output_path = Path("plots") / "describe.png"
	output_path.parent.mkdir(exist_ok=True)
	fig.savefig(output_path, dpi=150)
	plt.close(fig)
	return output_path

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

parser = argparse.ArgumentParser(description="Summarize the numeric columns of a CSV.")
parser.add_argument("dataset", type=Path, help="Path to the input CSV")
parser.add_argument("--plot", action="store_true", help="Save a summary sheet to plots/describe.png")
args = parser.parse_args()

try:
	rows = load_csv(args.dataset)
except FileNotFoundError:
	parser.error(f"File {args.dataset} not found.")
row_count = ft_count(rows)
stats = describe(to_columns(rows), row_count)
if args.plot and not stats:
	parser.error("No numeric columns to plot.")
print_summary(stats)
if args.plot:
	output_path = plot_summary(stats, args.dataset.name, row_count)
	print(f"Summary sheet saved to {output_path}")

