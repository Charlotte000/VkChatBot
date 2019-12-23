import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from time import time

import base64
import os

values = {
	'main_login': os.environ.get('login'),
	'main_password': os.environ.get('password')
}

headers = {
	'Referer': 'https://edu.tatar.ru/logon',
}

currentDay = str((datetime.now() + timedelta(days=1)).day)

homework = []
with requests.Session() as s:
	s.post('https://edu.tatar.ru/logon', data=values, headers=headers)
	r = s.get(f'https://edu.tatar.ru/user/diary/week?date={round(time() + 86400)}')

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

st = f'Домашняя работа на {currentDay}\n' + '\n\n'.join([f'{h[0]}: {h[1]}' for h in homework])

encodedBytes = base64.b64encode(st.encode("utf-8"))
encodedStr = str(encodedBytes, "utf-8")

print(encodedStr)


