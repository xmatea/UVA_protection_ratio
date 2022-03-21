import pandas as pd
import numpy as np
from pathlib import Path
from tabulate import tabulate
import sigfig
import matplotlib.pyplot as plt

REMOVAL_THRESHOLD = 10
STABILITY_THRESHOLD = 15
SHOW_RATIOS = False
SHOW_ALL_STEPS = False
SHOW_ALL = False
SHOW_MINIMAL = False

# load dataframe from csv file
def get_data(path: str) -> pd.DataFrame:
	return pd.read_csv(path, sep=";")


# remove lead values below threshold
def remove_leading(df: pd.DataFrame, threshold: int) -> None:
	indices_below = []
	for index, row in df.iterrows():
		if row["UVA"] < threshold or row["UVB"] < threshold:
			indices_below.append(index)
			continue

		break

	cleaned_df = df.drop(indices_below)
	cleaned_df.reset_index(drop=True, inplace=True)

	return cleaned_df


# remove trailing values below threshold
# TODO make this remove trailing peaks like in C_2
def remove_trailing(df: pd.DataFrame, threshold: int) -> None:
	indices_below = []
	for index, row in df[::-1].iterrows():
		if row["UVA"] < threshold or row["UVB"] < threshold:
			indices_below.append(index)
			continue

		break

	cleaned_df = df.drop(indices_below)
	cleaned_df.reset_index(drop=True, inplace=True)

	return cleaned_df


# split the dataset where the values dip below the threshold (adding filter)
def split_filtered(df: pd.DataFrame, threshold: int) -> tuple[pd.DataFrame, pd.DataFrame]:
	indices_below = []
	for index, row in df.iterrows():
		if row["UVA"] < threshold or row["UVB"] < threshold:
			indices_below.append(index)

	split_index = indices_below[len(indices_below)//2] # get the middle value incase there are any dips before or after the filter change
	filtered = df[:split_index]
	unfiltered = df[split_index:]

	# clean up data
	filtered = remove_trailing(filtered, threshold)
	unfiltered = remove_leading(unfiltered, threshold)

	return (filtered, unfiltered)


def get_stable_values(df: pd.DataFrame, stability_threshold: int) -> pd.DataFrame:
	unstable_values = [i for i in range(len(df.index) - stability_threshold)]
	stable_values = df.drop(unstable_values)
	stable_values.reset_index(drop=True, inplace=True)

	return stable_values


def process_data(data_path: str):
	global SHOW_ALL_STEPS, REMOVAL_THRESHOLD, STABILITY_THRESHOLD, SHOW_RATIOS, SHOW_ALL_SUMMARY, SHOW_MINIMAL
	sunscreen, run = get_sunscreen(data_path)
	#print(f"sunscreen {sunscreen} run {run}")
	uv_data = get_data(data_path)

	if SHOW_ALL_STEPS:
		ax = uv_data.plot.line()
		plt.title("RAW UV DATA")
		plt.show()

	# remove leading and trailing dips so that the only dip in the values is when the filter is added
	uv_data = remove_leading(uv_data, REMOVAL_THRESHOLD)
	uv_data = remove_trailing(uv_data, REMOVAL_THRESHOLD)

	if SHOW_ALL_STEPS:
		ax = uv_data.plot.line()
		plt.title("TRIMMED RAW UV DATA")
		plt.show()

	# split at dip
	uv_data_unfiltered, uv_data_filtered = split_filtered(uv_data, REMOVAL_THRESHOLD)

	# disregard 2nd peak after filtered data if it exists.
	try:
		uv_data_filtered, _ = split_filtered(uv_data_filtered, REMOVAL_THRESHOLD)
	except Exception:
		pass

	if SHOW_ALL_STEPS:
		ax = uv_data_unfiltered.plot.line()
		plt.title("UNSTABILISED UV DATA BEFORE SUN FILTER")
		plt.show()

		ax = uv_data_filtered.plot.line()
		plt.title("UNSTABILISED UV DATA AFTER SUN FILTER")
		plt.show()

	# remove leading values until value is stable
	uv_data_unfiltered = get_stable_values(uv_data_unfiltered, STABILITY_THRESHOLD)
	uv_data_filtered = get_stable_values(uv_data_filtered, STABILITY_THRESHOLD)

	if SHOW_ALL_STEPS:
		ax = uv_data_unfiltered.plot.line()
		plt.title("STABILISED UV DATA BEFORE SUN FILTER")
		plt.show()

		ax = uv_data_filtered.plot.line()
		plt.title("STABILISED UV DATA AFTER SUN FILTER")
		plt.show()


	uva_unfiltered_avg = np.average(uv_data_unfiltered["UVA"].to_numpy())
	uvb_unfiltered_avg = np.average(uv_data_unfiltered["UVB"].to_numpy())
	uva_filtered_avg = np.average(uv_data_filtered["UVA"].to_numpy())
	uvb_filtered_avg = np.average(uv_data_filtered["UVB"].to_numpy())

	if SHOW_ALL_STEPS:
		print(f"Average UVA before filter: {round(uva_unfiltered_avg, 3)}")
		print(f"Average UVB before filter: {round(uvb_unfiltered_avg, 3)}")
		print(f"Average UVA after filter: {round(uva_filtered_avg, 3)}")
		print(f"Average UVB after filter: {round(uvb_filtered_avg, 3)}")

	uva_ratio = round((1-(uva_filtered_avg / uva_unfiltered_avg))*100, 1)
	uvb_ratio = round((1-(uvb_filtered_avg / uvb_unfiltered_avg))*100, 1)

	if SHOW_ALL_STEPS or SHOW_RATIOS:
		print(f"UVA protection ratio: {round(uva_ratio, 4)}")
		print(f"UVB protetion ratio: {round(uvb_ratio, 4)}")

	uv_ratio = (uva_ratio / uvb_ratio)
	return [sunscreen, run, round(uva_unfiltered_avg, 1), round(uvb_unfiltered_avg, 1), round(uva_filtered_avg, 1), round(uvb_filtered_avg, 1), uva_ratio, uvb_ratio, sigfig.round(uv_ratio, 3)]


def get_sunscreen(path: str) -> str:
	split_path = path.split("\\")
	sunscreen = split_path[-2]
	test = split_path[-1].split(".")[0]

	return sunscreen, test

sunscreens = {
  'A': "Aderma Protect AD",
  'B': "Avene B Protect",
  'C': "Eucerin Photoaging"
}

def get_uv_table(SHOW_MINIMAL=False, SHOW_ALL=False) -> list:
	data_path = Path(__file__).parent.parent / "data" / "uv"
	data_paths = list(map(str, data_path.rglob("*.csv")))

	if SHOW_ALL:
		table = [process_data(path) for path in data_paths]
		table = [[sunscreens[sunscreen[0]]] + sunscreen[1:] for sunscreen in table]
		table.insert(0, ["Type", "Run", "UVA before filter", "UVB before filter", "UVA after filter", "UVA after filter", "UVA blocked (%)", "UVB blocked (%)", "Blocking ratio"])
		return table

	if SHOW_MINIMAL:
		table = [process_data(path) for path in data_paths]
		table = [[sunscreens[sunscreen[0]]] + sunscreen[1:] for sunscreen in table]
		table = [sunscreen[0:2] + sunscreen[6:] for sunscreen in table]
		table.insert(0, ["Type", "Run", "UVA blocked (%)", "UVB blocked (%)", "Blocking ratio"])
		return table

	else:
		from random import choice
		path = choice(data_paths)
		return process_data(path)

if __name__ == "__main__":
	datatable(SHOW_MINIMAL=True)
