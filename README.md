<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [空闲教室本地化查询](#%E7%A9%BA%E9%97%B2%E6%95%99%E5%AE%A4%E6%9C%AC%E5%9C%B0%E5%8C%96%E6%9F%A5%E8%AF%A2)
  - [目录结构](#%E7%9B%AE%E5%BD%95%E7%BB%93%E6%9E%84)
  - [使用](#%E4%BD%BF%E7%94%A8)
  - [说明](#%E8%AF%B4%E6%98%8E)
  - [最后](#%E6%9C%80%E5%90%8E)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# 空闲教室本地化查询

![avatar](https://img.shields.io/badge/license-MIT-blue)

找空教室一碰一个在上课, 登录教务处还需要校园网,真是醉死了. 直接爬在本地然后结合ios的快捷指令在手机上方便地查询.

## 目录结构

```bash
.
├── 1
│   └── g.json          周一的楼层数据
├── 2
│   └── g.json          周二的楼层数据
├── 3
│   └── g.json
├── 4
│   └── g.json
├── 5
│   └── g.json
│
├── login
│   └── login_api.py    登录的接口
│
├── server
│   ├── main.py         放在服务器上的代码
│   └── server.py       放在服务器上的代码
│
├── main.py             本地爬取数据的代码
├── LICENSE
├── README.md
└── upload_data.py      将本地数据存入服务器上的redis库中
```

## 使用

![image](https://github.com/crazyhubox/RoomUse/blob/main/static/ru.gif)

## 说明

**注意**:要使用一定要修改一些类似于路径和和账户名密码, 数据库的连接信息需自己修改.login_api.py登录的接口文件中的获取密码加密数据的server端如何写,请参照[crazyhubox/Shu_pwKey](https://github.com/crazyhubox/Shu_pwKey)

如果需要运行, 请依照以下流程逐步调试, 其余查看注释

```bash
main.py 爬取数据, 本学期的数据已上传1-5的文件夹

配置upload.py 上传数据到服务器, 用以随时查询

将server文件夹拷贝到服务器

根据需要自行选择如何使用server中的文件
```

## 最后

项目仅仅作为同学们参考和讨论交流, 并不属于拿来即用类型的项目,如果需要实际使用还需要根据自身情况进行修改.
