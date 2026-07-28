import csv

def _parse_csv_entry(entry, passed)->tuple[str,str,str]:
    csp = entry[0]
    assertion = entry[1]
    status = entry[passed]

    return csp,assertion,status

def parse_csv(csv_file):
    with open(csv_file, "r", newline='') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        line = next(reader)
        passed = line.index("Passed")

        try:
            lines = {}
            for row in reader:
                csp, assertion, status = _parse_csv_entry(row, passed)
                lines.update({csp+assertion: [csp,assertion,status]})
        except csv.Error as e:
            print(f'file {csv_file}, line {reader.line_num}: {e}')


    return lines

def parse_csp(csp_file):
    with open(csp_file, "r", newline='') as f:
        content = f.read()

    return content