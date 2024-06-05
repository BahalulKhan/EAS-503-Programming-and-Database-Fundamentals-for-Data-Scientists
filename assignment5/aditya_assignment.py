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
#  - set_index
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
 
    types=[list,tuple] 
    def __init__(self,values): 
        self.values= values 
    def __repr__(self): 
        return f'{self.values}' 

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index >= len(self.values):
            raise StopIteration
        value = self.values[self.index]
        self.index += 1
        return value

    def __add__(self, another_values): 
        if type(another_values) == ListV2: 
            if len(self.values) != len(another_values.values): 
                raise ValueError("valuess must have the same length") 
            return ListV2([self.values[i] + another_values.values[i] for i in range(len(self.values))])
        elif type(another_values) in self.types:
            if len(self.values) != len(another_values): 
                raise ValueError("valuess must have the same length")
            return ListV2([self.values[i] + another_values[i] for i in range(len(self.values))]) 
        elif type(another_values) in (int, float): 
            return ListV2([x + another_values for x in self.values]) 
        else:
            raise ValueError("The values must be a list, tuple, int, or float") 
    def __sub__(self, another_values):
        if type(another_values) == ListV2:
            if len(self.values) != len(another_values.values):
                raise ValueError("valuess must have the same length")
            return ListV2([self.values[i] - another_values.values[i] for i in range(len(self.values))])
        elif type(another_values) in self.types: 
            if len(self.values) != len(another_values):
                raise ValueError("valuess must have the same length")
            return ListV2([self.values[i] - another_values[i] for i in range(len(self.values))])
        elif type(another_values) in (int, float): 
            return ListV2([x - another_values for x in self.values])
        else:
            raise ValueError("The values must be a list, tuple, int, or float")
    def __mul__(self, another_values):
        if type(another_values) == ListV2:
            if len(self.values) != len(another_values.values):
                raise ValueError("valuess must have the same length")
            return ListV2([self.values[i] * another_values.values[i] for i in range(len(self.values))])
        elif type(another_values) in self.types: 
            if len(self.values) != len(another_values):
                raise ValueError("valuess must have the same length")
            return ListV2([self.values[i] * another_values[i] for i in range(len(self.values))])
        elif type(another_values) in (int, float):  
            return ListV2([x * another_values for x in self.values])
        else:
            raise ValueError("The values must be a list, tuple, int, or float")
    def __truediv__(self, another_values):
        if type(another_values) == ListV2:
            if len(self.values) != len(another_values.values):
                raise ValueError("valuess must have the same length")
            return ListV2([round(self.values[i] / another_values.values[i],2) for i in range(len(self.values))])
        elif type(another_values) in self.types: 
            if len(self.values) != len(another_values):
                raise ValueError("valuess must have the same length")
            return ListV2([round(self.values[i] / another_values[i] ,2)for i in range(len(self.values))])
        elif type(another_values) in (int, float):  
            return ListV2([round(x / another_values,2) for x in self.values])
        else:
            raise ValueError("The values must be a list, tuple, int, or float")
    def mean(self):
        sum=0
        for x in self.values:
            sum=sum+x
        return sum/len(self.values)
    def append(self,anothervalue):
        return self.values
    def __getitem__(self, key):
        return self.values[key]
    
    
    


class DataFrame:
    def __init__(self, data, columns):
        data1 = []
        for row in data:
            row_dict = {}
            for i, value in enumerate(row): 
                name = columns[i]
                row_dict[name] = ListV2([value])
            data1.append(row_dict)
        self.data = {column:[d[column][0] for d in data1] for column in data1[0]}
        self.columns = columns
        self.n_rows = len(data)
        self.index={}
        self.n_cols = len(columns)
        for i in range(self.n_rows):
            self.index[i]=i
        

    def set_index(self,inputlist):
        setindexdict={}
        for i in range(len(inputlist)):
            setindexdict[inputlist[i]]=int(i)
        self.index=setindexdict
        return self
        
    def iterrows(self):
        reslis = []
        z = list(zip(*self.data.values()))
        studentname = list(self.index.keys())
        for i in range(len(z)):
            result = (studentname[i], tuple(z[i]))
            reslis.append(result)
        return reslis
    
    def iteritems(self):
        return self.data.items()
        
    
    def __repr__(self):
        rows = []
        for i, rowlabel in enumerate(self.index.keys()):
            rowdata = [str(rowlabel)]
            for collabel in self.columns:
                colidx = self.columns.index(collabel)
                rowidx = list(self.index.keys()).index(rowlabel)
                rowdata.append(str(self.data[collabel][rowidx]))
            rows.append(','.join(rowdata))
        return '\n'.join([','.join([''] + list(self.columns))] + rows)


    def __getitem__(self, key):
        if isinstance(key, str):
            return ListV2(self.data[key])
        elif isinstance(key, list):
            new_data = {column: self.data[column] for column in key}
            return DataFrame(data=[list(row) for row in zip(*new_data.values())], columns=key)
        elif isinstance(key, slice):
                start, stop, step = key.start, key.stop, key.step
                if start is None:
                    start = 0
                if stop is None:
                    stop = self.n_rows
                if step is None:
                    step = 1
                new_data = {}
                for column in self.columns:
                    new_data[column] = self.data[column][start:stop:step]
                return DataFrame(data=[list(row) for row in zip(*new_data.values())], columns=self.columns)
        elif isinstance(key, tuple):
            row = key[0]
            col = key[1]
            column_names = list(self.data.keys())
            columns = column_names[col]
            data = [self.data[col] for col in columns]
            all_rows = list(zip(*data))
            output = all_rows[row.start:row.stop:row.step]
            return DataFrame(data=output,columns=columns)

        else:
            raise TypeError(f"Invalid key type: {type(key)}")
    def as_type(self, column, cast_type):
        self.data[column] = list(map(cast_type, self.data[column]))
    def mean(self):
        mean=[]
        for ccol in self.columns:
            sum=0
            for x in self.data[ccol]:
                sum=sum+int(x)
            means=sum/len(self.data[ccol])
            mean.append(means)

        return dict(zip(self.columns,mean))
    
    def drop(self, columns):
        self.data.pop(columns)
        self.columns = [col for col in self.columns if col not in columns]
        self.n_cols = len(self.columns)
        
    def loc(self, *args):
        if len(args) == 1 and args[0] == 0:
            keylist = list(self.data.keys())
            return self.data[keylist[0]]
        elif len(args) == 1 and type(args[0]) != tuple and args[0] > 0:
            row_idx = args[0] - 1
            keylist = list(self.data.keys())
            return self.data[keylist[row_idx]]
        elif len(args) == 1 and type(args[0]) == tuple:
            row_labels, col_labels = args[0][0], args[0][1]

            row_indices = [i for i, key in enumerate(self.index) if key in row_labels]
            col_indices = [i for i in range(self.n_cols) if self.columns[i] in col_labels]
            lines = [[self.data[self.columns[j]][i] if self.columns[j] in self.data and i in row_indices else '' for j in col_indices] for i in row_indices]

            header = col_labels
            return DataFrame(data=lines, columns=header).set_index(row_labels)
        else:
            raise ValueError('Invalid arguments')

    def __len__(self):
        return self.n_rows  



