from memory_ai import extract_memory


def update_long_term_memory(user_input, long_term_memory):
    new_memory = extract_memory(user_input)

    if "facts" not in long_term_memory:
        long_term_memory["facts"] = []

    for fact in new_memory.get("facts", []):
        if fact not in long_term_memory["facts"]:
            long_term_memory["facts"].append(fact)

    return long_term_memory