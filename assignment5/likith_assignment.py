class ListV2:
    def __init__(self, values=None):
        if values is None:
            self.values = []
        else:
            self.values = values.copy()

    def get_values(self):
        return self._values

    def __add__(self, other):
        if isinstance(other, ListV2):
            if len(other.values) != len(self.values):
                raise ValueError("Input lists must have the same length for addition.")
            result = [x + y for x, y in zip(self.values, other.values)]
        elif isinstance(other, (int, float)):
            result = [x + other for x in self.values]
        elif isinstance(other, list):
            if len(other) != len(self.values):
                raise ValueError("Input list must have the same length for addition.")
            result = [x + y for x, y in zip(self.values, other)]
        else:
            raise ValueError("Operand must be a number, a ListV2 object, or a list of numbers")
        return ListV2(result)

    def __sub__(self, other):
        return [a - b for a, b in zip(self.values, other.values)]

    def __mul__(self, other):
        return [a * b for a, b in zip(self.values, other.values)]

    def __truediv__(self, other):
        return [a / b for a, b in zip(self.values, other.values)]

    def append(self, value):
        self.values.append(value)

    def mean(self):
        return sum(self.values) / len(self.values)

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index >= len(self.values):
            raise StopIteration
        result = self.values[self.index]
        self.index += 1
        return result

    def __getitem__(self, idx):
        return self.values[idx]

    def __repr__(self):
        return f'ListV2({self.values})'

