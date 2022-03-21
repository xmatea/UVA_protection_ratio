import pandas as pd
from pathlib import Path

def get_data(path: str) -> pd.DataFrame:
	return pd.read_csv(path, sep=";")


def extract_uvs(raw_path: str, uv_path: str) -> None:
	raw_data = get_data(raw_path)
	column_names = raw_data.columns

	uv_data = raw_data.drop([column_names[i] for i in [0, 1, 4, 5, 6, 7]], axis=1)
	uv_data.rename(columns={
				column_names[2]: "UVA",
				column_names[3]: "UVB"},
		inplace=True)

	uv_data.to_csv(uv_path, sep=";", index=False)


def make_uv_path(raw_path: str) -> str:
	split_path = raw_path.split("\\")
	parent_path = "\\".join(split_path[:-1]).replace("raw", "uv")
	parent_path += "\\" + split_path[-1][0]
	file_name = split_path[-1][2:]

	path = parent_path + "\\" + file_name
	return path


if __name__ == "__main__":
	raw_data_path = Path(__file__).parent.parent / "data" / "raw"
	uv_data_path = Path(__file__).parent.parent / "data" / "uv"

	raw_data_paths = list(map(str, raw_data_path.glob("*.csv")))

	sunscreens = {path.split("\\")[-1][0] for path in raw_data_paths}

	for sunscreen in sunscreens:
		(uv_data_path / sunscreen).mkdir(exist_ok=True)

	uv_data_paths = map(make_uv_path, raw_data_paths)

	data_paths = zip(raw_data_paths, uv_data_paths)

	for raw_path, uv_path in data_paths:
		extract_uvs(raw_path, uv_path)
