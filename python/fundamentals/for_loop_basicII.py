# Biggie Size - Given a list, write a function that changes all positive numbers in the list to "big".
# Example: biggie_size([-1, 3, 5, -5]) returns that same list, but whose values are now [-1, "big", "big", -5]
def biggie_size(arr):
    for x in range(0, len(arr), 1):
        if arr[x]>0:
           arr[x]='big'
    return arr

print(biggie_size([-1, 3, 5, -5]))

# Count Positives - Given a list of numbers, create a function to replace the last value with the number of positive values. 
# (Note that zero is not considered to be a positive number).
# Example: count_positives([-1,1,1,1]) changes the original list to [-1,1,1,3] and returns it
# Example: count_positives([1,6,-4,-2,-7,-2]) changes the list to [1,6,-4,-2,-7,2] and returns it

def count_positives(arr):
    sum = 0
    for i in range(len(arr)):
        if arr[i]>0:
            sum = sum+1
    arr.append(sum)
    return arr
print(count_positives([-1,1,1,1]))


# Sum Total - Create a function that takes a list and returns the sum of all the values in the array.
# Example: sum_total([1,2,3,4]) should return 10
# Example: sum_total([6,3,-2]) should return 7

def sum_total(arr):
    sum = 0
    for i in range (len(arr)):
        sum = sum + arr[i]
    arr.append(sum)
    return arr
print(sum_total([1,2,3,4]))

# Average - Create a function that takes a list and returns the average of all the values.
# Example: average([1,2,3,4]) should return 2.5
def average(arr):
    ave = 0.0
    sum = 0.0
    for i in arr:
        sum = sum + i
    ave = sum/len(arr)
    return ave

print(average([1,2,3,4]))


# Length - Create a function that takes a list and returns the length of the list.
# Example: length([37,2,1,-9]) should return 4
# Example: length([]) should return 0
def length(arr):
    return len(arr)

print(length([37,2,1,-9]))

# Minimum - Create a function that takes a list of numbers and returns the minimum value in the list. 
# If the list is empty, have the function return False.
# Example: minimum([37,2,1,-9]) should return -9
# Example: minimum([]) should return False
def minimum(arr):
    if len(arr)>0:
        min=arr[0]
        for x in arr:
            if x<min:
                min = x
        return min
    else:
        return False


print(minimum([37,2,1,-9]))
print(minimum([]))

# Maximum - Create a function that takes a list and returns the maximum value in the array. If the list is empty, have the function return False.
# Example: maximum([37,2,1,-9]) should return 37
# Example: maximum([]) should return False
def maximum(arr):
    if len(arr)>0:
        max=arr[0]
        for x in arr:
            if x>max:
                max = x
        return max
    else:
        return False


print(maximum([37,2,1,-9]))
print(maximum([]))
# Ultimate Analysis - Create a function that takes a list and returns a dictionary that has the sumTotal, average, minimum, maximum and length of the list.
# Example: ultimate_analysis([37,2,1,-9]) should return {'sumTotal': 31, 'average': 7.75, 'minimum': -9, 'maximum': 37, 'length': 4 }
def ultimate_analysis(arr):
    if len(arr)>0:
        ave = 0.0
        sum = 0.0
        max=arr[0]
        min=arr[0]
        for x in arr:
            sum = sum+x
            ave = sum/len(arr)
            if x>max:
                max = x
            elif x<min:
                min = x
            
        return {'sumTotal': sum, 'average': ave, 'minimum': min, 'maximum': max, 'length': len(arr)}
    else:
        return False


print(ultimate_analysis([37,2,1,-9]))
print(ultimate_analysis([]))

# Reverse List - Create a function that takes a list and return that list with values reversed. Do this without creating a second list.
#  (This challenge is known to appear during basic technical interviews.)
# Example: reverse_list([37,2,1,-9]) should return [-9,1,2,37]

def reverse_list(arr):
    for x in range(len(arr)/2):
        a =arr[x]
        arr[x] = arr[len(arr)-1-x]
        arr[len(arr)-1-x] = a
    return arr


print(reverse_list([37,2,1,-9]))
print(reverse_list([37,2,1,-9, 10, 27, 34]))

