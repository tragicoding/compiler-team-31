# =============================================================================
# grammar.py
#
# SLR 파서에서 사용하는 문법 상수를 정의한다.
#
# 포함 내용:
#   - TERMINALS    : 터미널 심볼 목록
#   - NON_TERMINALS: 논터미널 심볼 목록
#   - PRODUCTIONS  : 생성 규칙 번호 → (LHS, RHS) 매핑
#
# 주의:
#   TERMINALS + NON_TERMINALS의 순서는 slr_parsing_table.txt의
#   LR table 헤더 열 순서와 반드시 일치해야 한다.
#   PRODUCTIONS의 번호는 SLR table의 reduce 번호(rN)와 일치해야 한다.
# =============================================================================


# -----------------------------------------------------------------------------
# 터미널 심볼 목록
#
# SLR table의 ACTION 열 순서와 동일하게 정의한다.
# "$"는 입력의 끝을 나타내는 end marker로, 파서가 자동으로 추가한다.
# -----------------------------------------------------------------------------
TERMINALS = [
    "vtype",     # 변수/함수 타입 키워드 (int, boolean 등)
    "id",        # 변수/함수 식별자
    "semi",      # 세미콜론 ;
    "assign",    # 대입 연산자 =
    "literal",   # 문자열 리터럴 "..."
    "character", # 문자 리터럴 '.'
    "boolstr",   # 불린 값 (true / false)
    "addsub",    # 덧셈/뺄셈 연산자 + -
    "multdiv",   # 곱셈/나눗셈 연산자 * /
    "lparen",    # 여는 소괄호 (
    "rparen",    # 닫는 소괄호 )
    "num",       # 정수 숫자 리터럴
    "lbrace",    # 여는 중괄호 {
    "rbrace",    # 닫는 중괄호 }
    "comma",     # 쉼표 ,
    "if",        # if 키워드
    "while",     # while 키워드
    "comp",      # 비교 연산자 < > == != 등
    "else",      # else 키워드
    "return",    # return 키워드
    "class",     # class 키워드
    "$"          # 입력 끝 표시자 (end marker)
]

# -----------------------------------------------------------------------------
# 논터미널 심볼 목록
#
# SLR table의 GOTO 열 순서와 동일하게 정의한다.
# "S"는 augmented start symbol로, SLR 생성 과정에서 추가된다.
# -----------------------------------------------------------------------------
NON_TERMINALS = [
    "S",         # augmented start symbol (S → CODE)
    "CODE",      # 전체 프로그램 (변수/함수/클래스 선언의 나열)
    "VDECL",     # 변수 선언
    "ASSIGN",    # 대입식
    "RHS",       # 대입 우변 (EXPR | literal | character | boolstr)
    "EXPR",      # 산술식
    "EXPRTAIL",  # 산술식 꼬리 (addsub 이후 재귀)
    "TERM",      # 항 (곱셈/나눗셈 단위)
    "TERMTAIL",  # 항 꼬리 (multdiv 이후 재귀)
    "FACTOR",    # 인수 (id | num | 괄호 식)
    "FDECL",     # 함수 선언
    "ARG",       # 함수 첫 번째 인자
    "MOREARGS",  # 추가 인자 목록 (콤마로 구분)
    "BLOCK",     # 문장 블록 (STMT의 나열)
    "STMT",      # 단일 문장
    "COND",      # 조건식
    "CONDTAIL",  # 조건식 꼬리 (comp 이후)
    "ELSE",      # else 절 (선택적)
    "RETURN",    # return 문
    "CDECL",     # 클래스 선언
    "ODECL"      # 클래스 멤버 선언 목록
]

