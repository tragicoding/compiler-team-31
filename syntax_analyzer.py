#!/usr/bin/env python3
import sys

TERMINALS = [
    "vtype", "id", "semi", "assign", "literal", "character", "boolstr",
    "addsub", "multdiv", "lparen", "rparen", "num",
    "lbrace", "rbrace", "comma", "if", "while", "comp",
    "else", "return", "class", "$"
]

NON_TERMINALS = [
    "S", "CODE", "VDECL", "ASSIGN", "RHS", "EXPR", "EXPRTAIL",
    "TERM", "TERMTAIL", "FACTOR", "FDECL", "ARG", "MOREARGS",
    "BLOCK", "STMT", "COND", "CONDTAIL", "ELSE", "RETURN",
    "CDECL", "ODECL"
]

# =========================
# Production Rules
# =========================
# Format:
# rule_number: (LHS, RHS)
#
# Empty RHS [] means epsilon production.

PRODUCTIONS = {
    0: ("S", ["CODE"]),

    1: ("CODE", ["VDECL", "CODE"]),
    2: ("CODE", ["FDECL", "CODE"]),
    3: ("CODE", ["CDECL", "CODE"]),
    4: ("CODE", []),

    5: ("VDECL", ["vtype", "id", "semi"]),
    6: ("VDECL", ["vtype", "ASSIGN", "semi"]),

    7: ("ASSIGN", ["id", "assign", "RHS"]),

    8: ("RHS", ["EXPR"]),
    9: ("RHS", ["literal"]),
    10: ("RHS", ["character"]),
    11: ("RHS", ["boolstr"]),

    12: ("EXPR", ["TERM", "EXPRTAIL"]),
    13: ("EXPRTAIL", ["addsub", "TERM", "EXPRTAIL"]),
    14: ("EXPRTAIL", []),

    15: ("TERM", ["FACTOR", "TERMTAIL"]),
    16: ("TERMTAIL", ["multdiv", "FACTOR", "TERMTAIL"]),
    17: ("TERMTAIL", []),

    18: ("FACTOR", ["lparen", "EXPR", "rparen"]),
    19: ("FACTOR", ["id"]),
    20: ("FACTOR", ["num"]),

    21: ("FDECL", ["vtype", "id", "lparen", "ARG", "rparen", "lbrace", "BLOCK", "RETURN", "rbrace"]),

    22: ("ARG", ["vtype", "id", "MOREARGS"]),
    23: ("ARG", []),

    24: ("MOREARGS", ["comma", "vtype", "id", "MOREARGS"]),
    25: ("MOREARGS", []),

    26: ("BLOCK", ["STMT", "BLOCK"]),
    27: ("BLOCK", []),

    28: ("STMT", ["VDECL"]),
    29: ("STMT", ["ASSIGN", "semi"]),
    30: ("STMT", ["if", "lparen", "COND", "rparen", "lbrace", "BLOCK", "rbrace", "ELSE"]),
    31: ("STMT", ["while", "lparen", "COND", "rparen", "lbrace", "BLOCK", "rbrace"]),

    32: ("COND", ["boolstr", "CONDTAIL"]),
    33: ("CONDTAIL", ["comp", "boolstr"]),
    34: ("CONDTAIL", []),

    35: ("ELSE", ["else", "lbrace", "BLOCK", "rbrace"]),
    36: ("ELSE", []),

    37: ("RETURN", ["return", "RHS", "semi"]),

    38: ("CDECL", ["class", "id", "lbrace", "ODECL", "rbrace"]),

    39: ("ODECL", ["VDECL", "ODECL"]),
    40: ("ODECL", ["FDECL", "ODECL"]),
    41: ("ODECL", []),
}


# =========================
# ACTION / GOTO Tables
# =========================
# These tables will be filled based on the generated SLR parsing table.

ACTION = {
}

GOTO = {
}


# =========================
# Parse Tree Node
# =========================

class Node:
    """
    Parse tree node.
    Each node stores a grammar symbol and its child nodes.
    """

    def __init__(self, symbol, children=None):
        self.symbol = symbol
        self.children = children or []


def print_tree(node, prefix="", is_last=True):
    """
    Print parse tree in a readable tree structure.
    """
    connector = "└── " if is_last else "├── "
    print(prefix + connector + node.symbol)

    child_prefix = prefix + ("    " if is_last else "│   ")

    for index, child in enumerate(node.children):
        is_last_child = index == len(node.children) - 1
        print_tree(child, child_prefix, is_last_child)

def read_tokens(filename):
    """
    입력 파일에서 terminal token sequence를 읽는다.
    각 token은 공백 또는 줄바꿈으로 구분된다.
    오류 보고를 위해 각 token의 line number도 함께 저장한다.
    """
    tokens = []
    last_line_no = 1

    with open(filename, "r", encoding="utf-8") as file:
        for line_no, line in enumerate(file, start=1):
            last_line_no = line_no

            for token in line.split():
                tokens.append((token, line_no))

    # SLR parser의 입력 끝을 표시하기 위한 end marker
    tokens.append(("$", last_line_no))

    return tokens

