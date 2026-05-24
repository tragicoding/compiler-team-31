# Compiler Term Project - SLR Syntax Analyzer

## 1. 프로젝트 개요

본 프로젝트는 simplified Java programming language에 대한 bottom-up syntax analyzer를 구현하는 것을 목표로 한다.

입력은 실제 Java source code가 아니라, lexical analysis가 완료된 terminal token sequence이다.
예를 들어 `vtype id semi`와 같은 형태의 토큰 시퀀스를 입력으로 받는다.

본 syntax analyzer는 수정된 non-ambiguous CFG와 SLR parsing table을 기반으로
입력 토큰 시퀀스가 문법적으로 유효한지 검사한다.

## 2. 구현 환경

- 개발 환경: WSL Ubuntu
- 사용 언어: Python 3
- 실행 환경: Linux / Unix-like OS

## 3. 파일 구조

```
team_31/
├── syntax_analyzer.py   진입점 (main)
├── parser.py            토큰 읽기 + SLR 파싱 루프
├── slr_table.py         SLR table 파일 로드 → ACTION / GOTO 생성
├── parse_tree.py        파스 트리 노드 구조 및 출력
├── grammar.py           터미널 / 논터미널 / 생성 규칙 정의
├── grammar/
│   ├── modified_cfg.txt       ambiguity를 제거한 수정 CFG
│   ├── slr_input_cfg.txt      SLR table 생성 도구 입력용 CFG
│   └── slr_parsing_table.txt  SLR parsing table
├── test_inputs/         테스트 입력 파일 (21개)
├── test_outputs/        테스트 실행 결과 파일 (21개)
└── docs/
    ├── test_cases.md                        테스트 케이스 입력/출력 정리
    └── 2026_compiler_term_project (1).pdf   과제 명세서
```

## 4. 실행 방법

```bash
python3 syntax_analyzer.py <input_file>
```

예시:

```bash
python3 syntax_analyzer.py test_inputs/01_variable_declaration.txt
```

또는 실행 권한을 부여한 뒤 다음과 같이 실행할 수 있다.

```bash
chmod +x syntax_analyzer.py
./syntax_analyzer.py test_inputs/01_variable_declaration.txt
```

## 5. 입력 파일 형식

입력 파일은 공백 또는 줄바꿈으로 구분된 terminal token sequence로 구성된다.

```
vtype id semi
```

여러 줄로 작성할 수도 있다.

```
vtype id lparen rparen lbrace
return num semi
rbrace
```

## 6. 출력 형식

입력 토큰 시퀀스가 문법적으로 올바른 경우:

```
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

입력 토큰 시퀀스가 문법적으로 올바르지 않은 경우:

```
REJECT

Syntax Error:
Line: 1
Unexpected token: $
Expected one of: assign, lparen, semi
```

오류 리포트는 오류가 발생한 line number, 예상하지 못한 token, 예상 가능한 token 목록을 포함한다.

## 7. 테스트 케이스

총 21개의 테스트 케이스를 제공한다. (ACCEPT 17개 / REJECT 4개)

| 번호 | 테스트 내용 | 예상 결과 |
| --- | --- | --- |
| 01 | 변수 선언 | ACCEPT |
| 02 | 변수 초기화 | ACCEPT |
| 03 | 산술식 포함 변수 초기화 | ACCEPT |
| 04 | 함수 선언 | ACCEPT |
| 05 | 인자가 있는 함수 선언 | ACCEPT |
| 06 | if-else 문 | ACCEPT |
| 07 | while 문 | ACCEPT |
| 08 | class 선언 | ACCEPT |
| 09 | 세미콜론 누락 | REJECT |
| 10 | 비교 연산 조건식 | ACCEPT |
| 11 | literal RHS 대입 | ACCEPT |
| 12 | character RHS 대입 | ACCEPT |
| 13 | boolstr RHS 대입 | ACCEPT |
| 14 | 여러 개의 함수 인자 선언 | ACCEPT |
| 15 | 괄호가 포함된 산술식 | ACCEPT |
| 16 | 함수 블록 내부의 변수 선언 및 대입문 | ACCEPT |
| 17 | class 내부 함수 선언 | ACCEPT |
| 18 | 잘못된 토큰 (vtype 뒤 semi) | REJECT |
| 19 | 닫는 중괄호 누락 | REJECT |
| 20 | 최상위 레벨 대입문 | REJECT |
| 21 | 연산자 연속 사용 | REJECT |

각 테스트 케이스의 상세 입력/출력은 [docs/test_cases.md](docs/test_cases.md)를 참고한다.

## 8. 참고

- Chung-Ang University, Department of Software Engineering
- Compiler (Professor: Kim Hyo Su)