class DataFrame:
    """A class to represent a 2D table of data
    def __init__(self, data, columns=None):
        self.index = {}
        self.data = {col: ListV2() for col in columns} if columns else {}
        self.columns = columns or []

        for row_idx, row in enumerate(data):
            self.index[row[0]] = row_idx
            for col_idx, value in enumerate(row):
                if columns:
                    col = columns[col_idx]
                    self.data[col].append(value)
                else:
                    self.data[col_idx].append(value)
                    if len(self.data) <= col_idx:
                        self.columns.append(col_idx)"""
    def __init__(self, data, columns=None, index=None):
        self.columns = columns or []
        self.data = {col: [] for col in self.columns}

        if index is None:
            self.index = {}
            for row_idx, row in enumerate(data):
                self.index[row[0]] = row_idx
                for col_idx, value in enumerate(row):
                    if self.columns:
                        col = self.columns[col_idx]
                        self.data[col].append(value)
                    else:
                        self.data[col_idx].append(value)
                        if len(self.data) <= col_idx:
                            self.columns.append(col_idx)
        else:
            self.index = {str(i): i for i in range(len(data))}
            for row_idx, row in enumerate(data):
                for col_idx, value in enumerate(row):
                    col = columns[col_idx]
                    self.data[col].append(value)

    def set_index(self, col_name):
        index_col = self.data.pop(col_name)
        self.index = {val: idx for idx, val in enumerate(index_col) if val is not None}

    def __setitem__(self, col_name, values):
        if col_name in self.data:
            self.data[col_name] = ListV2(values)
        else:
            self.columns.append(col_name)
            self.data[col_name] = ListV2(values)
    def __getitem__(self, idx):
        if isinstance(idx, tuple):
          print('tuple')
          if isinstance(idx[0], slice) and isinstance(idx[1], slice):
              rows = range(idx[0].start or 0, idx[0].stop or len(self.index), idx[0].step or 1)
              cols = range(idx[1].start or 0, idx[1].stop or len(self.columns), idx[1].step or 1)
              data = [[self.data[self.columns[col]][row] for col in cols] for row in rows]
              return DataFrame(data, [self.columns[col] for col in cols])
        elif isinstance(idx, str):
          print("str0")
          if idx == self.columns[0]:
             return self.data[idx]
          elif idx in self.columns:
              return self.data[idx]
          
        elif isinstance(idx, int):
            print('int')
            col_name = self.columns[idx]
            return DataFrame([[self.data[col_name][row_idx]] for row_idx in range(len(self.index))], columns=[col_name], index=list(self.index.keys()))
        elif isinstance(idx, slice):
            print('slice')
            start = idx.start or 0
            stop = idx.stop or len(self.index)
            step = idx.step or 1
            new_index = list(self.index.keys())[start:stop:step]
            new_data = [[self.data[col_name][row_idx] for col_name in self.columns] for row_idx in range(start, stop, step)]
            return DataFrame(new_data, self.columns)
        elif isinstance(idx, list):
            col_indices = [self.columns.index(col_name) for col_name in idx]
            new_data = [[self.data[self.columns[col_idx]][row_idx] for col_idx in col_indices] for row_idx in range(len(self.index))]
            new_columns = [self.columns[col_idx] for col_idx in col_indices]
            return DataFrame(new_data, columns=new_columns)
        else:
            print('final else')
            col_name = self.columns[idx]
            return DataFrame[[col_name][:]]
    '''def __getitem__(self, idx):
        if isinstance(idx, str):
            if idx == self.columns[0]:
                return self.index.keys()
            elif idx in self.columns:
                return self.data[idx][:]
            else:
                raise KeyError(f"Column {idx} not found.")
        elif isinstance(idx, int):
            col_name = self.columns[idx]
            return self.data[col_name][:]
        elif isinstance(idx, slice):
            start = idx.start or 0
            stop = idx.stop or len(self.index)
            step = idx.step or 1
            new_index = list(self.index.keys())[start:stop:step]
            new_data = [[self.data[col_name][row_idx] for col_name in self.columns] for row_idx in range(start, stop, step)]
            return DataFrame(new_data, columns=self.columns)
        elif isinstance(idx, list):
            col_indices = [self.columns.index(col_name) for col_name in idx]
            new_data = [[self.data[self.columns[col_idx]][row_idx] for col_idx in col_indices] for row_idx in range(len(self.index))]
            new_columns = [self.columns[col_idx] for col_idx in col_indices]
            return DataFrame(new_data, columns=new_columns)
        else:
            col_name = self.columns[idx]
            return self.data[col_name][:]
    def __getitem__(self, idx):
      if isinstance(idx, tuple):
          rows, cols = idx
          if isinstance(rows, slice):
              start = rows.start or 0
              stop = rows.stop or len(self.index)
              step = rows.step or 1
              rows = list(self.index.keys())[start:stop:step]
          elif isinstance(rows, list):
              rows = [self.index[row_name] for row_name in rows]
          if isinstance(cols, slice):
              start = cols.start or 0
              stop = cols.stop or len(self.columns)
              step = cols.step or 1
              cols = self.columns[start:stop:step]
          elif isinstance(cols, list):
              cols = [col_name for col_name in cols if col_name in self.columns]
          data = {col: [self.data[col][row_idx] for row_idx in rows] for col in cols}
          return data
      elif isinstance(idx, str):
          if idx == self.columns[0]:
              return list(self.index.keys())
          elif idx in self.columns:
              return self.data[idx]
          else:
              raise KeyError(f"Column {idx} not found.")
      elif isinstance(idx, int):
          col_name = self.columns[idx]
          return self.data[col_name]
      else:
          raise TypeError("Invalid index type")'''

    def loc(self, row_idx):
        return {col: self.data[col][row_idx] for col in self.columns}

    def iteritems(self):
        for col_name in self.columns:
            yield col_name, self.data[col_name][:]

    def iterrows(self):
        for index, row_idx in self.index.items():
            yield index, self.loc(row_idx)
        
    def as_type(self, col_name, dtype):
        self.data[col_name] = ListV2(list(map(dtype, list(self.data[col_name]))))

    def drop(self, column_name):
      if column_name in self.columns:
          self.data = {key: value for key, value in self.data.items() if key != column_name}
          self.columns = [col for col in self.columns if col != column_name]
      else:
          print("Column not found in dataset.")
    # def drop(self, labels, axis=0):
    #     if axis == 0:
    #         for label in labels:
    #             row_idx = self.index.pop(label)
    #             for col_name in self.columns:
    #                 self.data[col_name][row_idx] = None
    #     elif axis == 1:
    #         for label in labels:
    #             self.columns.remove(label)
    #             self.data.pop(label)

    def mean(self):
      output = {i: sum(map(float, self.data[i])) / len(self.data[i]) for i in self.columns}
      return output

    def __repr__(self):
        lines = [f",{','.join(self.columns)}"]
        for index, row_idx in self.index.items():
            row = [str(row_idx)]
            for col in self.columns:
                row.append(str(self.data[col][row_idx]))
            lines.append(','.join(row))
        return '\n'.join(lines)