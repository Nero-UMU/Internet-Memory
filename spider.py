import requests
import time
import os
from datetime import datetime, timedelta, timezone

def fetch_tieba_topic():
    os.makedirs("tieba", exist_ok=True)
    url = 'https://tieba.baidu.com/hottopic/browse/topicList'

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Host': 'tieba.baidu.com',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
    }

    for i in range(3):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            res = response.json()
            beijing_tz = timezone(timedelta(hours=8))
            now = datetime.now(beijing_tz)
            filename = now.strftime('%Y-%m-%d_%H.%M')
            markdown_name = f'tieba/{filename}.md'

            markdown = ''
            topic_list = res['data']['bang_topic']['topic_list']
            for i, topic in enumerate(topic_list):
                topic_name = topic['topic_name']
                abstract = topic['abstract']
                discuss_num = topic['discuss_num']
                create_time = topic['create_time']
                topic_time = datetime.fromtimestamp(create_time, beijing_tz).strftime('%Y-%m-%d %H:%M')
                markdown += f'# {i + 1}.{topic_name}  \n{abstract}  \n讨论数：{discuss_num}  \n话题创建时间：{topic_time}\n\n'

            with open(markdown_name, 'w', encoding='utf-8') as f:
                f.write(markdown)
            break
        else:
            time.sleep(5)
            continue

fetch_tieba_topic()
