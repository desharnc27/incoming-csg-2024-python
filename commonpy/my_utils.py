import hashlib
import json
import random
from typing import List, Tuple, Any, TypeVar
import re

T = TypeVar('T')


def read_from_path(path: str) -> str:
    with open(path, 'r') as file:
        return file.read()


def file_to_string_array(filename: str) -> List[str]:
    return read_from_path(filename).splitlines()


def string_array_to_file(arr: List[str], filename: str) -> None:
    with open(filename, 'w') as file:
        for i in range(len(arr) - 1):
            file.write(arr[i] + '\n')
        file.write(arr[-1])


def json_file_to_list(json_file: str) -> List[str]:
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
            if isinstance(data, list) and all(isinstance(item, str) for item in data):
                return data
            else:
                print(f'The JSON file does not contain an array of strings.')
                return []
    except FileNotFoundError:
        print(f'File not found: {json_file}')
        return []
    except Exception as e:
        print(f'An error occurred: {str(e)}')
        return []


def list_to_json_file(json_file: str, data: List[str]):
    try:
        with open(json_file, 'w') as file:
            json.dump(data, file, separators=(',', ':'))

        print(f'Successfully created {json_file} from the list.')
    except Exception as e:
        print(f'An error occurred: {str(e)}')


def sort_with_indices(arr: List[int]) -> Tuple[List[int], List[int]]:
    # Enumerate the original array to create pairs of (element, index)
    indexed_arr = list(enumerate(arr))

    # Sort the indexed array based on the values of the elements
    sorted_arr = sorted(indexed_arr, key=lambda x: x[1])

    # Extract the sorted elements and their original indices
    sorted_elements: List[int] = [element for _, element in sorted_arr]
    original_indices: List[int] = [index for index, _ in sorted_arr]

    return sorted_elements, original_indices


def restore_to_original_order(sorted_elements: List[int], original_indices: List[int]) -> List[int]:
    # Create a list of tuples with original indices and sorted elements
    indexed_sorted_elements: List[Tuple[int, int]] = list(zip(original_indices, sorted_elements))

    # Sort the list of tuples based on the original indices
    indexed_sorted_elements.sort(key=lambda x: x[0])

    # Extract the sorted elements in their original order
    restored_array: List[int] = [element for _, element in indexed_sorted_elements]

    return restored_array


def is_tuple_of_two_integers(variable: Any) -> bool:
    # Check if it's a tuple
    if not isinstance(variable, tuple):
        return False

    # Check if the tuple has exactly two elements
    if len(variable) != 2:
        return False

    # Check if both elements are integers
    if not all(isinstance(element, int) for element in variable):
        return False

    return True


def get_sha1(input_string: str) -> str:
    sha1 = hashlib.sha1()
    sha1.update(input_string.encode('utf-8'))
    return sha1.hexdigest()


def my_flag(input_string: str) -> str:
    return "FLAG{{{0}}}".format(input_string)


def my_sha1_flag(input_string: str) -> str:
    return my_flag(get_sha1(input_string))


def add_arrow_pattern(original_str: str, wanted_len: int, add_space: bool = False) -> str:
    """
    Will append a "----->" to the original string so that the modified
    string reaches wanted_len\n
    Be careful, passing a wanted_len value under minimal possible value is not supported

    :param original_str:
    :param wanted_len:
    :param add_space: true to add space between original string and arrow.
        Space included in length count
    :return: the modified string
    """
    if add_space:
        original_str = original_str + " "
    # Warning: does not support the case line_remain < 0
    line_remain = wanted_len - len(original_str) - 1
    return original_str + "-" * line_remain + ">"


def arrow_intuitive_format(attributes: List[str],
                           values: List[str],
                           add_space: bool = False) -> List[str]:
    """
    :param attributes: list of attributes
    :param values: values of attributes. Both list must have same length
    :param add_space: true if you want to add spaces before and after arrows
    :return: the list of all arrowed "attribute-->value" pair. Length
        of arrows are adjusted to uniformize the index of the arrows' among attributes
    """
    left_len = max(len(a) for a in attributes) + 2
    if add_space:
        left_len = left_len + 1
    res = []
    for i in range(len(attributes)):
        left = add_arrow_pattern(attributes[i], left_len, add_space)
        right = values[i]
        if add_space:
            right = " " + right
        res.append(left + right)
    return res


def len_or_1(var: Any) -> int:
    if not isinstance(var, list) and not isinstance(var, tuple):
        return 1
    return len(var)


def at_index_or_first(var: List[T] | T, idx: int) -> T:
    if not isinstance(var, list):
        return var
    if len(var) <= idx:
        return var[0]
    return var[idx]


def listify(var: List[T] | T) -> List[T]:
    """
    :param var: anything
    :return: var itself if it's a list, otherwise returns a list with var as sole element
    """
    if type(var) == list:
        return var
    return [var]


def double_exclaim_replacement(val_str_list: List[str], val_list: List[str], text: str) -> str:
    for i in range(len(val_list)):
        expr = "!!" + val_str_list[i] + "!!"
        text = text.replace(expr, val_list[i])
    return text


def raw_print(arr: List[List[str]]):
    for line in arr:
        print("".join(line))


def swap_rows(matrix: List[List[Any]], row_a: int, row_b: int) -> None:
    matrix[row_a], matrix[row_b] = matrix[row_b], matrix[row_a]


def move_row(matrix: List[List[Any]], row_a: int, row_b: int) -> None:
    row_to_move = matrix.pop(row_a)
    matrix.insert(row_b, row_to_move)


def swap_columns(matrix: List[List[Any]], col_a: int, col_b: int) -> None:
    for row in matrix:
        row[col_a], row[col_b] = row[col_b], row[col_a]


def move_column(matrix: List[List[Any]], col_a: int, col_b: int) -> None:
    for row in matrix:
        if 0 <= col_a < len(row) and 0 <= col_b < len(row):  # Check if indices are valid
            row[col_b:col_b] = [row.pop(col_a)]


def random_2d_shuffle(matrix: List[List[T]]) -> List[List[T]]:
    random.shuffle(matrix)  # Shuffle rows
    transposed_matrix = list(map(list, zip(*matrix)))  # Transpose the matrix
    random.shuffle(transposed_matrix)  # Shuffle rows of the transposed matrix
    permuted_matrix = list(map(list, zip(*transposed_matrix)))  # Transpose it back
    return permuted_matrix


def detect_fraction(maybe_frac: str) -> None | Tuple[int, int]:
    regex = r"(-?\d+)/(\d+)"
    pattern = re.compile(regex)
    match = pattern.fullmatch(maybe_frac)
    if not match:
        return
    return int(match.group(1)), int(match.group(2))
