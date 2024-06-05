
# - ListV2
#  - __init__
#     - self.values
#  - __add__
#  - __sub__
#  - __mul__
#  - __truediv__
#  - append
#  - mean
#  - __iter__
#  - __next__
#  - __repr___
 
# - DataFrame
#  - __init__
#      - self.index - a dictionary to map text to row index
#      - self.data (dict of ListV2 where each column is a key)
#      - self.columns a simple list
#  - set_idxex
#  - __setitem__
#  - __getitem__
#  - loc
#  - iteritems
#  - iterrows
#  - as_type
#  - drop
#  - mean
#  - __repr__

class ListV2: 
    def __init__(self, values=None):
        self.values = [] if values is None else values.copy() 

    def __add__(self, value):
        if isinstance(value, (int, float)):
            value = [value] * len(self.lst)
        return ListV2([x + y for x, y in zip(self.values, value)])
    

    def __sub__(self, value):
        if isinstance(value, (int, float)):
            value = [value] * len(self.lst)
        return ListV2([x - y for x, y in zip(self.values, value)])
    
    def __mul__(self, value):
        if isinstance(value, (int, float)):
            value = [value] * len(self.lst)
        return ListV2([x * y for x, y in zip(self.values, value)])
    
    def __truediv__(self, value):
        if isinstance(value, (int, float)):
            value = [value] * len(self.lst)
        return ListV2([round(x / y, 2) for x, y in zip(self.values, value)])
    
    def mean(self):
        return sum(self.values) / len(self.values)
    
    def append(self, value):
        return self.values.append(value)

    def __iter__(self):
        self.count = 0
        return self
    
    def __next__(self):
        if self.count < len(self.values):
            result = self.values[self.count]
            self.count += 1
            return result
        else:
            raise StopIteration
    
    def __repr__(self):
        return repr(self.values)
    
    def get_values(self):
        return self._values
    
    def __getitem__(self, other_value):
        return self.values[other_value]
 
class DataFrame:
    def __init__(self, data, columns):
        self.index = {other_value: other_value for other_value, row in enumerate(data)}
        self.data = {key: ListV2([row[i] for row in data]) for i, key in enumerate(columns)}
        self.columns = columns

    def set_index(self, inplst):
        my_dict = {}
        for index, value in enumerate(inplst):
            my_dict[value] = index
        self.index = my_dict
        return self


    def __setitem__(self, key, value):
        if isinstance(value, ListV2):
            self.data[key] = value
        else:
            self.data[key] = ListV2(value)

    def __getitem__(self, other_value):
        if type(other_value) == tuple:
            rows, cols = other_value
            if type(other_value[0]) == slice and type(other_value[1]) == slice:
                row_ind = self._process_index(other_value[0], self.index)
                col_ind = self._process_index(other_value[1], self.columns)
                data = []
                for i in row_ind:
                    row_data_lst = []
                    for j in col_ind:
                        row_data_lst.append(self.data[self.columns[j]][i])
                    data.append(row_data_lst)
                columns = [self.columns[j] for j in col_ind]
                return DataFrame(data, columns)
        elif type(other_value) == str:
            return self.data[other_value]
        elif type(other_value) == int:
            col_name = self.columns[other_value]
            data = [[self.data[col_name][i]] for i in range(len(self.index))]
            return DataFrame(data, columns=[col_name], index=list(self.index.keys()))
        elif type(other_value) == slice:
            rows = self._process_index(other_value, self.index)
            cols = self.columns
            data = [[self.data[col][i] for col in cols] for i in rows]
            return DataFrame(data, self.columns)
        elif type(other_value) == list:
            col_ind = []
            for col_name in other_value:
                col_index = self.columns.index(col_name)
                col_ind.append(col_index)
            len_rows = len(self.index)
            new_data_lst = []
            for row_idx in range(len_rows):
                new_row_lst = []
                for col_index in col_ind:
                    new_val = self.data[self.columns[col_index]][row_idx]
                    new_row_lst.append(new_val)
                new_data_lst.append(new_row_lst)
            new_columns = [self.columns[col_index] for col_index in col_ind]
            return DataFrame(new_data_lst, columns=new_columns)
    
    def _process_index(self, index, val):
        if isinstance(index, slice):
            start = index.start or 0
            stop = index.stop or len(val)
            step = index.step or 1
            return list(range(start, stop, step))
        elif isinstance(index, list):
            return [val.index(item) for item in index]
        else:
            return [val.index(index)]
            
    def loc(self, row_idx):
        result = {}
        for col in self.columns:
            result[col] = self.data[col][row_idx]
        return result

    def iteritems(self):
        return ((key, self.data[key]) for key in self.columns)

    def iterrows(self):
        return ((self.columns[0], *[self.data[key][i] for key in self.columns[1:]]) for i in range(len(self)))

    def as_type(self, col_name, dtype):
        new_col_data = []
        for old_val in self.data[col_name]:
            new_val = dtype(old_val)
            new_col_data.append(new_val)
        self.data[col_name] = ListV2(new_col_data)

    def drop(self, column_name):
        self.columns = list(filter(lambda col: col != column_name, self.columns))
        self.data = {key: value for key, value in self.data.items() if key != column_name} if column_name in self.columns else self.data

    def mean(self):
        print(self.data)
        avg = []
        for ele in list(self.data.values()):
            sumoflist = sum(ele)
            lenoflist = 0
            for i in ele:
                lenoflist = lenoflist+1
            avgoflist = avg.append(sumoflist/lenoflist)
        return dict(zip(list(self.data.keys()),avg))

    def __repr__(self):
        header = ','.join(self.columns)
        body = [f",{header}"]
        index_list = list(self.index.items())
        i = 0
        while i < len(index_list):
            index, row_idx = index_list[i]
            row = [str(index)]
            col_list = list(self.columns)
            j = 0
            while j < len(col_list):
                col = col_list[j]
                row.append(str(self.data[col][row_idx]))
                j += 1
            body.append(','.join(row))
            i += 1
        return '\n'.join(body)

    def __len__(self):
        return len(self.data[self.columns[0]].values)