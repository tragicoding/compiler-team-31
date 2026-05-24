# Test Cases

| 번호 | 테스트 내용 | 입력 파일 | 예상 결과 |
| --- | --- | --- | --- |
| 1 | 변수 선언 | `01_variable_declaration.txt` | ACCEPT |
| 2 | 변수 초기화 | `02_variable_initialization.txt` | ACCEPT |
| 3 | 산술식 포함 변수 초기화 | `03_expression.txt` | ACCEPT |
| 4 | 함수 선언 | `04_function_declaration.txt` | ACCEPT |
| 5 | 인자가 있는 함수 선언 | `05_function_with_argument.txt` | ACCEPT |
| 6 | if-else 문 | `06_if_else.txt` | ACCEPT |
| 7 | while 문 | `07_while.txt` | ACCEPT |
| 8 | class 선언 | `08_class_declaration.txt` | ACCEPT |
| 9 | 세미콜론 누락 | `09_reject_missing_semi.txt` | REJECT |
| 10 | 비교 연산 조건식 | `10_condition_comp.txt` | ACCEPT |
| 11 | literal RHS 대입 | `11_rhs_literal.txt` | ACCEPT |
| 12 | character RHS 대입 | `12_rhs_character.txt` | ACCEPT |
| 13 | boolstr RHS 대입 | `13_rhs_boolstr.txt` | ACCEPT |
| 14 | 여러 개의 함수 인자 선언 | `14_multi_args.txt` | ACCEPT |
| 15 | 괄호가 포함된 산술식 | `15_paren_expr.txt` | ACCEPT |
| 16 | 함수 블록 내부의 변수 선언 및 대입문 | `16_stmt_in_block.txt` | ACCEPT |
| 17 | class 내부 함수 선언 | `17_class_with_method.txt` | ACCEPT |
| 18 | 잘못된 토큰 (vtype 뒤 semi) | `18_reject_wrong_token.txt` | REJECT |
| 19 | 닫는 중괄호 누락 | `19_reject_missing_rbrace.txt` | REJECT |
| 20 | 최상위 레벨 대입문 | `20_reject_assign_at_top.txt` | REJECT |
| 21 | 연산자 연속 사용 | `21_reject_double_operator.txt` | REJECT |

---

### `01_variable_declaration.txt`

```
입력 : vtype id semi

출력 :
ACCEPT

Parse Tree:
└── CODE
    ├── VDECL
    │   ├── vtype
    │   ├── id
    │   └── semi
    └── CODE
        └── ε
```

### `02_variable_initialization.txt`

```
입력 : vtype id assign num semi

출력 :
ACCEPT

Parse Tree:
└── CODE
    ├── VDECL
    │   ├── vtype
    │   ├── ASSIGN
    │   │   ├── id
    │   │   ├── assign
    │   │   └── RHS
    │   │       └── EXPR
    │   │           ├── TERM
    │   │           │   ├── FACTOR
    │   │           │   │   └── num
    │   │           │   └── TERMTAIL
    │   │           │       └── ε
    │   │           └── EXPRTAIL
    │   │               └── ε
    │   └── semi
    └── CODE
        └── ε
```

### `03_expression.txt`

```
입력 : vtype id assign id addsub num multdiv id semi

출력 :
ACCEPT

Parse Tree:
└── CODE
    ├── VDECL
    │   ├── vtype
    │   ├── ASSIGN
    │   │   ├── id
    │   │   ├── assign
    │   │   └── RHS
    │   │       └── EXPR
    │   │           ├── TERM
    │   │           │   ├── FACTOR
    │   │           │   │   └── id
    │   │           │   └── TERMTAIL
    │   │           │       └── ε
    │   │           └── EXPRTAIL
    │   │               ├── addsub
    │   │               ├── TERM
    │   │               │   ├── FACTOR
    │   │               │   │   └── num
    │   │               │   └── TERMTAIL
    │   │               │       ├── multdiv
    │   │               │       ├── FACTOR
    │   │               │       │   └── id
    │   │               │       └── TERMTAIL
    │   │               │           └── ε
    │   │               └── EXPRTAIL
    │   │                   └── ε
    │   └── semi
    └── CODE
        └── ε
```

