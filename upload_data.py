
from redis import Redis
from json import loads
import os
# 星期[1,2,3,4,5]
import os

PRO_PATH = os.path.dirname(os.path.abspath(__file__))


def read_datas(file_path:str) -> dict:
    with open(file_path,'r',encoding='utf-8') as f:
        strings = f.read()
        return loads(strings)


def generateor_data():
    """
    这个函数用于将爬取到的数据整理后生成给外部调用以使用

    Yields:
        tuple -- 返回所有楼的的信息,以及对应的星期数
    """
    weekdays = ("1","2","3","4","5")
    file_name = 'g.json'
    for each_day in weekdays:
        file_path = "{}/{}/{}".format(PRO_PATH,each_day,file_name)
        
        room_info_each_day = read_datas(file_path)
        yield room_info_each_day,each_day 



def clean_list(data:list):
    """
    对每个房间的信息列表进行标记,红的表示被不空闲标记为0,绿的标记为1
    得到类似的输出 A101/1100110000000

    Arguments:
        data {list} -- 房间的每一节课的信息

    Returns:
        str -- 格式化后的每个房间的信息
    """
    c_lsit = list(map(clean,data))
    room = c_lsit[0]
    room_info = '{}/{}'.format(room,''.join(c_lsit[1:]))
    return room_info

def clean(x):
    if x != "Red" and x != "Green":
        return x
    if x == "Red":
        return "0"
    return "1"


def upload_datas():
    """
    这个函数将本地爬取到的数据上传到服务器的redis数据库当中
    对本地数据的读取通过generateor_data()这个方法, 是一个生成器
    """
    # rdb  = Redis('127.0.0.1',db=1) # 本地
    rdb  = Redis('your host of redis-server',db=1,password='your redis password') # server
    
    for datas,each_day in generateor_data():
        data_info:list = datas['rooms_info']

        for each_room in data_info:
            build_num = each_room[0][0]
            # print(build_num)
            key_name = '{}{}'.format(each_day,build_num)
            each_room_data = clean_list(each_room)
            res = rdb.rpush(key_name,each_room_data)
            print(res)


def main():   
    upload_datas()
    
if __name__ == '__main__':
    main()
