#!/usr/bin/env python3
# =========================
# syntax_analyzer.py
# =========================
# 프로그램 진입점.
# 실행 방법: python3 syntax_analyzer.py <input_file>
# =========================

import sys

from parser    import read_tokens, parse
from slr_table import load_slr_table


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
