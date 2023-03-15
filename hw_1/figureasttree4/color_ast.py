import ast
from typing import Any
import pygraphviz as pgv
from inspect import getsource

from figureasttree4 import fibonacci


class Node:
    def __init__(self, node_id, ast_node, value, color):
        self.node_id = node_id
        self.ast_node = ast_node
        self.color = color
        self.name = self._get_name(value)

    def _get_name(self, value) -> str:
        node_type = type(self.ast_node).__name__
        if value == 0:
            value = str('0')
        value = value if value else ''
        return f'{node_type}\n{value}'


# Еще одна хорошая библиотека для построения графа https://pygraphviz.github.io/documentation/latest/pygraphviz.pdf
class WalkerTree(ast.NodeVisitor):
    def __init__(self):
        self.cur_id = 0
        self.path = []
        self.tree = pgv.AGraph()
        self.colors = {
            "Add": "red",
            "Mult": "red",
            "Mod": "red",
            "For": "lightblue",
            "BinOp": "magenta",
            "BoolOp": "magenta",
            "UnaryOp": "magenta",
            "Constant": "lightgray",
            "Name": "lightseagreen",
            "FunctionDef": "lightblue",
            "arguments": "lightgray",
            "Eq": "cornflowerblue",
            "Lt": "cornflowerblue",
            "And": "purple",
            "Or": "purple",
            "Assign": "lightyellow",
            "Compare": "aqua",
            "Call": "lightcoral",
            "Tuple": "lightslategrey",
            "Return": "limegreen",
            "If": "mediumpurple",
            "IfExp": "mediumpurple"
        }

    def generic_visit(self, ast_node: ast.AST, value=None) -> Any:
        node_type = type(ast_node).__name__
        color = self.colors.get(node_type, "lightgreen")
        node = Node(self.cur_id, ast_node, value, color)
        self.cur_id += 1

        settings = {
            "fillcolor": node.color,
            "style": "filled",
            "shape": "box"
        }
        self.tree.add_node(node.node_id, label=node.name, **settings)
        if self.path:
            parent = self.path[-1]
            self.tree.add_edge(parent, node.node_id)

        self.path.append(node.node_id)
        super().generic_visit(ast_node)
        self.path.pop()

    def visit_Constant(self, node: ast.Constant) -> Any:
        return self.generic_visit(node, node.value)

    def visit_Name(self, node: ast.Constant) -> Any:
        return self.generic_visit(node, node.id)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        return self.generic_visit(node, node.name)

    def build(self) -> pgv.AGraph:
        self.tree.layout(prog='dot')
        return self.tree


def draw_graph(source: str, filename: str) -> None:
    ast_tree = ast.parse(source)
    visitor = WalkerTree()
    visitor.visit(ast_tree)
    visitor.build().draw(filename)


def get_plot(fname: str) -> None:
    source = getsource(fibonacci)
    draw_graph(source, fname)


if __name__ == '__main__':
    get_plot("../artifacts/ast_tree.png")