def load_slr_table(filename="grammar/slr_parsing_table.txt"):
    """
    Read the LR table copied from the SLR table generation website,
    and convert it into ACTION and GOTO dictionaries.

    ACTION[state][terminal] = "sN" / "rN" / "acc"
    GOTO[state][non_terminal] = next_state
    """
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()

    lr_index = content.rfind("LR table")
    if lr_index == -1:
        raise ValueError("LR table section not found in slr_parsing_table.txt")

    lr_content = content[lr_index:]

    # Remove website test input section if it exists
    if "Input (tokens):" in lr_content:
        lr_content = lr_content.split("Input (tokens):")[0]

    lines = [line for line in lr_content.splitlines() if line.strip()]

    header_line_index = None
    for i, line in enumerate(lines):
        if line.startswith("vtype\tid\tsemi"):
            header_line_index = i
            break

    if header_line_index is None:
        raise ValueError("LR table header line not found.")

    headers = lines[header_line_index].split("\t")

    expected_headers = TERMINALS + NON_TERMINALS
    if headers != expected_headers:
        raise ValueError(
            "LR table headers do not match expected terminals/non-terminals.\n"
            f"Expected: {expected_headers}\n"
            f"Found: {headers}"
        )

    action_table = {}
    goto_table = {}

    for line in lines[header_line_index + 1:]:
        parts = line.split("\t")

        if not parts[0].isdigit():
            continue

        state = int(parts[0])
        cells = parts[1:]

        # If a row is shorter due to copy/paste formatting, skip it
        if len(cells) < len(headers):
            continue

        action_table[state] = {}
        goto_table[state] = {}

        for index, symbol in enumerate(headers):
            value = cells[index].strip()

            if value == "":
                continue

            if symbol in TERMINALS:
                action_table[state][symbol] = value
            else:
                try:
                    goto_table[state][symbol] = int(value)
                except ValueError:
                    # Ignore invalid GOTO values
                    pass

    return action_table, goto_table

def parse(tokens, action_table, goto_table):
    """
    Perform SLR shift-reduce parsing.

    tokens: list of (token, line_no)
    action_table: ACTION table generated from LR table
    goto_table: GOTO table generated from LR table
    """
    state_stack = [0]
    symbol_stack = []
    node_stack = []

    input_index = 0

    while True:
        current_state = state_stack[-1]
        current_token, current_line = tokens[input_index]

        action = action_table.get(current_state, {}).get(current_token)

        if action is None:
            expected_tokens = sorted(action_table.get(current_state, {}).keys())

            print("REJECT")
            print()
            print("Syntax Error:")
            print(f"Line: {current_line}")
            print(f"Unexpected token: {current_token}")
            print(f"Expected one of: {', '.join(expected_tokens) if expected_tokens else 'None'}")
            return False, None

        # Accept
        if action == "acc":
            print("ACCEPT")
            print()
            print("Parse Tree:")

            if node_stack:
                print_tree(node_stack[-1])
            else:
                print("No parse tree generated.")

            return True, node_stack[-1] if node_stack else None

        # Shift
        if action.startswith("s"):
            next_state = int(action[1:])

            symbol_stack.append(current_token)
            state_stack.append(next_state)
            node_stack.append(Node(current_token))

            input_index += 1

        # Reduce
        elif action.startswith("r"):
            rule_number = int(action[1:])
            lhs, rhs = PRODUCTIONS[rule_number]

            children = []

            if len(rhs) == 0:
                # epsilon production
                children.append(Node("ε"))
            else:
                for _ in rhs:
                    state_stack.pop()
                    symbol_stack.pop()
                    children.insert(0, node_stack.pop())

            new_node = Node(lhs, children)
            node_stack.append(new_node)
            symbol_stack.append(lhs)

            goto_state = goto_table.get(state_stack[-1], {}).get(lhs)

            if goto_state is None:
                print("REJECT")
                print()
                print("Goto Error:")
                print(f"No GOTO entry for state {state_stack[-1]} and symbol {lhs}")
                return False, None

            state_stack.append(goto_state)

        else:
            print("REJECT")
            print()
            print(f"Invalid action: {action}")
            return False, None


def main():
    if len(sys.argv) != 2:
        print("사용법: python3 syntax_analyzer.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        tokens = read_tokens(input_file)
    except FileNotFoundError:
        print(f"오류: 입력 파일을 찾을 수 없습니다: {input_file}")
        sys.exit(1)

    try:
        action_table, goto_table = load_slr_table()
    except Exception as error:
        print(f"SLR table 로드 오류: {error}")
        sys.exit(1)

    parse(tokens, action_table, goto_table)


if __name__ == "__main__":
    main()