### `04_function_declaration.txt`

```
입력 : vtype id lparen rparen lbrace return num semi rbrace

출력 :
ACCEPT

Parse Tree:
└── CODE
    ├── FDECL
    │   ├── vtype
    │   ├── id
    │   ├── lparen
    │   ├── ARG
    │   │   └── ε
    │   ├── rparen
    │   ├── lbrace
    │   ├── BLOCK
    │   │   └── ε
    │   ├── RETURN
    │   │   ├── return
    │   │   ├── RHS
    │   │   │   └── EXPR
    │   │   │       ├── TERM
    │   │   │       │   ├── FACTOR
    │   │   │       │   │   └── num
    │   │   │       │   └── TERMTAIL
    │   │   │       │       └── ε
    │   │   │       └── EXPRTAIL
    │   │   │           └── ε
    │   │   └── semi
    │   └── rbrace
    └── CODE
        └── ε
```

### `05_function_with_argument.txt`

```
입력 : vtype id lparen vtype id rparen lbrace return id semi rbrace

출력 :
ACCEPT

Parse Tree:
└── CODE
    ├── FDECL
    │   ├── vtype
    │   ├── id
    │   ├── lparen
    │   ├── ARG
    │   │   ├── vtype
    │   │   ├── id
    │   │   └── MOREARGS
    │   │       └── ε
    │   ├── rparen
    │   ├── lbrace
    │   ├── BLOCK
    │   │   └── ε
    │   ├── RETURN
    │   │   ├── return
    │   │   ├── RHS
    │   │   │   └── EXPR
    │   │   │       ├── TERM
    │   │   │       │   ├── FACTOR
    │   │   │       │   │   └── id
    │   │   │       │   └── TERMTAIL
    │   │   │       │       └── ε
    │   │   │       └── EXPRTAIL
    │   │   │           └── ε
    │   │   └── semi
    │   └── rbrace
    └── CODE
        └── ε
```

### `06_if_else.txt`

```
입력 : vtype id lparen rparen lbrace
if lparen boolstr rparen lbrace rbrace else lbrace rbrace
return num semi
rbrace

출력 :
ACCEPT

Parse Tree:
└── CODE
    ├── FDECL
    │   ├── vtype
    │   ├── id
    │   ├── lparen
    │   ├── ARG
    │   │   └── ε
    │   ├── rparen
    │   ├── lbrace
    │   ├── BLOCK
    │   │   ├── STMT
    │   │   │   ├── if
    │   │   │   ├── lparen
    │   │   │   ├── COND
    │   │   │   │   ├── boolstr
    │   │   │   │   └── CONDTAIL
    │   │   │   │       └── ε
    │   │   │   ├── rparen
    │   │   │   ├── lbrace
    │   │   │   ├── BLOCK
    │   │   │   │   └── ε
    │   │   │   ├── rbrace
    │   │   │   └── ELSE
    │   │   │       ├── else
    │   │   │       ├── lbrace
    │   │   │       ├── BLOCK
    │   │   │       │   └── ε
    │   │   │       └── rbrace
    │   │   └── BLOCK
    │   │       └── ε
    │   ├── RETURN
    │   │   ├── return
    │   │   ├── RHS
    │   │   │   └── EXPR
    │   │   │       ├── TERM
    │   │   │       │   ├── FACTOR
    │   │   │       │   │   └── num
    │   │   │       │   └── TERMTAIL
    │   │   │       │       └── ε
    │   │   │       └── EXPRTAIL
    │   │   │           └── ε
    │   │   └── semi
    │   └── rbrace
    └── CODE
        └── ε
```

### `07_while.txt`

