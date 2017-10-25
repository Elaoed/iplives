# iplive(server) Deploy 
-
<br>
### Introduction
-
Iplive is a **multiple node** detect target ip distribute sysetm.<br>
Using multiple node to get the real state of target ip<br>
Our project running on python3.6.2 and higher version



### Usage
1. make sure time of your server and nodes is correct(use ntpdate time.apple.com to sync time with apple)


### Feature
1. For superuser. when a new node is add, it will dynamiclly synchronize their data in	to new node. 


### Deploy
---
> git clone http://git.newdun.com/renxiaopeng/iplives<br>
> cd iplives <br>
> python3 -m venv venv <br>
> source venv/bin/activate <br>
> pip3 install -r requirements/requirements <br>
> mv scripts/iplives.ini /path/to/supervisor/config/dir<br>
> 
