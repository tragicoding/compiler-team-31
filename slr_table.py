# =============================================================================
# slr_table.py
#
# grammar/slr_parsing_table.txt 파일을 읽어
# SLR 파서가 사용하는 ACTION 테이블과 GOTO 테이블을 생성한다.
#
# ACTION 테이블:
#   ACTION[state][terminal] = "sN"  → 상태 N으로 shift
#                           = "rN"  → 규칙 N으로 reduce
#                           = "acc" → 파싱 성공 (accept)
#
# GOTO 테이블:
#   GOTO[state][non_terminal] = next_state (int)
#   reduce 후 LHS 심볼을 보고 다음 상태를 결정하는 데 사용한다.
# =============================================================================

from grammar import TERMINALS, NON_TERMINALS


def load_slr_table(filename="grammar/slr_parsing_table.txt"):
    """
    SLR table 파일을 파싱하여 ACTION / GOTO 딕셔너리를 반환한다.

    파일 구조 (slr_parsing_table.txt):
        [1] Grammar 섹션
        [2] FIRST/FOLLOW 섹션
        [3] SLR Closure Table 섹션
        [4] LR Table 섹션          ← 이 함수가 파싱하는 부분
            LR table
            State  ACTION  GOTO
            <헤더 행: 탭으로 구분된 터미널 + 논터미널>
            <데이터 행: 상태번호 + 각 셀 값>

    Args:
        filename (str): SLR table 파일 경로 (프로젝트 루트 기준 상대경로)

    Returns:
        action_table (dict): ACTION[state][terminal]  = "sN" / "rN" / "acc"
        goto_table   (dict): GOTO[state][non_terminal] = next_state (int)

    Raises:
        ValueError: "LR table" 섹션 또는 헤더 행을 찾을 수 없을 때,
                    또는 헤더가 TERMINALS + NON_TERMINALS와 불일치할 때
    """
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()

    # ── 1. LR Table 섹션 탐색 ────────────────────────────────────────────────
    # rfind를 사용해 파일 내 마지막 "LR table" 위치를 찾는다.
    lr_index = content.rfind("LR table")
    if lr_index == -1:
        raise ValueError("LR table section not found in slr_parsing_table.txt")

    lr_content = content[lr_index:]

    # 웹사이트(jsmachines)에서 복붙 시 포함될 수 있는 테스트 입력 섹션 제거
    if "Input (tokens):" in lr_content:
        lr_content = lr_content.split("Input (tokens):")[0]

    # 빈 줄 제거 후 줄 단위 리스트로 변환
    lines = [line for line in lr_content.splitlines() if line.strip()]

    # ── 2. 헤더 행 탐색 ──────────────────────────────────────────────────────
    # 헤더 행은 "vtype\tid\tsemi..." 로 시작하는 탭 구분 줄이다.
    header_line_index = None
    for i, line in enumerate(lines):
        if line.startswith("vtype\tid\tsemi"):
            header_line_index = i
            break

    if header_line_index is None:
        raise ValueError("LR table header line not found.")

    headers = lines[header_line_index].split("\t")

    # ── 3. 헤더 무결성 검증 ──────────────────────────────────────────────────
    # 헤더의 심볼 순서가 grammar.py의 TERMINALS + NON_TERMINALS와 일치하는지 확인.
    # 순서가 다르면 ACTION/GOTO 값이 잘못된 심볼에 매핑된다.
    expected_headers = TERMINALS + NON_TERMINALS
    if headers != expected_headers:
        raise ValueError(
            "LR table headers do not match expected terminals/non-terminals.\n"
            f"Expected: {expected_headers}\n"
            f"Found:    {headers}"
        )

    action_table = {}
    goto_table   = {}

    # ── 4. 데이터 행 파싱 ────────────────────────────────────────────────────
    for line in lines[header_line_index + 1:]:
        parts = line.split("\t")

        # 첫 번째 열이 숫자(상태 번호)가 아닌 행은 건너뜀
        if not parts[0].isdigit():
            continue

        state = int(parts[0])
        cells = parts[1:]  # 상태 번호를 제외한 나머지 셀

        # 셀 수가 헤더보다 적으면 잘못된 행으로 간주하고 건너뜀
        if len(cells) < len(headers):
            continue

        action_table[state] = {}
        goto_table[state]   = {}

        for index, symbol in enumerate(headers):
            value = cells[index].strip()

            # 빈 셀(해당 상태에서 해당 심볼에 대한 액션 없음)은 건너뜀
            if value == "":
                continue

            if symbol in TERMINALS:
                # 터미널 심볼 → ACTION 테이블에 저장
                # 값 형태: "s5" (shift), "r3" (reduce), "acc" (accept)
                action_table[state][symbol] = value
            else:
                # 논터미널 심볼 → GOTO 테이블에 정수로 저장
                try:
                    goto_table[state][symbol] = int(value)
                except ValueError:
                    # 유효하지 않은 GOTO 값(공백 등) 무시
                    pass

    return action_table, goto_table
