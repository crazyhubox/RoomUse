import requests
from parsel import Selector,SelectorList
from time import sleep
from re import compile
from json import dumps
import os
import time
from login.login_api import get_cookies

# 先得到 每天 每个楼区 每个教室 的空闲数据
# 保存到服务器,提供一个查询脚本
# 快捷指令给出参数,得到结果

color_finder = compile(r'.+?color:([a-zA-z]{3,5})')
file_path  = os.path.dirname(os.path.abspath(__file__))

def get_html_from_api(building_num:str,date:str):
    """
    通过教务处教室使用的api获取包含room信息的html给外部处理
    """
    cookies = get_cookies("u","p") #使用了获取cookie的接口    
    
    headers = {
        'authority': 'cj.shu.edu.cn',
        'accept': '*/*',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 Edg/89.0.774.48',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://cj.shu.edu.cn',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://cj.shu.edu.cn/RoomUse/RoomUseDate',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cookie': f'ASP.NET_SessionId={cookies["value"]}',
    }

    data = {
      'CurrentDate': date,
      'R_roomNo': "",
      'R_BuildNo': building_num,
      'R_CampusNo': '',
      'Mark': '0',
      'PageIndex': '1',
      'FunctionString': 'CtrlRoomUseDate'
    }

    response = requests.post('https://cj.shu.edu.cn/RoomUse/CtrlRoomUseDate', headers=headers, data=data)
    return response.text


def get_each_building_datas(data_eachBuilding:dict,date:int):
    """
    得到当日这个楼层所有房间的列表保存在json文件的rooms_info中
    {
        "building_num": "g", 
        "rooms_info": [[],[],...]
    }
    """
    date = f'2021/4/{date}'
    print(date)
    html = get_html_from_api(data_eachBuilding['building_num'],date)
    find = Selector(text=html)
    datas:SelectorList = find.css("#roomsearchtab >tr")

    for each in datas:        
        collect_each_room(each,data_eachBuilding)

    for each_room in data_eachBuilding['rooms_info']:
        print(each_room)

    return data_eachBuilding


def collect_each_room(room:Selector,data_eachBuilding):
    """
    这里是将每一个room的信息保存为一个列表
    [
        "A201", 
        "Red", 
        "Red", 
        "Red", 
        "Red", 
        "Red", 
        "Red", 
        "Red", 
        "Red", 
        "Green", 
        "Green", 
        "Green", 
        "Green", 
        "Green"
    ]
    再插入到整个楼层的列表rooms_info中
    {
        "building_num": "g", 
        "rooms_info": [[],[],...]
    }
    """
    each_rooms_info = []
    room_id:str = room.css("td:nth-child(3)::text").get()
    if not room_id:
        return 
    room_id = room_id.strip() if room_id else None
    each_rooms_info.append(room_id)
    for index in range(4,17):
        color = room.css(f"td:nth-child({index})::attr(style)").get()
        color = get_color(color)
        each_rooms_info.append(color)
    data_eachBuilding["rooms_info"].append(each_rooms_info)

def get_color(raw_style) -> str:
    """
    通过标签值得到房间是否空闲的标识
    """
    res = color_finder.search(raw_style)
    color = res[1]
    return color


def write_json(data:dict,build:str,folder:str):
    """
    爬取到的数据存入json
    """
    folder_path = os.path.join(file_path,folder)
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    
    save_path = os.path.join(folder_path,build) + '.json'
    json_str = dumps(data,sort_keys=False,indent=4,separators=(', ', ': '))
    with open(save_path,'w',encoding='utf-8') as f:
        f.write(json_str)
    

def get_today():
    """
    获取当日的日期
    格式为{}/{}/{}
    """
    time_get = time.gmtime(time.time())
    return '{}/{}/{}'.format(time_get.tm_year,time_get.tm_mon,time_get.tm_mday),time_get.tm_mday

    
def main():
    """
    进行当日room使用的爬取
    因为学校room_api的限制, 最多只能查询到当日和前一天的数据
    所以需要在第一个星期每天运行一次, 然后将数据入库
    """
    building_data = {
        "building_num":"a",
        "rooms_info":[]
    }

    buildings = ("a",'b','c','d','e','f','g')
    time_date,today_num = get_today()
    date = (today_num,)
    
    for each_day in date:
        for each_building in buildings:
            building_data['building_num'] = each_building
            buid_datas = get_each_building_datas(data_eachBuilding=building_data,date=each_day)
            print(f"{each_day}FINISHED WAIT 10 S...")
            sleep(10)
        write_json(buid_datas,building_data['building_num'],folder=str(each_day))
    

if __name__ == '__main__':
    main()
    

