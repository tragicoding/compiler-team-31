# =============================================================================
# parse_tree.py
#
# 파스 트리(Parse Tree) 노드 구조와 출력 함수를 정의한다.
#
# 파스 트리는 SLR 파싱 과정에서 shift/reduce 동작에 따라
# bottom-up으로 구성된다.
#   - shift  : 터미널 토큰을 leaf 노드로 생성해 node_stack에 push
#   - reduce : RHS 길이만큼 node_stack에서 pop하여 자식 노드로 연결하고,
#              LHS를 부모 노드로 생성해 push
# =============================================================================


class Node:
    """
    파스 트리의 단일 노드.

    Attributes:
        symbol   (str)        : 이 노드가 나타내는 문법 심볼
                                터미널이면 토큰 문자열 (예: "vtype", "id"),
                                논터미널이면 규칙 LHS (예: "VDECL", "EXPR"),
                                epsilon production이면 "ε"
        children (list[Node]) : 자식 노드 목록.
                                터미널 노드와 "ε" 노드는 항상 빈 리스트.
    """

    def __init__(self, symbol, children=None):
        self.symbol   = symbol
        self.children = children or []


def print_tree(node, prefix="", is_last=True):
    """
    파스 트리를 터미널에 계층 구조(트리 형태)로 출력한다.

    출력 예시:
        └── CODE
            ├── VDECL
            │   ├── vtype
            │   ├── id
            │   └── semi
            └── CODE
                └── ε

    Args:
        node    (Node) : 출력할 현재 노드
        prefix  (str)  : 현재 줄 앞에 붙는 들여쓰기 문자열 (재귀 호출 시 전달)
        is_last (bool) : 부모의 자식 목록에서 마지막 자식인지 여부
                         True  → "└── " 사용
                         False → "├── " 사용
    """
    # 마지막 자식이면 └──, 아니면 ├── 를 연결선으로 사용
    connector = "└── " if is_last else "├── "
    print(prefix + connector + node.symbol)

    # 자식 노드의 들여쓰기:
    #   마지막 자식 아래는 수직선(│) 없이 공백만, 그 외는 │ 추가
    child_prefix = prefix + ("    " if is_last else "│   ")

    for index, child in enumerate(node.children):
        is_last_child = (index == len(node.children) - 1)
        print_tree(child, child_prefix, is_last_child)
