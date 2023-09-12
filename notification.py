from sudoku import Sudoku


# Ví dụ sử dụng
list1 = Sudoku()
list2 = Sudoku()
list3 = Sudoku()
list1.get_Grid().add_value_grid(0,0,1)
list1.get_Grid().add_value_grid(0,1,2)
# print(list1.get_Grid().get_grid())
# print(list2.get_Grid().get_grid())

list3 = list1.get_different(list2)

print(list3.get_Grid().get_grid())