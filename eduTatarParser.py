import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from time import time

import base64
import sys

values = {
	'main_login': sys.argv[1],
	'main_password': sys.argv[2]
}

headers = {
	'Referer': 'https://edu.tatar.ru/logon',
}

currentDay = str((datetime.now() + timedelta(days=1)).day)

homework = []
with requests.Session() as s:
	s.post('https://edu.tatar.ru/logon', data=values, headers=headers)
	r = s.get('https://edu.tatar.ru/user/diary/week?date={}'.format(str(round(time() + 86400))))
	
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

st = 'Домашняя работа на {}\n'.format(currentDay)
st += '\n\n'.join(['{}: {}'.format(h[0], h[1]) for h in homework])

encodedBytes = base64.b64encode(st.encode("utf-8"))
encodedStr = str(encodedBytes, "utf-8")
print(encodedStr)



