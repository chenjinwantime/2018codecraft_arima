import math
import Tools
#class ARMAMath(object):
import random

def get_mean(data):
    return float(sum(data))/len(data)
    
def get_varerr(data):
    if len(data)==0:
        return 0.0
    variance=0.0
    meansum=Tools.get_mean(data)
    for i in range(0,len(data)):
        data[i]-=meansum
        variance+=data[i]*data[i]   
    return variance/(len(data)-1)

def stderr(data):
    return math.sqrt(get_varerr(data))
    
def get_autocov(data,order):
    #autoCov=[1]*(order+1)
    #define a list ,len(list)=order+1
    #print 'data'
    #print data
    autoCov=[]
    order=int(order)
    for i in range(0,order+1):
        autoCov.append(0.0)
    mu =get_mean(data)
    order=int(order)
    for i in range(0,order+1):
        autoCov[i]=0.0
        for j in range(0,len(data)-i):
            autoCov[i]+=(data[j+i]-mu)*(data[j]-mu)
        #print 'i'
        #print i
        #print autoCov[i]
        autoCov[i]/=(len(data)-i)
    return autoCov
    
#order=p+q
def get_autocor(data,order):
    autoCor=[]
    autoCov=get_autocov(data,order)
    var=get_varerr(data)
    if var!=0:
        for i in range(order):
            autoCor.append(autoCov[i]/var)
    return autoCor

    
    
def get_mutalCorr(dataFir,dataSec):
    sumX=0.0
    sumY=0.0
    sumXY=0.0
    sumXSq=0.0
    sumYSq=0.0
    length=0
    if len(dataFir)!=len(dataSec):
        length=min(len(dataFir),len(dataSec))
    else:
        length=len(dataFir)
    for i in range(length):
        sumX+=dataFir[i]
        sumY+=dataSec[i]
        sumXY+=dataFir[i]*dataSec[i]
        sumXSq+=dataFir[i]*dataFir[i]
        sumYSq+=dataSec[i]*dataSec[i]
    numerator = sumXY - sumX*sumY/length
    denominator=math.sqrt((sumXSq-sumX*sumX/len)*(sumYSq-sumY*sumY/len))
    if denominator==0:
        return 0.0
    return numerator/denominator
 
#random.gauss(mu,sigma)     
 
 
def get_ModelAIC(vec,data,type):
    n=len(data)
    p=0
    q=0
    tmpAR=0.0
    tmpMA=0.0
    sumErr=0.0
    if type==1:
        #print vec[0]
        #print type
        maCoe=vec[0]
        q=int(len(maCoe))
        #errData=[1]*(q+1)
        errData=[]
        for i in range(0,q+1):
            errData.append(0.0)
        for i in range(q-1,n):
            tmpMA=0.0
            for j in range(1,q):
                tmpMA+=maCoe[j]*errData[j]
            for j in range(q-1,0,-1):
                errData[j]=errData[j-1]
            #print type(random.gauss(0,1)*(float)math.sqrt(maCoe[0]))
            #print maCoe[0]
            #a=math.sqrt(float(maCoe[0]))
            #print a
            random.seed(i)
            errData[0]=float(random.gauss(0,1))*float(math.sqrt(maCoe[0]))
            sumErr+=(data[i]-tmpMA)*(data[i]-tmpMA)
        return (n-(q-1))*math.log(sumErr/(n-(q-1)))+(q+1)*2
    elif type==2:
        arCoe=vec[0]
        p=int(len(arCoe))
        for i in range(p-1,n):
            tmpAR=0.0
            for j in range(0,p-1):
                tmpAR+=arCoe[j]*data[i-j-1]
            sumErr+=(data[i]-tmpAR)*(data[i]-tmpAR)
        return (n-(p-1))*math.log(sumErr/(n-(p-1)))+(p+1)*2
    else:
        arCoe=vec[0]
        maCoe=vec[1]
        q=int(len(maCoe))
        p=int(len(arCoe))
        #errData=[0]*(q+1)
        errData=[]
        for i in range(0,q+1):
            errData.append(0)
        for i in range(p-1,n):
            tmpAR=0.0
            for j in range(0,p-1):
                tmpAR+=arCoe[j]*data[i-j-1]
            tmpMA=0.0
            for j in range(q-1,0,-1):
                errData[j]=errData[j-1]
            #print maCoe[0]
            if maCoe[0]<0:
                maCoe[0]=0
            random.seed(i+3)
            errData[0]=random.gauss(0,1)*math.sqrt(maCoe[0])
            sumErr += (data[i] - tmpAR - tmpMA) * (data[i] - tmpAR - tmpMA)
        return (n - (q + p - 1)) * math.log(sumErr / (n - (q + p - 1))) + (p + q) * 2
        
