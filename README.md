# cspm-inspector

Reads in a CSV of CSPM entries, or single CSP file, and analyses the number of 
operators present. Outputs a table of statistics in the command line.

## Requirements

- Python 3.11+

## Usage

```bash
python3 main.py path/to/spec.csv
```

Performs analysis of all entries within the provided CSV file. Generates 
statistics for the dataset, counting each operator as encountered across all
dataset entries, differentiating between passing and failing cases, and 
calculates their probabilities:

- the operator
- the count across all passing CSP entries
- the count across all failing CSP entries
- the count across all CSP entries
- the probability of the operator within a passing CSP entry
- the probability of the operator within a failing CSP entry
- the probability of the operator within a CSP entry


Further statistics are provided on the presence of operators across all unique
CSP entries within the dataset, including:

- the operator
- the count across all unique CSP entries
- the probability of the operator within a CSP entry

```bash
python3 main.py path/to/spec.csp
```

Performs analysis of the provided CSP file. Counts the presence of each operator 
within the CSP.


### Optional: Output explanation to CSV

```bash
python3 main.py --output_csv path/to/spec.csp
python3 main.py --o path/to/spec.csp
```

Passing "--output_csv" triggers the generation of an output file of the form 
`<file>-output.csv` containing the generated statistics of the dataset as a whole.
An output file of the form `<file>-output-entries.csv` is created to indicate the 
statistics for operators across unique CSP entries in the CSV.

```bash
python3 main.py --output_csv path/to/spec.csp
python3 main.py --o path/to/spec.csp
```

Passing "--output_csv" triggers the generation of an output file of the form 
`<file>-output.csv` containing the generated statistics for the singular CSP file.


