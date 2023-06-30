from cell import Cell


class Table:
    def __init__(self, cells_list) -> None:
        self._cells_list = cells_list

    @property
    def cells_list(self):
        return self._cells_list

    def get_dimension(self):
        """
        Method returns table dimension, which is length of cells_list
        """
        return len(self._cells_list)

    def get_cell_by_index(self, index_x, index_y) -> Cell:
        '''
        Method takes two indexes (x index and y index) as arguments and returns cell which is stored in cells_list[x index][y index]
        '''
        return self._cells_list[index_x][index_y]

    def is_empty(self):
        """
        Method chcecks if table's cells_list is empty
        """
        inner_cell: Cell
        for cell in self._cells_list:
            for inner_cell in cell:
                if (not inner_cell.is_empty()):
                    return False
        return True

    @staticmethod
    def generate_empty_cells_list(table_dimension):
        """
        Method creates and returns empty cells list according to table dimension given as an argument
        """
        list = []
        for i in range(0, table_dimension):
            sub_list = []
            for j in range(0, table_dimension):
                cell = Cell(j, i, [])
                sub_list.append(cell)
            list.append(sub_list)
        return list
