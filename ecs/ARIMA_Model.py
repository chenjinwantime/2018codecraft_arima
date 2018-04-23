import math
import ARMAMath
import random
import AR_Model
import MA_Model
import ARMA_Model

class ARIMAModel(object):

    data=[]
    dataFirDiff=[]
    arima=[]

    def __init__(self, data):
        self.data=data
    
    
    def preFirDiff(self,preData):
        res=[]
        for i in range(0,len(preData)-1):
            tmpData=preData[i+1]-preData[i]
            res.append(tmpData)
        return res

    def preSeasonDiff(self,preData,period):
        res=[]
        for i in range(0,len(preData)-period):
            tmpData=preData[i+period]-preData[i]
            res.append(tmpData)
        return res
        
    def preDealDiff(self,period):
        if period>=len(self.data)-1:
            period=0
        if period==0:
            return self.data
        elif period==1:
            tmp=self.preFirDiff(self.data)
            self.dataFirDiff=tmp
            return tmp
        else: 
            tmp=self.preSeasonDiff(self.data,period)
            return tmp
     
    def getARIMAModel(self,period,notModel,needNot):
        ##print 'getARIMAModel'
        data=self.preDealDiff(period)
        minAIC=1.7976931348623157E308
        bestModel=[0,0,0]
        
        type=0
        coe=[]
        
        length=len(data)
        if length>5:
            length=5
        
        size =(length+2)*(length+1)/2-1
        #print 'size'
        #print size
        #model=[[0]*2]*size
        model=[]
        #print model
        cnt=0
        for i in range(0,length+1):
            for j in range(0,length-i+1):
                if i==0 and j==0:
                    continue
                #print i
                #print j
                #print cnt
                sub_model=[]
                sub_model.append(i)
                sub_model.append(j)
                model.append(sub_model)
                cnt=cnt+1
                #print model
        #print 'size'
        #print model
        for i in range(0,cnt):
            #print i
            token=False
            if needNot:
                for k in range(0,len(notModel)):
                    if model[i][0]==notModel[k][0] and model[i][1]==notModel[k][1]:
                        token=True
                        #print 'break'
                        break
            #print 'wai_break'            
            if token: 
                continue
            #print 'model'
            #print model
            
            if model[i][0]==0:
                ma=MA_Model.MAModel(data,model[i][1])
                coe,flag=ma.solveCoeOfMA()
                type=1
            elif model[i][1]==0:
                ar=AR_Model.ARModel(data,model[i][0])
                coe,flag=ar.solveCoeOfAR()
                type=2
            else: 
                #print 'arma'
                arma=ARMA_Model.ARMAModel(data,model[i][0],model[i][1])
                coe,flag=arma.solveCoeOfARMA();
                type=3
            #print 'type'
            #print type
            aic=ARMAMath.get_ModelAIC(coe,data,type)
            #print 'aic'
            #print aic
            
            if aic<1.7976931348623157E308 and not math.isnan(aic) and aic < minAIC:
                #print 'minAIC'
                minAIC=aic
                bestModel[0]=model[i][0]
                bestModel[1]=model[i][1]
                bestModel[2]=int(round(minAIC))
                self.arima=coe
                #print 'coe'
                #print coe
        #print 'bestModel_fuction'        
        #print bestModel        
        return bestModel,flag
    
        ##print bestModel
        #return bestModel
            
    def aftDeal(self,predictValue,period):
        if period>=len(self.data):
            period=0
        if period==0:
            return int(predictValue)
        elif period==1:
            return int(predictValue+self.data[len(self.data)-1])
        else: 
            return int(predictValue+self.data[len(self.data)-period])
        
    def predictValue(self,p,q,period):
        #print 'predictValue'
        #print p
        #print q
        #print period
        data=self.preDealDiff(period)
        n=len(data)
        predict=0
        tmpAR=0.0
        tmpMA=0.0
        #errData=[0]*(q+1)
        errData=[]
        for i in range(0,q+1):
            errData.append(0)
            
            
           
        #FIRST
        if p==0:
            maCoe=self.arima[0]
            for k in range(q,n):
                tmpMA=0.0
                for i in range(1,q+1):
                    tmpMA+=maCoe[i]*errData[i]
                for j in range(q,0,-1):
                    errData[i]=errData[j-1]
                random.seed(k+5)
                errData[0]=random.gauss(0,1)*math.sqrt(abs(maCoe[0]))
                #print 'tmpMA'
                #print tmpMA
            #predict=math.ceil(tmpMA)
            #predict=math.floor(tmpMA)
            predict=round(tmpMA)
            predict=float(tmpMA)
       
        
        elif q==0:
            arCoe=self.arima[0]
            for k in range(p,n):
                tmpAR=0.0
                for i in range(0,p):
                    tmpAR+=arCoe[i]*data[k-i-1]
                #print 'tmpAR'
                #print tmpAR
            #predict=math.ceil(tmpAR)
            #predict=math.floor(tmpAR)
            predict=float(tmpAR)
        else:
            #print self.arima
            arCoe=self.arima[0]
           
            maCoe=self.arima[1]
            for k in range(p,n):
                tmpAR=0.0
                tmpMA=0.0
                for i in range(0,p):
                    tmpAR+=arCoe[i]*data[k-i-1]
                for i in range(1,q+1):
                    tmpMA+=maCoe[i]*errData[i]
                for j in range(q,0,-1):
                    errData[j] = errData[j-1]
                random.seed(k+7)
                errData[0] = random.gauss(0,1)* math.sqrt(abs(maCoe[0]))
            
                #print 'tmpAR'
                #print tmpAR
                #print 'tmpMA'
                #print tmpMA
            #predict = (math.ceil)(tmpAR + tmpMA)
            #predict = (math.floor)(tmpAR + tmpMA)
            predict = float(tmpAR + tmpMA)
        return predict
                
                
        


'''
        #SECOND
        if p==0:
            
            
            eps=[]
            for i in range(0,n):
                eps.append(0)
            #del errData[-1]
            #print len(errData)
            
            maCoe=self.arima[0]
            #print len(maCoe)
            eps[0]=data[0]
            for i in range(1,n):
                if i<q:
                    eps[i]=data[i]-ARMAMath.inner_product(maCoe[0:i],errData,0)
                else: 
                    #errData[i]=data[i]-ARMAMath.inner_product(maCoe,errData[i-q:],0)
                    eps[i]=data[i]-ARMAMath.inner_product(maCoe,eps[i-q:],0)
            for i in range(0,q):
                    tmpMA+=maCoe[i]*eps[i-q]
        '''                  
        
        
        
        
        
        