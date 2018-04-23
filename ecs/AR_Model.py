import ARMAMath
class ARModel(object):
    data=[]
    p=0
    def __init__(self,data,p):
        self.data=data
        self.p=p
    def solveCoeOfAR(self):
        vec=[]
        arCoe,flag=ARMAMath.computeARCoe(self.data,self.p)
        vec.append(arCoe)
        return vec,flag