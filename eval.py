import ast
import operator
import math
from decimal import Decimal


def forgiving_sum(value_list):
    """
    sums a list that may include falsy values (None etc.)
    """
    return sum([v or 0 for v in value_list])


def expression(node: int):
    """
    evaluate an expression
    """
    return _eval(node.body)


def binary_operation(node: ast.AST):
    """
    perform a binary operation
    """
    return operations[type(node.op)](_eval(node.left), _eval(node.right))


def bool_operation(node: ast.AST):
    """
    perform a boolean operation
    """
    result = operations[type(node.op)](*_eval(node.values[0:2]))
    if len(node.values) > 2:
        result = result and _eval(ast.BoolOp(op=node.op, values=node.values[1:]))
    return result


def unary_operation(node: ast.AST):
    """
    perform a unary operation
    """
    return operations[type(node.op)](_eval(node.operand))


def comparison(node: ast.AST):
    """
    perform a comparison
    """
    if isinstance(node.ops[0], (ast.In, ast.NotIn)):
        comp = operations[type(node.ops[0])](
            _eval(node.comparators[0]),
            _eval(node.left),
        )
    else:
        comp = operations[type(node.ops[0])](
            _eval(node.left),
            _eval(node.comparators[0])
        )
    if len(node.ops) > 1:
        return _eval(
            ast.Compare(
                left=node.comparators[0],
                ops=node.ops[1:],
                comparators=node.comparators[1:]
            )
        ) and comp
    return comp


def constant(node: ast.AST):
    """
    map an ast.Constant to a node
    """
    return node.value


def ast_list(node: ast.AST):
    """
    map an ast.List to a node
    """
    return [_eval(n) for n in node.elts]


def true_list(node: ast.AST):
    """
    map a python list to a node
    """
    return [_eval(n) for n in node]


def call(node: ast.AST):
    """
    map an ast.Call to a callable
    """
    args = [_eval(x) for x in node.args]
    r = callables[node.func.id](*args)
    return r


class Operations:
    """
    maps ast operations to python operations  
    """

    def __init__(self):
        base_operations = {
            ast.Expression: expression,
        }

        def combine(*dicts):
            dict_1 = dicts[0]
            for d in dicts[1:]:
                dict_1.update(d)
            return dict_1

        self.map = combine(
            base_operations, self.type_operations, self.bool_operations,
            self.unary_operations, self.bitwise_operations, self.binary_operations,
            self.comparators, self.callables
        )

    def __getitem__(self, key: str):
        return self.map[key]

    @property
    def type_operations(self):
        """
        Types
        Integers: 1
        Floats: 1.1
        Strings: "abc"
        NoneType: None
        Boolean: True, False
        Lists: [a, b, c], [1, 2, 3]
        """
        return {
            ast.Constant: constant,
            ast.List: ast_list,  # [a, b, c]
            list: true_list,  # [a, b, c]
        }

    @property
    def bool_operations(self):
        """
        Bool operations
        And: a and b
        Or: a or b
        """
        return {
            ast.BoolOp: bool_operation,
            ast.And: operator.iand,
            ast.Or: operator.ior,
        }

    @property
    def unary_operations(self):
        """
        Unary operations
        Not: not b, not a
        """
        return {
            ast.UnaryOp: unary_operation,
            ast.Not: operator.not_,
        }

    @property
    def bitwise_operations(self):
        """
        Bitwise operations
        And: a & b
        Or: a | b
        Xor: a ^ b
        """
        return {
            ast.BitAnd: operator.and_,
            ast.BitOr: operator.or_,
            ast.BitXor: operator.xor,
        }

    @property
    def binary_operations(self):
        """
        Mathematical/Binary operations
        Multiplication: 1 * 2
        Subtraction: 2 - 1
        Addition: 1 + 2
        Power: 1 ** 2
        Division: 1 / 2
        """
        return {
            ast.BinOp: binary_operation,
            ast.Mult: operator.mul,
            ast.Sub: operator.sub,
            ast.Add: operator.add,
            ast.Pow: operator.pow,
            ast.Div: operator.truediv,
        }

    @property
    def comparators(self):
        """
        Comparators
        Equals: 1 == 1
        Not equals: 1 != 2
        Greater than: 2 > 1
        Greater than or equals: 2 >= 2
        Less than: 1 < 2
        Less than or equals: 2 <= 2
        Is: None is None, True is True
        Is not: True is not None, None is not True
        In: 1 in [1, 2, 3]
        Not in: 1 in [2, 3, 4]
        """
        return {
            ast.Compare: comparison,
            ast.Eq: operator.eq,
            ast.NotEq: operator.ne,
            ast.GtE: operator.ge,
            ast.LtE: operator.le,
            ast.Lt: operator.lt,
            ast.Gt: operator.gt,
            ast.Is: operator.is_,
            ast.IsNot: operator.is_not,
            ast.In: operator.contains,
            ast.NotIn: lambda *x: not operator.contains(*x)
        }

    @property
    def callables(self):
        """
        """
        return {
            ast.Call: call
        }


callables = {}
callables.update({x: getattr(math, x) for x in dir(math) if "__" not in x})
callables.update({
    'sum': forgiving_sum,
    'any': any,
    'all': all,
    'round': round,
    'int': int,
    'str': str,
    'float': float,
    'Decimal': Decimal
})


operations = Operations()


def _eval(node: ast.AST):
    if type(node) in operations.map:
        return operations.map[type(node)](node)
    raise SyntaxError(f"Bad syntax, {type(node)}")


def safe_eval(s: str):
    tree = ast.parse(s, mode='eval')
    return _eval(tree)
