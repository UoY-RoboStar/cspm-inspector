#!/usr/bin/env python3
"""cspm-explain: run FDR on a CSP file and explain any deadlock counter-examples."""

import argparse
import os
import sys

from cspm_inspector import file_parser, statistics_generator
from cspm_inspector.csv_writer import write_entry_csv, write_dataset_csv, write_entries_csv


def _print_dataset_header():
    print('{:25s} {:>27s} {:>27s} {:>24s} {:>20s} {:>24s} {:>24s}'.format("Operator",
                                                                       "Count for Entries",
                                                                       "Count for Entries",
                                                                       "Total Count across" ,
                                                                       "Average Count" ,
                                                                       "Average Count Per" ,
                                                                       "Average Count Per"))
    print('{:25s} {:>27s} {:>27s} {:>24s} {:>20s} {:>24s} {:>24s}'.format("",
                                                                       "with a Passing Assertion",
                                                                       "with a Failing Assertion",
                                                                       "all Dataset Entries" ,
                                                                       "Per Entry" ,
                                                                       "Passing Entry" ,
                                                                       "Failing Entry"))


def _print_unique_entry_dataset_header(count):
    print()
    print('{:14} {:5d} {:20s}'.format("Figures across ",count," unique CSP cases"))
    print()
    print('{:25s} {:>21s} {:>21s}'.format("Operator","Total Count across",
                                          "Average Count"))
    print('{:25s} {:>21s} {:>21s}'.format("","all Dataset Entries",
                                          "Per Dataset Entry"))


def _print_entries_header():
    print('{:25s} {:>15s}'.format("Operator", "Total Count"))


def _print_dataset_statistics(data,output):
    _print_dataset_header()
    print('{:25s} {:27d} {:27d} {:24d} {:20f} {:24f} {:24f}'
          .format("# of dataset entries",
                  data.get("pass").get("# of dataset entries"),
                  data.get("fail").get("# of dataset entries"),
                  data.get("total").get("# of dataset entries"),
                  0 if data.get("total").get("# of dataset entries") == 0 else
                  data.get("total").get("# of dataset entries") / data.get("total").get("# of dataset entries"),
                  0 if data.get("pass").get("# of dataset entries") == 0 else
                  data.get("pass").get("# of dataset entries") / data.get("pass").get("# of dataset entries"),
                  0 if data.get("fail").get("# of dataset entries") == 0 else
                  data.get("fail").get("# of dataset entries") / data.get("fail").get("# of dataset entries")
                  )
          )

    for operator in data.get("total"):
        if not operator=="# of unique dataset entries" and not operator=="# of dataset entries":
            print('{:25s} {:27d} {:27d} {:24d} {:20f} {:24f} {:24f}'
                  .format(operator,
                          data.get("pass").get(operator),
                          data.get("fail").get(operator),
                          data.get("total").get(operator),
                          0 if data.get("total").get("# of dataset entries") == 0 else
                                            data.get("total").get(operator)/data.get("total").get("# of dataset entries"),
                          0 if data.get("pass").get("# of dataset entries") == 0 else
                                            data.get("pass").get(operator)/data.get("pass").get("# of dataset entries"),
                          0 if data.get("fail").get("# of dataset entries") == 0 else
                                            data.get("fail").get(operator)/data.get("fail").get("# of dataset entries")
                          )
                  )

    if output is not None:
        write_dataset_csv(data, output)

def _print_unique_entries_statistics(data,output):
    record = {"# of unique dataset entries":0,"# of dataset entries":0,"e -> P":0,"P \\ A":0,
              "P[[from<-to]]":0,"P |\\ A":0,"P |~| Q":0,
              "P [] Q":0,"P [| A |] Q":0,"P ||| Q":0,
              "P [ A || B ] Q":0,"P ; Q":0,"P [| A |> Q":0,
              "P [> Q":0,"P /\\ Q":0,"b & P":0,
              "||| x:{} @ P(x)":0,"[] x:{} @ P(x)":0,
              "|~| x:{} @ P(x)":0,"[|A|] x:{} @ P(x)":0,
              "|| x:{} @ P(x)": 0, "[l <-> r] x:{} @ P(x)": 0,
              "; x:{} @ P(x)":0, "[+ A +] x:{} @ P(x)": 0, "@":0,
              "let_within":0, "\\ ps @ e":0, "if_then_else":0,
              "P /+ A +\\ Q":0, "P [+ A +] Q":0, "P [c <-> d] Q":0}

    for entry in data:
        if not entry=="fail" and not entry=="pass" and not entry=="total":
            updated = {k: data.get(entry).get(k, 0) + record.get(k, 0)
               for k in data.get(entry).keys() | record.keys()}
            record.update(updated)

    _print_unique_entry_dataset_header(data.get("total").get("# of unique dataset entries"))

    for operator in record:
        if not operator=="# of unique dataset entries" and not operator=="# of dataset entries":
            print('{:25s} {:21d} {:21f}'.format(operator, record.get(operator),
                                                record.get(operator)/data.get("total").get("# of unique dataset entries")))


    if output is not None:
        write_entries_csv(record, data.get("total").get("# of unique dataset entries"), output)


def _print_single_entry_statistics(data, output):
    _print_entries_header()
    for entry in data:
        for operator in data.get(entry):
            print('{:25s} {:15d}'.format(operator, data.get(entry).get(operator)))

    if output is not None:
        write_entry_csv(data, output)


