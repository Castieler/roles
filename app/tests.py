import datetime

from django.test import TestCase
startdate = '2018-12-15'
# Create your tests here.
a = startdate.split('-')
# print(a)
# print(datetime.datetime(int(a[0]),int(a[1]),int(a[2])))

aa = datetime.datetime.strptime(startdate, "%Y-%m-%d") +datetime.timedelta(days=1)
print(aa.date())

import datetime
today = datetime.date.today()
print(today)
tomorrow = today + datetime.timedelta(days=1)
print(tomorrow)
