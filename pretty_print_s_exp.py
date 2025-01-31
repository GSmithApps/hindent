def pretty_s_expr(ast, indent=0):
    """
    Pretty-print an s-expression stored as a nested Python list.
    Empty lists become "()".
    """
    if not isinstance(ast, list):
        # Token
        return str(ast)

    # Empty list => "()"
    if len(ast) == 0:
        return "()"

    lines = []
    lines.append("(")
    
    for i, item in enumerate(ast):
        line_prefix = "  " * (indent + 1)
        printed_item = pretty_s_expr(item, indent + 1)

        if i == len(ast) - 1:  
            # Last in the list
            if isinstance(item, list):
                lines.append(line_prefix + printed_item + ")")
            else:
                # attach the token + closing paren to the same line
                lines[-1] += " " + printed_item + ")"
        else:
            lines.append(line_prefix + printed_item)

    return "\n".join(lines)
