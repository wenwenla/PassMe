import re
import requests
import json


class Pu(object):

    headers = {
        'Accept': '* / *',
        'Accept-Encoding': 'br,gzip,deflate',
        'Accept-Language': 'zh-Hans-CN;q = 1',
        'User-Agent': 'client:iOS version:6.4.7 Product:iPad OsVersion:11.3',
    }

    def __init__(self, info=None):
        self.info = info
        self.result = {'apply': [], 'event': []}
        requests.packages.urllib3.disable_warnings()

    def login(self, email, password):
        url = 'https://pocketuni.net/?app=api&mod=Sitelist&act=login'
        data = {
            'client': 2,
            'email': email,
            'password': password,
        }
        cnt = 0
        flag = False
        while cnt < 5 and not flag:
            try:
                ret = requests.post(url, data, headers=Pu.headers, verify=False, timeout=3)
                self.info = json.loads(ret.text)
                flag = True
            except requests.exceptions.Timeout:
                cnt += 1
        return cnt < 5 and self.info.get('status') != 0

    def is_login(self):
        return self.info is not None and self.info.get('userToken') is not None

    def get_event(self):
        url = 'https://pocketuni.net/index.php?app=api&mod=UserCredit&act=eventLists&' \
              'oauth_token={token}&' \
              'oauth_token_secret={secret}&' \
              'version=6.4.0'

        if not self.is_login():
            print('not login')
            return None

        event_id = set()

        session = requests.Session()
        session.headers = Pu.headers

        token = self.info['userToken']['oauth_token']
        secret = self.info['userToken']['oauth_token_secret']

        for pageIdx in range(1, 20):
            flag = False
            cnt = 0
            page = None
            while cnt < 5 and not flag:
                try:
                    page = session.post(url.format(token=token,
                                                   secret=secret),
                                        data={'page': pageIdx}, verify=False, timeout=3)
                    flag = True
                except requests.exceptions.Timeout:
                    cnt += 1

            if not page:
                return
            data = json.loads(page.text)
            if not data['content']['eventList']:
                break
            for e_id in data['content']['eventList']:
                event_id.add(e_id['id'])

        for e_id in event_id:
            cnt = 0
            flag = False
            page = None
            e_url = 'https://pocketuni.net/index.php?app=api&mod=UserCredit&act=eventDetail&' \
                    'oauth_token={token}&' \
                    'oauth_token_secret={secret}&' \
                    'version=6.4.0'.format(token=token,
                                           secret=secret)
            while cnt < 5 and not flag:
                try:
                    page = session.post(e_url, data={'id': e_id}, verify=False, timeout=3).text
                    flag = True
                except requests.exceptions.Timeout:
                    cnt += 1
                    print('time_out')

            if not page:
                return

            data = json.loads(page)
            if data['content'].get('event'):
                data = data['content']
                regex = re.compile(r'\d+\.?\d*')
                try:
                    credit = data['event']['userCredit']
                    credit = regex.findall(credit)[0]
                except KeyError:
                    credit = 0
                self.result['event'].append({
                    'category': data['event']['category'],
                    'credits': float(credit),
                    'title': data['event']['title'],
                })

    def get_apply(self):
        url = 'https://pocketuni.net/index.php?app=api&mod=UserCredit&act=applyLists&' \
              'oauth_token={token}&' \
              'oauth_token_secret={secret}&' \
              'version=6.4.0'

        if not self.is_login():
            print('not login')
            return None

        apply_id = set()

        session = requests.Session()
        session.headers = Pu.headers

        token = self.info['userToken']['oauth_token']
        secret = self.info['userToken']['oauth_token_secret']

        for pageIdx in range(1, 20):
            page = None
            flag = False
            cnt = 0
            while cnt < 5 and not flag:
                try:
                    page = session.post(url.format(token=token,
                                                   secret=secret),
                                        data={'page': pageIdx}, verify=False, timeout=3)
                    flag = True
                except requests.exceptions.Timeout:
                    cnt += 1
            data = json.loads(page.text)
            if not data['content']['applyList']:
                break
            for a_id in data['content']['applyList']:
                apply_id.add(a_id['id'])

        for a_id in apply_id:
            a_url = 'https://pocketuni.net/index.php?app=api&mod=UserCredit&act=applyDetail&' \
                    'oauth_token={token}&' \
                    'oauth_token_secret={secret}&' \
                    'version=6.4.0'.format(token=token,
                                           secret=secret)
            flag = False
            cnt = 0
            page = None
            while cnt < 5 and not flag:
                try:
                    page = session.post(a_url, data={'id': a_id}, verify=False, timeout=3).text
                    flag = True
                except requests.exceptions.Timeout:
                    cnt += 1
                    print('time_out')

            if not page:
                return

            data = json.loads(page)
            if data['content'].get('apply'):
                data = data['content']
                regex = re.compile(r'\d+\.?\d*')
                try:
                    credit = data['apply']['userCredit']
                    credit = regex.findall(credit)[0]
                except KeyError:
                    credit = 0
                self.result['apply'].append({
                    'category': data['apply']['category'],
                    'credits': float(credit),
                    'title': data['apply']['title'],
                })

    def run(self):
        self.get_apply()
        self.get_event()
        return self.result


class DataAnalysis(object):

    def __init__(self, info):
        self.info = info
        self.result = {}

    def run(self):
        total = 0.0
        self.result['zhi_yuan'] = {}
        self.result['zhi_yuan']['detail'] = []
        for item in self.info['event']:
            if item['category'] == '志愿服务':
                total += item['credits']
                self.result['zhi_yuan']['detail'].append({
                    'category': item['category'],
                    'credits': item['credits'],
                    'title': item['title'],
                })
        self.result['zhi_yuan']['total'] = total

        total = 0.0
        self.result['huo_dong'] = {}
        self.result['huo_dong']['detail'] = []

        for item in self.info['event']:
            if item['category'] != '志愿服务':
                total += item['credits']
                self.result['huo_dong']['detail'].append({
                    'category': item['category'],
                    'credits': item['credits'],
                    'title': item['title'],
                })
        self.result['huo_dong']['total'] = total

        total = 0.0
        self.result['jia_qi'] = {}
        self.result['jia_qi']['detail'] = []
        for item in self.info['apply']:
            if item['category'] == '寒暑期社会实践':
                total += item['credits']
                self.result['jia_qi']['detail'].append({
                    'category': item['category'],
                    'credits': item['credits'],
                    'title': item['title'],
                })
        self.result['jia_qi']['total'] = total

        total = 0.0
        self.result['jin_sai'] = {}
        self.result['jin_sai']['detail'] = []
        for item in self.info['apply']:
            if item['category'] == '学科竞赛':
                total += item['credits']
                self.result['jin_sai']['detail'].append({
                    'category': item['category'],
                    'credits': item['credits'],
                    'title': item['title'],
                })
        self.result['jin_sai']['total'] = total

        total = 0.0
        self.result['qi_ta'] = {}
        self.result['qi_ta']['detail'] = []
        for item in self.info['apply']:
            if item['category'] != '学科竞赛' and item['category'] != '寒暑期社会实践':
                total += item['credits']
                self.result['qi_ta']['detail'].append({
                    'category': item['category'],
                    'credits': item['credits'],
                    'title': item['title'],
                })
        self.result['qi_ta']['total'] = total
        return self.result


if __name__ == '__main__':
    test = Pu()

    result = test.login('账号@hhu.com', '密码')
    print(result)
    print(test.info)
    if result:
        test.run()

    print(test.result)
    print(DataAnalysis(test.result).run())
