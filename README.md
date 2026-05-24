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

## 3. 실행 방법

다음 명령어를 사용하여 실행한다.

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

## 4. 입력 파일 형식

입력 파일은 공백 또는 줄바꿈으로 구분된 terminal token sequence로 구성된다.

예시:

```
vtype id semi
```

여러 줄로 작성할 수도 있다.

```
vtype id lparen rparen lbrace
return num semi
rbrace
```

## 5. 출력 형식

입력 토큰 시퀀스가 문법적으로 올바른 경우 다음과 같이 출력한다.

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

입력 토큰 시퀀스가 문법적으로 올바르지 않은 경우 다음과 같이 출력한다.

```
REJECT

Syntax Error:
Line: 1
Unexpected token: $
Expected one of: assign, lparen, semi
```

오류 리포트는 오류가 발생한 line number, 예상하지 못한 token, 예상 가능한 token 목록을 포함한다.

## 6. 제출 파일 구성

```
syntax_analyzer.py         SLR parsing table 기반 syntax analyzer 소스 코드
grammar/
  modified_cfg.txt         ambiguity를 제거한 수정 CFG
  slr_input_cfg.txt        SLR table 생성 도구 입력용 CFG
  slr_parsing_table.txt    SLR parsing table
test_inputs/               테스트 입력 파일
test_outputs/              테스트 실행 결과 파일
```

## 7. 참고

- Chung-Ang University, Department of Software Engineering
- Compiler (Professor: Kim Hyo Su)
