#!/usr/bin/env python
# coding:utf-8
import hackhttp
hh = hackhttp.hackhttp()
raw = '''POST /post HTTP/1.1
Host: httpbin.org
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:45.0) Gecko/20100101 Firefox/45.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 19

key1=val1&key2=val2'''

code, head, html, redirect, log = hh.http('http://httpbin.org/post', raw=raw)

print log['request']
