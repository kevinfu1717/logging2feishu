from baseopensdk import BaseClient,JSON
from baseopensdk.api.base.v1 import *


# APP_TOKEN = os.environ['APP_TOKEN']
# PERSONAL_BASE_TOKEN = os.environ['PERSONAL_BASE_TOKEN']
# TABLE_ID = os.environ['TABLE_ID']
def resultAnilysis(thisResponse):# ='1' True ,else failed
    result=''
    try:
        records=thisResponse.data.records
    except:
        result='0'
        return result
    for record in records:
        try:
            rid=record.record_id
            if len(rid)>0:
                result+='1'
            else:
                result+='0'
        except:
            result+='0'
    if '0' not in result: result='1'
    return result

def createBase(APP_TOKEN,PERSONAL_BASE_TOKEN):
      # 1. 构建client
    client: BaseClient = BaseClient.builder() \
        .app_token(APP_TOKEN) \
        .personal_base_token(PERSONAL_BASE_TOKEN) \
        .build()
    return client
def combineDict(keyList,stringsList):
    resultList=[]
    for strings in stringsList:
        
        fieldDict={}
        for index,key in  enumerate(keyList):
            fieldDict.update({key:str(strings[index]) })
        resultList.append({'fields':fieldDict})
    return resultList
def createAppRecord(APP_TOKEN:str,PERSONAL_BASE_TOKEN:str,TABLE_ID:str,recordList: list,reverse:bool =True):
    try:
        client=createBase(APP_TOKEN,PERSONAL_BASE_TOKEN)

        if reverse:
            recordList.reverse()
        # for value in valueList :
        #     recordList.append({'fields':{key:str(value)}})

        
        builder=BatchCreateAppTableRecordRequest().builder()
        requestBody=BatchCreateAppTableRecordRequestBody.builder().records(recordList).build()
        #BatchUpdateAppTableRecordRequestBody.builder().records(records_need_update).build()
        thisRequest=builder.table_id(TABLE_ID).request_body(requestBody).build()                  
        thisResponse = client.base.v1.app_table_record.batch_create(thisRequest)
        result=resultAnilysis(thisResponse)
    except:
        result='0'
    # 打印序列化数据
    # print(JSON.marshal(thisResponse.data, indent=4))
    return result

def delAppRecords(TABLE_ID,recordIDList,APP_TOKEN='',PERSONAL_BASE_TOKEN='',client=None):
    try:
        if client is None:
            client=createBase(APP_TOKEN,PERSONAL_BASE_TOKEN)    
        
        builder=BatchDeleteAppTableRecordRequest().builder()
        requestBody=BatchDeleteAppTableRecordRequestBody.builder().records(recordIDList).build()
        #BatchUpdateAppTableRecordRequestBody.builder().records(records_need_update).build()
        thisRequest=builder.table_id(TABLE_ID).request_body(requestBody).build()                  
        thisResponse = client.base.v1.app_table_record.batch_delete(thisRequest)
        result=resultAnilysis(thisResponse)
    except:
        result='0'
    # 打印序列化数据
    # print(JSON.marshal(thisResponse.data, indent=4))
    return result

def listAppRecords(TABLE_ID,APP_TOKEN='',PERSONAL_BASE_TOKEN='',client=None):
    
    fieldList=[]
    recordIDList=[]
    try:
        if client is None:
            client=createBase(APP_TOKEN,PERSONAL_BASE_TOKEN)    
        
        builder=ListAppTableRecordRequest().builder()
        requestBody=builder.page_size(1000).table_id(TABLE_ID).build()

        thisResponse= client.base.v1.app_table_record.list(requestBody)
        records = getattr(thisResponse.data, 'items', [])
        for record in records:
            record_id, fields = record.record_id, record.fields
            recordIDList.append(record_id)
            fieldList.append(fields)
    except:
        pass

    
    return recordIDList,fieldList
def clearTableRecords(TABLE_ID,APP_TOKEN,PERSONAL_BASE_TOKEN,retainNum=0):
    cl=createBase(APP_TOKEN,PERSONAL_BASE_TOKEN)
    recordIDList,_=listAppRecords(TABLE_ID,client=cl)
    recordNum=len(recordIDList)
    if retainNum<recordNum:
        res=delAppRecords(TABLE_ID,recordIDList[retainNum:recordNum],client=cl)
    else:
        res='1'
    return res
if __name__ == "__main__":
    # 替换所有文本字段中 'abc' 为 '233333'
    keyList=['data','level']
    stringsList=[['123123123','ERROR'],['asdfasdf','INFO'],['OOOOOOOOO','DEBUG'],['---------','WARNING']]
    recordList=combineDict(keyList,stringsList)
    print(recordList)
    res=createAppRecord(TABLE_ID,recordList)
    # recordIDList,_=listAppRecords(TABLE_ID)
    # RES=delAppRecords(TABLE_ID,recordIDList)