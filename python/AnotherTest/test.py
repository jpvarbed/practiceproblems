# assume no cycles?
class Spreadsheet:
    def __init__(self):
        self.cells = {}

    def set_cell(self, cell, value: str):
        self.cells[cell] = value

    def get_cell(self, cell):
        if cell in self.cells:
            visited = set()
            try:
                return self._evaluate(cell, visited)
            except ValueError:
                return "#!REF"
        return None

    # check if its an expression
    # calculate expression
    # return
    # assuming not a cycle 
    def _evaluate(self, cell, visited):
        if cell in visited:
            raise ValueError("#!REF")
        value = self.cells[cell]
        visited.add(cell)
        # D3 = C1*C2 C2 = D1 + D3
        # D3
        # = C1*C2
        # C1 C2
        # D1 + D2
        # 
        # check if its a  expression
        # if its an expression evaluate on each of those cels
        # perform formula result
        # return

        result = 0
        if value.isdigit():
            result = int(value)
        elif value[0] == "=":
            # always cells not a number
            # parse each value in here
            # C1 * C2
            parts = self._split_expression(value)
            # i always have operator, first cell and second cell
            operator = None
            first_cell_value = None
            second_cell_value = None
            for part in parts:
                if part in ('+', '-', '*', '/'):
                    operator = part
                elif first_cell_value is None:
                    first_cell_value = self._evaluate(part, visited)
                else:
                    second_cell_value = self._evaluate(part, visited)
            if operator in '+':
                result = first_cell_value + second_cell_value
            elif operator == '-':
                result = first_cell_value - second_cell_value
            elif operator == '*':
                result = first_cell_value * second_cell_value
            elif operator == '/':
                result = first_cell_value / second_cell_value
        else:
            # string case
            return value

        return result
    
    # return operator, operands
    def _split_expression(self, expression):
        parts = []
        start = 1
        # all things from 1 to index of operator is cell 0, everything after is cell 1
        for i, c in enumerate(expression):
            if c in ('+', '-', '*', '/'):
                # cell 0
                parts.append(expression[start:i])
                # operator
                parts.append(c)
                parts.append(expression[i + 1:])
            elif c == "=":
                pass
        return parts
    
# cycle detection
# #!REF

def test_Spreadsheet():
    s = Spreadsheet()
    s.set_cell("A1", "name")
    assert s.get_cell("A1") == "name"
    s.set_cell("B1", "263")
    assert s.get_cell("B1") == 263
    s.set_cell("C1", "50")
    s.set_cell("C2", "100")
    s.set_cell("D2", "=C1+C2")
    assert s.get_cell("D2") == 150


    s.set_cell("D3", "=D2*B1") 
    result = s.get_cell("D3")
    print(result)
    assert result == 39450

    s.set_cell("D4", "=D4+D3")
    assert s.get_cell("D4") == "#!REF"
        
    
if __name__ == '__main__':
    test_Spreadsheet()