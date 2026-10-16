import csv

def _parse_csv_entry(entry, csp_pos, assertion_pos, passed)->tuple[str,str,str]:
    csp = entry[csp_pos]
    assertion = entry[assertion_pos] if assertion_pos!=-1 else ""
    status = entry[passed] if passed!=-1 else ""

    return csp,assertion,status

def parse_csv(csv_file):
    with open(csv_file, "r", newline='') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        line = next(reader)
        csp_pos = line.index("CSP")
        assertion_pos = line.index("Assertion") if "Assertion" in line else -1
        passed = line.index("Passed") if "Passed" in line else -1

        try:
            lines = {}
            for row in reader:
                csp, assertion, status = _parse_csv_entry(row, csp_pos, assertion_pos, passed)
                lines.update({csp+assertion: [csp,assertion,status]})
        except csv.Error as e:
            print(f'file {csv_file}, line {reader.line_num}: {e}')


    return lines

def parse_csp(csp_file):
    with open(csp_file, "r", newline='') as f:
        content = f.read()

    return content