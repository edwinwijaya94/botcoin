import threading
from botcoin import cron

if __name__ == '__main__':
    thr = threading.Thread(target=cron.init_cron, args=())
    thr.start()
    thr.join()
