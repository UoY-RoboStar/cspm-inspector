import csv
import os

def write_dataset_csv(data, file_path: str) -> None:
    print(f"Writing to {file_path}")

    with open(file_path, mode="a+") as csv_file:
        csv_writer = csv.writer(csv_file)
        if not (os.path.isfile(file_path) and os.path.getsize(file_path) > 0):
            csv_writer.writerow(["Operator","Pass" , "Fail" , "Total" , "Per Entry" , "Per Pass" , "Per Fail"])

        for operator in data.get("total"):
            if not operator == "unique_entry":
                csv_writer.writerow([operator,
                              data.get("pass").get(operator),
                              data.get("fail").get(operator),
                              data.get("total").get(operator),
                              0 if data.get("total").get("entry") == 0 else data.get("total").get(operator) / data.get(
                                  "total").get("entry"),
                              0 if data.get("pass").get("entry") == 0 else data.get("pass").get(operator) / data.get(
                                  "pass").get("entry"),
                              0 if data.get("fail").get("entry") == 0 else data.get("fail").get(operator) / data.get(
                                  "fail").get("entry")
                              ])


def write_entries_csv(record, count, file_path: str) -> None:
    updated_file_path = file_path.split(".csv")[0] + "-entries.csv"
    print(f"Writing to {updated_file_path}")

    with open(updated_file_path, mode="a+") as csv_file:
        csv_writer = csv.writer(csv_file)
        if not (os.path.isfile(updated_file_path) and os.path.getsize(updated_file_path) > 0):
            csv_writer.writerow(["Operator","Total Count","Average Count Per Entry"])
            csv_writer.writerow(["No. of entries",count,""])
        for operator in record:
            if not operator == "entry" and not operator == "unique_entry":
                csv_writer.writerow([operator, record.get(operator),
                                                    record.get(operator) / count])


def write_entry_csv(data, file_path: str) -> None:
    print(f"Writing to {file_path}")

    with open(file_path, mode="a+") as csv_file:
        csv_writer = csv.writer(csv_file)
        if not (os.path.isfile(file_path) and os.path.getsize(file_path) > 0):
            csv_writer.writerow(["Operator", "Count"])
        for entry in data:
            for operator in data.get(entry):
                csv_writer.writerow([operator, data.get(entry).get(operator)])
