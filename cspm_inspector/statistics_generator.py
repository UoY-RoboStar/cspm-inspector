def perform_analysis(entry:str) -> tuple[
    int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]:

    prefix = entry.count("->", 0, len(entry))

    hide = entry.count("\\{", 0, len(entry))

    rename =  entry.count("[[", 0, len(entry))

    project =  entry.count("|\\", 0, len(entry))

    internal_choice =  entry.count(") |~|", 0, len(entry))

    external_choice =  entry.count(") []", 0, len(entry))

    generalised_parallel =  entry.count(") [|", 0, len(entry))

    alphabetised_parallel =  entry.count(") [ ", 0, len(entry))

    interleave =  entry.count(") |||", 0, len(entry))

    sequential_composition =  entry.count(";", 0, len(entry))

    exception =  entry.count("|>", 0, len(entry))

    timeout =  entry.count("[>", 0, len(entry))

    interrupt =  entry.count("/\\", 0, len(entry))

    guard =  entry.count("&", 0, len(entry))

    rep_interleave = entry.count("= ||| ", 0, len(entry))

    rep_external_choice = entry.count("= [] ", 0, len(entry))

    rep_internal_choice = entry.count("= |~| ", 0, len(entry))

    rep_generalised_parallel = entry.count("= [|", 0, len(entry))

    rep_alphabetised_parallel = entry.count("= || ", 0, len(entry))

    replicated = entry.count("@", 0, len(entry))


    return (prefix,hide,rename,project,internal_choice,external_choice,generalised_parallel,alphabetised_parallel,
            interleave,sequential_composition,exception,timeout,interrupt,guard,rep_generalised_parallel,
            rep_alphabetised_parallel,rep_interleave,rep_internal_choice,rep_external_choice, replicated)
