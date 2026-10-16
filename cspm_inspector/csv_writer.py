import csv
import os

def write_dataset_csv(data, file_path: str) -> None:
    print(f"Writing to {file_path}")

    with open(file_path, mode="a+") as csv_file:
        csv_writer = csv.writer(csv_file)
        if not (os.path.isfile(file_path) and os.path.getsize(file_path) > 0):
            csv_writer.writerow(["Operator", "Count for Entries with a Passing Assertion",
                                 "Count for Entries with a Failing Assertion",
                                 "Total Count across all Dataset Entries",
                                 "Average Count Per Entry", "Average Count Per Passing Entry",
                                 "Average Count Per Failing Entry"])

        csv_writer.writerow(["# of dataset entries",
                      data.get("pass").get("# of dataset entries"),
                      data.get("fail").get("# of dataset entries"),
                      data.get("total").get("# of dataset entries"),
                      0 if data.get("total").get("# of dataset entries") == 0 else
                      data.get("total").get("# of dataset entries") / data.get("total").get("# of dataset entries"),
                      0 if data.get("pass").get("# of dataset entries") == 0 else
                      data.get("pass").get("# of dataset entries") / data.get("pass").get("# of dataset entries"),
                      0 if data.get("fail").get("# of dataset entries") == 0 else
                      data.get("fail").get("# of dataset entries") / data.get("fail").get("# of dataset entries")
                      ]
              )

        for operator in data.get("total"):
            if not operator == "# of dataset entries" and not operator == "# of unique dataset entries":
                csv_writer.writerow([operator,
                              data.get("pass").get(operator),
                              data.get("fail").get(operator),
                              data.get("total").get(operator),
                              0 if data.get("total").get("# of dataset entries") == 0 else
                                     data.get("total").get(operator) / data.get("total").get("# of dataset entries"),
                              0 if data.get("pass").get("# of dataset entries") == 0 else
                                     data.get("pass").get(operator) / data.get("pass").get("# of dataset entries"),
                              0 if data.get("fail").get("# of dataset entries") == 0 else
                                     data.get("fail").get(operator) / data.get("fail").get("# of dataset entries")
                              ])



def write_neutral_dataset_csv(data, file_path: str) -> None:
    print(f"Writing to {file_path}")

    with open(file_path, mode="a+") as csv_file:
        csv_writer = csv.writer(csv_file)
        if not (os.path.isfile(file_path) and os.path.getsize(file_path) > 0):
            csv_writer.writerow(["Operator",
                                 "Total Count across all Dataset Entries",
                                 "Average Count Per Entry"])

        csv_writer.writerow(["# of dataset entries",
                      data.get("total").get("# of dataset entries"),
                      0 if data.get("total").get("# of dataset entries") == 0 else
                      data.get("total").get("# of dataset entries") / data.get("total").get("# of dataset entries")
                      ]
              )

        for operator in data.get("total"):
            if not operator == "# of dataset entries" and not operator == "# of unique dataset entries":
                csv_writer.writerow([operator,
                              data.get("total").get(operator),
                              0 if data.get("total").get("# of dataset entries") == 0 else
                                     data.get("total").get(operator) / data.get("total").get("# of dataset entries")
                              ])


def write_entries_csv(record, count, file_path: str) -> None:
    updated_file_path = file_path.split(".csv")[0] + "-entries.csv"
    print(f"Writing to {updated_file_path}")

    with open(updated_file_path, mode="a+") as csv_file:
        csv_writer = csv.writer(csv_file)
        if not (os.path.isfile(updated_file_path) and os.path.getsize(updated_file_path) > 0):
            csv_writer.writerow(["Operator","Total Count across all Dataset Entries",
                                          "Average Count Per Dataset Entry"])
            csv_writer.writerow(["No. of entries",count,""])
        for operator in record:
            if not operator == "# of dataset entries" and not operator == "# of unique dataset entries":
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
