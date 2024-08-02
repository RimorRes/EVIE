import time
from picamera2 import Picamera2, Preview


picam1 = Picamera2(0)
picam2 = Picamera2(1)
config1 = picam1.create_preview_configuration({"size": (2304, 1296)})
config2 = picam2.create_preview_configuration({"size": (2304, 1296)})
picam1.align_configuration(config1)
picam2.align_configuration(config2)
print(config1["main"])
picam1.configure(config1)
picam2.configure(config2)
picam1.start_preview(Preview.QTGL, x=0, y=250, width=1280, height=1440)
picam2.start_preview(Preview.QTGL, x=1280, y=250, width=1280, height=1440)
picam1.start()
picam2.start()
time.sleep(100)
picam1.close()
time.sleep(1)
picam2.close()
