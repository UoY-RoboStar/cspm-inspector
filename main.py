#!/usr/bin/env python3
"""cspm-explain: run FDR on a CSP file and explain any deadlock counter-examples."""

import argparse
import os
import sys

from cspm_inspector import file_parser, statistics_generator
from cspm_inspector.csv_writer import write_entry_csv, write_dataset_csv, write_entries_csv


def _print_dataset_header():
    print('{:25s} {:>8s} {:>8s} {:>8s} {:>15s} {:>15s} {:>15s}'.format("Operator","Pass" , "Fail" , "Total" , "Per Entry" , "Per Pass" , "Per Fail"))


def _print_unique_entry_dataset_header(count):
    print()
    print('{:14} {:5d} {:20s}'.format("Figures across ",count," unique CSP cases"))
    print()
    print('{:25s} {:>15s} {:>25s}'.format("Operator","Total Count","Average Count Per Entry"))


def _print_entries_header():
    print('{:25s} {:>15s}'.format("Operator", "Count"))


def _print_dataset_statistics(data,output):
    _print_dataset_header()

    for operator in data.get("total"):
        if not operator=="unique_entry":
            print('{:25s} {:8d} {:8d} {:8d} {:15f} {:15f} {:15f}'
                  .format(operator,
                          data.get("pass").get(operator),
                          data.get("fail").get(operator),
                          data.get("total").get(operator),
                          0 if data.get("total").get("entry") == 0 else data.get("total").get(operator)/data.get("total").get("entry"),
                          0 if data.get("pass").get("entry") == 0 else data.get("pass").get(operator)/data.get("pass").get("entry"),
                          0 if data.get("fail").get("entry") == 0 else data.get("fail").get(operator)/data.get("fail").get("entry")
                          )
                  )

    if output is not None:
        write_dataset_csv(data, output)

def _print_unique_entries_statistics(data,output):
    record = {"unique_entry": 0, "entry": 0, "e -> P": 0, "P \\ A": 0,
              "P[[from<-to]]": 0, "P |\\ A": 0, "P |~| Q": 0,
              "P [] Q": 0, "P [| A |] Q": 0, "P ||| Q": 0,
              "P [ A || B ] Q": 0, "P ; Q": 0, "P [| A |> Q": 0,
              "P [> Q": 0, "P /\\ Q": 0, "b & P": 0,
              "||| x:{} @ P(x)": 0, "[] x:{} @ P(x)": 0,
              "|~| x:{} @ P(x)": 0, "[|A|] x:{} @ P(x)": 0,
              "|| x:{} @ [A] P(x)": 0, "@": 0}

    for entry in data:
        if not entry=="fail" and not entry=="pass" and not entry=="total":
            updated = {k: data.get(entry).get(k, 0) + record.get(k, 0)
               for k in data.get(entry).keys() | record.keys()}
            record.update(updated)

    _print_unique_entry_dataset_header(data.get("total").get("unique_entry"))

    for operator in record:
        if not operator=="unique_entry" and not operator=="entry":
            print('{:25s} {:15d} {:25f}'.format(operator, record.get(operator), record.get(operator)/data.get("total").get("unique_entry")))


    if output is not None:
        write_entries_csv(record, data.get("total").get("unique_entry"), output)


def _print_single_entry_statistics(data, output):
    _print_entries_header()
    for entry in data:
        for operator in data.get(entry):
            print('{:25s} {:15d}'.format(operator, data.get(entry).get(operator)))

    if output is not None:
        write_entry_csv(data, output)


