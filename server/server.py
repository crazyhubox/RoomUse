from typing import NewType
from redis import Redis
from re import compile

room_check = compile(r'[a-zA-z]{1,2}[0-9]{3}$')
OtherInputType = NewType('OtherInput',str)
RoomSelectType = NewType("RoomSelect",str)
BuildSelectType = NewType("RoomSelect",str)
OtherInput = OtherInputType('OtherInput')
RoomSelect = RoomSelectType("RoomSelect")
BuildSelect = BuildSelectType("BuildSelect")


def get_time(time:str):
    if not time.isnumeric():
        raise ValueError("time format error")

    if len(time) > 2:
        return time

    if time == '11':
        return ['11','12','13']#代表11 12 13

    t1 = int(time)
    if t1 > 11:
        return ['11','12','13']

    if t1 < 1:
        raise ValueError("time format error")
    
    if t1 % 2 == 0:
        t2 = t1 - 1
        return [str(t2),str(t1)]
    
    t2 = t1 + 1
    return [str(t1),str(t2)]



def deal_command(com:str):
    if not com:
        return OtherInput

    if len(com) < 3 :
        return OtherInput

    try:
        i = com.index("/")
        time_for_check = get_time(time=com[i+1:])
        build_num = com[:i]
        return build_num.upper(),time_for_check

    except Exception as e:
        if not room_check.match(com):    
            return OtherInput

        return com.upper()
    
class Server:
    """
    这个类是放在服务器上的
    封装了查询的方法和具体的查询实现,用于对redis的中数据的查询和交互方式
    """
    def __init__(self) -> None:
        self.__rdb = Redis("127.0.0.1", 6379, db=1, decode_responses=True)
        self.__com:tuple

    def set_command(self,com:str):
        self.__com = deal_command(com)
        print(self.__com)
        if isinstance(self.__com,tuple):
            return 1
        return 0

    def _select_singal_room(self,week_day):
        room_datas = self._read_room_datas(week_day)
        if not room_datas:
            return None

        for each_room in room_datas:
            room,info =  each_room.split('/')
            if room == self.__com:
                return info
        return None

    @staticmethod
    def show_res_signal(res):
        if not res:
            print('没有结果') 
            return 

        for index,each in enumerate(res,1):
            if each == '1':
                print(index,'Green')

    def _read_room_datas(self,check_day):
        if not self.__com:
            return None       
        key_name = '{}{}'.format(check_day,self.__com[0])
        return self.__rdb.lrange(key_name, 0, self.__rdb.llen(key_name))
        
    def room_select_today(self,com,week_day):    
        res = self._select_singal_room(week_day)
        self.show_res_signal(res)
        
    def build_green_today(self,com,week_day):
        res = self._select_build_green(week_day)
        self.show_res_builds(res)

    @staticmethod
    def show_res_builds(res):
        if not res:
            print('没有结果') 
            return 
        for each in res:
            print(each,"Green")

    def _select_build_green(self,weekday):
        #此时com是个元祖
        green_rooms = []        
        check_time = self.__com[1] #['1', '2']
        check_flag = True
        # ('A', ['1', '2'])
        for each_room in self._read_room_datas(weekday):
            room,info =  each_room.split('/')
            for each_class in check_time:
                if info[int(each_class) - 1] == '0':
                    check_flag = False
                    break
            
            if check_flag:
                green_rooms.append(room)

            check_flag = True

        return green_rooms

    def deal_error_input(self,com,week_day):
        if not isinstance(week_day,int):
            if not week_day.isnumeric():
                return OtherInputType('week day must be int')
            week_day = int(week_day)

        if week_day < 1 or week_day > 5:
            return OtherInputType('week day must be between 1 and 5')

        res = self.set_command(com)

        if  self.__com == OtherInput:
            return self.__com
        
        if res:
            return BuildSelect
        return RoomSelect

    def Select(self,com:str,weekday:int):
        """
        查询的对外接口,根据查询命令和查询的星期数得到结果并打印
        会首先检查com是否合法,
        com的类型分成了
            OtherInput    其他收入类型
            RoomSelect    特定房间查询类型
            BuildSelect   楼层的查询类型
        
        如果检查com是OtherInput,直接打印
        否则根据具体进行类型做相应的输出

        输入说明: 
            com=a106,weekday=1  -- 周一a106房间的使用情况 
            com=a/2,weekday=1   -- 周一a楼23节课空闲的房间 
            com=a/6,weekday=    -- 周一a楼56节课空闲的房间
            com=a/11,weekday=1  -- 周一a楼11,12,13节课空闲的房间

        Arguments:
            com {str} -- 查询命令
            weekday {int} -- 查询星期几的数据
        """
        check_flag = self.deal_error_input(com,weekday)
        if check_flag == OtherInput:
            print(check_flag)
            return 

        if check_flag == BuildSelect:
            self.build_green_today(com,weekday)
            return 

        self.room_select_today(com,weekday)
        
        
def main():
    s = Server()
    s.Select('a/11',2)

   
if __name__ == '__main__':
    main()
