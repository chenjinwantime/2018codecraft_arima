#coding=utf-8
import lof
def input_data(A):
    t=len(A)
    instances=[]
    for i in range(t):
        instances.append((A[i],0))
    return instances
    # `instances = [(0,0) ,(14,0),(4,0)  ,(1,0) ,(5,0), (4,0), (3,0) ,(2,0)]
def test_outliers(instances):
    t=lof.outliers(2, instances)
    for outlier in t:
        print outlier["lof"], outlier["instance"]
    return t
def average(A,B):
    a=0
    for i in range(len(A)):
        if A[i]!=B:
            a+=A[i]
    a=a/(len(A)-1)
    return a

def ErrorDection3(A,ave,de):
    # A=[2,2,3,4,2,3,19]
    # B=[(1,2)]
    # print B[0][0]
    # print("Running tests, nothing more should appear if everything goes well.")
    instances=input_data(A)
    # print "instances",instances
    t=test_outliers(instances)
    max_outer=0
    max_insta=(0,0)
    if t:
        for outlier in t:
            if outlier["lof"]>max_outer:
                max_outer=outlier["lof"]
                max_insta=outlier["instance"]
    #if t:
    #    for i in range(len(A)):
    #        if A[i] == max_insta[0]:
    #            t = average(A, A[i])
    #            if (max_insta[0] > t):
    #                A[i]=t
    #                if i == 0:
    #                    A[i] = A[i + 1]
    #                else:
    #                    A[i] = A[i - 1]
    if t:
        for outlier in t:
            for i in range(len(A)):
                if A[i]==outlier["instance"][0]:
                    # tm= average(A, A[i])
                    if (outlier["instance"][0]> ave):
                        if i==0:
                            A[i]=(A[i+1]+A[i])/2
                        elif i==len(A)-1:
                            A[i]=(A[i-1]+A[i])/2
                        else:
                            A[i]=(A[i+1]+A[i-1]+A[i])/3
                    
    for i in range(len(A)):
        if i==0 or i==len(A)-1:
            continue
        if (A[i]>2*(A[i+1]+A[i])):
            A[i]=(A[i+1]+A[i-1]+A[i])/3


    return A
    
    
def ErrorDection(A):
    # A=[2,2,3,4,2,3,19]
    # B=[(1,2)]
    # print B[0][0]
    # print("Running tests, nothing more should appear if everything goes well.")
    instances=input_data(A)
    # print "instances",instances
    t=test_outliers(instances)
    max_outer=0
    max_insta=(0,0)
    if t:
        for outlier in t:
            if outlier["lof"]>max_outer:
                max_outer=outlier["lof"]
                max_insta=outlier["instance"]
    if t:
        for i in range(len(A)):
            if A[i] == max_insta[0]:
                t = average(A, A[i])
                if (max_insta[0] > t):
                    A[i]=t
                    if i == 0:
                        A[i] = A[i + 1]
                    else:
                        A[i] = A[i - 1]
    # if t:
    #     for outlier in t:
    #         for i in range(len(A)):
    #             if A[i]==outlier["instance"][0]:
    #                 # tm= average(A, A[i])
    #                 if (outlier["instance"][0]> ave):
    #                     A[i]=ave+de
    #                 else:
    #                     A[i]=ave-de
    #


    return A

