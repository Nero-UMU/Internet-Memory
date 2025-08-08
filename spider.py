import requests
import time
import os

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
            markdown_name = 'tieba/{}.md'.format(time.strftime('%Y-%m-%d_%H.%M', time.localtime()))
            markdown = ''
            topic_list = res['data']['bang_topic']['topic_list']
            for i, topic in enumerate(topic_list):
                topic_name = topic['topic_name']
                abstract = topic['abstract']
                discuss_num = topic['discuss_num']
                create_time = topic['create_time']
                markdown += '# {}.{}  \n{}  \n讨论数：{}  \n话题创建时间：{}\n\n'.format(i + 1, topic_name, abstract, discuss_num, time.strftime('%Y-%m-%d %H:%M', time.localtime(create_time)))
            with open(markdown_name, 'w', encoding='utf-8') as f:
                f.write(markdown)
            break
        else:
            time.sleep(5)
            continue
fetch_tieba_topic()