```
입력 : vtype id lparen rparen lbrace
while lparen boolstr rparen lbrace rbrace
return num semi
rbrace

출력 :
ACCEPT

Parse Tree:
└── CODE
    ├── FDECL
    │   ├── vtype
    │   ├── id
    │   ├── lparen
    │   ├── ARG
    │   │   └── ε
    │   ├── rparen
    │   ├── lbrace
    │   ├── BLOCK
    │   │   ├── STMT
    │   │   │   ├── while
    │   │   │   ├── lparen
    │   │   │   ├── COND
    │   │   │   │   ├── boolstr
    │   │   │   │   └── CONDTAIL
    │   │   │   │       └── ε
    │   │   │   ├── rparen
    │   │   │   ├── lbrace
    │   │   │   ├── BLOCK
    │   │   │   │   └── ε
    │   │   │   └── rbrace
    │   │   └── BLOCK
    │   │       └── ε
    │   ├── RETURN
    │   │   ├── return
    │   │   ├── RHS
    │   │   │   └── EXPR
    │   │   │       ├── TERM
    │   │   │       │   ├── FACTOR
    │   │   │       │   │   └── num
    │   │   │       │   └── TERMTAIL
    │   │   │       │       └── ε
    │   │   │       └── EXPRTAIL
    │   │   │           └── ε
    │   │   └── semi
    │   └── rbrace
    └── CODE
        └── ε
```

### `08_class_declaration.txt`

```
입력 : class id lbrace vtype id semi rbrace

출력 :
ACCEPT

Parse Tree:
└── CODE
    ├── CDECL
    │   ├── class
    │   ├── id
    │   ├── lbrace
    │   ├── ODECL
    │   │   ├── VDECL
    │   │   │   ├── vtype
    │   │   │   ├── id
    │   │   │   └── semi
    │   │   └── ODECL
    │   │       └── ε
    │   └── rbrace
    └── CODE
        └── ε
```

### `09_reject_missing_semi.txt`

```
입력 : vtype id

출력 :
REJECT

Syntax Error:
Line: 1
Unexpected token: $
Expected one of: assign, lparen, semi
```

### `10_condition_comp.txt`

```
입력 : vtype id lparen rparen lbrace
if lparen boolstr comp boolstr rparen lbrace rbrace else lbrace rbrace
return num semi
rbrace

출력 :
ACCEPT

Parse Tree:
└── CODE
    ├── FDECL
    │   ├── vtype
    │   ├── id
    │   ├── lparen
    │   ├── ARG
    │   │   └── ε
    │   ├── rparen
    │   ├── lbrace
    │   ├── BLOCK
    │   │   ├── STMT
    │   │   │   ├── if
    │   │   │   ├── lparen
    │   │   │   ├── COND
    │   │   │   │   ├── boolstr
    │   │   │   │   └── CONDTAIL
    │   │   │   │       ├── comp
    │   │   │   │       └── boolstr
    │   │   │   ├── rparen
    │   │   │   ├── lbrace
    │   │   │   ├── BLOCK
    │   │   │   │   └── ε
    │   │   │   ├── rbrace
    │   │   │   └── ELSE
    │   │   │       ├── else
    │   │   │       ├── lbrace
    │   │   │       ├── BLOCK
    │   │   │       │   └── ε
    │   │   │       └── rbrace
    │   │   └── BLOCK
    │   │       └── ε
    │   ├── RETURN
    │   │   ├── return
    │   │   ├── RHS
    │   │   │   └── EXPR
    │   │   │       ├── TERM
    │   │   │       │   ├── FACTOR
    │   │   │       │   │   └── num
    │   │   │       │   └── TERMTAIL
    │   │   │       │       └── ε
    │   │   │       └── EXPRTAIL
    │   │   │           └── ε
    │   │   └── semi
    │   └── rbrace
    └── CODE
        └── ε
```

### `11_rhs_literal.txt`

