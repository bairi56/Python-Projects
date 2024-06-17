

import time             #time is imported fo calculating time
import random           #random is imported fo chosing random elements
import matplotlib.pyplot as plt         #matplotlib is imported for plotting graphs
E1_time=[]              #time for buble sort
E2_time=[]              #time for insertion sort

def buble_sort(lst):            # function for buble sort
    print("Dry Run Of Insertion Sort is")
    for i in range(len(lst)):
        # print(lst[i],"I")
        for j in range(len(lst)-1):
            # print(lst[j],"J")
            # print("value of i",i,"value of j",lst[j])
            if lst[j+1]<lst[j]:
                # print("swaping in buble",lst[j+1],lst[j])
                lst[j],lst[j+1]=lst[j+1],lst[j]
                 # print("list after swapings",lst)
        # print(lst,"lst behavior at each iteration")
    print("sorted list by bubble sort is", lst)
    return lst
def insertion_sort(lst2):               # function for insertion sort
    for i in range(1,len(lst2)):
        # print(i)
        key=lst2[i]            #key equal to 2nd element
        j=i-1                   #decreament in i
        while j>=0 and lst2[j]>key:         #j= or >0  and lst2[j]>key  then perform
            lst2[j+1],lst2[j]=lst2[j],lst2[j+1]         #swaping
            # print(lst2[j+1],lst2[j])
            j=j-1           #decreament in i
        #when condition is false then
        lst2[j+1],key=key,lst2[j+1]             #swaping
        # print(lst2[j+1],key)
random_size=[]      #list for input size
l=10
for i in range(5):
    random_lst=[]           #list for elements according to each input size
    random_integer = random.randint(l, l+100)           #chose random numbers in a given range for list size
    # print(random_integer)
    random_size.append(random_integer)                  #store in lst
    for j in range(random_integer):
        random_lst.append( random.randint(1, 100))           #chose random numbers in a given range for list entries according to its size and store in list
    # print(random_lst)
    # print(end,"at end")
    lsttt=random_lst.copy()             #o create a copy of the list 
    start1 = time.time()                                #start time
    buble_sort(random_lst)              #buble sort calling
    end1=time.time()                        #end time
    # print("end time of 1",end1)
    execution_time1=end1-start1             #execution time
    # print("execution 1",execution_time1)
    E1_time.append(execution_time1)
    start2 = time.time()                                #start time
    insertion_sort(lsttt)                       #insertion sort calling
    end2=time.time()                        #end time
    # print("end time of 2",end2)
    execution_time2=end2-start2              #execution time
    # print("execution 2",execution_time2)
    E2_time.append(execution_time2)
    l+=500                  #increament in i
print(random_size,"Input Size List")            #print random size made
print(E1_time,"Time for Bubble sort")           #all the executions time for bubble sort according to its size
print(E2_time,"Time for Insertion Sort")                #all the executions time for insertion sort according to its size
plt.plot(random_size,E1_time,"ro-",marker="o",label="Execution Time of 1")            #plot for bubble sort
plt.plot(random_size,E2_time,"b^-",marker="o",label="Execution Time of 2")         #plot for bubble sort
plt.xlabel('Input Size')            #x axis label
plt.ylabel('Time')                      #y axis label
plt.title('Variation of Time with respect to Input Size')           #title of graph
plt.legend()                # Add a legend
plt.show()                      #Display the Plot
