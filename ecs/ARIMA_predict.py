#coding=utf-8
import ARIMA_Model
import math
import Tools
import test_lof
def predict_arima_sigle(data):
    period=0
    modelCnt=5
    cnt=0
    list=[]
    #tmpPredict=[0]*modelCnt
    tmpPredict=[]
    for i in range(0,modelCnt):
        tmpPredict.append(0)
    arima=ARIMA_Model.ARIMAModel(data)
    list=[]
    flag=True
    for k in range(0,modelCnt):
        bestModel=[]
        #print k
        if k==0:
            #print 'the first if'
            bestModel,flag=arima.getARIMAModel(period,list,False)
            #print bestModel
        else:
            bestmodel,flag=arima.getARIMAModel(period,list,True)
        #print 'bestModel'
        #print bestModel
        #print len(bestModel)
        #tmp=len(bestModel)
        if flag==False:
            list.append(bestModel)
            continue
        if len(bestModel)==0:
            #print 'k'
            #print k
            tmpPredict[k]=int(data[len(data)-period-1])
            cnt=cnt+1
            break
        else:
            predictDiff = arima.predictValue(bestModel[0], bestModel[1], period)
            #print 'predictDiff'
            #print predictDiff
            tmpPredict[k] = arima.aftDeal(predictDiff, period)
            cnt=cnt+1
        list.append(bestModel)
        print 'list'
        print list
    sumPredict=0.0
    
    
    print tmpPredict
    #print cnt
    for k in range(0,cnt):
        sumPredict+=float(tmpPredict[k])/float(cnt)
    predict=int(round(sumPredict))
    #print 'predict'
    #print predict
    if predict<0:
        predict=0
    return predict

  
def predict_arima_forecast(data,days):
    period=1
    
    print '原始data',data
    
    ave=Tools.average(data)
    de=Tools.delat(data,ave)
    
    data = test_lof.ErrorDection3(data,ave,de)
    print 'first qu noise_data',data,ave,de
    
    ave=Tools.average(data)
    de=Tools.delat(data,ave)
    
    #data = test_lof.ErrorDection3(data,ave,de)
    print 'second qu noise_data',data,ave,de
    
    
    #归一化
    min,max=Tools.getmin_max(data)
    min=float(min)
    print "max   ",max,"  mimi  " ,min
    for i in range(len(data)):
        data[i]=float((data[i]-min)/(max-min))
        data[i]=data[i]*8
    print 'data',data
    
    
    
    #差分
    #print 'period'
    #print period
    for day in range(0,days):

        modelCnt=5
        #取modelCnt均值，与ARIMAModel.getARIMAModel中的length一致
        cnt=0
        list=[]
        flag=True
        #tmpPredict=[0]*modelCnt
        tmpPredict=[]
        for i in range(0,modelCnt):
            tmpPredict.append(0.0)
        arima=ARIMA_Model.ARIMAModel(data)
        list=[]
        
        for k in range(0,modelCnt):
            #print 'modelCnt_k'
            #print k
            bestModel=[]
            #print k
            if k==0:
                #print 'the first if'
                bestModel,flag=arima.getARIMAModel(period,list,False)
                #print 'bestModel'
                #print bestModel
                #print k
                #print bestModel
            else:
                bestModel,flag=arima.getARIMAModel(period,list,True)
                #print 'else_bestModel'
                #print bestModel
                #print k
            
            
            if flag==False:
                list.append(bestModel)
                continue
            #print len(bestModel)
            #tmp=len(bestModel)
            if len(bestModel)==0:
                #print 'k'
                #print k
                tmpPredict[k]=float(data[len(data)-period-1])
                if tmpPredict[k]<0:
                    tmpPredict[k]=0
                else:
                    cnt=cnt+1
                break
            else:
                predictDiff = arima.predictValue(bestModel[0], bestModel[1], period)
                #print 'predictDiff'
                #print predictDiff
                #predictDiff=predictDiff
                tmpPredict[k] = arima.aftDeal(predictDiff, period)
                if tmpPredict[k]<0:
                    tmpPredict[k]=0
                else:
                    cnt=cnt+1
            list.append(bestModel)
        #print 'list'
        #print list
        sumPredict=0.0
        print 'tmpPredict'
        print tmpPredict
        for i in range(0,len(tmpPredict)):
            if tmpPredict[i]<0:
                tmpPredict[i]=0
                cnt=cnt-1
        
        #data.append(int(tmpPredict[1]))
        
        #print tmpPredict
        #print cnt
        for k in range(0,cnt):
            sumPredict+=float(tmpPredict[k])/float(cnt)
        #predict=int(math.floor(sumPredict))
        #predict=int(math.ceil(sumPredict))
        predict=sumPredict
        #print 'predict'
        #print predict
        
        if predict<0:
            predict=0
        data.append(predict)
        
    print 'data_predict',data
    for i in range(len(data)):
        data[i]=data[i]/8
        data[i]=data[i]*(max-min)+min
        
    print 'data_transform'
    print data
    return int(sum(data[-7:]))


    
