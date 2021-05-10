import requests

def get_password_key(password):
    """
    这个在本地开启了一个rpc调用的服务端
    专门实现登录密码的加密js运行
    返回的数据由于是字符串返回所以需要讲"符号去掉
    """
    url = "http://127.0.0.1:8989/key?pw={}".format(password)
    response =  requests.get(url=url)
    key = response.text.replace('"','')#接口数据的格式一致性和确认非常关键
    return key

def login(username,password):
    """
    学校登录的api
    其中的password是加密后password
    """
    cookies = {
        'SHU_OAUTH2_SESSION': 'RXIBQXHKDBUWPTVD6FVBUGF76CFD37AXTI6E34PWPKQMOVBU6BSCE7VCFX3UB6KABJQNUYRFQPBCQFEGTIOR2UBISPHWLW5RE63EITY',
    }

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'https://oauth.shu.edu.cn',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 Edg/89.0.774.48',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://oauth.shu.edu.cn/login/eyJ0aW1lc3RhbXAiOjE2MTk1NzE4NjcyMDY0NTU2MDksInJlc3BvbnNlVHlwZSI6ImNvZGUiLCJjbGllbnRJZCI6IkJ3Vk5IVVZZMTdZVTBjMEJVTjRWY2FDNjBLMzRkT1g1Iiwic2NvcGUiOiIiLCJyZWRpcmVjdFVyaSI6Imh0dHBzOi8vY2ouc2h1LmVkdS5jbi9wYXNzcG9ydC9yZXR1cm4iLCJzdGF0ZSI6IiJ9',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    }

    data = {
      'username': username,
      'password': password
    }
    response = requests.post('https://oauth.shu.edu.cn/login/eyJ0aW1lc3RhbXAiOjE2MTk1NzE4NjcyMDY0NTU2MDksInJlc3BvbnNlVHlwZSI6ImNvZGUiLCJjbGllbnRJZCI6IkJ3Vk5IVVZZMTdZVTBjMEJVTjRWY2FDNjBLMzRkT1g1Iiwic2NvcGUiOiIiLCJyZWRpcmVjdFVyaSI6Imh0dHBzOi8vY2ouc2h1LmVkdS5jbi9wYXNzcG9ydC9yZXR1cm4iLCJzdGF0ZSI6IiJ9', headers=headers,  data=data,cookies=cookies)
    for each in response.history:
        for k,v in each.cookies.items():
            if k == "ASP.NET_SessionId":
                return {
                    "name":k,
                    "value":v
                }

    return None


def get_cookies(username,password):
    """
    外部获取cookie的接口,传入的是直接的学号和密码
    都是没有加密的
    返回登录需要的cookie
    """
    pw = get_password_key(password)
    return login(username,pw)
   
if __name__ == '__main__':
    cookies = get_cookies('u','p')
    print(cookies)
    
    

