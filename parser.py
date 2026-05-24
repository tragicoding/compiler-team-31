# =========================
# parser.py
# =========================
# 토큰 시퀀스를 읽고 SLR shift-reduce 파싱을 수행한다.
#
# read_tokens : 입력 파일에서 토큰 시퀀스를 읽어 리스트로 반환
# parse       : ACTION/GOTO 테이블을 이용해 파싱을 수행하고
#               ACCEPT 시 파스 트리를, REJECT 시 에러 리포트를 출력
# =========================

from grammar import PRODUCTIONS
from parse_tree import Node, print_tree


def read_tokens(filename):
    """
    입력 파일에서 terminal token sequence를 읽는다.
    각 token은 공백 또는 줄바꿈으로 구분된다.
    오류 보고를 위해 각 token의 line number도 함께 저장한다.

    반환값: [(token, line_no), ..., ("$", last_line_no)]
    """
    tokens = []
    last_line_no = 1

    with open(filename, "r", encoding="utf-8") as file:
        for line_no, line in enumerate(file, start=1):
            last_line_no = line_no
            for token in line.split():
                tokens.append((token, line_no))

    # SLR parser의 입력 끝을 표시하는 end marker
    tokens.append(("$", last_line_no))

    return tokens


def parse(tokens, action_table, goto_table):
    """
    SLR shift-reduce 파싱을 수행한다.

    파싱 루프:
      1. 현재 상태(state_stack top)와 현재 토큰으로 ACTION을 조회
      2. shift  → 토큰을 스택에 push, 다음 토큰으로 이동
      3. reduce → 생성 규칙 RHS 길이만큼 스택에서 pop,
                  LHS 노드를 생성하고 GOTO로 다음 상태 결정
      4. accept → 파스 트리 출력 후 종료
      5. error  → REJECT + 에러 리포트 출력 후 종료

    매개변수:
      tokens       : read_tokens()의 반환값
      action_table : load_slr_table()의 ACTION 반환값
      goto_table   : load_slr_table()의 GOTO 반환값
    """
    state_stack  = [0]   # SLR 상태 스택
    symbol_stack = []    # 심볼 스택 (상태 스택과 동기화)
    node_stack   = []    # 파스 트리 노드 스택

    input_index = 0

    while True:
        current_state = state_stack[-1]
        current_token, current_line = tokens[input_index]

        action = action_table.get(current_state, {}).get(current_token)

        # ── Error ──────────────────────────────────────────
        if action is None:
            expected_tokens = sorted(action_table.get(current_state, {}).keys())
            print("REJECT")
            print()
            print("Syntax Error:")
            print(f"Line: {current_line}")
            print(f"Unexpected token: {current_token}")
            print(f"Expected one of: {', '.join(expected_tokens) if expected_tokens else 'None'}")
            return False, None

        # ── Accept ─────────────────────────────────────────
        if action == "acc":
            print("ACCEPT")
            print()
            print("Parse Tree:")
            if node_stack:
                print_tree(node_stack[-1])
            else:
                print("No parse tree generated.")
            return True, node_stack[-1] if node_stack else None

        # ── Shift ──────────────────────────────────────────
        if action.startswith("s"):
            next_state = int(action[1:])
            symbol_stack.append(current_token)
            state_stack.append(next_state)
            node_stack.append(Node(current_token))
            input_index += 1

        # ── Reduce ─────────────────────────────────────────
        elif action.startswith("r"):
            rule_number = int(action[1:])
            lhs, rhs = PRODUCTIONS[rule_number]

            children = []

            if len(rhs) == 0:
                # epsilon production: ε 노드 생성 (스택은 건드리지 않음)
                children.append(Node("ε"))
            else:
                # RHS 길이만큼 스택에서 pop (역순이므로 insert(0, ...) 로 복원)
                for _ in rhs:
                    state_stack.pop()
                    symbol_stack.pop()
                    children.insert(0, node_stack.pop())

            new_node = Node(lhs, children)
            node_stack.append(new_node)
            symbol_stack.append(lhs)

            # GOTO 테이블로 다음 상태 결정
            goto_state = goto_table.get(state_stack[-1], {}).get(lhs)
            if goto_state is None:
                print("REJECT")
                print()
                print("Goto Error:")
                print(f"No GOTO entry for state {state_stack[-1]} and symbol {lhs}")
                return False, None

            state_stack.append(goto_state)

        else:
            print("REJECT")
            print()
            print(f"Invalid action: {action}")
            return False, None
