# =========================
# grammar.py
# =========================
# SLR 파서에서 사용하는 문법 상수를 정의한다.
# - TERMINALS   : 터미널 심볼 목록 (SLR table 헤더 순서와 일치해야 함)
# - NON_TERMINALS: 논터미널 심볼 목록 (SLR table 헤더 순서와 일치해야 함)
# - PRODUCTIONS  : 생성 규칙 번호 → (LHS, RHS) 매핑
#                  번호는 slr_parsing_table.txt의 reduce 번호와 정확히 일치해야 함
# =========================

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

# Format: rule_number: (LHS, RHS)
# RHS가 빈 리스트 []이면 epsilon production.
PRODUCTIONS = {
    0: ("S", ["CODE"]),

    1: ("CODE", ["VDECL", "CODE"]),
    2: ("CODE", ["FDECL", "CODE"]),
    3: ("CODE", ["CDECL", "CODE"]),
    4: ("CODE", []),

    5: ("VDECL", ["vtype", "id", "semi"]),
    6: ("VDECL", ["vtype", "ASSIGN", "semi"]),

    7: ("ASSIGN", ["id", "assign", "RHS"]),

    8:  ("RHS", ["EXPR"]),
    9:  ("RHS", ["literal"]),
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
