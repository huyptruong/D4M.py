# Import packages
from __future__ import print_function, division

from scipy import sparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import warnings
import numbers
import random
import string
import csv
import itertools
import math


# Auxiliary/Helper functions

def string_gen(length):
    """ Create randomly-generated string of given length. """
    rand_string = ''
    for _ in range(length):
        rand_string += random.SystemRandom().choice(string.ascii_letters)
    return rand_string


def num_string_gen(length, n):
    """ Create string list of integers <= n of given length. """
    rand_string = [str(random.randint(0, n)) for _ in range(length)] + ['']
    rand_string = ','.join(rand_string)
    return rand_string


def is_numeric(obj):
    """ Check if obj is numeric (int, float, complex, etc) or not. """
    if isinstance(obj, numbers.Number):
        is_num = True
    else:
        is_num = False

    return is_num


def sorted_union(arr_1, arr_2, return_index=False):
    """
    Returns the union of two sorted arrays with index maps (if return_index=True).
        Usage:
            union = sorted_union(arr_1,arr_2)
        Input:
            arr_1 = sorted array of values with no duplicates
            arr_2 = sorted array of values with no duplicates
            return_index = boolean
        Output:
            union = sorted array of values coming from either arr_1 or arr_2
            index_map_1 = list of indices of the elements of arr_1 in union
            index_map_2 = list of indices of the elements of arr_2 in union
        Example:
            sorted_union(np.array([0,1,4,6]), np.array([0,4,7]), return_index = True)
                = np.array([0,1,4,6,7]), [0,1,2,3], [0,2,4]
            sorted_union(np.array([0,1,4,6]), np.array([0,4,7]))
                = np.array([0,1,4,6,7])
    """
    union = list()
    index_map_1 = list()
    index_map_2 = list()
    i_1 = 0
    i_2 = 0

    size_1 = np.size(arr_1)
    size_2 = np.size(arr_2)
    union_size = 0

    while i_1 < size_1 or i_2 < size_2:
        if i_1 >= size_1:
            if return_index:
                index_map_2.append(union_size)
            union.append(arr_2[i_2])
            union_size += 1
            i_2 += 1
        elif i_2 >= size_2:
            if return_index:
                index_map_1.append(union_size)
            union.append(arr_1[i_1])
            union_size += 1
            i_1 += 1
        elif arr_1[i_1] == arr_2[i_2]:
            if return_index:
                index_map_1.append(union_size)
                index_map_2.append(union_size)
            union.append(arr_1[i_1])
            union_size += 1
            i_1 += 1
            i_2 += 1
        elif arr_1[i_1] < arr_2[i_2]:
            if return_index:
                index_map_1.append(union_size)
            union.append(arr_1[i_1])
            union_size += 1
            i_1 += 1
        else:
            if return_index:
                index_map_2.append(union_size)
            union.append(arr_2[i_2])
            union_size += 1
            i_2 += 1

    union = np.array(union)

    if return_index:
        index_map_1 = np.array(index_map_1)
        index_map_2 = np.array(index_map_2)
        return union, index_map_1, index_map_2
    else:
        return union


def sorted_intersect(arr1, arr2,
                     return_index=False, return_index_1=False, return_index_2=False):
    """
    Returns the intersection of two sorted arrays with index maps
    (if return_index, return_index_1, or return_index_2 are True).
        Usage:
            intersection = sorted_intersection(arr_1,arr_2)
        Input:
            arr_1 = sorted array of values with no duplicates
            arr_2 = sorted array of values with no duplicates
            return_index = boolean
        Output:
            intersection = sorted array of values coming from both arr_1 and arr_2
            index_map_1 = list of indices of elements of intersection in arr_1
            index_map_2 = list of indices of elements of intersection in arr_2
        Example:
            sorted_intersect(np.array([0,1,4]), np.array([0,4,7]), return_index = True)
                = np.array([0,4]), [0,2], [0,1]
            sorted_intersect(np.array([0,1,4]), np.array([0,4,7]))
                = np.array([0,4])
    """

    set2 = set(arr2)
    inter = [item for item in arr1 if item in set2]

    if return_index or return_index_1:
        A_index = {arr1[index]: index for index in range(len(arr1))}
        index_map_A = [A_index[x] for x in inter]
    else:
        index_map_A = None

    if return_index or return_index_2:
        B_index = {arr2[index]: index for index in range(len(arr2))}
        index_map_B = [B_index[x] for x in inter]
    else:
        index_map_B = None

    if return_index:
        return np.array(inter), np.array(index_map_A), np.array(index_map_B)
    elif return_index_1:
        return np.array(inter), np.array(index_map_A)
    elif return_index_2:
        return np.array(inter), np.array(index_map_B)
    else:
        return np.array(inter)


def contains(substrings):
    """
    Returns another function which accepts a list of strings and returns the list of indices
    of those strings which contain some element of substrings
        Usage:
            contains("a,b,")
            contains(['a','b'])
        Inputs:
            substrings = string of (delimiter separated) values (delimiter is last character)
                or list of values of length n
        Outputs:
            func(listofstrings) = returns a list of indices of the strings in listofstrings which have some element of
                substrings as a substring
    """
    substrings = sanitize(substrings)

    def func(listofstrings):
        listofstrings = sanitize(listofstrings)
        goodstrings = list()
        for i in range(len(listofstrings)):
            item = listofstrings[i]
            for substring in substrings:
                if substring in item:
                    goodstrings.append(i)
                    break
        return goodstrings

    return func


def startswith(prefixes):
    """
    Returns another function which accepts a list of strings and returns the list of indices
    of those strings which have some element of prefixes as a prefix
        Usage:
            startswith("a,b,")
            startswith(['a','b'])
        Inputs:
            prefixes = string of (delimiter separated) values (delimiter is last character)
                or list of values of length n
        Outputs:
            func(listofstrings) = returns a list of indices of the strings in listofstrings which have some element of
                prefixes as a prefix
    """
    prefixes = sanitize(prefixes)

    def func(listofstrings):
        listofstrings = sanitize(listofstrings)
        goodstrings = list()

        for i in range(len(listofstrings)):
            item = listofstrings[i]
            for prefix in prefixes:
                if item.startswith(prefix):
                    goodstrings.append(i)
                    break
        return goodstrings

    return func


def str_to_num(obj, delimiter=None):
    """ Convert string to float if possible, optionally appending a delimiter otherwise. """
    if isinstance(obj, str):
        try:
            obj = int(obj)
        except ValueError:
            try:
                obj = float(obj)
            except ValueError:
                if delimiter is not None:
                    obj += delimiter
    return obj


def num_to_str(arr):
    """ Convert array of numbers to array of strings. """
    strarr = arr.astype('str')
    return strarr


def sanitize(obj, convert=None):
    """
    Converts strings of (delimiter-separated) values into a list of values
    (the delimiter is the last character),
    iterables into numpy arrays,
    and all other objects into a numpy array having that object.
        Usage:
            sanitized list = sanitize(obj)
        Inputs:
            obj = string of (delimiter separated) values (delimiter is last character)
                or iterable of values of length n or single value
            convert = Boolean indicating whether strings which represent numbers should
                be replaced with numbers
        Outputs:
            list of values
        Examples:
            sanitize("a,b,") = ['a', 'b']
            sanitize("1,1,") = [1, 1]
            sanitize([10, 3]) = [10, 3]
            sanitize(1) = [1]
    """
    if convert is None:
        convert = False

    # Convert delimiter-separated string list by splitting using last character
    try:
        delimiter = obj[-1]
        obj = obj.split(delimiter)
        obj.pop()  # Get rid of empty strings

        # Convert to numbers if requested
        if convert:
            obj = [str_to_num(item) for item in obj]  # Convert applicable items to numbers

    except (AttributeError, IndexError, TypeError):
        pass

    # Convert to numpy array
    if not isinstance(obj, np.ndarray):
        if hasattr(obj, '__iter__'):
            obj = np.array(obj, dtype=object)  # use dtype=object to prevent silent upcasting
        else:
            obj = np.array([obj])

    return obj


def length(iterable):
    """ Return length of iterable. """

    if isinstance(iterable, np.ndarray):
        return np.size(iterable)
    else:
        return len(iterable)


