#!/usr/bin/env python
# coding:utf-8
from thread_pool import ThreadPool
import hackhttp
import re
import os

hh = hackhttp.hackhttp(hackhttp.httpconpool(500))
tp = ThreadPool(500)
package = "wooyun"

if not os.path.exists(package):
    os.mkdir(package)


def vlun(wid):
    print "[+]%s" % wid
    if os.path.isfile(wid + ".html"):
        return
    _, _, html, _, _ = hh.http(
        url="http://wooyun.org/bugs/%s" % wid, cookcookie=False)
    open(package + "/" + wid + '.html', 'wb').write(html)


def catalog(page):
    _, _, html, _, _ = hh.http(
        url="http://wooyun.org/bugs/new_public/page/%d" % page,
        cookcookie=False)
    for wid in re.findall(r'href="/bugs/(wooyun-\d+-\d+)">', html):
        tp.add_task(vlun, wid)
    if page > 0:
        tp.add_task(catalog, page - 1)

tp.add_task(catalog, 1925)