def _run_dataset_calculator(parsed_csv, output):
    record = {"unique_entry":0,"entry":0,"e -> P":0,"P \\ A":0,
              "P[[from<-to]]":0,"P |\\ A":0,"P |~| Q":0,
              "P [] Q":0,"P [| A |] Q":0,"P ||| Q":0,
              "P [ A || B ] Q":0,"P ; Q":0,"P [| A |> Q":0,
              "P [> Q":0,"P /\\ Q":0,"b & P":0,
              "||| x:{} @ P(x)":0,"[] x:{} @ P(x)":0,
              "|~| x:{} @ P(x)":0,"[|A|] x:{} @ P(x)":0,
              "|| x:{} @ [A] P(x)":0,"@":0}
    data = {"pass":record.copy(), "fail": record.copy()}
    count = 0
    for entry in parsed_csv:
        unique=False

        if not parsed_csv.get(entry)[0] in data:
            entry_record = record.copy()

            (prefix, hide, rename, project, internal_choice, external_choice, generalised_parallel,
             alphabetised_parallel,
             interleave, sequential_composition, exception, timeout, interrupt, guard, rep_generalised_parallel,
             rep_alphabetised_parallel, rep_interleave, rep_internal_choice, rep_external_choice,
             rep) = statistics_generator.perform_analysis(parsed_csv.get(entry)[0])

            entry_record.update({"e -> P": prefix})
            entry_record.update({"P \\ A": hide})
            entry_record.update({"P[[from<-to]]": rename})
            entry_record.update({"P |\\ A": project})
            entry_record.update({"P |~| Q": internal_choice})
            entry_record.update({"P [] Q": external_choice})
            entry_record.update({"P [| A |] Q": generalised_parallel})
            entry_record.update({"P ||| Q": interleave})
            entry_record.update({"P [ A || B ] Q": alphabetised_parallel})
            entry_record.update({"P ; Q": sequential_composition})
            entry_record.update({"P [| A |> Q": exception})
            entry_record.update({"P [> Q": timeout})
            entry_record.update({"P /\\ Q": interrupt})
            entry_record.update({"b & P": guard})
            entry_record.update({"||| x:{} @ P(x)": rep_interleave})
            entry_record.update({"[] x:{} @ P(x)": rep_external_choice})
            entry_record.update({"|~| x:{} @ P(x)": rep_internal_choice})
            entry_record.update({"[|A|] x:{} @ P(x)": rep_generalised_parallel})
            entry_record.update({"|| x:{} @ [A] P(x)": rep_alphabetised_parallel})
            entry_record.update({"@": rep})
            entry_record.update({"entry": 1})

            data[parsed_csv.get(entry)[0]] = entry_record
            unique=True
        else:
            entry_record = data.get(parsed_csv.get(entry)[0])
            entry_count = entry_record.get("entry")
            entry_record.update({"entry": entry_count+1})
            data.update({entry: entry_record})


        if parsed_csv.get(entry)[2] == "true":
            passed = data.get("pass")
        else:
            passed = data.get("fail")

        updated = {k: passed.get(k, 0) + (1 if data.get(parsed_csv.get(entry)[0]).get(k, 0) != 0 else 0)
                         for k in passed.keys() | data.get(parsed_csv.get(entry)[0]).keys()}

        if unique:
            updated.update({"unique_entry": passed.get("unique_entry") + 1})

        if parsed_csv.get(entry)[2] == "true":
            data.update({"pass":updated})
        else:
            data.update({"fail":updated})

        count+=1

    print(count)

    data["total"] = {k: data.get("pass").get(k, 0) + data.get("fail").get(k, 0)
                     for k in data.get("pass").keys() | data.get("fail").keys()}


    _print_dataset_statistics(data,output)
    print()
    _print_unique_entries_statistics(data,output)


def _run_calculator(parsed_csp, output):
    entry_record = {"e -> P":0,"P \\ A":0,
              "P[[from<-to]]":0,"P |\\ A":0,"P |~| Q":0,
              "P [] Q":0,"P [| A |] Q":0,"P ||| Q":0,
              "P [ A || B ] Q":0,"P ; Q":0,"P [| A |> Q":0,
              "P [> Q":0,"P /\\ Q":0,"b & P":0,
              "||| x:{} @ P(x)":0,"[] x:{} @ P(x)":0,
              "|~| x:{} @ P(x)":0,"[|A|] x:{} @ P(x)":0,
              "|| x:{} @ [A] P(x)":0,"@":0}
    data = {}

    (prefix, hide, rename, project, internal_choice, external_choice, generalised_parallel,
     alphabetised_parallel,
     interleave, sequential_composition, exception, timeout, interrupt, guard, rep_generalised_parallel,
     rep_alphabetised_parallel, rep_interleave, rep_internal_choice, rep_external_choice,
     rep) = statistics_generator.perform_analysis(parsed_csp)

    entry_record.update({"e -> P": prefix})
    entry_record.update({"P \\ A": hide})
    entry_record.update({"P[[from<-to]]": rename})
    entry_record.update({"P |\\ A": project})
    entry_record.update({"P |~| Q": internal_choice})
    entry_record.update({"P [] Q": external_choice})
    entry_record.update({"P [| A |] Q": generalised_parallel})
    entry_record.update({"P ||| Q": interleave})
    entry_record.update({"P [ A || B ] Q": alphabetised_parallel})
    entry_record.update({"P ; Q": sequential_composition})
    entry_record.update({"P [| A |> Q": exception})
    entry_record.update({"P [> Q": timeout})
    entry_record.update({"P /\\ Q": interrupt})
    entry_record.update({"b & P": guard})
    entry_record.update({"||| x:{} @ P(x)": rep_interleave})
    entry_record.update({"[] x:{} @ P(x)": rep_external_choice})
    entry_record.update({"|~| x:{} @ P(x)": rep_internal_choice})
    entry_record.update({"[|A|] x:{} @ P(x)": rep_generalised_parallel})
    entry_record.update({"|| x:{} @ [A] P(x)": rep_alphabetised_parallel})
    entry_record.update({"@": rep})

    data[parsed_csp] = entry_record

    _print_single_entry_statistics(data, output)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Calculate the statistical prevalence and probability of CSPM Operators within a csv file of records, or an individual csp file."
    )
    parser.add_argument("csv_p_file", help="Path to the .csv or .csp file to check")
    parser.add_argument(
        "-o",
        "--output_csv",
        action="store_true",
        help="Write a <file>-output.csv, and <file>-output-entries.csv if a csv is input",
    )
    args = parser.parse_args()

    if not os.path.isfile(args.csv_p_file):
        sys.exit(f"Error: file not found: {args.csv_p_file}")

    output = args.csv_p_file.split(".csv")[0] + "-output.csv" if args.output_csv else None

    if args.csv_p_file.endswith(".csv"):
        parsed_csv = file_parser.parse_csv(args.csv_p_file)
        _run_dataset_calculator(parsed_csv, output)
    elif args.csv_p_file.endswith(".csp"):
        parsed_csp = file_parser.parse_csp(args.csv_p_file)
        _run_calculator(parsed_csp, output)


if __name__ == "__main__":
    main()