def unique(iterable, return_index=None, return_inverse=None):
    """ Uniquify and sorts an iterable, optionally providing index maps. """

    if return_index is None:
        return_index = False
    if return_inverse is None:
        return_inverse = False

    if isinstance(iterable, np.ndarray):
        return np.unique(iterable, return_index=return_index, return_inverse=return_inverse)
    else:  # Assume iterable is a list

        # If no index maps needed, extract unique items in iterable and sort
        if not (return_index or return_inverse):
            return sorted(list(dict.fromkeys(iterable)))

        # If both index maps are needed, loop to extract unique items and build partial maps, then sort
        elif return_index and return_inverse:
            sui = list()
            seen = dict()
            index_map_unique = list()
            index_map_unique_inverse = list()
            latest = 0
            for index in range(len(iterable)):
                item = iterable[index]
                if item in seen.keys():
                    index_map_unique_inverse.append(seen[item])
                else:
                    index_map_unique_inverse.append(latest)
                    index_map_unique.append(index)
                    seen[item] = latest
                    latest += 1
                    sui.append(item)

            sorting_map = sorted(range(len(sui)), key=lambda k: sui[k])
            sorting_map_inverse = list(np.arange(len(sorting_map))[np.argsort(sorting_map)])
            sui = [sui[i] for i in sorting_map]

            index_map = [index_map_unique[i] for i in sorting_map]
            index_map_inverse = [sorting_map_inverse[i] for i in index_map_unique_inverse]

            return sui, index_map, index_map_inverse

        # Same as above but do not build index_map_inverse
        elif return_index and not return_inverse:
            sui = list()
            seen = set()
            index_map_unique = list()
            for index in range(len(iterable)):
                item = iterable[index]
                if item in seen:
                    pass
                else:
                    seen.add(item)
                    index_map_unique.append(index)
                    sui.append(item)

            sorting_map = sorted(range(len(sui)), key=lambda k: sui[k])
            sui = [sui[i] for i in sorting_map]

            index_map = [index_map_unique[i] for i in sorting_map]

            return sui, index_map

        # Same as above, but do not build index_map
        else:
            sui = list()
            seen = dict()
            index_map_unique_inverse = list()
            latest = 0
            for index in range(len(iterable)):
                item = iterable[index]
                if item in seen.keys():
                    index_map_unique_inverse.append(seen[item])
                else:
                    index_map_unique_inverse.append(latest)
                    seen[item] = latest
                    latest += 1
                    sui.append(item)

            sorting_map = sorted(range(len(sui)), key=lambda k: sui[k])
            sorting_map_inverse = list(np.arange(len(sorting_map))[np.argsort(sorting_map)])
            sui = [sui[i] for i in sorting_map]

            index_map_inverse = [sorting_map_inverse[i] for i in index_map_unique_inverse]

            return sui, index_map_inverse


def aggregate(row, col, val, func):
    """
        Aggregate (row[i], col[i], val[i]) triples using func as collision function.
            Usage:
                aggregate(row, col, val, func)
            Inputs:
                row = array of objects of length n
                col = array of objects of length n
                val = array of objects of length n
                func = collision function (e.g. add, times, max, min, first, last)
            Output:
                newrow, newcol, newval = subarrays of row, col, val in which pairs (r, c) = (newrow[i], newcol[i])
                                            are unique and newval[i] is the resulting of iteratively
                                            applying func to the values corresponding to triples
                                            (r, c, value) = (row[j], col[j], val[j])
            Example:
                aggregate(['a', 'a', 'b'], ['A', 'A', 'B'], [1, 2, 3], add) = ['a', 'b'], ['A', 'B'], [3, 3]
                aggregate(['a', 'a', 'b'], ['A', 'A', 'B'], [1, 2, 3], first) = ['a', 'b'], ['A', 'B'], [1, 3]
                aggregate(['a', 'a', 'b'], ['A', 'A', 'B'], [1, 2, 3], last) = ['a', 'b'], ['A', 'B'], [2, 3]
                aggregate(['a', 'a', 'a', 'b'], ['A', 'A', 'A', 'B'], [1, 2, 0, 3], min)
                        = ['a', 'b'], ['A', 'B'], [0, 3]
                (where lists are stand-ins for the corresponding numpy arrays)
    """
    agg_dict = dict()
    for k in range(np.size(row)):
        if (row[k], col[k]) not in agg_dict:
            agg_dict[(row[k], col[k])] = val[k]
        else:
            agg_dict[(row[k], col[k])] = func(agg_dict[(row[k], col[k])], val[k])

    newrow = np.array([item[0] for item in list(agg_dict.keys())])
    newcol = np.array([item[1] for item in list(agg_dict.keys())])
    newval = np.array(list(agg_dict.values()))
    return newrow, newcol, newval


def add(a, b):
    """ Binary addition. """
    return a + b


def times(a, b):
    """ Binary multiplication. """
    return a * b


def first(a, b):
    """ Binary projection onto first coordinate (Returns first argument). """
    return a


def last(a, b):
    """ Binary projection onto last coordinate (Returns last argument). """
    return b


def catstr(s1, s2, sep=None):
    """ Concatenate strings/numbers s1 and s2 with separator sep between them. """
    s1 = num_to_str(s1)
    s2 = num_to_str(s2)
    if sep is None:
        sep = '|'
    separr = np.full(1, sep)
    s1sep = np.core.defchararray.add(s1, separr)
    s12 = np.core.defchararray.add(s1sep, s2)
    return s12


def val2col(A, splitSep=None):
    """
        Converts from adjacency array to incidence array.
            Usage:
                val2col(A,splitSep)
            Inputs:
                A = Associative Array
                splitSep = (new) delimiting character (default '|') to separate column labels from values
            Output:
                val2col(A,splitSep) = Associative Array B where B.row == A.row and
                                        B[rowlabel, collabel+splitSep+value] == 1 if and only if
                                        A[rowlabel, collabel] == value
    """
    r, cType, cVal = A.find()
    cType = num_to_str(cType)
    cVal = num_to_str(cVal)
    if splitSep is None:
        splitSep = '|'
    c = catstr(cType, cVal, splitSep)
    A = Assoc(r, c, 1)
    return A


def col2type(A, splitSep=None):
    """
        Splits column keys of associative array and sorts first part as column key and second part as value.
        Inverse of val2col.
            Usage:
                B = col2type(A, splitSep)
            Inputs:
                A = Associative array with string column keys assumed to be of the form 'key'+splitSep+'val'
                splitSep = separator for A's column keys (default '|')
            Outputs:
                col2type(A, splitSep) = Associative array whose row keys are the same as A, but whose column keys
                                        are the first parts of A's column keys and whose values are the second
                                        parts of A's column keys
            Example:
                col2type(A, '|')
                col2type(A, '/')
            Note:
                - A's column keys must be in the desired form.
    """
    
    # Extract row and column keys from A
    r, c, v = A.find()
    if splitSep is None:
        splitSep = '|'
    
    # Split column keys according to splitSep
    try:
        elsplit = [colkey.split(splitSep) for colkey in c]
    except:
        raise ValueError('Input column keys not of correct form.')
    
    # Extract column types and values
    cType = [item[0] for item in elsplit]
    cVal = [item[1] for item in elsplit]
    
    B = Assoc(r, cType, cVal)
    
    return B


# Main class and methods

