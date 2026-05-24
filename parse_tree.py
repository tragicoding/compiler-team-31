# =========================
# parse_tree.py
# =========================
# 파스 트리 노드 구조와 출력 함수를 정의한다.
# =========================


class Node:
    """
    파스 트리 노드.
    각 노드는 문법 심볼(symbol)과 자식 노드 리스트(children)를 가진다.
    - 터미널 심볼: children이 비어 있음
    - 논터미널 심볼: children에 하위 노드들이 연결됨
    - epsilon production: children = [Node("ε")]
    """

    def __init__(self, symbol, children=None):
        self.symbol = symbol
        self.children = children or []


def print_tree(node, prefix="", is_last=True):
    """
    파스 트리를 터미널에 계층 구조로 출력한다.

    node    : 출력할 루트 노드
    prefix  : 현재 줄에 앞서 붙는 들여쓰기 문자열
    is_last : 부모의 마지막 자식 여부 (연결선 모양 결정)
    """
    connector = "└── " if is_last else "├── "
    print(prefix + connector + node.symbol)

    child_prefix = prefix + ("    " if is_last else "│   ")

    for index, child in enumerate(node.children):
        is_last_child = (index == len(node.children) - 1)
        print_tree(child, child_prefix, is_last_child)
