#!/usr/bin/env python
# coding:utf-8
import hackhttp

hh = hackhttp.hackhttp()
url = "http://httpbin.org/post"
post_str = "key1=val1&key2=val2"
# proxy_str = ('127.0.0.1', 9119)
headers_dict = {
    'X-Forwarder-For': 'https://q.bugscan.net',
    'Hack-Http': 'Header Dict Val'
}

code, head, html, redirect, log = hh.http(
    url, post=post_str, headers=headers_dict)

print log['request']
print "============="
print log['response']