def LevisonSolve(garma):
    #print 'garma'
    #print garma
    flag=True
    order=len(garma)-1
    #result=[[0]*(order+1)]*(order+1)
    result=[]
    for i in range(0,order+1):
        tmp=[]
        for j in range(0,order+1):
            tmp.append(0)
        result.append(tmp)
        
    #sigmaSq=[0]*(order+1)
    sigmaSq=[]
    for i in range(0,order+1):
        sigmaSq.append(0)
    sigmaSq[0]=garma[0]
    
    if sigmaSq[0]==0:
        result[1][1]=0
        flag=False
    else:
        flag=True
        result[1][1]=garma[1]/sigmaSq[0]
    sigmaSq[1]=sigmaSq[0]*(1.0-result[1][1]*result[1][1])
    
    for k in range(1,order):
        sumTop=0.0
        sumSub=0.0
        for j in range(1,k+1):
            sumTop += garma[k + 1 - j] * result[k][j]
            sumSub += garma[j] * result[k][j]
        if garma[0]-sumSub==0:
            result[k+1][k+1]=0
            flag=False
        else:
            result[k+1][k+1]=(garma[k + 1] - sumTop) / (garma[0] - sumSub)
            flag=True
        for j in range(1,k+1):
            result[k + 1][j] = result[k][j] - result[k + 1][k + 1] * result[k][k + 1 - j]
        sigmaSq[k + 1] = sigmaSq[k] * (1.0 - result[k + 1][k + 1] * result[k + 1][k + 1])
    result[0] = sigmaSq
    return result,flag
    
def computeARCoe(data,p):
    garma=get_autocov(data,p)
    #print 'AR_171'
    result,flag=LevisonSolve(garma)
    #ARCoe=[0]*(p+1)
    ARCoe=[]
    for i in range(0,p+1):
        ARCoe.append(0)
    for i in range(0,p):
        ARCoe[i]=result[p][i+1]
    ARCoe[p]=result[0][p]
    return ARCoe,flag

def computeMACoe(data,q):
    p=math.log(len(data))
    bestGarma=get_autocov(data,p)
    #print 'MA_184'
    bestResult,flag=LevisonSolve(bestGarma)
    p=int(p)
    #alpha=[0]*(int(p)+1)
    alpha=[]
    for i in range(0,p+1):
        alpha.append(0)
    alpha[0]=-1
    for i in range(1,int(p)+1):
        alpha[i]=bestResult[p][i]
    #paraGarma=[0]*(q+1)
    paraGarma=[]
    for i in range(0,q+1):
        paraGarma.append(0)
    for k in range(0,q+1):
        sum=0.0
        for j in range(0,p-k+1):
            sum+=alpha[j]*alpha[k+j]
        paraGarma[k]=sum/bestResult[0][p]
    #print 'MA_202'
    tmp,flag=LevisonSolve(paraGarma)
    #MACoe=[0]*(q+1)
    MACoe=[]
    for i in range(0,q+1):
        MACoe.append(0)
    
    for i in range(1,len(MACoe)):
        MACoe[i]=-tmp[q][i]
    MACoe[0]=1/tmp[0][q]
    return MACoe,flag

def computeARMACoe(data,p,q):
    allGarma=get_autocov(data,p+q)
    #garma=[0]*(p+1)
    garma=[]
    for i in range(0,p+1):
        garma.append(0)
    
    for i in range(0,len(garma)):
        garma[i]=allGarma[q+i]
    #print 'ARMA_222'
    #print garma
    #print p 
    #print q
    arResult,flag=LevisonSolve(garma)
    
    #ARCoe=[0]*(p+1)
    ARCoe=[]
    for i in range(0,p+1):
        ARCoe.append(0)
        
    for i in range(0,p):
        ARCoe[i]=arResult[p][i+1]
    ARCoe[p]=arResult[0][p]
    
    #alpha=[0]*(p+1)
    alpha=[]
    for i in range(0,p+1):
        alpha.append(0)
    alpha[0]=-1
    for i in range(1,p+1):
        alpha[i]=ARCoe[i-1]
    #paraGarma=[0]*(q+1)
    paraGarma=[]
    for i in range(0,q+1):
        paraGarma.append(0)
    for k in range(0,q+1):
        sum=0.0
        for i in range(0,p+1):
            for j in range(0,p-k+1):
                sum += alpha[i] * alpha[j] * allGarma[abs(k + i - j)]
        paraGarma[k]=sum
    #print 'ARMA_251'
    maResult,flag=LevisonSolve(paraGarma)
    #MACoe=[0]*(q+1)
    MACoe=[]
    for i in range(0,q+1):
        MACoe.append(0)
    for i in range(1,len(MACoe)):
        MACoe[i]=maResult[q][i]
    MACoe[0]=maResult[0][q]
    
    #ARMACoe=[0]*(p+q+2)
    ARMACoe=[]
    for i in range(0,p+q+2):
        ARMACoe.append(0)
    for i in range(0,len(ARMACoe)):
        if i<len(ARCoe):
            ARMACoe[i]=ARCoe[i]
        else:
            ARMACoe[i]=MACoe[i-len(ARCoe)]
    return ARMACoe,flag
    
    
    
def inner_product(data1,data2,init):
    length1=len(data1)
    length2=len(data2)
    #print length1
    #print length2
    for i in range(0,length1):
        init=init+data1[i]*data2[i]
    return init
    