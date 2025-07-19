from sqlito.types import Field

class Expression:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    # def evaluate(self):
    #     """
    #     Evaluates the expression based on the operator and operands into a new 
    #     Field.
    #     """
    #     left_value = self.left.evaluate() if isinstance(self.left, Expression) else self.left
    #     right_value = self.right.evaluate() if isinstance(self.right, Expression) else self.right

    #     if self.operator == "+":
    #         # 
    #     elif self.operator == "-":
    #         return Field(left_value - right_value)
    #     elif self.operator == "*":
    #         return Field(left_value * right_value)
    #     elif self.operator == "/":
    #         return Field(left_value / right_value)
    #     elif self.operator == "%":
    #         return Field(left_value % right_value)
    #     else:
    #         raise SQLitoNotImplemented(f"Operator {self.operator} is not supported.")

    def __str__(self):
        return f"({self.left} {self.operator} {self.right})"