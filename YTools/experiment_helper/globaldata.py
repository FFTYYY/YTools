from typing import Any, Union, Callable, List


LoggerModeType = Callable[[str,Any,Union[int,None],dict,str], Any]

global_datas = {}
global_now_times = {}
global_modes = {}

class GlobalDataLogger:
    '''用来记录全局信息的组件。	
	'''

    def __init__(self, namespace: str = "global", mode: List[LoggerModeType] = []):
        '''mode：在获得记录时要向何处输出。mode的每个元素是一个输出方法，获得四个参数，分别是key，val，timestamp和当前的全部data。
        '''
        global global_datas
        global global_now_times
        global global_modes

        if global_datas.get(namespace) is None:
            global_datas[namespace] = {}

        if global_now_times.get(namespace) is None:
            global_now_times[namespace] = {}

        if global_modes.get(namespace) is None:
            global_modes[namespace] = []
        for md in mode:
            global_modes[namespace].append(md) # 要用原地修改

        self.data = global_datas[namespace]
        self.now_time = global_now_times[namespace]
        self.mode = global_modes[namespace]

        self.set = self.update
        self.log = self.update

    def update(self, key: str, val: Any, timestamp: Union[int,None] = None, modespace = None):
        
        if self.data.get(key) is None:
            self.data[key] = {}
            self.now_time[key] = -1
        
        now_time = timestamp
        if now_time is None:
            now_time = self.now_time[key] + 1 # 自动更新时间戳
        self.data[key][self.now_time[key]] = val
        
        self.now_time[key] = now_time

        for md in self.mode:
            md(key,val,timestamp,self.data,modespace)
        
    def get(self, key):
        return self.data.get(self.now_time.get(key))

GlobalData = GlobalDataLogger()

def init_globaldata(mode: List[LoggerModeType] = []):
    '''mode：在获得记录时要向何处输出。mode的每个元素是一个输出方法，获得四个参数，分别是key，val，timestamp和当前的全部data。
    '''
    return GlobalDataLogger(mode = mode)
