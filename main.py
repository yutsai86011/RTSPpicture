import cv2
import os
import threading
import time
from threading import Lock
import configparser

import numpy as np
import datetime
# from dlicense import d_license
# from truck_d import d_truck
# from datetime import datetime
class Camera:
    def __init__(self, lane, rtsp_link):
        self.lane = lane
        self.rtsp_link = rtsp_link
       

        self.flag = True
        self.last_frame = None
        self.last_ready = None
        self.lock = Lock()

        capture = cv2.VideoCapture(self.rtsp_link)
        self.fps = capture.get(cv2.CAP_PROP_FPS) % 100
        thread = threading.Thread(target=self.rtsp_cam_buffer, args=(capture,), name="rtsp_read_thread")
        thread.daemon = True
        thread.start()

    def get_ready(self):
        return self.last_ready

    def rtsp_cam_buffer(self, capture):
        while self.flag:
            with self.lock:
                self.last_ready, self.last_frame = capture.read()

                if not self.last_ready:
                    self.flag = False
                    print(f"{self.rtsp_link} has a problem")
                    # ================= 因為連結不到............... 發信通知
                    

            # self.fps = 10
            time.sleep(1 / self.fps)
        # print(f"{self.rtsp_link} camera closed")

    def get_frame(self):
        if (self.last_ready is not None) and (self.last_frame is not None):
            return self.last_frame.copy()
        else:
            return None

class obj_x:
    def __init__(self, lane):

        config = configparser.ConfigParser()
        config.read('cctv.ini')
        self.savepath = "D:\car"
        self.lane = lane
       # 讀取各個區段的數值
        self.lane1_f_camera = config.get('lane1', 'f_camera')


        self.f_camera = Camera(1 , f"{self.lane1_f_camera}")
        # dt = 1
        # self.itruck = d_truck(dt,self.lane)  # 偵測車牌


class Girls(obj_x):
    def __init__(self, lane, img_id=0, work_id=" " , carin_time=0, stay_time=0 , platenum = 0, person_s = 0, head_s = 0, helmet_s = 0 ):
        super().__init__(lane)

        self.carin_time_a = None

        self.car_a = []
        self.car_b = []
        self.car_num = 0

        self.nocar_img = []
        self.carOne_img = []
        self.timelok = 0
        self.start_time = datetime.time(6, 0, 0)
        self.end_time = datetime.time(18, 0, 0)
        


        self.create_timer()
    def create_timer(self):
        t = threading.Timer(1, self.go)
        t.start()

    def go(self):
        if self.f_camera.get_frame() is not None:
            self.current_time = datetime.datetime.now().time()
            # print(self.current_time)
            if self.start_time <= self.current_time <= self.end_time:
                if self.timelok < 2 :
                    self.timelok += 1
                else:
                    self.timelok = 0
                    timeout = time.strftime('%Y%m%d%H%M%S', time.localtime())
                    cv2.imwrite(f"pic/{timeout}.jpg"  , self.f_camera.get_frame())
                # print(self.timelok)
                
            



            # if self.itruck.frame is None:
            #     self.itruck.frame = self.f_camera.get_frame()
         
            
            # print(f"{len(self.itruck.car_box)}  目前偵測到的車輛數")
            # # 只偵測到1台車狀況!!!
            # if len(self.itruck.car_box) ==1 :

            #     # 儲存影像
            #     self.carOne_img = self.f_camera.get_frame()
            #     now_date_time = datetime.now()

            #     # 檢查車子有沒有大衛魔術
            #     if self.carin_time_a is not None and len(self.car_a)!=0:
            #         x = int(self.car_a[0][0])
            #         x_b = int(self.itruck.car_box[0][0])
            #         check  = abs(x-x_b)
            #         print(f"{check}        CCCCCCCCCCCCCCCCCCCCCCCCCCCc")
            #         if check < 200:
            #             print("一樣的車")
            #         else:
            #             # 初始化
            #             self.carin_time_a = None
            #             self.car_a = []

            #     # 紀錄車子時間
            #     if self.carin_time_a is None:
            #         self.carin_time_a = now_date_time

            #     # 檢查是否真的有車跟儲存資料
            #     if self.carin_time_a is not None:
            #         time_diff = now_date_time - self.carin_time_a
            #         if time_diff.total_seconds() > 5 and len(self.car_a)==0:
            #             # 直接紀錄 >> 代表剛進入
            #             self.car_a  = self.itruck.car_box

            #             # 儲存影像
            #             timestr = time.strftime("%Y%m%d%H%M%S")
            #             cv2.imwrite(f'{timestr}_car_in_before.jpg', self.nocar_img )    
            #             cv2.imwrite(f'{timestr}_car_in_after.jpg', self.carOne_img )
                        
            
            # if len(self.itruck.car_box) == 0 :
            #     # 如果畫面都沒有車 暫時存影像  keep save
            #     self.nocar_img = self.f_camera.get_frame()

            #     if self.carin_time_a is not None:
            #         # 儲存影像
            #         timestr = time.strftime("%Y%m%d%H%M%S")
            #         cv2.imwrite(f'{timestr}_car_out_before.jpg', self.carOne_img )
            #         cv2.imwrite(f'{timestr}_car_out_after.jpg', self.carOne_img )

            #     #　車子進入時間　取消
            #     self.carin_time_a = None      

        self.create_timer()


if __name__ == '__main__':
    admin_l1 = Girls(1)