def _run_dataset_calculator(parsed_csv, output):
    record = {"# of unique dataset entries":0,"# of dataset entries":0,"e -> P":0,"P \\ A":0,
              "P[[from<-to]]":0,"P |\\ A":0,"P |~| Q":0,
              "P [] Q":0,"P [| A |] Q":0,"P ||| Q":0,
              "P [ A || B ] Q":0,"P ; Q":0,"P [| A |> Q":0,
              "P [> Q":0,"P /\\ Q":0,"b & P":0,
              "||| x:{} @ P(x)":0,"[] x:{} @ P(x)":0,
              "|~| x:{} @ P(x)":0,"[|A|] x:{} @ P(x)":0,
              "|| x:{} @ P(x)": 0, "[l <-> r] x:{} @ P(x)": 0,
              "; x:{} @ P(x)":0, "[+ A +] x:{} @ P(x)": 0, "@":0,
              "let_within":0, "\\ ps @ e":0, "if_then_else":0,
              "P /+ A +\\ Q":0, "P [+ A +] Q":0, "P [c <-> d] Q":0}
    data = {"pass":record.copy(), "fail": record.copy()}
    count = 0
    for entry in parsed_csv:
        unique=False

        if not parsed_csv.get(entry)[0] in data:
            entry_record = record.copy()

            (prefix, hide, rename, project, internal_choice, external_choice, generalised_parallel,
             alphabetised_parallel, interleave, sequential_composition, exception, timeout, interrupt, guard,
             rep_generalised_parallel, rep_alphabetised_parallel, rep_interleave, rep_internal_choice,
             rep_external_choice, rep, rep_sequential_composition, rep_linked_parallel, lambda_pattern,
             rep_synchronising_parallel, let_within, if_then, linked_parallel, synchronising_interrupt,
             synchronising_external_choice) = (statistics_generator.perform_analysis(parsed_csv.get(entry)[0]))

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
            entry_record.update({"[l <-> r] x:{} @ P(x)": rep_linked_parallel})
            entry_record.update({"; x:{} @ P(x)": rep_sequential_composition})
            entry_record.update({"[+ A +] x:{} @ P(x)": rep_synchronising_parallel})
            entry_record.update({"let_within":let_within})
            entry_record.update({"\\ ps @ e":lambda_pattern})
            entry_record.update({"if_then_else":if_then})
            entry_record.update({"P /+ A +\\ Q":synchronising_interrupt})
            entry_record.update({"P [+ A +] Q":synchronising_external_choice})
            entry_record.update({"P [c <-> d] Q":linked_parallel})
            entry_record.update({"# of dataset entries": 1})

            data[parsed_csv.get(entry)[0]] = entry_record
            unique=True
        else:
            entry_record = data.get(parsed_csv.get(entry)[0])
            entry_count = entry_record.get("# of dataset entries")
            entry_record.update({"# of dataset entries": entry_count+1})
            data.update({entry: entry_record})


        if parsed_csv.get(entry)[2] == "true":
            passed = data.get("pass")
        else:
            passed = data.get("fail")

        updated = {k: passed.get(k, 0) + (1 if data.get(parsed_csv.get(entry)[0]).get(k, 0) != 0 else 0)
                         for k in passed.keys() | data.get(parsed_csv.get(entry)[0]).keys()}

        if unique:
            updated.update({"# of unique dataset entries": passed.get("# of unique dataset entries") + 1})

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
              "|| x:{} @ P(x)": 0, "[l <-> r] x:{} @ P(x)": 0,
              "; x:{} @ P(x)":0, "[+ A +] x:{} @ P(x)": 0, "@":0,
              "let_within":0, "\\ ps @ e":0, "if_then_else":0,
              "P /+ A +\\ Q":0, "P [+ A +] Q":0, "P [c <-> d] Q":0}
    data = {}

    (prefix,hide,rename,project,internal_choice,external_choice,generalised_parallel,alphabetised_parallel,
            interleave,sequential_composition,exception,timeout,interrupt,guard,rep_generalised_parallel,
            rep_alphabetised_parallel,rep_interleave,rep_internal_choice,rep_external_choice, replicated,
            rep_sequential_composition, rep_linked_parallel, lambda_pattern,
            rep_synchronising_parallel, let_within, if_then, linked_parallel, synchronising_interrupt,
            synchronising_external_choice) = statistics_generator.perform_analysis(parsed_csp)

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
    entry_record.update({"@": replicated})
    entry_record.update({"[l <-> r] x:{} @ P(x)": rep_linked_parallel})
    entry_record.update({"; x:{} @ P(x)": rep_sequential_composition})
    entry_record.update({"[+ A +] x:{} @ P(x)": rep_synchronising_parallel})
    entry_record.update({"let_within":let_within})
    entry_record.update({"\\ ps @ e":lambda_pattern})
    entry_record.update({"if_then_else":if_then})
    entry_record.update({"P /+ A +\\ Q":synchronising_interrupt})
    entry_record.update({"P [+ A +] Q":synchronising_external_choice})
    entry_record.update({"P [c <-> d] Q":linked_parallel})

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


    if args.csv_p_file.endswith(".csv"):
        output = args.csv_p_file.split(".csv")[0] + "-output.csv" if args.output_csv else None

        parsed_csv = file_parser.parse_csv(args.csv_p_file)
        _run_dataset_calculator(parsed_csv, output)
    elif args.csv_p_file.endswith(".csp"):
        output = args.csv_p_file.split(".csp")[0] + "-output.csp" if args.output_csv else None

        parsed_csp = file_parser.parse_csp(args.csv_p_file)
        _run_calculator(parsed_csp, output)


if __name__ == "__main__":
    main()
