import time
import threading
# 使用 threading 模块创建线程
import queue
# 优先级队列模块
# 线程优先级队列(Queue)
import datetime
import requests
import os
import urllib3
# Python的urllib3软件包的证书认证及警告的禁用
urllib3.disable_warnings()

# m3u8是本地的文件路径
m3u8_path = "E:\\PySpider\\playlist.m3u8"
# request请求头，若无可能被禁止访问
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.20 Safari/537.36"}

exitFlag = 0


# 从m3u8文件中取出并生成ts文件的下载链接
def get_ts_urls(m3u8_path, base_url):
    urls = []
    with open(m3u8_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            if line.endswith(".ts\n"):
                urls.append(base_url + line.strip("\n"))
    return urls


# 取出下载链接并下载
def download(ts_urls, download_path, i):
    ts_path = download_path + "\\{0}.ts".format(i)
    ts_url = ts_urls
    file_name = ts_url.split("/")[-1]

    try:
        print("ts_url", ts_url)
        print("开始下载 %s" % file_name)
        time.sleep(1)  # 防止爬虫间隔时间过短被禁止请求
        start = datetime.datetime.now().replace(microsecond=0)
        try:
            response = requests.get(headers=header, url=ts_url, stream=True, verify=False)
        except Exception as e:
            print("异常请求：%s" % e.args)
            return

        with open(ts_path, "wb+") as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        print("下载完成 %s  " % ts_path)
        end = datetime.datetime.now().replace(microsecond=0)
        print("耗时：%s" % (end - start))
    except:
        print("{} 已经存在，开始下载下一个ts".format(file_name))


# 将已经下载的ts文件的路径进行排序
def file_walker(path):
    file_list = []
    for root, dirs, files in os.walk(path):  # 生成器
        for fn in files:
            p = str(root + '/' + fn)
            file_list.append(p)
    file_list.sort(key=lambda x: int(x[20:-3]))
    print(file_list)
    return file_list


# 将所有下载好的ts文件组合成一个文件
# ts_path: 下载好的一堆ts文件的文件夹
# combine_path: 组合好的文件的存放位置
# file_name: 组合好的视频文件的文件名
def combine(ts_path, combine_path, file_name):
    file_list = file_walker(ts_path)
    file_path = combine_path + file_name + '.ts'
    with open(file_path, 'wb+') as fw:
        for i in range(len(file_list)):
            fw.write(open(file_list[i], 'rb').read())



class myThread (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q

    def run(self):
        print ("开启线程：" + self.name)
        process_data(self.threadID, self.name, self.q)
        print ("退出线程：" + self.name)


def process_data(id, threadName, q):
    while not exitFlag:
        id += 1
        t_s+1
        if id >= 6:
            download(q.get(), "E:\\PySpider\\tsfiles", t_s)
            print("%s processing %s" % (threadName, q.get()))
        time.sleep(1)


threadList = ["Thread-1", "Thread-2", "Thread-3", "Thread-4", "Thread-5"]
nameList = get_ts_urls(m3u8_path=m3u8_path, base_url="https://youku.letv-cdn.com/2019/08/07/VX60SrY8hItErZXA/")
workQueue = queue.Queue()
threads = []
threadID = 1
t_s = 0
# 填充队列
for word in nameList:
    workQueue.put(word)
# 创建新线程
for tName in threadList:
    thread = myThread(threadID, tName, workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1
# 等待队列清空
while not workQueue.empty():
    pass
# 通知线程是时候退出
exitFlag = 1
# 等待所有线程完成
for t in threads:
    t.join()
print("退出主线程")
combine("E://PySpider//tsfile", "E://PySpider//ts", "test")
