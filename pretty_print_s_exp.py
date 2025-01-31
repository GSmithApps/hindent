def pretty_s_expr(ast, indent=0):
    """
    Pretty-print an s-expression stored as a nested Python list,
    correctly handling empty lists by printing ().
    """
    if not isinstance(ast, list):
        # A single token (string, number, etc.)
        return str(ast)

    # If this list is empty, represent it as "()"
    if len(ast) == 0:
        return "()"

    # Otherwise, ast is a non-empty list: print it across multiple lines.
    spacer = "  " * indent
    lines = []
    # Start with "(" on a new line
    lines.append("(")
    
    # We'll iterate over items in the list and pretty-print each, 
    # then decide whether to put them on one line or multiple lines.
    for i, item in enumerate(ast):
        line_prefix = "  " * (indent + 1)
        printed_item = pretty_s_expr(item, indent + 1)
        
        if i == len(ast) - 1:
            # Last item in the list
            if isinstance(item, list):
                # If the last item is a sub-list, put it on its own line,
                # then close the parenthesis
                lines.append(line_prefix + printed_item + ")")
            else:
                # If it's a single token, we can close on the same line
                lines[-1] += " " + printed_item + ")"
        else:
            # Not the last item, just put it on its own line
            lines.append(line_prefix + printed_item)

    return "\n".join(lines)
