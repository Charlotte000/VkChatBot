import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from time import time
from random import choice
import base64
import sys


def getProxy():
	r = requests.get('https://www.proxy-list.download/api/v1/get?type=https&country=ru').text
	proxies = []
	for i in r.split('\n'):
		if i:
			proxies.append(f'https://{i[:-1]}')
	return choice(proxies)


def register(session):
	while True:
		try:
			r = session.post(
				'https://edu.tatar.ru/logon', 
				headers=headers, 
				data=data, 
				proxies={'https': getProxy()},
				timeout=20
			)
			if r.status_code == 200 and r.url == 'https://edu.tatar.ru/':
				break
		except:
			pass

def getInformation(session):
	while True:
		try:
			r = s.get('https://edu.tatar.ru/user/diary/week?date={}'.format(str(round(time() + 86400))))
			if r.status_code == 200:
				return r
		except:
			pass


headers = {
	'Referer': 'https://edu.tatar.ru/logon',
}

data = {
	'main_login': sys.argv[1],
	'main_password': sys.argv[2]
}

currentDay = str((datetime.now() + timedelta(days=1)).day)

homework = []
with requests.Session() as s:
	register(s)
	r = getInformation(s)
	
	soup = BeautifulSoup(r.text, 'html.parser')

	t = soup.find("table").findAll('tr')

	for index, d in enumerate(t):
		day = d.findChild().find('span')
		if day and day.text == currentDay:

			for i in range(0, 8):
				subj = t[index + i].find('td', {'class': 'tt-subj'}).text.strip()
				task = t[index + i].find('td', {'class': 'tt-task'}).text.strip()
				if subj:
					homework.append([subj, task])

st = 'Домашняя работа на {} число:\n\n'.format(currentDay)
st += '\n'.join(['{}: {}'.format(h[0], h[1]) for h in homework])

encodedBytes = base64.b64encode(st.encode("utf-8"))
encodedStr = str(encodedBytes, "utf-8")
print(encodedStr)
input()