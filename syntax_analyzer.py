#!/usr/bin/env python3
# =============================================================================
# syntax_analyzer.py
#
# 프로그램 진입점 (main).
#
# 실행 방법:
#   python3 syntax_analyzer.py <input_file>
#
# 동작 흐름:
#   1. 커맨드라인 인자에서 입력 파일 경로를 읽는다.
#   2. read_tokens()  : 입력 파일에서 token sequence를 읽는다.
#   3. load_slr_table(): grammar/slr_parsing_table.txt에서
#                        ACTION / GOTO 테이블을 로드한다.
#   4. parse()        : SLR shift-reduce 파싱을 수행하고
#                       ACCEPT 시 파스 트리, REJECT 시 에러 리포트를 출력한다.
# =============================================================================

import sys

from parser    import read_tokens, parse
from slr_table import load_slr_table


def main():
    # ── 인자 검사 ──────────────────────────────────────────────────────────────
    # 실행 시 반드시 입력 파일 경로 하나만 인자로 받아야 한다.
    if len(sys.argv) != 2:
        print("사용법: python3 syntax_analyzer.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    # ── 토큰 읽기 ──────────────────────────────────────────────────────────────
    try:
        tokens = read_tokens(input_file)
    except FileNotFoundError:
        print(f"오류: 입력 파일을 찾을 수 없습니다: {input_file}")
        sys.exit(1)

    # ── SLR 테이블 로드 ────────────────────────────────────────────────────────
    # grammar/slr_parsing_table.txt 에서 ACTION / GOTO 딕셔너리를 생성한다.
    # 이 파일은 프로그램 실행 위치(프로젝트 루트)를 기준으로 찾는다.
    try:
        action_table, goto_table = load_slr_table()
    except Exception as error:
        print(f"SLR table 로드 오류: {error}")
        sys.exit(1)

    # ── 파싱 수행 ──────────────────────────────────────────────────────────────
    # ACCEPT → 파스 트리 출력
    # REJECT → 에러 리포트 출력 (line number, unexpected token, expected tokens)
    parse(tokens, action_table, goto_table)


if __name__ == "__main__":
    main()
