# -*- coding: utf-8 -*-

from workflow import Workflow3, web
import time
import sys
import datetime
import logging

reload(sys)
sys.setdefaultencoding('utf8')


def get_current_time():
    url = 'http://api.m.taobao.com/rest/api3.do?api=mtop.common.getTimestamp'
    new_rt = {}
    try:
        rt = web.get(url, timeout=2).json()
        wf.logger.debug('===>获取互联网时间rt:', rt)
        if rt is None or rt["data"] is None:
            new_rt = get_pc_current_time()
            logging.info('===>获取本地时间:new_rt', new_rt)
            return new_rt
        else:
            milSecFormat = rt["data"].get("t")
            if milSecFormat is None:
                new_rt = get_pc_current_time()
                return new_rt
            new_rt['milSecFormat'] = milSecFormat
            new_rt['secStampFormat'] = milSecFormat / 1000
            new_rt['normalFormat'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(milSecFormat / 1000))
            return new_rt
    except:
        return get_pc_current_time()


def get_pc_current_time():
    ISOTIMEFORMAT = '%Y-%m-%d %H:%M:%S'
    rt = {}
    current_time = datetime.datetime.now()
    normalFormat = current_time.strftime(ISOTIMEFORMAT)
    t = time.time()
    # 标准时间格式
    rt['normalFormat'] = normalFormat
    # 秒级时间戳
    rt['secStampFormat'] = int(t)
    # 毫秒级别时间戳
    rt['milSecFormat'] = int(round(t * 1000))
    return rt


def main(wf):
    query = wf.args[0].strip()
    if not isinstance(query, unicode):
        query = query.decode('utf8')
    # 获取当前时间
    if len(query) == 0 or query == "*":
        rt = get_current_time()
        for rtKey in rt:
            if rtKey == 'milSecFormat':
                wf.add_item(valid=True, title=rt[rtKey], subtitle="（毫秒）单击复制到剪贴板", arg=rt[rtKey])
            elif rtKey == 'secStampFormat':
                wf.add_item(valid=True, title=rt[rtKey], subtitle="（秒）单击复制到剪贴板", arg=rt[rtKey])
            else:
                wf.add_item(valid=True, title=rt[rtKey], subtitle="（标准格式）单击复制到剪贴板", arg=rt[rtKey])
    else:
        # 时间戳格式
        if query.find("-") == -1:
            # 时间戳长度判断
            if 10 <= len(query) <= 13:
                # 时间戳截取
                new_query = query[0:10]
                normalFormat = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(new_query)))
                wf.add_item(valid=True, title=normalFormat, subtitle="（标准格式）单击复制到剪贴板", arg=normalFormat)
            else:
                wf.add_item(valid=False, title="时间戳长度不合法", subtitle="时间戳长度不合法", arg="时间戳长度不合法")
        else:
            # 标准格式转换
            t = time.mktime(time.strptime(query, "%Y-%m-%d %H:%M:%S"))
            wf.add_item(valid=True, title=int(t), subtitle="（秒）单击复制到剪贴板", arg=int(t))
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))
