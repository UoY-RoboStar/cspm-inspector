import re

def regex_cnt(string, pattern):
    matches = re.findall(pattern, string)
    return len(matches)

def perform_analysis(entry:str) -> tuple[
    int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int,
    int, int, int, int, int, int, int, int, int]:

    prefix = entry.count("->", 0, len(entry))

    hide = entry.count("\\{", 0, len(entry))

    rename =  entry.count("[[", 0, len(entry))

    project =  regex_cnt(entry, '\s*\|\\\\\s*')

    internal_choice =  regex_cnt(entry, '(?:^|[^=;\s(]\s*)(\|~\|)\s*') #entry.count(") |~|", 0, len(entry))

    external_choice =  regex_cnt(entry, '(?:^|[^=;\s(]\s*)\[\]\s*') #entry.count(") []", 0, len(entry))

    generalised_parallel =  regex_cnt(entry, '(?:^|[^=;\s(]\s*)(\[\|(?s:.)*\|\])\s*') #entry.count(") [|", 0, len(entry))

    alphabetised_parallel =  regex_cnt(entry, '(?:^|[^=;\s(]\s*)(\[[^|>]([^\]]*?)\|\|)\s*') #entry.count(") [ ", 0, len(entry))

    interleave =  regex_cnt(entry, '(?:^|[^=;\s(]\s*)(\|\|\|)\s*') #entry.count(") |||", 0, len(entry))

    sequential_composition =  regex_cnt(entry, '(?:^|[^=\s(]\s*)(;)\s*') #entry.count(";", 0, len(entry))

    exception =  regex_cnt(entry, '\s*\|\>\s*')

    timeout =  regex_cnt(entry, '\s*\[\>\s*')

    interrupt =  regex_cnt(entry, '\s*/\\\s*')

    guard =  entry.count("&", 0, len(entry))

    rep_interleave = regex_cnt(entry, '(?:^|[=;(]\s*)(\|\|\|)\s*') #entry.count("= ||| ", 0, len(entry))

    rep_external_choice = regex_cnt(entry, '(?:^|[=;(]\s*)(\[\])\s*') #entry.count("= [] ", 0, len(entry))

    rep_internal_choice = regex_cnt(entry, '(?:^|[=;(]\s*)(\|\~\|)\s*') #entry.count("= |~| ", 0, len(entry))

    rep_generalised_parallel = regex_cnt(entry, '(?:^|[=;(]\s*)(\[\|)\s*') #entry.count("= [|", 0, len(entry))

    rep_alphabetised_parallel = regex_cnt(entry, '(?:^|[=;(]\s*)(\|\|(?!\|))\s*') #entry.count("= || ", 0, len(entry))

    rep_sequential_composition = regex_cnt(entry, '(?:^|[=(]\s*)(;\s)\s*') #entry.count("= ; ", 0, len(entry))

    rep_linked_parallel = regex_cnt(entry, '(?:^|[=;(]\s*)(\[(?s:.*?)<->(?s:.*?)\])\s*')

    rep_synchronising_parallel = regex_cnt(entry, '(?:^|[=;(]\s*)(\[\+)\s*')

    replicated = (rep_interleave+rep_sequential_composition+rep_alphabetised_parallel+rep_generalised_parallel
                  +rep_internal_choice+rep_external_choice+rep_linked_parallel)

    let_within = regex_cnt(entry, "(?s)(?<![a-zA-Z0-9])let(?![a-zA-Z0-9]).*?(?<![a-zA-Z0-9])within(?![a-zA-Z0-9])")

    if_then = regex_cnt(entry, "(?s)(?<![a-zA-Z0-9])if(?![a-zA-Z0-9]).*?(?<![a-zA-Z0-9])then(?![a-zA-Z0-9])")

    linked_parallel =regex_cnt(entry, '(?:^|[^=;(]\s*)(\[(?s:.*?)<->(?s:.*?)\])\s*')

    lambda_pattern = regex_cnt(entry, '(?:^|[=;(]\s*)\\\s*')

    synchronising_external_choice = regex_cnt(entry, '(?:^|[^=;(]\s*)(\[\+)\s*')

    synchronising_interrupt = regex_cnt(entry, '(?:^|[^=;(]\s*)(\/\+)\s*')


    return (prefix,hide,rename,project,internal_choice,external_choice,generalised_parallel,alphabetised_parallel,
            interleave,sequential_composition,exception,timeout,interrupt,guard,rep_generalised_parallel,
            rep_alphabetised_parallel,rep_interleave,rep_internal_choice,rep_external_choice, replicated,
            rep_sequential_composition, rep_linked_parallel, lambda_pattern,
            rep_synchronising_parallel, let_within, if_then, linked_parallel, synchronising_interrupt,
            synchronising_external_choice)