# noinspection PyPep8Naming
class Assoc:
    """
    Associative arrays, supporting basic sparse linear algebra on sparse matrices with
    values of variable (string or numerical) type, variable operations (plus-times, max-min, etc)
    and row and column indices of variable (string or numerical) type.

    Structure:
        row = sorted array of strings/numbers (row indices)
        col = sorted array of strings/numbers (column indices)
        val = sorted array of values
                or 1.0 to indicate that all the values are numerical and stored in adj
        adj = adjacency array implemented as sparse matrix (COO format)
            if val==1.0 then adj is a sparse matrix containing the actual numerical values
            otherwise
            adj[row_id,col_id] = index+1 of corresponding value in val, or 0 if empty
    """

    def __init__(self, row, col, val, arg=None):
        """
        Constructs an associative array either from an existing sparse matrix (spmatrix) or
        from row, column, and value triples.
            Usage:
                A = Assoc(row,col,val)
                A = Assoc(row,col,val,func)
                A = Assoc(row,col,number,func)
                A = Assoc(row,col,val,sparse_matrix)
            Inputs:
                row = string of (delimiter separated) values (delimiter is last character)
                    or list of values of length n
                col = string of (delimiter separated) values (delimiter is last character)
                    or list of values of length n
                val = string of (delimiter separated) values (delimiter is last character)
                    or list of values of length n
                    or 1.0 (which signals arg to be a sparse matrix)
                    or other single value
                arg = either
                        a sparse matrix (to be used as the adjacency array) where
                            - if val=1.0, then arg is expected to contain the _actual_ values
                            - otherwise, val is expected to be a list of _actual_ values;
                                unique sorted entries in row, col, val are extracted
                                and the row/column indices and values of arg are assumed to match
                                up with the resulting row, col, val
                        or string representing collision function,
                            e.g. add, first, last, min, max
                            default is min
                        or "unique" which assumes there are no collisions
            Outputs:
                A = Associative array made from the triples row, col, and val
            Examples:
                A = Assoc('r1,r2,', 'c1,c2,', 'v1;v2;')
                A = Assoc(['r1','r2'], 'c1/c2/', [1,2], sum)
                A = Assoc('1,', 'c1,', np.array([3]))
                A = Assoc('r1,r2,', 'c1,c2,', 1.0, sparse_matrix)
            Notes:
                - If expected data is numerical, arg=add gives slight speed-up
                - If val == 1.0 and optional sparse matrix is supplied, it will be used as the adjacency array
                    where the row and column indices of the sparse matrix will be assumed to correspond
                    to the ordered row and col. Will throw an error if they aren't of the appropriate sizes.
                - To determine whether the data is numerical, values are sorted and the last element is examined.
                    From testing, Numpy appears to sort all non-numerical data types (strings, arrays, lists,
                    dicts, tuples, sets) to come after numerical data, so this should indicate whether there is
                    any non-numerical data.
        """

        # Sanitize
        row = sanitize(row)
        col = sanitize(col)

        row_size = np.size(row)
        col_size = np.size(col)

        single_val = False

        # Short-circuit if empty assoc
        if row_size == 0 or col_size == 0 or np.size(val) == 0:
            self.row = np.empty(0)
            self.col = np.empty(0)
            self.val = 1.0  # Considered numerical
            self.adj = sparse.coo_matrix(([], ([], [])), shape=(0, 0))  # Empty sparse matrix
        else:
            # Handle data

            # Case 1: sparse matrix provided which contains pointers to actual values
            if sparse.issparse(arg) and val != 1.0:
                arg.sum_duplicates()

                val = sanitize(val, convert=True)
                self.row = np.unique(row)
                self.col = np.unique(col)
                self.val = np.unique(val)
                self.adj = arg.tocoo()

                (rowdim, coldim) = self.adj.shape

                # Ensure that there are enough unique row, col, vals to make sense of adj
                errormessage = 'Invalid input:'
                goodrow = np.size(self.row) >= rowdim
                goodcol = np.size(self.col) >= coldim
                goodval = np.size(self.val) >= np.size(np.unique(self.adj.data))
                if not goodrow:
                    errormessage += ' not enough unique row indices'
                    if not goodcol or not goodval:
                        errormessage += ','
                    else:
                        errormessage += '.'
                if not goodcol:
                    errormessage += ' not enough unique col indices'
                    if not goodval:
                        errormessage += ','
                    else:
                        errormessage += '.'
                if not goodval:
                    errormessage += ' not enough unique values.'

                if not (goodrow and goodcol and goodval):
                    raise ValueError(errormessage)

            # Case 2: sparse matrix provided which contains actual values
            elif sparse.issparse(arg) and val == 1.0:
                arg.sum_duplicates()

                self.row = np.unique(row)
                self.col = np.unique(col)
                self.val = 1.0
                self.adj = arg.tocoo()

                if (np.size(self.row), np.size(self.col)) != arg.shape:
                    raise ValueError("Unique row and column indices do not match sp_matrix.")

            # Case 3: No sparse matrix provided
            else:
                val = sanitize(val, convert=True)
                val_size = np.size(val)

                # If single value (or no value) is given for row/col/val, extend to proper length
                N = max(row_size, col_size, val_size)
                if row_size == 1:
                    row = np.full(N, row[0])
                    row_size = N
                if col_size == 1:
                    col = np.full(N, col[0])
                    col_size = N
                if val_size == 1:
                    val = np.full(N, val[0])
                    val_size = N
                    single_val = True

                # Check that row, col, and val have same length
                if min(row_size, col_size, val_size) != N:
                    raise ValueError("Invalid input: row, col, val must have compatible lengths.")

                # In case single value was given or arg is sum or expecting unique, don't bother aggregating now
                if single_val or arg == add or arg == "unique":
                    pass
                else:
                    if arg is None:
                        arg = min

                    row, col, val = aggregate(row, col, val, arg)

                # Get unique sorted row and column indices
                self.row, fromrow = np.unique(row, return_inverse=True)
                self.col, fromcol = np.unique(col, return_inverse=True)
                self.val, fromval = np.unique(val, return_inverse=True)

                # Check if numerical; numpy sorts numerical values to front, so only check last entry
                if is_numeric(self.val[-1]):
                    self.adj = sparse.coo_matrix((val, (fromrow, fromcol)), dtype=float,
                                                 shape=(np.size(self.row), np.size(self.col)))
                    self.val = 1.0

                    if single_val and arg != add:
                        self.adj.data[:] = val[0]
                elif single_val:
                    self.adj = sparse.coo_matrix((np.ones(row_size), (fromrow, fromcol)))
                else:
                    # If not numerical, self.adj has entries given by indices+1 of self.val
                    val_indices = fromval + np.ones(np.size(fromval))
                    self.adj = sparse.coo_matrix((val_indices, (fromrow, fromcol)), dtype=int)

        self.adj.sum_duplicates()

    def find(self, orderby=None):
        """
            Get row, col, and val arrays that would generate the Assoc (reverse constructor).
                Usage:
                    self.find()
                Input:
                    self = Associative Array
                    orderby = optional paramater to control the ordering of result.
                                if 0, then order by row first, then column
                                if 1, then order by column first, then row
                                if None, no particular order is guaranteed
                Output:
                    row,col,val = arrays for which self = Assoc(row,col,val)
        """
        # Use self.adj to extract row, col, and val
        if orderby == 0:  # Order by row first, then column
            row_adj = self.adj.tocsr().tocoo()
            enc_val, enc_row, enc_col = row_adj.data, row_adj.row, row_adj.col
        elif orderby == 1:  # Order by column first, then row
            col_adj = self.adj.tocsc().tocoo()
            enc_val, enc_row, enc_col = col_adj.data, col_adj.row, col_adj.col
        else:  # Otherwise don't order
            enc_val, enc_row, enc_col = self.adj.data, self.adj.row, self.adj.col

        if np.size(enc_row) != 0:
            row = self.row[enc_row]
        else:
            row = np.array([])
        if np.size(enc_col) != 0:
            col = self.col[enc_col]
        else:
            col = np.array([])

        if isinstance(self.val, float):
            val = enc_val
        else:
            enc_val = [int(item - 1) for item in enc_val]
            if np.size(enc_val) != 0:
                val = self.val[enc_val]
            else:
                val = np.array([])

        return row, col, val

    def dict(self):
        """ Returns a two-dimensional dictionary adj_dict for which adj_dict[index1][index2]=value. """
        row, col, val = self.find()
        adj_dict = dict()

        for index in range(np.size(row)):
            if row[index] not in adj_dict:
                adj_dict[row[index]] = {col[index]: val[index]}
            else:
                adj_dict[row[index]][col[index]] = val[index]

        return adj_dict

    def getval(self):
        """ Returns list of unique values. """
        if isinstance(self.val, float):
            unique_values = np.unique(self.adj.data)
        else:
            unique_values = self.val

        return unique_values


    # print tabular form
    def printfull(self):
        """ Print associative array in tabular form. """

        df = pd.DataFrame(self.dict())
        df = df.transpose()  # Transpose it to get correct order of rows/cols

        # Replace NaN's with empty string
        df.fillna('', inplace=True)

        print(df)
        return None

    def spy(self):
        """ Print spy plot of self.adj """
        plt.spy(self.adj, markersize=0.2, aspect='auto')
        plt.show()
        return None

    # Overload print
    def __str__(self):
        """ Print the attributes of associative array. """
        print_string = "Row indices: " + str(self.row) + "\n"
        print_string += "Column indices: " + str(self.col) + "\n"
        print_string += "Values: " + str(self.val) + "\n"
        print_string += "Adjacency array: " + "\n" + str(self.adj.toarray())
        return print_string

    def triples(self, orderby=None):
        """ Return list of triples of form (row_label,col_label,value). """
        r, c, v = self.find(orderby=orderby)
        triples = list(zip(list(r), list(c), list(v)))
        return triples

    def getvalue(self, rowkey, colkey):
        """
        Get the value in self corresponding to given rowkey and colkey, otherwise return 0.
            Usage:
                v = A.getvalue('a', 'B')
            Inputs:
                A = self = Associative Array
                rowkey = row key
                colkey = column key
            Output:
                v = value of A corresponding to the pair (rowkey, colkey), i.e. (rowkey, colkey, v) is in A.triples()
            Note:
                If either of rowkey or colkey are integers, they are taken as indices instead of *actual*
                row and column keys, respectively.
        """

        if not isinstance(rowkey, int) and rowkey in self.row:
            index1 = np.where(self.row == rowkey)[0][0]
        else:
            index1 = rowkey

        if not isinstance(colkey, int) and colkey in self.col:
            index2 = np.where(self.col == colkey)[0][0]
        else:
            index2 = colkey

        if isinstance(self.val, float):
            try:
                return self.adj.todok()[index1, index2]
            except (IndexError, TypeError):
                return 0
        else:
            try:
                return self.val[self.adj.todok()[index1, index2] - 1]
            except (IndexError, TypeError):
                return 0

    # Overload getitem; allows for subsref
    def __getitem__(self, obj):
        """
        Returns a sub-associative array of self according to object1 and object2 or corresponding value
            Usage:
                B = A[object1,object2]
            Inputs:
                A = Associative Array
                obj = tuple (object1,object2) where
                    object1 = string of (delimiter separate) values (delimiter is last character)
                        or iterable or int or slice object or function
                    object2 = string of (delimiter separate) values (delimiter is last character)
                        or iterable or int or slice object or function
                        e.g. "a,:,b,", "a,b,c,d,", ['a',':','b'], 3, [1,2], 1:2, startswith("a,b,"),
                            "a *,"
            Outputs:
                B = sub-associative array of A whose row indices are selected by object1 and whose
                    column indices are selected by object2, assuming not both of object1, object2 are single
                    indices
                B = value of A corresponding to single indices of object1 and object2
            Examples:
                A['a,:,b,',['0','1']]
                A[1:2:1, 1]
            Note:
                - Regular slices are NOT right end-point inclusive
                - 'Slices' of the form "a,:,b," ARE right end-point inclusive (i.e. includes b)
                - Integer object1 or object2, and by extension slices, do not reference A.row or A.col,
                    but the induced indexing of the rows and columns
                    e.g. A[:,0:2] will give the subarray consisting of all rows and the columns col[0], col[1],
                        A[:,0] will give the subarray consisting of the 0-th column
                        A[2,4] will give the value in the 2-nd row and 4-th column
        """
        keys = [self.row, self.col]
        object1, object2 = obj
        obj = [object1, object2]

        # For each object, replace with corresponding array of row/col keys
        for index in [0, 1]:
            objecti = obj[index]
            # If object is a single integer, replace with corresponding row/col key
            if isinstance(objecti, int):
                obj[index] = [keys[index][objecti]]
                continue

            # If object is an iterable of integers, replace with corresponding row/col keys
            all_integers = True
            if hasattr(objecti, '__iter__'):
                for item in objecti:
                    if not isinstance(item, int):
                        all_integers = False
                        break
            else:
                all_integers = False

            if all_integers:
                obj[index] = keys[index][objecti]
                continue

            # If object is a function on iterables returing list of indices, apply it
            if callable(objecti):
                obj[index] = keys[index][objecti(keys[index])]
                continue

            # If object is a slice object, convert to appropriate list of keys
            if isinstance(objecti, slice):
                obj[index] = keys[index][objecti]
                continue

            # If object is of form ":", convert to appropriate list of keys
            if isinstance(objecti, str):
                if objecti == ":":
                    obj[index] = keys[index]
                    continue

            # Then, or otherwise, sanitize to get appropriate list of keys
            objecti = sanitize(objecti)

            # If resulting object is 'slice-like', replace with appropriate list of keys,
            # getting all keys where objecti[0] <= element <= objecti[2]
            # so find first index of key with objecti[0] <= key and first index of key with
            # objecti[2] < key (so all earlier keys are <= objecti[2]).

            if len(objecti) == 3 and objecti[1] == ":":
                start_compare = (keys[index] >= objecti[0])
                stop_compare = (keys[index] > object1[2])
                try:
                    start_index = np.argwhere(start_compare)[0][0]
                except IndexError:
                    start_index = np.size(keys[index])
                try:
                    stop_index = np.argwhere(stop_compare)[0][0]
                except IndexError:
                    stop_index = np.size(keys[index])
                obj[index] = keys[index][start_index:stop_index]

            obj[index] = objecti

        # Now everything is a list of row/col keys
        object1, object2 = obj

        # Create new row, col, val triple to construct sub-assoc array
        object1 = np.sort(object1)
        object2 = np.sort(object2)

        newrow, row_index_map = sorted_intersect(self.row, object1, return_index_1=True)
        newcol, col_index_map = sorted_intersect(self.col, object2, return_index_1=True)

        B = Assoc([], [], [])
        B.row = np.array(newrow)
        B.col = np.array(newcol)
        B.val = self.val
        B.adj = self.adj.tocsr()[row_index_map, :][:, col_index_map].tocoo()

        B = B.condense()
        B = B.deepcondense()

        return B

    # Overload setitem
    def __setitem__(self, col_index, row_index, value):
        return NotImplemented

    def copy(self):
        """ Creates a copy of self. """
        A = Assoc([], [], [])
        A.row = self.row.copy()
        A.col = self.col.copy()
        if isinstance(self.val, float):
            A.val = 1.0
        else:
            A.val = self.val.copy()
        A.adj = self.adj.copy()

        return A

    def size(self):
        """ Returns dimensions of self. """
        size1 = np.size(self.row)
        size2 = np.size(self.col)
        return size1, size2

    def nnz(self):
        """
        Returns number of stored entries.
            Usage:
                A.nnz()
            Input:
                self = Associative array
            Output:
                The number of stored entries (i.e., the number of entries in the adjacency array).
            Notes:
                - If null values (0, None, '') are explicitly stored in the array, then they are counted. To count only
                    non-null values, use self.get_nonzero()
        """
        nnz = self.adj.getnnz()
        return nnz

    def count_nonzero(self):
        """
        Returns number of non-null stored entries.
            Usage:
                A.count_nonzero()
            Input:
                self = Associative array
            Output:
                The number of stored non-null entries (i.e., the number of non-null entries in the adjacency array).
            Notes:
                - If null values (0, None, '') are explicitly stored in the array, then they are not counted. To count
                only all stored values, use self.nnz()
        """
        null = [0, None, '']

        # If data is numerical, return number of nonzero values.
        if isinstance(self.val, float):
            nonzero = np.where(self.adj.data)
            actual_nnz = np.size(nonzero)
        # Otherwise, check against list of null values
        else:
            _, _, val = self.find()
            nonzero = [value not in null for value in val]
            actual_nnz = np.size(val[nonzero])

        return actual_nnz

    # Remove zeros/empty strings/None from being recorded
    def dropzeros(self, copy=False):
        """
        Return copy of Assoc without null values recorded.
            Usage:
                A.dropzeros()
                A.dropzeros(copy = True)
            Inputs:
                self = Associative array
                copy = Whether a new Assoc instance should be made or
                    if existing instance should be modified
            Outputs:
                Associative subarray of A consisting only of non-null values
            Notes:
                - Null values include 0, '', and None
        """

        # Enumerate the 'null' values
        null = ['', 0, None]

        # If numerical, just use scipy.sparse's eliminate_zeros()
        if isinstance(self.val, float):
            if not copy:
                A = self
            else:
                A = self.copy()

            # Remove zeros and update row and col appropriately
            A.adj.eliminate_zeros()
            A.condense()
        # Otherwise, manually remove and remake Assoc instance
        else:
            if not copy:
                A = self
            else:
                A = Assoc([], [], [])

            row, col, val = self.find()

            # Determine which values are non-zero
            good_indices = [value not in null for value in val]

            # Remove the row/col/val triples that correspond to a zero value
            row = row[good_indices]
            col = col[good_indices]
            val = val[good_indices]

            # Get unique sorted row and column indices
            A.row, fromrow = np.unique(row, return_inverse=True)
            A.col, fromcol = np.unique(col, return_inverse=True)
            A.val, fromval = np.unique(val, return_inverse=True)

            # Fix empty results
            if np.size(A.row) == 0:
                A.row = np.array([])
            if np.size(A.col) == 0:
                A.col = np.array([])
            if np.size(A.val) == 0:
                A.val = 1.0

            # Make adjacency array
            val_indices = fromval + np.ones(np.size(fromval))
            A.adj = sparse.coo_matrix((val_indices, (fromrow, fromcol)), dtype=int,
                                      shape=(np.size(A.row), np.size(A.col)))

        return A

    # Redefine adjacency array
    def setadj(self, new_adj):
        """
            Replace the adjacency array of self with new_adj. (in-place)
                Usage:
                    A.setadj(new_adj)
                Input:
                    self = Associative array
                    new_adj = A sparse matrix whose dimensions are at least that of self.
                Output:
                    self = Associative array with given sparse matrix as adjacency array
                        and row and column values cut down to fit the dimensions of the
                        new adjacency array
        """
        self.val = 1.0

        # Get shape of new_adj and cut down self.row/self.col to size
        (row_size, col_size) = new_adj.shape

        if np.size(self.row) < row_size or np.size(self.col) < col_size:
            raise ValueError("new_adj is too large for existing row and column indices.")
        else:
            self.row = self.row[0:row_size]
            self.col = self.col[0:col_size]
            self.adj = new_adj.tocoo()

        return self

    # Get diagonal; output as a numpy array
    def diag(self):
        """ Output the diagonal of self.arg as a numpy array. """
        enc_diag = self.adj.diagonal()
        if isinstance(self.val, float):
            diag = enc_diag
        else:
            # Append 0 to the start of self.val so that indices of enc_kdiag match up
            inc_val = np.append(np.zeros(1), self.val)
            diag = inc_val[enc_diag]
        return diag

    def sum(self, axis=None):
        """
            Sum over the given axis or over whole array if None.
                Usage:
                    A.sum()
                    A.sum(0)
                    A.sum(1)
                Input:
                    self = Associative array
                    axis = 0 if summing down columns, 1 if summing across rows, and None if over whole array
                Output:
                    A.sum(axis) = Associative array resulting from summing over indicated axis
        """

        # If any of the values are strings, convert to logical
        # In this case, the adjacency array is the desired sparse matrix to sum over
        if not isinstance(self.val, float):
            new_sparse = self.logical(copy=True).adj.copy()
        # Otherwise, build a new sparse matrix with actual (numerical) values
        else:
            new_sparse = self.adj.copy()

        # Sum as a sparse matrix over desired axis
        summed_sparse = new_sparse.sum(axis)

        # Depending on axis, build associative array
        if axis is None:
            A = summed_sparse
        elif axis == 1:
            A = Assoc([], [], [])
            A.row = self.row.copy()
            A.col = np.array([0])
            A.val = 1.0
            A.adj = sparse.coo_matrix(summed_sparse)

        elif axis == 0:
            A = Assoc([], [], [])
            A.row = np.array([0])
            A.col = self.col.copy()
            A.val = 1.0
            A.adj = sparse.coo_matrix(summed_sparse)
        else:
            A = None

        return A

    # replace all non-zero values with ones
    def logical(self, copy=True):
        """
            Replaces every non-zero value with 1.0
                Usage:
                    A.logical()
                    A.logical(copy=False)
                Input:
                    self = Associative array
                    copy = boolean indicating whether the operation is in-place or not
                Output:
                    self.logical() = a copy of self with all non-zero values replaced with 1.0
                    self.logical(copy=False) = self with all non-zero values replaced with 1.0
        """
        if copy:
            A = self.dropzeros(copy=True)
        else:
            A = self.dropzeros()

        A.val = 1.0

        A.adj.data[:] = 1.0
        return A

    # Overload element-wise addition
    def __add__(self, B):
        """
            Element-wise addition of self and B, matched up by row and column indices.
                Usage:
                    A + B
                Input:
                    A = self = Associative array
                    B = Associative array
                Output:
                    A + B =
                        * element-wise sum of A and B (if both A and B are numerical)
                        * element-wise minimum of A and B otherwise
                Note:
                    - When either A or B are non-numerical the .logical() method is run on them.
        """

        A = self

        if isinstance(A.val, float) and isinstance(B.val, float):
            # Take union of rows and cols while keeping track of indices
            row_union, row_index_A, row_index_B = sorted_union(A.row, B.row, return_index=True)
            col_union, col_index_A, col_index_B = sorted_union(A.col, B.col, return_index=True)

            row = np.append(row_index_A[A.adj.row], row_index_B[B.adj.row])
            col = np.append(col_index_A[A.adj.col], col_index_B[B.adj.col])
            val = np.append(A.adj.data, B.adj.data)

            # Make sparse matrix and sum duplicates
            C = Assoc([], [], [])
            C.row = row_union
            C.col = col_union
            C.val = 1.0
            C.adj = sparse.coo_matrix((val, (row, col)),
                                      shape=(np.size(row_union), np.size(col_union)))
            C.adj.sum_duplicates()
        else:
            # Take union of rows, cols, and vals
            rowA, colA, valA = A.find()
            rowB, colB, valB = B.find()
            row = np.append(rowA, rowB)
            col = np.append(colA, colB)
            val = np.append(valA, valB)

            # Construct with min as collision function
            C = Assoc(row, col, val, min)

        return C

    def __sub__(self, B):
        """ Subtract array B from array A=self, i.e. A-B. """

        A = self
        C = B.copy()

        # If not numerical, convert to logical
        if not isinstance(A.val, float):
            A = A.logical(copy=True)
        if not isinstance(B.val, float):
            C = C.logical(copy=True)

        # Negate second array argument's numerical data
        C.adj.data = -C.adj.data

        D = A + C
        return D

    # Overload matrix multiplication
    def __mul__(self, B):
        """
            Array multiplication of A and B, with A's column indices matched up with B's row indices
                Usage:
                    A * B
                Input:
                    A = self = Associative array
                    B = Associative array
                Output:
                    A * B = array multiplication of A and B
                Note:
                    - When either A or B are non-numerical the .logical() method is run on them.
        """

        A = self
        # If either A=self or B are not numerical, replace with logical()
        if not isinstance(A.val, float):
            A = A.logical()
        if not isinstance(B.val, float):
            B = B.logical()

        # Convert to CSR format for better performance
        A_sparse = A.adj.tocsr()
        B_sparse = B.adj.tocsr()

        # Intersect A.col and B.row
        intersection, index_map_1, index_map_2 = sorted_intersect(A.col, B.row,
                                                                  return_index=True)

        # Get appropriate sub-matrices
        A_sparse = A_sparse[:, index_map_1]
        B_sparse = B_sparse[index_map_2, :]

        # Multiply sparse matrices
        AB_sparse = A_sparse * B_sparse

        # Construct Assoc array
        AB = Assoc([], [], [])  # Construct empty array
        AB.row = A.row
        AB.col = B.col
        AB.val = 1.0
        AB.adj = AB_sparse.tocoo()

        return AB

    # element-wise multiplication
    def multiply(self, B):
        """
            Element-wise multiplication of self and B, matched up by row and column indices.
                Usage:
                    A.multiply(B)
                Input:
                    A = self = Associative array
                    B = Associative array
                Output:
                    A + B = element-wise product of A and B
                Note:
                    - When either A or B are non-numerical the .logical() method is run on them.
        """

        A = self
        # Only multiply if both numerical, so logical() as appropriate
        if not isinstance(B.val, float):
            B = B.logical()
        if not isinstance(A.val, float):
            A = A.logical()

        row_int, row_index_A, row_index_B = sorted_intersect(A.row, B.row, return_index=True)
        col_int, col_index_A, col_index_B = sorted_intersect(A.col, B.col, return_index=True)

        C = Assoc([], [], [])
        C.row = row_int
        C.col = col_int
        C.val = 1.0
        Asub = A.adj.tocsr()[:, col_index_A][row_index_A, :]
        Bsub = B.adj.tocsr()[:, col_index_B][row_index_B, :]
        C.adj = Asub.multiply(Bsub).tocoo()

        return C

    def transpose(self, copy=True):
        """ Transpose array, switching self.row and self.col and transposing self.adj. """
        if copy:
            A = Assoc([], [], [])
            A.row = self.col.copy()
            A.col = self.row.copy()
            if isinstance(self.val, float):
                A.val = 1.0
            else:
                A.val = self.val.copy()
            A.adj = self.adj.copy().transpose()
        else:
            A = self
            temp = self.row.copy()
            self.row = self.col
            self.col = temp
            self.adj = self.adj.transpose()

        return A

    # Remove row/col indices that do not appear in the data
    def condense(self):
        """
            Remove items from self.row and self.col which do not correspond to values, according to self.adj.
                Usage:
                    A.condense()
                    B = A.condense()
                Input:
                    self = Associative array
                Output:
                    self = self.condense() = Associative array which removes all elements of self.row and self.col
                            which are not associated with some (nonzero) value.
                Notes:
                    - In-place operation.
                    - Elements of self.row or self.col which correspond to rows or columns of all 0's
                        (but not '' or None) are removed.
        """
        row, col, _ = self.find()

        # First do row, determine which indices in self.row show up in row, get index map, and select
        present_row = np.isin(self.row, row)
        index_map = np.where(present_row)[0]

        self.row = self.row[present_row]
        self.adj = self.adj.tocsr()[index_map, :].tocoo()  # Removes indices corresponding to zero rows

        # Col
        present_col = np.isin(self.col, col)
        index_map = np.where(present_col)[0]

        self.col = self.col[present_col]
        self.adj = self.adj.tocsr()[:, index_map].tocoo()  # Removes indices corresponding to zero cols

        return self

    # extension of condense() which also removes unused values
    def deepcondense(self):
        """ Remove values from self.val which are not reflected in self.adj. """

        # If numerical, do nothing (no unused values)
        if isinstance(self.val, float):
            return self
        else:
            # Otherwise, re-run corresponding part of constructor

            # Get actually-used row,col,val
            row, col, val = self.find()

            # Get unique sorted row, column indices and values
            self.row, fromrow = np.unique(row, return_inverse=True)
            self.col, fromcol = np.unique(col, return_inverse=True)
            self.val, fromval = np.unique(val, return_inverse=True)

            # Remake adjacency array
            val_indices = fromval + np.ones(np.size(fromval))
            self.adj = sparse.coo_matrix((val_indices, (fromrow, fromcol)), dtype=int,
                                         shape=(np.size(self.row), np.size(self.col)))

            # If self.val is now empty, replace with 1.0
            if np.size(self.val) == 0:
                self.val = 1.0

            return self

    # Eliminate columns
    def nocol(self, copy=True):
        """ Eliminate columns.
            Usage:
                A.nocol()
                A.nocol(copy=False)
            Input:
                copy = boolean indicating whether operation should be in-place
            Output:
                A.nocol() = Associative array with same row indices as A and single column index 0.
                            The i-th row of A.nocol() is 1 only when the i-th row of A had a non-zero entry.
                A.nocol(copy=False) = in-place version
        """
        if copy:
            A = self.copy()
        else:
            A = self

        # Take logical, sum over rows, then logical again
        A.logical(copy=False)
        A = A.sum(1)
        A.logical(copy=False)
        A.col = np.array([0])

        return A

    # Eliminate rows
    def norow(self, copy=True):
        """ Eliminate rows.
            Usage:
                A.norow()
                A.norow(copy=False)
            Input:
                copy = boolean indicating whether operation should be in-place
            Output:
                A.norow() = Associative array with same col indices as A and single row index 0.
                            The i-th col of A.norow() is 1 only when the i-th col of A had a non-zero entry.
                A.norow(copy=False) = in-place version
        """
        if copy:
            A = self.copy()
        else:
            A = self

        # Take logical, sum over cols, then logical again
        A.logical(copy=False)
        A = A.sum(0)
        A.logical(copy=False)
        A.row = np.array([0])

        return A

    # element-wise division -- for division by zero, replace with 0 (and remove)
    def divide(self, B):
        """
            Element-wise division of self and B, matched up by row and column indices.
                Usage:
                    A.divide(B)
                Input:
                    A = self = Associative array
                    B = Associative array
                Output:
                    A.divide(B) = element-wise quotient of A by B
                Note:
                    - Removes all explicit zeros and ignores division by zero
                    - Implicitly runs .logical() method on non-numerical arrays
        """

        Binv = B.dropzeros(copy=True)
        Binv.adj.data = np.reciprocal(Binv.adj.data.astype(float, copy=False))

        C = self.multiply(Binv)

        return C

    # element-wise And
    def __and__(self, B):
        """
            Element-wise logical AND of self and B, matched up by row and column indices.
                Usage:
                    A & B
                Input:
                    A = self = Associative array
                    B = Associative array
                Output:
                    A & B = element-wise logical AND of A.logical() and B.logical()
        """

        A = self.logical(copy=True)
        B = B.logical(copy=True)

        C = A.multiply(B)
        return C

    # element-wise or
    def __or__(self, B):
        """
            Element-wise logical OR of self and B, matched up by row and column indices.
                Usage:
                    A | B
                Input:
                    A = self = Associative array
                    B = Associative array
                Output:
                    A | B = element-wise logical OR of A.logical() and B.logical()
        """

        A = self.logical(copy=True)
        B = B.logical(copy=True)

        C = A + B
        C = C.logical(copy=False)
        return C

    def sqin(self):
        """ self.transpose() * self """
        return self.transpose() * self

    def sqout(self):
        """ self * self.transpose() """
        return self * self.transpose()

    # CatKeyMul
    def catkeymul(self, B, delimiter=None):
        """
            Computes the array product, but values are delimiter-separated string list of
                the row/column indices which contribute to the value in the product
                Usage:
                    A.catkeymul(B)
                    A.catkeymul(B,delimiter)
                Input:
                    A = Associative array
                    B = Associative Array
                    delimiter = optional delimiter to separate the row/column indices. Default is semi-colon ';'
                Output:
                    A.catkeymul(B) = Associative array where the (i,j)-th entry is null unless the (i,j)-th entry
                        of A.logical() * B.logical()  is not null, in which case that entry is the string list of
                        the k-indices for which A[i,k] and B[k,j] were non-zero.
        """
        A = self
        intersection = sorted_intersect(A.col, B.row)

        Alog = A[:, intersection].logical()
        Blog = B[intersection, :].logical()
        C = Alog * Blog

        intersection = np.array([str(item) for item in intersection])

        row, col, val = C.find()
        catval = np.zeros(np.size(row), dtype=object)

        if delimiter is None:
            delimiter = ';'

        # Create dictionaries for faster lookups
        row_ind = {C.row[index]: index for index in range(np.size(C.row))}
        col_ind = {C.col[index]: index for index in range(np.size(C.col))}

        rows = Alog.adj.tolil().rows
        cols = Blog.adj.transpose().tolil().rows

        # Enumerate all the row/col key lists to be intersected
        row_keys = {r: intersection[rows[row_ind[r]]] for r in C.row}
        col_keys = {c: set(intersection[cols[col_ind[c]]]) for c in C.col}  # Use set for O(1) lookup

        # Instantiate dictionary to hold already-calculated intersections
        cat_inters = dict()

        for i in range(np.size(row)):
            r = row[i]
            c = col[i]
            if (r, c) in cat_inters:
                catval[i] = cat_inters[(r, c)]
            else:
                catval[i] = delimiter.join([item for item in row_keys[r]
                                            if item in col_keys[c]]) + delimiter
                cat_inters[(r, c)] = catval[i]

        D = Assoc(row, col, catval, add)

        return D

    def catvalmul(self, B, pair_delimiter=None, delimiter=None):
        """
            Computes the array product, but values are delimiter-separated string list of
                the values of A and B which contribute to the value in the product
                Usage:
                    A.catvalmul(B)
                    A.catvalmul(B,pair_delimiter=given1,delimiter=given2)
                Input:
                    A = Associative array
                    B = Associative Array
                    pair_delimiter = optional delimiter to separate the values in A and B. Default is comma ','
                    delimiter = optional delimiter to separate the value pairs. Default is semi-colon ';'
                Output:
                    A.catvalmul(B) = Associative array where the (i,j)-th entry is null unless the (i,j)-th entry
                        of A.logical() * B.logical()  is not null, in which case that entry is the string list of
                        the non-trivial value pairs 'A[i,k],B[k,j],'.
        """
        A = self

        intersection = sorted_intersect(A.col, B.row)

        Alog = A[:, intersection].logical()
        Blog = B[intersection, :].logical()
        C = Alog * Blog

        row, col, val = C.find()
        catval = np.zeros(np.size(row), dtype=object)

        if delimiter is None:
            delimiter = ';'
        if pair_delimiter is None:
            pair_delimiter = ','

        # Create dictionaries for faster lookups
        row_ind = {C.row[index]: index for index in range(np.size(C.row))}
        col_ind = {C.col[index]: index for index in range(np.size(C.col))}
        A_dict = A.dict()
        B_dict = B.dict()

        rows = Alog.adj.tolil().rows
        cols = Blog.adj.transpose().tolil().rows

        # Enumerate all the row/col key lists to be intersected
        row_keys = {r: intersection[rows[row_ind[r]]] for r in C.row}
        col_keys = {c: set(intersection[cols[col_ind[c]]]) for c in C.col}  # Use set for O(1) lookup

        # Instantiate dictionary to hold already-calculated intersections
        cat_inters = dict()

        for i in range(np.size(row)):
            r = row[i]
            c = col[i]
            if (r, c) in cat_inters:
                catval[i] = cat_inters[(r, c)]
            else:
                rc_keys = [item for item in row_keys[r] if item in col_keys[c]]
                rc_valpairs = [str(A_dict[r][key])
                               + pair_delimiter
                               + str(B_dict[key][c])
                               + pair_delimiter for key in rc_keys]
                catval[i] = delimiter.join(rc_valpairs) + delimiter
                cat_inters[(r, c)] = catval[i]

        D = Assoc(row, col, catval, add)

        return D

    def __eq__(self, other):
        """
            Element-wise equality comparison between self and other.
                Usage:
                    A == B
                Input:
                    A = Associative Array
                    B = other object, e.g., another associative array, a number, or a string
                Output:
                    A == B = An associative array such that for row and column labels r and c, resp., such that
                            (A == B)(r,c) = 1 if and only if...
                                (Case 1) A(r,c) == B(r,c) (when B is another associative array
                                    and assuming A(r,c) and B(r,c) are not null)
                                (Case 2) A(r,c) == B (when B is not another associative array)
                            otherwise (A == B)(r,c) = null.
                Notes:
                    Returns an error if other is null (0, '', or None)
        """
        null = [0, '', None]

        selfdict = self.dict()
        selfkeys = self.dict().keys()
        goodrows = list()
        goodcols = list()

        if isinstance(other, Assoc):
            otherdict = other.dict()
            otherkeys = otherdict.keys()

            for key in selfkeys:
                if key in otherkeys:
                    if selfdict[key] not in null and otherdict[key] not in null and selfdict[key] == otherdict[key]:
                        goodrows.append(key[0])
                        goodcols.append(key[1])
        elif other not in null:
            for key in selfkeys:
                if selfdict[key] == other:
                    goodrows.append(key[0])
                    goodcols.append(key[1])
        else:
            raise ValueError("Comparison with a null value")

        A = Assoc(goodrows, goodcols, 1)
        return A

    def __ne__(self, other):
        """
                    Element-wise inequality comparison between self and other.
                        Usage:
                            A != B
                        Input:
                            A = Associative Array
                            B = other object, e.g., another associative array, a number, or a string
                        Output:
                            A != B = An associative array such that for row and column labels r and c, resp., such that
                                    (A != B)(r,c) = 1 if and only if...
                                        (Case 1) A(r,c) != B(r,c) (when B is another associative array
                                                and at least one of A(r,c) and B(r,c) are not null)
                                        (Case 2) A(r,c) != B (when B is not another associative array)
                                    otherwise (A != B)(r,c) = null.
        """
        null = [0, '', None]

        selfdict = self.dict()
        selfkeys = self.dict().keys()
        goodrows = list()
        goodcols = list()

        if isinstance(other, Assoc):
            otherdict = other.dict()
            otherkeys = otherdict.keys()

            for key in selfkeys:
                selfval = selfdict[key]

                if key in otherkeys:
                    otherval = otherdict[key]

                    if (otherval not in null and selfval in null) \
                            or (otherval in null and selfval not in null) \
                            or (otherval not in null and selfval not in null and
                                selfval != otherval):
                        goodrows.append(key[0])
                        goodcols.append(key[1])
            for key in otherkeys:
                otherval = otherdict[key]

                if otherval not in null:
                    if key in selfkeys:
                        continue  # Already addressed
                    else:
                        goodrows.append(key[0])
                        goodcols.append(key[1])
        elif other not in null:
            for key in selfkeys:
                if selfdict[key] != other:
                    goodrows.append(key[0])
                    goodcols.append(key[1])
        else:
            for key in selfkeys:
                if selfdict[key] not in null:
                    goodrows.append(key[0])
                    goodcols.append(key[1])

        A = Assoc(goodrows, goodcols, 1)
        return A

    def __lt__(self, other):
        """
                    Element-wise strictly less than comparison between self and other.
                        Usage:
                            A < B
                        Input:
                            A = Associative Array
                            B = other object, e.g., another associative array, a number, or a string
                        Output:
                            A < B = An associative array such that for row and column labels r and c, resp., such that
                                    (A < B)(r,c) = 1 if and only if...
                                        (Case 1) A(r,c) < B(r,c) (when B is another associative array)
                                        (Case 2) A(r,c) < B (when B is not another associative array)
                                    otherwise (A < B)(r,c) = null.
                        Notes:
                            - Only numeric and string data types are supported.
                            - Any non-null string is always greater than null.
                            - If A(r,c) and B (or B(r,c) if B is another associative array) are incomparable
                            (e.g., if the former is a non-null number and the latter is a non-null string)
                            then an error is raised.
        """
        null = [0, '', None]

        selfdict = self.dict()
        selfkeys = self.dict().keys()
        goodrows = list()
        goodcols = list()

        if isinstance(other, Assoc):
            otherdict = other.dict()
            otherkeys = otherdict.keys()

            for key in selfkeys:
                selfval = selfdict[key]
                if key in otherkeys:
                    otherval = otherdict[key]

                    # Check if selfval and otherval have compatible types and whether selfval < otherval,
                    # where selfval and otherval are interpreted appropriately if null
                    if (selfval in null and ((is_numeric(otherval) and otherval > 0)
                                             or (isinstance(otherval, str) and otherval not in null)))\
                            or (otherval in null and is_numeric(selfval) and selfval < 0)\
                            or (is_numeric(otherval) and is_numeric(selfval) and selfval < otherval)\
                            or (isinstance(otherval, str) and isinstance(otherval) and selfval < otherval):
                        goodrows.append(key[0])
                        goodcols.append(key[1])
                else:
                    if is_numeric(selfval) and selfval < 0:
                        goodrows.append(key[0])
                        goodcols.append(key[1])
            for key in otherkeys:
                otherval = otherdict[key]

                if key in selfkeys:
                    continue  # Already addressed
                else:
                    if (isinstance(otherval, str) and otherval not in null) or (is_numeric(otherval) and 0 < otherval):
                        goodrows.append(key[0])
                        goodcols.append(key[1])
        else:
            for key in selfkeys:
                selfval = selfdict[key]

                # Check if selfval and other have compatible types and whether selfval < other,
                # where selfval and other are interpreted appropriately if null
                if (selfval in null and ((is_numeric(other) and other > 0)
                                                 or (isinstance(other, str) and other not in null)))\
                                or (other in null and is_numeric(selfval) and selfval < 0)\
                                or (is_numeric(other) and is_numeric(selfval) and selfval < other)\
                                or (isinstance(other, str) and isinstance(other) and selfval < other):
                    goodrows.append(key[0])
                    goodcols.append(key[1])

        A = Assoc(goodrows, goodcols, 1)
        return A

    def __gt__(self, other):
        """
                    Element-wise strictly greater than comparison between self and other.
                        Usage:
                            A > B
                        Input:
                            A = Associative Array
                            B = other object, e.g., another associative array, a number, or a string
                        Output:
                            A > B = An associative array such that for row and column labels r and c, resp., such that
                                    (A > B)(r,c) = 1 if and only if...
                                        (Case 1) A(r,c) > B(r,c) (when B is another associative array)
                                        (Case 2) A(r,c) > B (when B is not another associative array)
                                    otherwise (A > B)(r,c) = null.
                        Notes:
                            - Only numeric and string data types are supported.
                            - Any non-null string is always greater than null.
                            - If A(r,c) and B (or B(r,c) if B is another associative array) are incomparable
                            (e.g., if the former is a non-null number and the latter is a non-null string)
                            then an error is raised.
        """
        null = [0, '', None]

        selfdict = self.dict()
        selfkeys = self.dict().keys()
        goodrows = list()
        goodcols = list()

        if isinstance(other, Assoc):
            otherdict = other.dict()
            otherkeys = otherdict.keys()

            for key in selfkeys:
                selfval = selfdict[key]
                if key in otherkeys:
                    otherval = otherdict[key]

                    # Check if selfval and otherval have compatible types and whether selfval > otherval,
                    # where selfval and otherval are interpreted appropriately if null
                    if (selfval in null and is_numeric(otherval) and otherval < 0)\
                            or (otherval in null and ((is_numeric(selfval) and selfval > 0)
                                                      or (isinstance(selfval, str) and selfval not in null)))\
                            or (is_numeric(otherval) and is_numeric(selfval) and selfval > otherval)\
                            or (isinstance(otherval, str) and isinstance(otherval, str) and selfval > otherval):
                        goodrows.append(key[0])
                        goodcols.append(key[1])
                else:
                    if (is_numeric(selfval) and selfval > 0) or (isinstance(selfval, str) and selfval not in null):
                        goodrows.append(key[0])
                        goodcols.append(key[1])
            for key in otherkeys:
                otherval = otherdict[key]

                if key in selfkeys:
                    continue  # Already addressed
                else:
                    if is_numeric(otherval) and 0 > otherval:
                        goodrows.append(key[0])
                        goodcols.append(key[1])
        else:
            for key in selfkeys:
                selfval = selfdict[key]

                # Check if selfval and other have compatible types and whether selfval > other,
                # where selfval and other are interpreted appropriately if null
                if (selfval in null and is_numeric(other) and other < 0) \
                        or (other in null and ((is_numeric(selfval) and selfval > 0)
                                                  or (isinstance(selfval, str) and selfval not in null))) \
                        or (is_numeric(other) and is_numeric(selfval) and selfval > other) \
                        or (isinstance(other, str) and isinstance(other, str) and selfval > other):
                    goodrows.append(key[0])
                    goodcols.append(key[1])

        A = Assoc(goodrows, goodcols, 1)
        return A

    def __le__(self, other):
        """
                    Element-wise less than or equal comparison between self and other.
                        Usage:
                            A <= B
                        Input:
                            A = Associative Array
                            B = other object, e.g., another associative array, a number, or a string
                        Output:
                            A <= B = An associative array such that for row and column labels r and c, resp., such that
                                    (A <= B)(r,c) = 1 if and only if...
                                        (Case 1) A(r,c) <= B(r,c) (when B is another associative array)
                                        (Case 2) A(r,c) <= B (when B is not another associative array)
                                    otherwise (A <= B)(r,c) = null.
                        Notes:
                            - Only numeric and string data types are supported.
                            - Any non-null string is always greater than null.
                            - If A(r,c) and B (or B(r,c) if B is another associative array) are incomparable
                            (e.g., if the former is a non-null number and the latter is a non-null string)
                            then an error is raised.
        """
        null = [0, '', None]

        selfdict = self.dict()
        selfkeys = self.dict().keys()
        goodrows = list()
        goodcols = list()

        if isinstance(other, Assoc):
            otherdict = other.dict()
            otherkeys = otherdict.keys()

            for key in selfkeys:
                selfval = selfdict[key]
                if key in otherkeys:
                    otherval = otherdict[key]

                    # Check if selfval and otherval have compatible types and whether selfval <= otherval,
                    # where selfval and otherval are interpreted appropriately if null
                    if (selfval in null and ((is_numeric(otherval) and otherval >= 0)
                                             or isinstance(otherval, str)))\
                            or (otherval in null and is_numeric(selfval) and selfval <= 0)\
                            or (is_numeric(otherval) and is_numeric(selfval) and selfval <= otherval)\
                            or (isinstance(otherval, str) and isinstance(otherval, str) and selfval <= otherval):
                        goodrows.append(key[0])
                        goodcols.append(key[1])
                else:
                    if is_numeric(selfval) and selfval <= 0:
                        goodrows.append(key[0])
                        goodcols.append(key[1])
            for key in otherkeys:
                otherval = otherdict[key]

                if key in selfkeys:
                    continue  # Already addressed
                else:
                    if isinstance(otherval, str) or (is_numeric(otherval) and 0 <= otherval):
                        goodrows.append(key[0])
                        goodcols.append(key[1])
        else:
            for key in selfkeys:
                selfval = selfdict[key]

                # Check if selfval and other have compatible types and whether selfval <= other,
                # where selfval and other are interpreted appropriately if null
                if (selfval in null and ((is_numeric(other) and other >= 0)
                                         or isinstance(other, str))) \
                        or (other in null and is_numeric(selfval) and selfval <= 0) \
                        or (is_numeric(other) and is_numeric(selfval) and selfval <= other) \
                        or (isinstance(other, str) and isinstance(other, str) and selfval <= other):
                    goodrows.append(key[0])
                    goodcols.append(key[1])

        A = Assoc(goodrows, goodcols, 1)
        return A

    def __ge__(self, other):
        """
                    Element-wise greater than or equal comparison between self and other.
                        Usage:
                            A >= B
                        Input:
                            A = Associative Array
                            B = other object, e.g., another associative array, a number, or a string
                        Output:
                            A >= B = An associative array such that for row and column labels r and c, resp., such that
                                    (A >= B)(r,c) = 1 if and only if...
                                        (Case 1) A(r,c) >= B(r,c) (when B is another associative array)
                                        (Case 2) A(r,c) >= B (when B is not another associative array)
                                    otherwise (A >= B)(r,c) = null.
                        Notes:
                            - Only numeric and string data types are supported.
                            - Any non-null string is always greater than null.
                            - If A(r,c) and B (or B(r,c) if B is another associative array) are incomparable
                            (e.g., if the former is a non-null number and the latter is a non-null string)
                            then an error is raised.
        """
        null = [0, '', None]

        selfdict = self.dict()
        selfkeys = self.dict().keys()
        goodrows = list()
        goodcols = list()

        if isinstance(other, Assoc):
            otherdict = other.dict()
            otherkeys = otherdict.keys()

            for key in selfkeys:
                selfval = selfdict[key]
                if key in otherkeys:
                    otherval = otherdict[key]

                    # Check if selfval and otherval have compatible types and whether selfval >= otherval,
                    # where selfval and otherval are interpreted appropriately if null
                    if (selfval in null and is_numeric(otherval) and otherval <= 0)\
                            or (otherval in null and ((is_numeric(selfval) and selfval >= 0)
                                                      or isinstance(selfval, str)))\
                            or (is_numeric(otherval) and is_numeric(selfval) and selfval >= otherval)\
                            or (isinstance(otherval, str) and isinstance(otherval, str) and selfval >= otherval):
                        goodrows.append(key[0])
                        goodcols.append(key[1])
                else:
                    if (is_numeric(selfval) and selfval >= 0) or isinstance(selfval, str):
                        goodrows.append(key[0])
                        goodcols.append(key[1])
            for key in otherkeys:
                otherval = otherdict[key]

                if key in selfkeys:
                    continue  # Already addressed
                else:
                    if is_numeric(otherval) and 0 > otherval:
                        goodrows.append(key[0])
                        goodcols.append(key[1])
        else:
            for key in selfkeys:
                selfval = selfdict[key]

                # Check if selfval and other have compatible types and whether selfval >= other,
                # where selfval and other are interpreted appropriately if null
                if (selfval in null and is_numeric(other) and other <= 0) \
                        or (other in null and ((is_numeric(selfval) and selfval >= 0)
                                                  or isinstance(selfval, str))) \
                        or (is_numeric(other) and is_numeric(selfval) and selfval >= other) \
                        or (isinstance(other, str) and isinstance(other, str) and selfval >= other):
                    goodrows.append(key[0])
                    goodcols.append(key[1])

        A = Assoc(goodrows, goodcols, 1)
        return A



