import re

corner_map = {
    '┌': 'open', '┬': 'open', '┐': 'open',
    '├': 'split', '┼': 'split', '┤': 'split',
    '└': 'close', '┴': 'close', '┘': 'close',
}

def parse_box_drawing_chunk(text):
    """
    Parse a chunk of text containing multiple box-drawing 'forms'.
    Return a list of top-level forms (each is a nested Python list).
    """
    lines = text.splitlines()
    
    # stack[0] = the root: a list of all top-level forms
    # deeper indices hold nested sub-lists for nested corners
    stack = [[]]  # root = a list containing 0..N top-level forms

    def current_list():
        return stack[-1]

    for line in lines:
        line = line.rstrip()
        
        # Separate box art from payload
        match = re.match(r'^([\u2500-\u257F\s]*)(.*)$', line)
        if match:
            box_part, token_part = match.groups()
            token_part = token_part.strip()
        else:
            box_part, token_part = "", line.strip()
        
        # Extract all corners in left-to-right order
        # e.g. "└─┴─┴─┴─┴─" might yield ['└', '┴', '┴', '┴', '┴']
        corners = re.findall(r'[┌┬┐├┼┤└┴┘]', box_part)
        
        # Process each corner
        for corner in corners:
            ctype = corner_map.get(corner)
            if ctype == 'open':
                # Open a new nested list
                new_list = []
                current_list().append(new_list)
                stack.append(new_list)
            elif ctype == 'split':
                # Close the current list, then open a sibling at same level
                if len(stack) > 1:
                    stack.pop()
                sibling = []
                current_list().append(sibling)
                stack.append(sibling)
            elif ctype == 'close':
                # Close the current list (pop once)
                if len(stack) > 1:
                    stack.pop()
            # else: unknown corner, ignore or handle error

        # Add tokens (if any) to the *current* list
        if token_part:
            current_list().extend(token_part.split())

    # At the end, if something didn’t close, pop back to root
    while len(stack) > 1:
        stack.pop()

    # stack[0] is now a list of top-level forms
    return stack[0]
