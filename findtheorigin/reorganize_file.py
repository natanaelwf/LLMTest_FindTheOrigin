#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def reorganize_file(input_file, output_file, d):

    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Separates the rows into two groups: even and odd indices
    even_lines = lines[::2]
    odd_lines = lines[1::2]

    # Determines the order based on the sign of d
    first_group, second_group = (odd_lines, even_lines) if d < 0 else (even_lines, odd_lines)

    # Use abs(d) for calculations
    d = abs(d)

    # Calculates the number of groups
    num_groups = min(len(even_lines), len(odd_lines)) // d

    # Opens the output file for writing
    with open(output_file, 'w') as file:
        for i in range(num_groups):
            # Write d lines of the first group
            file.writelines(first_group[i*d:(i+1)*d])
            # Write d lines of the second group
            file.writelines(second_group[i*d:(i+1)*d])

        # Adjust the remaining lines
        remaining_first = first_group[num_groups*d:]
        remaining_second = second_group[num_groups*d:]

        # Write the remaining lines of the first group
        file.writelines(remaining_first)
        # Write the remaining lines of the second group
        file.writelines(remaining_second)

