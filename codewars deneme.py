import numpy as np
# return the first arithmetic sequence contained within the list set. 
def find_arithmetic_sequence(lst):
    if len(lst)<3:
        return []
    else:
        list=np.sort(lst)
        result = []
        for i in list:
            if list[i+1]-list[i]==list[i+2]-list[i+1]:
                result.append(list[i])
                result.append(list[i+1])
                result.append(list[i+2])
                return result



find_arithmetic_sequence([1,2,4,9,25]),[]       