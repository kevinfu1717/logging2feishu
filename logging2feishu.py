import logging
from logging.handlers import RotatingFileHandler
import feishuConnector as FS
import time
import threading
from multiprocessing import Process
CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0

_levelToName = {
    CRITICAL: 'CRITICAL',
    ERROR: 'ERROR',
    WARNING: 'WARNING',
    INFO: 'INFO',
    DEBUG: 'DEBUG',
    NOTSET: 'NOTSET',
}
_nameToLevel = {
    'CRITICAL': CRITICAL,
    'FATAL': FATAL,
    'ERROR': ERROR,
    'WARN': WARNING,
    'WARNING': WARNING,
    'INFO': INFO,
    'DEBUG': DEBUG,
    'NOTSET': NOTSET,
}

class LoggerThread(logging.Logger,threading.Thread):

    def __init__(self, name, local_level='DEBUG', file=None, encoding='utf-8',updateInterval=90,
                 feishu_level='DEBUG',feishu_app_token='',feishu_personal_base_token='',print_table_id=None,history_table_id=None):
        TT=threading.Thread
        TT.__init__(self,)
        # logger init
        self.name=name
        self.local_level=local_level
        self.feishuLevel=feishu_level
        self.file=file
        self.encoding=encoding
        self.loggerInit()
        # feishu init
        retainHistoryNums=500
        if len(feishu_app_token)>0 and len(feishu_personal_base_token)>0 and len(print_table_id)>0:
            self.printTableID=print_table_id
            self.historyTableID=history_table_id
            self.feishu_personal_base_token=feishu_personal_base_token
            self.feishu_app_token=feishu_app_token
            FS.clearTableRecords(self.printTableID,self.feishu_app_token,self.feishu_personal_base_token,0)
            if self.historyTableID is not None:
                FS.clearTableRecords(self.historyTableID,self.feishu_app_token,self.feishu_personal_base_token,retainHistoryNums)
        
        
        # interval update to feishu
        self.updateInterval=updateInterval
        self.msgBufferList=[]
        self.runFlag=True
    def loggerInit(self):
        self.LL=logging.Logger
        # 日志收集器
        # self.logger = logging.getLogger(name)
        self.LL.__init__(self,name=self.name) # Logger(name)
        # 级别
        # loggingLevel=eval('logging.'+level)
        
        # 格式
        fmt = '%(asctime)s %(filename)s %(funcName)s [line:%(lineno)d] %(levelname)s %(message)s'
        ft = logging.Formatter(fmt)
        
        # 初始化输出渠道
        if self.file:
            file_handle = RotatingFileHandler(self.file,encoding=self.encoding, maxBytes=1024*1024*10, backupCount=10)
            file_handle.setLevel(self.local_level)
            file_handle.setFormatter(ft)
            self.addHandler(file_handle)
        
        console=logging.StreamHandler()
        console.setLevel(self.local_level)
        console.setFormatter(ft)
        self.addHandler(console)
    def run(self):
        
        while self.runFlag:
            # print('loop')
            self.processUpateBuffer()
            time.sleep(self.updateInterval)
    def add2UpdateBuffer(self,setting,msg):
        if self.printTableID is not None:
            oneMsg=[msg,_levelToName[setting]]
            self.msgBufferList.append(oneMsg)
    def processUpateBuffer(self):
        if len(self.msgBufferList)>0:
            res=self.add2feishu(self.msgBufferList,self.printTableID)
            if self.historyTableID is not None:
                self.add2feishu(self.msgBufferList,self.historyTableID)
            #
            if res:
                self.msgBufferList=[]
            else:
                newBuffer=[]
                for index,re in enumerate(res):
                    if re=='0':
                        newBuffer.append(self.msgBufferList[index])
                self.msgBufferList=newBuffer


    def add2feishu(self,msgBufferList,tableID):
        recordList=FS.combineDict(['data','level'],msgBufferList)
    
        res=FS.createAppRecord(self.feishu_app_token,self.feishu_personal_base_token,
                               tableID,recordList)
        return res
    def debug(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'DEBUG'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.debug("Houston, we have a %s", "thorny problem", exc_info=1)
        """
        setting=DEBUG
        if eval(self.feishuLevel)<=setting:
            res=self.add2UpdateBuffer(setting,msg)
        self.LL.debug(self,msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'INFO'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.info("Houston, we have a %s", "interesting problem", exc_info=1)
        """
        setting=INFO
        if eval(self.feishuLevel)<=setting:
            res=self.add2UpdateBuffer(setting,msg)
        self.LL.info(self,msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'WARNING'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.warning("Houston, we have a %s", "bit of a problem", exc_info=1)
        """
        
        setting=WARNING
        if eval(self.feishuLevel)<=setting:
            res=self.add2UpdateBuffer(setting,msg)
        self.LL.warning(self,msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'ERROR'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.error("Houston, we have a %s", "major problem", exc_info=1)
        """
        setting=ERROR
        if eval(self.feishuLevel)<=setting:
            res=self.add2UpdateBuffer(setting,msg)
        self.LL.error( self,msg, args, **kwargs)

    def exception(self, msg, *args, exc_info=True, **kwargs):
        """
        Convenience method for logging an ERROR with exception information.
        """
        self.error(msg, *args, exc_info=exc_info, **kwargs)

    def critical(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'CRITICAL'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.critical("Houston, we have a %s", "major disaster", exc_info=1)
        """
        setting='CRITICAL'
        if eval(self.feishuLevel)<=setting:
            res=self.add2UpdateBuffer(setting,msg)
        self.LL.critical(self, msg, args, **kwargs)

    fatal = critical

def Logger(name, local_level='DEBUG', file=None, encoding='utf-8',updateInterval=90,
            feishu_level='INFO',feishu_app_token='',feishu_personal_base_token='',print_table_id='',history_table_id=''):
    log = LoggerThread(name, local_level,file,encoding,updateInterval,
                        feishu_level,feishu_app_token,feishu_personal_base_token,print_table_id,history_table_id)
    
    log.start()
    return log


if __name__=='__main__':
    app_token='H2zYbWPAaaL6dosbQmscDybPnpo'
    base_token='pt-XnQYlq2Bc1_Nz29o8ZX4Ks5IvGxf4LDyYXe-XmWLAQAAA4CB3wKAwrLiVB_6'
    table_id='tblEhWjCKkJwVvmz'
    h_table_id='tblaC2SzfQMTRzPt'
    l = Logger(name='haha', file='test2.log',updateInterval=20,
            feishu_app_token=app_token,feishu_personal_base_token=base_token,print_table_id=table_id,history_table_id=h_table_id)
    
    l.debug('1111111info level是qqqqqq12sdf3')
    time.sleep(2)
    
    l.info('IIIIINFO level是qqqqqq12sdf3')
    time.sleep(2)
    l.warning('22222222222info level是qqqqqq12sdf3')
    # time.sleep(160)