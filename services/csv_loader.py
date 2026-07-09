import csv
import os

def load_csv_as_2d_array(path: str):
    with open(path, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    if len(rows) < 2:
        raise ValueError("CSV has no data rows.")

    header = [h.strip() for h in rows[0]]
    data_2d = [[cell.strip() for cell in row] for row in rows[1:]]
    return header, data_2d


def array2d_to_dicts(header: list[str], data_2d: list[list[str]]):
    records = []
    for row in data_2d:
        if len(row) < len(header):
            row = row + [""] * (len(header) - len(row))
        rec = {header[i]: row[i] for i in range(len(header))}
        records.append(rec)

    summary = {"rows": len(records), "columns": header}
    return records, summary

def clear_loaded_csv_from_memory(state: dict):
    state["header"] = None
    state["data_2d"] = None
    state["csv_dicts"] = None

def delete_csv_file(path: str) -> bool:
    if os.path.exists(path):
        os.remove(path)
        return True
    return False
