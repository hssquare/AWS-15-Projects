import requests
import threading

url = "http://MyNLB-b77738fdcd51439a.elb.ap-south-1.amazonaws.com"

def hit():
    while True:
        try:
            r = requests.get(url)
            print(r.status_code)
        except:
            print("Failed")

for i in range(50):   # 50 users
    t = threading.Thread(target=hit)
    t.start()