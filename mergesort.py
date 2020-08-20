def merge_sort(input_list):
    if len(input_list) == 1:
        return input_list
    else:
        midpoint = len(input_list)//2
        left = input_list[:midpoint]
        right = input_list[midpoint:]
        sorted_left = merge_sort(left)
        sorted_right = merge_sort(right)
        sorted_list = []
        while True:
            if sorted_right[0] < sorted_left[0]:
                sorted_list.append(sorted_right[0])
                sorted_right.pop(0)
            else:
                sorted_list.append(sorted_left[0])
                sorted_left.pop(0)
            if len(sorted_right) == 0 or len(sorted_left) == 0:
                break
        sorted_list = sorted_list + sorted_left + sorted_right
        return sorted_list


input_list = [9,5,8,20,6,7,1,2,4,3,11,15,13,12,14,19,18,16,17,10]
print(merge_sort(input_list))

