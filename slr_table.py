# =========================
# slr_table.py
# =========================
# grammar/slr_parsing_table.txt 파일을 읽어
# ACTION 테이블과 GOTO 테이블을 생성한다.
#
# ACTION[state][terminal]     = "sN" (shift) / "rN" (reduce) / "acc"
# GOTO[state][non_terminal]   = next_state (int)
# =========================

from grammar import TERMINALS, NON_TERMINALS


def load_slr_table(filename="grammar/slr_parsing_table.txt"):
    """
    SLR table 파일에서 [4] LR Table 섹션을 찾아 파싱한다.

    파일 구조:
      - 탭(\\t)으로 구분된 헤더 행: 터미널 + 논터미널 순서
      - 이후 각 행: 상태 번호 + 각 심볼에 대한 액션/이동 값

    반환값:
      action_table (dict), goto_table (dict)
    """
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()

    # 파일 내 마지막 "LR table" 위치부터 파싱 시작
    lr_index = content.rfind("LR table")
    if lr_index == -1:
        raise ValueError("LR table section not found in slr_parsing_table.txt")

    lr_content = content[lr_index:]

    # 웹사이트 복붙 시 포함될 수 있는 입력 예시 섹션 제거
    if "Input (tokens):" in lr_content:
        lr_content = lr_content.split("Input (tokens):")[0]

    lines = [line for line in lr_content.splitlines() if line.strip()]

    # 헤더 행 탐색: "vtype\tid\tsemi..." 로 시작하는 줄
    header_line_index = None
    for i, line in enumerate(lines):
        if line.startswith("vtype\tid\tsemi"):
            header_line_index = i
            break

    if header_line_index is None:
        raise ValueError("LR table header line not found.")

    headers = lines[header_line_index].split("\t")

    # 헤더가 TERMINALS + NON_TERMINALS 순서와 일치하는지 검증
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

        # 상태 번호로 시작하지 않는 행 건너뜀
        if not parts[0].isdigit():
            continue

        state = int(parts[0])
        cells = parts[1:]

        # 열 수가 부족한 행(복붙 오류 등) 건너뜀
        if len(cells) < len(headers):
            continue

        action_table[state] = {}
        goto_table[state] = {}

        for index, symbol in enumerate(headers):
            value = cells[index].strip()

            if value == "":
                continue

            if symbol in TERMINALS:
                # 터미널 심볼 → ACTION 테이블
                action_table[state][symbol] = value
            else:
                # 논터미널 심볼 → GOTO 테이블
                try:
                    goto_table[state][symbol] = int(value)
                except ValueError:
                    pass  # 유효하지 않은 GOTO 값 무시

    return action_table, goto_table
