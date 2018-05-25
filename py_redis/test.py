#coding: utf-8

from rq import Queue
from rq.job import Job
from worker import square_function, conn 
import time

q = Queue(connection=conn)

job = q.enqueue_call(square_function, args=(5, ), result_ttl=5000)   # 保存结果5000s
job_id = job.get_id()
print job_id

result1 = Job.fetch(job_id, connection=conn)
print result1.is_finished

time.sleep(1)  # 等待队列里任务完成

result2 = Job.fetch(job_id, connection=conn)
print result2.return_value



import requests
import time,sys

try:
    if sys.argv[1]:
        data = {'x': int(sys.argv[1])}
except:
    data = {'x': 2}
post_url = "http://localhost:5000"
post_result = requests.post(post_url, data=data)
job_id = post_result.content
print job_id

time.sleep(1)

get_url = "http://localhost:5000/result/{}".format(job_id)
get_result = requests.get(get_url)
print get_result.content