```
입력 : vtype id assign literal semi

출력 :
ACCEPT

Parse Tree:
└── CODE
    ├── VDECL
    │   ├── vtype
    │   ├── ASSIGN
    │   │   ├── id
    │   │   ├── assign
    │   │   └── RHS
    │   │       └── literal
    │   └── semi
    └── CODE
        └── ε
```

### `12_rhs_character.txt`

```
입력 : vtype id assign character semi

출력 :
ACCEPT

Parse Tree:
└── CODE
    ├── VDECL
    │   ├── vtype
    │   ├── ASSIGN
    │   │   ├── id
    │   │   ├── assign
    │   │   └── RHS
    │   │       └── character
    │   └── semi
    └── CODE
        └── ε
```

### `13_rhs_boolstr.txt`

```
입력 : vtype id assign boolstr semi

출력 :
ACCEPT

Parse Tree:
└── CODE
    ├── VDECL
    │   ├── vtype
    │   ├── ASSIGN
    │   │   ├── id
    │   │   ├── assign
    │   │   └── RHS
    │   │       └── boolstr
    │   └── semi
    └── CODE
        └── ε
```

### `14_multi_args.txt`

```
입력 : vtype id lparen vtype id comma vtype id comma vtype id rparen lbrace return num semi rbrace

출력 :
ACCEPT

Parse Tree:
└── CODE
    ├── FDECL
    │   ├── vtype
    │   ├── id
    │   ├── lparen
    │   ├── ARG
    │   │   ├── vtype
    │   │   ├── id
    │   │   └── MOREARGS
    │   │       ├── comma
    │   │       ├── vtype
    │   │       ├── id
    │   │       └── MOREARGS
    │   │           ├── comma
    │   │           ├── vtype
    │   │           ├── id
    │   │           └── MOREARGS
    │   │               └── ε
    │   ├── rparen
    │   ├── lbrace
    │   ├── BLOCK
    │   │   └── ε
    │   ├── RETURN
    │   │   ├── return
    │   │   ├── RHS
    │   │   │   └── EXPR
    │   │   │       ├── TERM
    │   │   │       │   ├── FACTOR
    │   │   │       │   │   └── num
    │   │   │       │   └── TERMTAIL
    │   │   │       │       └── ε
    │   │   │       └── EXPRTAIL
    │   │   │           └── ε
    │   │   └── semi
    │   └── rbrace
    └── CODE
        └── ε
```

### `15_paren_expr.txt`

```
입력 : vtype id assign lparen id addsub num rparen semi

출력 :
ACCEPT

Parse Tree:
└── CODE
    ├── VDECL
    │   ├── vtype
    │   ├── ASSIGN
    │   │   ├── id
    │   │   ├── assign
    │   │   └── RHS
    │   │       └── EXPR
    │   │           ├── TERM
    │   │           │   ├── FACTOR
    │   │           │   │   ├── lparen
    │   │           │   │   ├── EXPR
    │   │           │   │   │   ├── TERM
    │   │           │   │   │   │   ├── FACTOR
    │   │           │   │   │   │   │   └── id
    │   │           │   │   │   │   └── TERMTAIL
    │   │           │   │   │   │       └── ε
    │   │           │   │   │   └── EXPRTAIL
    │   │           │   │   │       ├── addsub
    │   │           │   │   │       ├── TERM
    │   │           │   │   │       │   ├── FACTOR
    │   │           │   │   │       │   │   └── num
    │   │           │   │   │       │   └── TERMTAIL
    │   │           │   │   │       │       └── ε
    │   │           │   │   │       └── EXPRTAIL
    │   │           │   │   │           └── ε
    │   │           │   │   └── rparen
    │   │           │   └── TERMTAIL
    │   │           │       └── ε
    │   │           └── EXPRTAIL
    │   │               └── ε
    │   └── semi
    └── CODE
        └── ε
```

### `16_stmt_in_block.txt`