import csv

def readcsvtotriples(filename, labels=True, triples=False, **fmtoptions):
    """
    Read CSV file to row, col, val lists.
        Usage:
            row, col, val = readCSV(filename, labels=False, triples=False)
            row, col, val = readCSV(filename, fmtoptions)
        Inputs:
            filename = name of file (string)
            labels = optional parameter to say whether row and column labels are 
                        the first column and row, resp.
            triples = optional parameter indicating whether each row is of the form 'row[i], col[i], val[i]'
            **fmtoptions = format options accepted by csv.reader, e.g. "delimiter='\t'" for tsv's
        Outputs:
            row, col, val = value in row[i]-th row and col[i]-th column is val[i] (if not triples,
                                else the transposes of the columns)
        Examples:
            row, col, val = readcsv('my_file_name.csv')
            row, col, val = readcsv('my_file_name.csv', delimiter=';')
            row, col, val = readcsv('my_file_name.tsv', triples=True, delimiter='\t')
    """

    # Read CSV file and create (row-index,col-index):value dictionary
    with open(filename, 'rU') as csvfile:
        Assocreader = csv.reader(csvfile, **fmtoptions)
        
        if triples:
            row = list()
            col = list()
            val = list()
            
            for line in Assocreader:
                if len(line) == 0:
                    continue
                if len(line) != 3:
                    raise ValueError('line has '+str(len(line))+' elements:\n'+str(line)
                                     +'\ntriples=True implies there are three columns')
                else:
                    row.append(line[0])
                    col.append(line[1])
                    val.append(line[2])
        else:
            Assocdict = dict()
            
            # If labels are expected, take first row to be the column labels
            if labels:
                headings = next(Assocreader)
            else:
                linenum = 0 # Otherwise start counting the lines

            for row in Assocreader:
                if len(row) == 0:
                    continue
                if labels and len(row) != len(headings):
                    raise ValueError("row has "+str(len(row))+" elements while there are "
                                     +str(len(headings))+" column labels.")
                else:
                    # If labels are expected, first element of row is row label, otherwise actual value
                    if labels:
                        start=1
                    else:
                        start=0

                    for i in range(start, len(row)):
                        # If labels are expected, use with dictionary
                        if row[i] is not None and row[i] != '':
                            if labels:
                                Assocdict[(row[0], headings[i])] = row[i]
                            else:
                                Assocdict[(linenum,i)] = row[i]
                # Increment line counter
                if not labels:
                    linenum += 1

            # Extract row, col, val from dictionary
            row_col_tuples = list(Assocdict.keys())
            row = [str_to_num(item[0]) for item in row_col_tuples]
            col = [str_to_num(item[1]) for item in row_col_tuples]
            val = [str_to_num(item) for item in list(Assocdict.values())]

    return row, col, val


