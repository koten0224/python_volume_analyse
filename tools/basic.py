# - * - coding: utf-8 - * -
import time
from threading import Thread as thr
from threading import Semaphore as sm

sem = sm(30)

def exception(func):
    '''
    把這個function當decorator掛在function前面
    當發生exception可以輸出錯誤報告
    '''
    def wrapper(*args , **kwargs):
        try:return func( *args , **kwargs)
        except Exception as exp:

            
            error_title = type(exp).__name__
            error_code = str(exp)
            error_message = error_title + ': ' + error_code
            with open('log.txt' , 'a' , newline = '' , encoding = 'utf-8-sig') as file:
                crtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                file.write('time: {}\r\n'.format(crtime))
                file.write('function: {}\r\n'.format(func.__name__))
                file.write('args: \r\n')
                for num,arg in enumerate(args,start=1):
                    arg = str(arg)[:100]
                    file.write('\targ{}: {}\r\n'.format(num,arg))
                for key , value in kwargs.items():
                    file.write('\t' + 'arg:{} = {}\r\n'.format(key,value))
                file.write('- ' * 10 + '\r\n')
                file.write(error_message + '\r\n')
                file.write('=' * 30 + '\r\n')
                
    return wrapper

class basic_scrapy(thr):
    '''
    多線程爬蟲使用之基本型別
    拿來繼承用的
    僅使用在本次專案，要拿作他用需改寫
    '''
    def __init__(self,url,type_):
        thr.__init__(self,name=url)
        self.url = url
        self.type = type_
    def __repr__(self):
        return '\ttype: {}\r\n\t\turl: {}'.format(self.type,self.url)
    def run(self):
        sem.acquire()
        self.run_content()
        sem.release()
    
    @exception
    def run_content(self):
        pass
