"""**Problem Statement: Counting Unique Occurrences**

You are given a list of integers. Your task is to write a Python program to determine whether the count of occurrences of each element in the list is unique or not. You must accomplish this without using built-in functions or libraries.

Write a function `is_unique_occurrences(lst)` that takes a list of integers `lst` as input and returns a boolean value:

- If the count of occurrences of each element in the list is unique, the function should return `True`.
- If there are any counts of occurrences that are not unique, the function should return `False`.

**Input:**
- A list of integers, `lst`, where 1 <= len(lst) <= 1000 and -1000 <= lst[i] <= 1000.

**Output:**
- A boolean value, `True` if all counts of occurrences are unique, `False` if there are any non-unique counts.

**Example:**

```python
>>> is_unique_occurrences([1, 2, 2, 3, 3, 3, 4, 4, 4, 4])
True
```

**Explanation:** In this example, each element in the list has a unique count of occurrences. The counts are: 1 (occurs once), 2 (occurs twice), 3 (occurs three times), and 4 (occurs four times). All counts are unique, so the function returns `True`.

```python
>>> is_unique_occurrences([1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 4])
False
```

**Explanation:** In this example, the count of occurrences for the number 4 is not unique. It occurs five times, which is not unique among the counts. Therefore, the function returns `False`."""


def count_occurrences(lst):
    # Create a dictionary to store the counts of each element
    element_count = {}
    
    # Count the occurrences of each element
    for element in lst:
        if element in element_count:
            element_count[element] += 1
        else:
            element_count[element] = 1

    # Create a dictionary to store the counts and check for uniqueness
    count_uniqueness = {}
    
    for count in element_count.values():
        if count in count_uniqueness:
            count_uniqueness[count] += 1
        else:
            count_uniqueness[count] = 1

    # Check if each count is unique (appears only once)
    is_unique = all(count == 1 for count in count_uniqueness.values())

    return is_unique

# Example usage:
my_list = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
result = count_occurrences(my_list)

if result:
    print("Each count of occurrence is unique.")
else:
    print("Some counts of occurrence are not unique.")
