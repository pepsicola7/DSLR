from collections import deque

import matplotlib.pyplot as plt


HOUSE_COLORS = {
	"Gryffindor": "#f36b70",
	"Hufflepuff": "#f3c456",
	"Ravenclaw": "#78aaff",
	"Slytherin": "#58d4a4",
}
BACKGROUND = "#101826"
FOREGROUND = "#eef3fb"
MUTED = "#a8b7cc"


class PredictionView:
	def __init__(self, houses, total):
		self.total = total
		self.processed = 0
		self.counts = dict.fromkeys(houses, 0)
		self.recent = deque(maxlen=6)
		# Keep the display responsive without redrawing after every student on large inputs.
		self.refresh_every = max(1, (total + 99) // 100)
		self.figure = plt.figure(figsize=(10.5, 5.5), facecolor=BACKGROUND)
		if self.figure.canvas.required_interactive_framework is None:
			plt.close(self.figure)
			raise RuntimeError("--visualize requires a desktop session and an interactive Matplotlib backend.")
		self.figure.canvas.manager.set_window_title("Hogwarts house predictions")
		self.figure.text(0.06, 0.88, "Hogwarts house predictions", color=FOREGROUND,
			fontsize=24, fontweight="bold")
		self.status = self.figure.text(0.06, 0.81, "", color=MUTED, fontsize=11)
		progress_axis = self.figure.add_axes([0.06, 0.735, 0.88, 0.04])
		progress_axis.set(xlim=(0, 1), ylim=(0, 1))
		progress_axis.set_axis_off()
		progress_axis.barh(0.5, 1, height=0.55, color="#2a374b")
		self.progress = progress_axis.barh(0.5, 0, height=0.55, color="#72dcc7")[0]

		self.figure.text(0.06, 0.65, "Predicted houses", color=FOREGROUND,
			fontsize=13, fontweight="bold")
		self.house_axis = self.figure.add_axes([0.18, 0.17, 0.35, 0.44], facecolor=BACKGROUND)
		self.bars = self.house_axis.barh(houses, [0] * len(houses),
			color=[HOUSE_COLORS[house] for house in houses], height=0.54)
		self.house_axis.invert_yaxis()
		self.house_axis.set_xticks([])
		self.house_axis.tick_params(axis="y", length=0, pad=10, colors=FOREGROUND)
		for spine in self.house_axis.spines.values():
			spine.set_visible(False)
		self.count_labels = [self.house_axis.annotate("0", (0, bar.get_y() + bar.get_height() / 2),
			xytext=(7, 0), textcoords="offset points", va="center", color=FOREGROUND)
			for bar in self.bars]

		self.figure.text(0.64, 0.65, "Recent predictions", color=FOREGROUND,
			fontsize=13, fontweight="bold")
		self.recent_labels = [self.figure.text(0.64, 0.57 - position * 0.066, "", fontsize=11)
			for position in range(self.recent.maxlen)]
		self.footer = self.figure.text(0.06, 0.08, "Generating houses.csv", color=MUTED, fontsize=10)
		self._refresh()
		plt.show(block=False)

	def _refresh(self, finished=False):
		fraction = self.processed / self.total if self.total else float(finished)
		status = "Complete" if finished else "Predicting"
		self.status.set_text(f"{status}  ·  {self.processed:,} / {self.total:,} students  ·  {fraction:.0%}")
		self.progress.set_width(fraction)
		self.house_axis.set_xlim(0, max(5, max(self.counts.values()) * 1.25))
		for bar, label, count in zip(self.bars, self.count_labels, self.counts.values()):
			bar.set_width(count)
			label.xy = (count, label.xy[1])
			label.set_text(f"{count:,}")
		for label, (student_index, house) in zip(self.recent_labels, self.recent):
			label.set_text(f"#{student_index}  ·  {house}")
			label.set_color(HOUSE_COLORS[house])
		self.figure.canvas.draw_idle()

	def record(self, student_index, house):
		if not plt.fignum_exists(self.figure.number):
			return
		self.processed += 1
		self.counts[house] += 1
		self.recent.appendleft((student_index, house))
		if self.processed < self.total and self.processed % self.refresh_every == 0:
			self._refresh()
			plt.pause(0.05)

	def finish(self):
		if plt.fignum_exists(self.figure.number):
			self.footer.set_text("Saved to houses.csv  ·  Close this window to exit")
			self._refresh(finished=True)
			plt.show(block=True)
