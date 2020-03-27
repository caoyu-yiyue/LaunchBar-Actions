#!/usr/bin/env python
#
# LaunchBar Action Script
#
import sys
import os
import re
import subprocess as sp
from validator_collection import checkers
import glob
# import logging

os.environ['PATH'] += os.pathsep + '/usr/local/bin/'

# Note: The first argument is the script's path
input_args = sys.argv[1:]
DOWNLOAD_PATH = os.path.expanduser('~/Downloads')

DOWNLOAD_COMMAND = ['you-get', 'url', '--no-caption', '-o', DOWNLOAD_PATH]
DOWNLOAD_ITEMS = []
FAILED_ITEMS = []


def download_video(url):
    DOWNLOAD_COMMAND[1] = url
    abv_num_match = re.search(r'(a|b)v[0-9a-zA-Z]+', url, re.IGNORECASE)
    try:
        sp.run(DOWNLOAD_COMMAND, check=True)
        if abv_num_match:
            abv_num = abv_num_match.group(0)
            # 对刚下载的视频名前加上av/bv 号
            file_in_download = glob.glob(DOWNLOAD_PATH + '/*')
            last_video = max(file_in_download, key=os.path.getctime)
            video_title = os.path.basename(last_video)
            os.rename(last_video,
                      DOWNLOAD_PATH + '/{} '.format(abv_num) + video_title)
            # 将av/bv 号加入到下载过的项目里
            DOWNLOAD_ITEMS.append(abv_num)
        else:
            DOWNLOAD_ITEMS.append(url)
    except sp.CalledProcessError:
        # 如果you-get CLI 出现错误则增加识别到FAILED_ITEMS 中
        FAILED_ITEMS.append(abv_num_match.group(0) if abv_num_match else url)


for one_arg in input_args:
    if checkers.is_url(one_arg):
        download_video(one_arg)
    else:
        # 在每个参数中寻找av/bv 值，如果是av 号则将其全部小写
        abvs = set(
            re.findall(r'(?:a|b)v[0-9a-zA-Z]+',
                       string=one_arg,
                       flags=re.IGNORECASE))
        abvs_list = [
            abv.lower() if abv.startswith(('a', 'A')) else abv for abv in abvs
        ]
        for abv in abvs_list:
            download_video(url='https://www.bilibili.com/video/' + abv)

downloaded_items_str = '\n'.join(DOWNLOAD_ITEMS)
notifi_content = '成功下载了 {} 个视频：\n{}'.format(len(DOWNLOAD_ITEMS),
                                            downloaded_items_str)
if len(FAILED_ITEMS) > 0:
    notifi_content += '\n{}个视频下载失败：\n{}'.format(len(FAILED_ITEMS),
                                                '\n'.join(FAILED_ITEMS))

os.system("""
    osascript -e 'display notification "{}" with title "Dowanload Complete!"'
    """.format(notifi_content))