# -----------------------------------------------------------------------------
# 생성 규칙 (Production Rules)
#
# 형식: rule_number: (LHS, RHS)
#   - LHS : 좌변 논터미널 심볼 (문자열)
#   - RHS : 우변 심볼 목록 (리스트). 빈 리스트 []는 epsilon(ε)을 의미한다.
#
# 번호는 slr_parsing_table.txt의 reduce 액션 번호와 정확히 대응한다.
# 예) 파서가 "r5"를 읽으면 PRODUCTIONS[5]의 규칙으로 reduce한다.
#
# Rule 0 (S → CODE)은 augmented production으로, accept 시 직접 사용되지 않는다.
# -----------------------------------------------------------------------------
PRODUCTIONS = {
    # ── Augmented Start ──────────────────────────────────
    0:  ("S",        ["CODE"]),

    # ── CODE : 프로그램 최상위 선언 나열 ─────────────────
    1:  ("CODE",     ["VDECL", "CODE"]),       # 변수 선언 후 계속
    2:  ("CODE",     ["FDECL", "CODE"]),       # 함수 선언 후 계속
    3:  ("CODE",     ["CDECL", "CODE"]),       # 클래스 선언 후 계속
    4:  ("CODE",     []),                      # ε (선언 없음)

    # ── VDECL : 변수 선언 ────────────────────────────────
    5:  ("VDECL",    ["vtype", "id", "semi"]),          # int x;
    6:  ("VDECL",    ["vtype", "ASSIGN", "semi"]),      # int x = ...;

    # ── ASSIGN : 대입식 ──────────────────────────────────
    7:  ("ASSIGN",   ["id", "assign", "RHS"]),          # x = RHS

    # ── RHS : 대입 우변 ──────────────────────────────────
    8:  ("RHS",      ["EXPR"]),        # 산술식
    9:  ("RHS",      ["literal"]),     # 문자열 리터럴
    10: ("RHS",      ["character"]),   # 문자 리터럴
    11: ("RHS",      ["boolstr"]),     # 불린 값

    # ── EXPR / EXPRTAIL : 덧셈·뺄셈 수준 산술식 ─────────
    # 원본 좌재귀·모호 문법을 우재귀·비모호 문법으로 변환
    # 원본: EXPR → EXPR addsub EXPR | EXPR multdiv EXPR | lparen EXPR rparen | id | num
    12: ("EXPR",     ["TERM", "EXPRTAIL"]),
    13: ("EXPRTAIL", ["addsub", "TERM", "EXPRTAIL"]),  # + 또는 - 이후 재귀
    14: ("EXPRTAIL", []),                              # ε

    # ── TERM / TERMTAIL : 곱셈·나눗셈 수준 (addsub보다 높은 우선순위) ──
    15: ("TERM",     ["FACTOR", "TERMTAIL"]),
    16: ("TERMTAIL", ["multdiv", "FACTOR", "TERMTAIL"]),  # * 또는 / 이후 재귀
    17: ("TERMTAIL", []),                                 # ε

    # ── FACTOR : 최소 단위 인수 ──────────────────────────
    18: ("FACTOR",   ["lparen", "EXPR", "rparen"]),  # ( EXPR )
    19: ("FACTOR",   ["id"]),                        # 변수
    20: ("FACTOR",   ["num"]),                       # 정수 리터럴

    # ── FDECL : 함수 선언 ────────────────────────────────
    21: ("FDECL",    ["vtype", "id", "lparen", "ARG", "rparen",
                      "lbrace", "BLOCK", "RETURN", "rbrace"]),

    # ── ARG / MOREARGS : 함수 인자 목록 ─────────────────
    22: ("ARG",      ["vtype", "id", "MOREARGS"]),         # 첫 번째 인자
    23: ("ARG",      []),                                  # ε (인자 없음)
    24: ("MOREARGS", ["comma", "vtype", "id", "MOREARGS"]),# 추가 인자
    25: ("MOREARGS", []),                                  # ε

    # ── BLOCK / STMT : 함수/제어문 내부 문장 ─────────────
    26: ("BLOCK",    ["STMT", "BLOCK"]),   # 문장 + 이후 블록
    27: ("BLOCK",    []),                  # ε (빈 블록)
    28: ("STMT",     ["VDECL"]),           # 변수 선언문
    29: ("STMT",     ["ASSIGN", "semi"]),  # 대입문
    30: ("STMT",     ["if", "lparen", "COND", "rparen",
                      "lbrace", "BLOCK", "rbrace", "ELSE"]),  # if(-else)문
    31: ("STMT",     ["while", "lparen", "COND", "rparen",
                      "lbrace", "BLOCK", "rbrace"]),           # while문

    # ── COND / CONDTAIL : 조건식 ─────────────────────────
    # 원본 좌재귀·모호 문법 변환: COND → COND comp COND | boolstr
    32: ("COND",     ["boolstr", "CONDTAIL"]),
    33: ("CONDTAIL", ["comp", "boolstr"]),  # 비교 연산자 + 우변
    34: ("CONDTAIL", []),                   # ε (단순 boolstr)

    # ── ELSE : else 절 (선택적) ──────────────────────────
    35: ("ELSE",     ["else", "lbrace", "BLOCK", "rbrace"]),  # else { ... }
    36: ("ELSE",     []),                                      # ε

    # ── RETURN : return 문 ───────────────────────────────
    37: ("RETURN",   ["return", "RHS", "semi"]),  # return RHS;

    # ── CDECL / ODECL : 클래스 선언 ─────────────────────
    38: ("CDECL",    ["class", "id", "lbrace", "ODECL", "rbrace"]),
    39: ("ODECL",    ["VDECL", "ODECL"]),   # 멤버 변수 후 계속
    40: ("ODECL",    ["FDECL", "ODECL"]),   # 멤버 함수 후 계속
    41: ("ODECL",    []),                   # ε (멤버 없음)
}
