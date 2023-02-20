from testmock import a
# print(a)
import time
from pymemcache.client import base

client = base.Client(('localhost', 11211))
print(client)
client.set('France','paris')
# s = client.get('France')
print(client.get('France'))
time.sleep(1)