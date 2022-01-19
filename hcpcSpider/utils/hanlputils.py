import requests

from hcpcSpider.settings import HANLP_TOKEN, HANLP_URL


def segment(text) -> list:
    params = {
        "token": HANLP_TOKEN,
        "text": text
    }
    res = requests.post(HANLP_URL + '/segment', params)
    if res.json()['code'] == 200:
        return res.json()['data']
    else:
        raise Exception('分词接口调用错误')


def get_keyword(text) -> list:
    params = {
        "token": HANLP_TOKEN,
        "text": text
    }
    res = requests.post(HANLP_URL + '/getKeyword', params)
    if res.json()['code'] == 200:
        return res.json()['data']
    else:
        raise Exception('分词接口调用错误')
