def select_sort(arr):
    
    for j in range(len(arr)):
        min_idx = j
        for i in range(j+1, len(arr), 1):
            print(i)
            if arr[min_idx]>arr[i]:
                 min_idx = i
                
        arr[j], arr[min_idx] = arr[min_idx], arr[j]
        

arr = [45, 6, 5, 3, 22, 11, 90] 

select_sort(arr)
print(arr)
