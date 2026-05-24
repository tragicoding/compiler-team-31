#!/usr/bin/env python3
import sys

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

    print("입력 토큰 목록:")
    for token, line_no in tokens:
        print(f"{token} (line {line_no})")


if __name__ == "__main__":
    main()