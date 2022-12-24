"""The inputs for the algorithms will be in four different types as shown below. Suppose that the data size is n.
InpType1. Each element of the list is an integer between 1 and 10*n. The elements are randomly chosen within this
range. Note that the elements in the list will be mostly distant integers due to the interval used to choose the
elements. InpType2. Each element of the list is an integer between 1 and 0.75*n. Note that in this case there will be
duplicate elements in the list. InpType3. Each element of the list is an integer between 1 and 0.25*n. Note that in
this case there will be much more duplicate elements in the list. InpType4. All the elements are the integer 1. """
from enum import IntEnum
from random import randint
from typing import Callable, List


class InputType(IntEnum):
    """This enum is used to specify the type of input. """
    InpType1 = 0
    InpType2 = 1
    InpType3 = 2
    InpType4 = 3


class Input:
    """Input class to hold the input data for the analysis. """

    def __init__(self, input_type: InputType, size: int):
        self.input_type: InputType = input_type
        self.size: int = size
        self.input_types: List[Callable] = [Input.generate_data1, Input.generate_data2,
                                            Input.generate_data3, Input.generate_data4]
        self.data: List[int] = []
        self.generate_data()

    def generate_data(self) -> None:
        """This function generates the data based on the input type. """
        self.data = self.input_types[self.input_type](self)

    def generate_data1(self) -> List[int]:
        """This function generates the data for InpType1. Each element of the list is an integer between 1 and 10*n.
        The elements are randomly chosen within this range. """
        return [randint(1, 10 * self.size) for _ in range(self.size)]

    def generate_data2(self) -> List[int]:
        """This function generates the data for InpType2. Each element of the list is an integer between 1 and
        0.75*n. """
        return [randint(1, int(0.75 * self.size)) for _ in range(self.size)]

    def generate_data3(self) -> List[int]:
        """This function generates the data for InpType3. Each element of the list is an integer between 1 and
        0.25*n. """
        return [randint(1, int(0.25 * self.size)) for _ in range(self.size)]

    def generate_data4(self) -> List[int]:
        """This function generates the data for InpType4.  All the elements are the integer 1. """
        return [1] * self.size

    def worst_case(self) -> None:
        """This function generates the data for worst case. """
        self.data.sort()
