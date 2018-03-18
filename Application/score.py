import requests
import bs4
import random
from passme import settings


class Score(object):

    url = 'http://jwxt1.hhu.edu.cn/'

    def __init__(self, jsessionid):
        self.jsessionid = jsessionid
        self.cookies = {
            'JSESSIONID': self.jsessionid
        }

    def get_image(self):
        img_url = self.url + 'validateCodeAction.do?random=' + str(random.random())
        cookies = requests.utils.cookiejar_from_dict(self.cookies, cookiejar=None, overwrite=True)
        img = requests.get(img_url, cookies=cookies)
        name = str(random.random())[2:] + '.jpg'
        real_dir = settings.STATIC_ROOT
        if img.status_code == 200:
            open(real_dir + '/Application/' + name, 'wb').write(img.content)
        return name

    def login(self, zjh, mm, v_yzm):
        data = {
            'zjh': zjh,
            'mm': mm,
            'v_yzm': v_yzm,
        }
        cookies = requests.utils.cookiejar_from_dict(self.cookies, cookiejar=None, overwrite=True)
        page = requests.post('http://jwxt1.hhu.edu.cn/loginAction.do', data=data, cookies=cookies)
        page = page.text
        return page.find('看不清，换一张') == -1

    def get_score_page(self):
        cookies = requests.utils.cookiejar_from_dict(self.cookies, cookiejar=None, overwrite=True)
        pg = requests.post('http://jwxt1.hhu.edu.cn/gradeLnAllAction.do?type=ln&oper=qbinfo', cookies=cookies)
        return pg.text

    @staticmethod
    def get_id():
        session = requests.Session()
        tmp = session.get('http://jwxt1.hhu.edu.cn/')
        return tmp.cookies['JSESSIONID']

    @staticmethod
    def phrase_page(score_page):
        soup = bs4.BeautifulSoup(score_page, 'html5lib')
        result = []
        for item in soup.find_all('table', class_='titleTop2'):
            name = Score.find_previous_name(item)
            one = {
                '学期': name,
                '课程': [],
            }
            for li in item.tbody.tbody.find_all('tr'):
                tmp = {}
                x = li.find_all('td')
                success = True
                try:
                    tmp['课程号'] = x[0].text.strip()
                    tmp['课序号'] = x[1].text.strip()
                    tmp['课程名'] = x[2].text.strip()
                    tmp['英文名'] = x[3].text.strip()
                    try:
                        tmp['学分'] = float(x[4].text.strip())
                    except ValueError:
                        tmp['学分'] = 0
                    tmp['课程属性'] = x[5].text.strip()
                    tmp['成绩'] = x[6].text.strip()
                except IndexError:
                    success = False

                if success:
                    one['课程'].append(tmp)
            result.append(one)
        return result

    @staticmethod
    def find_previous_name(item):
        for pre in item.previous_siblings:
            if pre.name == 'a':
                name = pre['name'].strip()
                return name

    @staticmethod
    def calculate_score(s_score):
        normal = True
        try:
            score = float(s_score)
        except ValueError:
            normal = False

        if normal:
            if score >= 90:
                ans = 5.0
            elif score >= 85:
                ans = 4.5
            elif score >= 80:
                ans = 4.0
            elif score >= 75:
                ans = 3.5
            elif score >= 70:
                ans = 3.0
            elif score >= 65:
                ans = 2.5
            elif score >= 60:
                ans = 2.0
            else:
                ans = 0.0
        else:
            if s_score == '优秀':
                ans = 5.0
            elif s_score == '良好':
                ans = 4.5
            elif s_score == '中等':
                ans = 3.5
            elif s_score == '合格' or s_score == '及格':
                ans = 3.0
            else:
                ans = 0.0
        return ans

    def get_result(self, score_object):
        result = {}
        for item in score_object:
            total = 0.0
            pts = 0.0
            for x in item['课程']:
                if x['课程属性'] == '必修':
                    total += x['学分']
                    pts += x['学分'] * Score.calculate_score(x['成绩'])
            item['结果'] = {
                '总学分': total,
                '总绩点': pts,
                '平均绩点': pts / total,
            }
        avg_page = self.get_avg_page()
        result['综合'] = Score.get_avg_score(avg_page)
        return result

    def solve(self):
        return self.get_result(self.phrase_page(self.get_score_page()))

    @staticmethod
    def get_avg_score(avg_page):
        data = Score.phrase_page(avg_page)
        item = data[0]
        total = 0.0
        pts = 0.0
        for x in item['课程']:
            if x['课程属性'] == '必修':
                total += x['学分']
                pts += x['学分'] * Score.calculate_score(x['成绩'])
        return {
            '总学分': total,
            '总绩点': pts,
            '平均绩点': pts / total,
        }

    def get_avg_page(self):
        cookies = requests.utils.cookiejar_from_dict(self.cookies, cookiejar=None, overwrite=True)
        pg = requests.post('http://jwxt1.hhu.edu.cn/gradeLnAllAction.do?type=ln&oper=fainfo', cookies=cookies)
        return pg.text


if __name__ == '__main__':
    idx = Score.get_id()
    print(idx)
    s = Score(idx)

    while True:
        s.get_image()
        code = input()
        ret = s.login('nidexuehao', 'nidemima', code)
        if ret:
            break

    page = s.get_score_page()
    # print(s.phrase_page(page))
    print(s.get_result(s.phrase_page(page)))
