import ast
import operator
import re

OPS = {
    ast.Add: operator.add, ast.Sub: operator.sub,
    ast.Mult: operator.mul, ast.Div: operator.truediv,
    ast.Pow: operator.pow, ast.Mod: operator.mod
}

def calculate(expression):
    expression = expression.replace("^", "**").strip()
    if not re.fullmatch(r"[0-9+\-*/().% \t]+|\d+\s*\*\*\s*\d+", expression):
        return None
    try:
        node = ast.parse(expression, mode="eval")
        def ev(n):
            if isinstance(n, ast.Expression): return ev(n.body)
            if isinstance(n, ast.Constant) and isinstance(n.value, (int,float)): return n.value
            if isinstance(n, ast.BinOp) and type(n.op) in OPS:
                return OPS[type(n.op)](ev(n.left), ev(n.right))
            if isinstance(n, ast.UnaryOp) and isinstance(n.op, (ast.UAdd, ast.USub)):
                v = ev(n.operand)
                return v if isinstance(n.op, ast.UAdd) else -v
            raise ValueError
        return ev(node)
    except Exception:
        return None
