#!/usr/bin/env python
import os
import json
import commands
import time
import sys
import random

if len(sys.argv) < 3:
    print "please input tx number and time span"
    sys.exit(-1)

sendCount = int(sys.argv[1])
timeSpan =  sys.argv[2]


count =0 
toAdd="\"LhZVFci1uvJNSSQB8NaSqku7Zy79tCxtiL\""

print ("begin send trans!")
while count < sendCount:
    return_code, unspents = commands.getstatusoutput("/home/chenhuan/BlockChainResearch/litecoind-src listunspent")

    if return_code != 0:
        print("system errors: cannot get unspents")
        sys.exit(-1)
    unspentlist = json.loads(unspents)
    for entry in unspentlist:
	
        if entry["confirmations"] < 10:
            continue
	print "count:" + str(count)
        txid= '"' + entry["txid"]+ '"'
        address='"'+entry["address"]+'"'
        vout = entry["vout"]
        amount = entry["amount"]
        sentamount = amount * random.random()
        keepamount = amount - 0.01 - sentamount
        if keepamount < 0 :
            continue
        cmd= '''/home/chenhuan/BlockChainResearch/litecoind-src createrawtransaction ''' + """'[{"""+'''"txid":'''+ txid+ ''',"vout":'''+str(vout)+"""}]'""" +""" '{"""+address+":"+str(keepamount)+"," + toAdd+":"+str(sentamount)+"""}'"""
        return_code,rawTrans = commands.getstatusoutput(cmd)

        signedCmd='''/home/chenhuan/BlockChainResearch/litecoind-src signrawtransaction ''' + rawTrans
        return_code,signedTrans = commands.getstatusoutput(signedCmd)
        signedHax=json.loads(signedTrans)["hex"]
    
        sendCmd='''/home/chenhuan/BlockChainResearch/litecoind-src sendrawtransaction ''' + signedHax
        return_code,newTxID = commands.getstatusoutput(sendCmd)
        
        toAdd=address
     
        if return_code == 0:
            print("new Tx:" +newTxID)
            count=count+1
            time.sleep(float(timeSpan))
	else:
	    print("send error:"+ return_code)
        if count >= sendCount:
            break

print("finish")

           

  
    

