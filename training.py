from typing import List, Union
def lower_join(seq:List[str]) :
    """Принимает на вход последовательность и создаёт из неё  
    строку в нижнем регистре."""
    return ''.join(seq).lower()

print(lower_join(1))