def readcsv(filename, labels=True, triples=False, **fmtoptions):
    """
    Read CSV file to Assoc instance.
        Usage:
            A = readCSV(filename)
            A = readCSV(filename, fmtoptions)
        Inputs:
            filename = name of file (string)
            labels = optional parameter to say whether row and column labels are 
                        the first column and row, resp.
            triples = optional parameter indicating whether each row is of the form 'row[i], col[i], val[i]'
            fmtoptions = format options accepted by csv.reader, e.g. "delimiter='\t'" for tsv's
        Outputs:
            A = Associative Array whose column indices are given in the first line of the file,
                whose row indices are given in the first column of the file, and whose values
                are the remaining non-empty/null items, paired with the appropriate row
                and col indices
        Examples:
            A = readcsv('my_file_name.csv')
            A = readcsv('my_file_name.csv', delimiter=';')
            A = readcsv('my_file_name.tsv', delimiter='\t')
    """
    
    row, col, val = readcsvtotriples(filename, labels=labels, triples=triples, **fmtoptions)

    A = Assoc(row, col, val)
    return A


def writecsv(A, filename, fmtparams=None):
    """
    Write CSV file from Assoc instance.
        Usage:
            writeCSV(filename)
            writeCSV(filename, fmtoptions)
        Inputs:
            A = Associative array to write to CSV
            filename = name of file to write to (string)
            fmtoptions = format options accepted by csv.writer
        Outputs:
            None
        Examples:
            writeCSV(A, 'my_file_name.csv')
            writeCSV(A, 'my_file_name.csv', delimiter=';')
    """

    with open(filename, 'w') as csvfile:
        Assocwriter = csv.writer(csvfile, fmtparams, lineterminator='\r')

        # Write the headings (offset by one to account for row indices)
        headings = [item for item in A.col]
        headings.insert(0, None)
        Assocwriter.writerow(headings)

        # Create lookup dictionary
        row, col, val = A.find()
        try:
            tups = itertools.izip(itertools.izip(row, col), val)
        except AttributeError:
            tups = list(zip(zip(row, col), val))
        adj_dict = dict(tups)

        for i in range(len(A.row)):
            newline = list()
            newline.append(A.row[i])  # Start with row index

            # Go through the row and add value if it exists, else None
            for j in range(len(A.col)):
                if (A.row[i], A.col[j]) in adj_dict.keys():
                    newline.append(adj_dict[(A.row[i], A.col[j])])
                else:
                    newline.append(None)

            Assocwriter.writerow(newline)

    return None