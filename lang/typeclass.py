# import lang.astnode as ast


# build-in types
class TypeInt(int):
    def __add__(self, value: int):
        return TypeInt(super().__add__(int(value)))

    def __sub__(self, value: int):
        return TypeInt(super().__sub__(value))

    def __mul__(self, value):
        return TypeInt(super().__mul__(int(value)))

    def __truediv__(self, value: int):
        return TypeInt(super().__truediv__(int(value)))

    def __floordiv__(self, value: int):
        return TypeInt(super().__floordiv__(value))

    def __mod__(self, value: int):
        return TypeInt(super().__mod__(value))

    def __pow__(self, value: int):
        return TypeInt(super().__pow__(value))

    def __lshift__(self, value: int):
        return TypeInt(super().__lshift__(value))

    def __rshift__(self, value: int):
        return TypeInt(super().__rshift__(value))

    def __and__(self, value: int):
        return TypeInt(super().__and__(value))

    def __or__(self, value: int):
        return TypeInt(super().__or__(value))

    def __xor__(self, value: int):
        return TypeInt(super().__xor__(value))

    def __neg__(self):
        return TypeInt(super().__neg__())

    def __pos__(self):
        return TypeInt(super().__pos__())

    def __abs__(self):
        return TypeInt(super().__abs__())

    def __invert__(self):
        return TypeInt(super().__invert__())

    def __lt__(self, value: int):
        return TypeBool(super().__lt__(value))

    def __le__(self, value: int):
        return TypeBool(super().__le__(value))

    def __eq__(self, value: int):
        return TypeBool(super().__eq__(value))

    def __ne__(self, value: int):
        return TypeBool(super().__ne__(value))

    def __gt__(self, value: int):
        return TypeBool(super().__gt__(value))

    def __ge__(self, value: int):
        return TypeBool(super().__ge__(value))

    def to_json(self):
        return {'type': 'typeClass', 'varType': 'int', 'value': super().__str__()}


class TypeFloat(float):
    def __add__(self, value: float) -> float:
        return TypeFloat(super().__add__(value))

    def __sub__(self, value: float) -> float:
        return TypeFloat(super().__sub__(value))

    def __mul__(self, value: float) -> float:
        return TypeFloat(super().__mul__(value))

    def __truediv__(self, value: float) -> float:
        return TypeFloat(super().__truediv__(value))

    def __floordiv__(self, value: float) -> float:
        return TypeFloat(super().__floordiv__(value))

    def __mod__(self, value: float) -> float:
        return TypeFloat(super().__mod__(value))

    def to_json(self):
        return {'type': 'typeClass', 'varType': 'float', 'value': super().__str__()}


class TypeString(str):
    def to_json(self):
        return {'type': 'typeClass', 'varType': 'string', 'value': super().__str__()}


class TypeBool:
    def __init__(self, value):
        if type(value) == str:
            self.value = value == 'true'
        elif type(value) == bool:
            self.value = value

    def to_json(self):
        return {'varType': 'bool', 'value': self.value}

    def __bool__(self):
        return self.value
