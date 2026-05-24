# =============================================================================
# parser.py
#
# 두 가지 기능을 제공한다.
#
# [1] read_tokens(filename)
#     입력 파일에서 terminal token sequence를 읽어 리스트로 반환한다.
#
# [2] parse(tokens, action_table, goto_table)
#     ACTION / GOTO 테이블을 이용해 SLR shift-reduce 파싱을 수행한다.
#     - ACCEPT: 파스 트리를 출력
#     - REJECT: 에러 리포트(line, unexpected token, expected tokens)를 출력
# =============================================================================

from grammar    import PRODUCTIONS
from parse_tree import Node, print_tree


# =============================================================================
# read_tokens
# =============================================================================

def read_tokens(filename):
    """
    입력 파일에서 terminal token sequence를 읽는다.

    - 각 토큰은 공백 또는 줄바꿈으로 구분된다.
    - 에러 리포트의 line number 출력을 위해 (token, line_no) 쌍으로 저장한다.
    - 마지막에 SLR end marker ("$", last_line_no)를 추가한다.

    Args:
        filename (str): 토큰 시퀀스가 담긴 입력 파일 경로

    Returns:
        list of (str, int): [(token, line_no), ..., ("$", last_line_no)]
    """
    tokens      = []
    last_line_no = 1

    with open(filename, "r", encoding="utf-8") as file:
        for line_no, line in enumerate(file, start=1):
            last_line_no = line_no
            # 공백·탭·줄바꿈 기준으로 분리해 각 토큰을 저장
            for token in line.split():
                tokens.append((token, line_no))

    # SLR 파서 입력의 끝을 표시하는 end marker 추가
    tokens.append(("$", last_line_no))

    return tokens


# =============================================================================
# parse
# =============================================================================

def parse(tokens, action_table, goto_table):
    """
    SLR shift-reduce 파싱을 수행한다.

    내부적으로 세 개의 스택을 유지한다:
        state_stack  : SLR 오토마톤의 상태 번호 스택
        symbol_stack : state_stack과 동기화되는 심볼 스택 (디버깅 용도)
        node_stack   : 파스 트리 노드 스택. reduce 시 자식 노드를 모아
                       부모 노드를 생성하는 데 사용된다.

    파싱 루프 동작:
        1. 현재 상태(state_stack top)와 현재 토큰으로 ACTION 조회
        2. ACTION이 없으면  → REJECT + 에러 리포트 출력
        3. "acc"이면        → ACCEPT + 파스 트리 출력
        4. "sN" (shift)이면 → 토큰을 스택에 push, 다음 토큰으로 이동
        5. "rN" (reduce)이면→ 규칙 N의 RHS 길이만큼 스택에서 pop,
                               LHS 노드 생성 후 push, GOTO로 상태 결정

    Args:
        tokens       (list): read_tokens()의 반환값
        action_table (dict): load_slr_table()의 ACTION 테이블
        goto_table   (dict): load_slr_table()의 GOTO 테이블

    Returns:
        (bool, Node | None): (파싱 성공 여부, 파스 트리 루트 노드)
    """
    state_stack  = [0]  # 초기 상태: 0
    symbol_stack = []   # state_stack과 1:1 대응 (state_stack[0]에 대응하는 심볼 없음)
    node_stack   = []   # 파스 트리 노드. reduce 시 자식으로 사용됨

    input_index = 0     # 현재 읽고 있는 토큰의 인덱스

    while True:
        current_state          = state_stack[-1]
        current_token, current_line = tokens[input_index]

        # ACTION 테이블 조회: 현재 상태에서 현재 토큰에 해당하는 액션
        action = action_table.get(current_state, {}).get(current_token)

        # ── Error ─────────────────────────────────────────────────────────────
        if action is None:
            # 현재 상태에서 가능한 토큰 목록을 오름차순으로 수집해 에러 리포트에 포함
            expected_tokens = sorted(action_table.get(current_state, {}).keys())

            print("REJECT")
            print()
            print("Syntax Error:")
            print(f"Line: {current_line}")
            print(f"Unexpected token: {current_token}")
            print(f"Expected one of: {', '.join(expected_tokens) if expected_tokens else 'None'}")
            return False, None

        # ── Accept ────────────────────────────────────────────────────────────
        if action == "acc":
            # 파싱 성공. node_stack의 최상단이 전체 파스 트리의 루트 노드
            print("ACCEPT")
            print()
            print("Parse Tree:")
            if node_stack:
                print_tree(node_stack[-1])
            else:
                print("No parse tree generated.")
            return True, node_stack[-1] if node_stack else None

        # ── Shift ─────────────────────────────────────────────────────────────
        if action.startswith("s"):
            next_state = int(action[1:])  # "s5" → 5

            # 현재 토큰을 스택에 push하고 다음 토큰으로 이동
            symbol_stack.append(current_token)
            state_stack.append(next_state)
            node_stack.append(Node(current_token))  # 터미널 leaf 노드 생성

            input_index += 1  # 다음 토큰 읽기

        # ── Reduce ────────────────────────────────────────────────────────────
        elif action.startswith("r"):
            rule_number    = int(action[1:])          # "r7" → 7
            lhs, rhs       = PRODUCTIONS[rule_number] # 예) ("VDECL", ["vtype","id","semi"])

            children = []

            if len(rhs) == 0:
                # Epsilon production: 스택을 건드리지 않고 ε 노드만 생성
                children.append(Node("ε"))
            else:
                # RHS 길이만큼 스택에서 pop
                # node_stack.pop()은 가장 오른쪽 심볼부터 꺼내므로,
                # insert(0, ...)로 앞에 삽입해 원래 순서를 복원한다
                for _ in rhs:
                    state_stack.pop()
                    symbol_stack.pop()
                    children.insert(0, node_stack.pop())

            # LHS 논터미널 노드를 생성하고 스택에 push
            new_node = Node(lhs, children)
            node_stack.append(new_node)
            symbol_stack.append(lhs)

            # GOTO 테이블로 reduce 후 다음 상태 결정
            # GOTO[pop 후 top 상태][LHS 심볼] → 새로운 상태
            goto_state = goto_table.get(state_stack[-1], {}).get(lhs)

            if goto_state is None:
                # GOTO 항목이 없으면 문법 또는 테이블 오류
                print("REJECT")
                print()
                print("Goto Error:")
                print(f"No GOTO entry for state {state_stack[-1]} and symbol {lhs}")
                return False, None

            state_stack.append(goto_state)

        # ── Unknown action ────────────────────────────────────────────────────
        else:
            # "sN" / "rN" / "acc" 이외의 값은 테이블 파싱 오류로 처리
            print("REJECT")
            print()
            print(f"Invalid action: {action}")
            return False, None
