import ARMAMath
class ARMAModel(object):
    data=[]
    p=0
    q=0
    
    def __init__(self,data,p,q):
        self.data=data
        self.p=p
        self.q=q
    
    
    def solveCoeOfARMA(self):
        vec=[]
        armaCoe,flag=ARMAMath.computeARMACoe(self.data,self.p,self.q)
        #arCoe=[0]*(self.p+1)
        arCoe=[]
        for i in range(0,self.p+1):
            arCoe.append(0)
        for i in range(0,len(arCoe)):
            arCoe[i]=armaCoe[i]
        #maCoe=[0]*(self.q+1)
        maCoe=[]
        for i in range(0,self.q+1):
            maCoe.append(0)
        for i in range(0,len(maCoe)):
            maCoe[i]=armaCoe[i+self.p+1]
        vec.append(arCoe)
        vec.append(maCoe)
        return vec,flag
        
    