```
입력 : vtype id lparen rparen lbrace
vtype id semi
id assign num semi
return num semi
rbrace

출력 :
ACCEPT

Parse Tree:
└── CODE
    ├── FDECL
    │   ├── vtype
    │   ├── id
    │   ├── lparen
    │   ├── ARG
    │   │   └── ε
    │   ├── rparen
    │   ├── lbrace
    │   ├── BLOCK
    │   │   ├── STMT
    │   │   │   └── VDECL
    │   │   │       ├── vtype
    │   │   │       ├── id
    │   │   │       └── semi
    │   │   └── BLOCK
    │   │       ├── STMT
    │   │       │   ├── ASSIGN
    │   │       │   │   ├── id
    │   │       │   │   ├── assign
    │   │       │   │   └── RHS
    │   │       │   │       └── EXPR
    │   │       │   │           ├── TERM
    │   │       │   │           │   ├── FACTOR
    │   │       │   │           │   │   └── num
    │   │       │   │           │   └── TERMTAIL
    │   │       │   │           │       └── ε
    │   │       │   │           └── EXPRTAIL
    │   │       │   │               └── ε
    │   │       │   └── semi
    │   │       └── BLOCK
    │   │           └── ε
    │   ├── RETURN
    │   │   ├── return
    │   │   ├── RHS
    │   │   │   └── EXPR
    │   │   │       ├── TERM
    │   │   │       │   ├── FACTOR
    │   │   │       │   │   └── num
    │   │   │       │   └── TERMTAIL
    │   │   │       │       └── ε
    │   │   │       └── EXPRTAIL
    │   │   │           └── ε
    │   │   └── semi
    │   └── rbrace
    └── CODE
        └── ε
```

### `17_class_with_method.txt`

```
입력 : class id lbrace vtype id lparen rparen lbrace return num semi rbrace rbrace

출력 :
ACCEPT

Parse Tree:
└── CODE
    ├── CDECL
    │   ├── class
    │   ├── id
    │   ├── lbrace
    │   ├── ODECL
    │   │   ├── FDECL
    │   │   │   ├── vtype
    │   │   │   ├── id
    │   │   │   ├── lparen
    │   │   │   ├── ARG
    │   │   │   │   └── ε
    │   │   │   ├── rparen
    │   │   │   ├── lbrace
    │   │   │   ├── BLOCK
    │   │   │   │   └── ε
    │   │   │   ├── RETURN
    │   │   │   │   ├── return
    │   │   │   │   ├── RHS
    │   │   │   │   │   └── EXPR
    │   │   │   │   │       ├── TERM
    │   │   │   │   │       │   ├── FACTOR
    │   │   │   │   │       │   │   └── num
    │   │   │   │   │       │   └── TERMTAIL
    │   │   │   │   │       │       └── ε
    │   │   │   │   │       └── EXPRTAIL
    │   │   │   │   │           └── ε
    │   │   │   │   └── semi
    │   │   │   └── rbrace
    │   │   └── ODECL
    │   │       └── ε
    │   └── rbrace
    └── CODE
        └── ε
```

### `18_reject_wrong_token.txt`

```
입력 : vtype semi

출력 :
REJECT

Syntax Error:
Line: 1
Unexpected token: semi
Expected one of: id
```

### `19_reject_missing_rbrace.txt`

```
입력 : vtype id lparen rparen lbrace return num semi

출력 :
REJECT

Syntax Error:
Line: 1
Unexpected token: $
Expected one of: rbrace
```

### `20_reject_assign_at_top.txt`

```
입력 : id assign num semi

출력 :
REJECT

Syntax Error:
Line: 1
Unexpected token: id
Expected one of: $, class, vtype
```

### `21_reject_double_operator.txt`

```
입력 : vtype id assign num addsub addsub num semi

출력 :
REJECT

Syntax Error:
Line: 1
Unexpected token: addsub
Expected one of: id, lparen, num
```

