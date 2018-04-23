import math
import ARMAMath
class MAModel(object):
    data=[]
    p=0
    def __init__(self,data,p):
        self.data=data
        self.p=p
    
    def solveCoeOfMA(self):
        vec=[]
        maCoe,flag=ARMAMath.computeMACoe(self.data,self.p)
        vec.append(maCoe)
        return vec,flag