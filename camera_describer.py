import wx
import threading
import cv2
from gpt_api import encode_image, get_image_description

class CameraDescriber(wx.Panel):
    def __init__(self, parent):
        super(CameraDescriber, self).__init__(parent)
        self.InitUI()

    def InitUI(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        self.camera_list = wx.ComboBox(self, choices=self.GetCameras(), style=wx.CB_READONLY)
        vbox.Add(self.camera_list, proportion=0, flag=wx.EXPAND|wx.ALL, border=10)
        
        self.capture_btn = wx.Button(self, label="Resim Çek ve Betimle")
        self.capture_btn.Bind(wx.EVT_BUTTON, self.OnCapture)
        vbox.Add(self.capture_btn, proportion=0, flag=wx.EXPAND|wx.ALL, border=10)
        
        self.description_txt = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.TE_READONLY)
        vbox.Add(self.description_txt, proportion=1, flag=wx.EXPAND|wx.ALL, border=10)
        
        self.progress_gauge = wx.Gauge(self, range=100, style=wx.GA_HORIZONTAL)
        vbox.Add(self.progress_gauge, proportion=0, flag=wx.EXPAND|wx.ALL, border=10)
        
        self.SetSizer(vbox)
    
    def GetCameras(self):
        # Detect available cameras
        index = 0
        arr = []
        while True:
            cap = cv2.VideoCapture(index)
            if not cap.read()[0]:
                break
            else:
                arr.append(f"Kamera {index}")
            cap.release()
            index += 1
        return arr
    
    def OnCapture(self, event):
        camera_index = self.camera_list.GetSelection()
        
        if camera_index != wx.NOT_FOUND:
            self.progress_gauge.SetValue(0)
            self.description_txt.SetValue("Resim çekiliyor ve betimleme hazırlanıyor...")
            threading.Thread(target=self.CaptureAndDescribe, args=(camera_index,)).start()
        else:
            self.description_txt.SetValue("Lütfen bir kamera seçin.")
    
    def CaptureAndDescribe(self, camera_index):
        try:
            cap = cv2.VideoCapture(camera_index)
            ret, frame = cap.read()
            if not ret:
                wx.CallAfter(self.description_txt.SetValue, "Kamera görüntüsü alınamadı.")
                return
            cap.release()
            
            image_path = "temp.jpg"
            cv2.imwrite(image_path, frame)
            
            base64_image = encode_image(image_path)
            
            for i in range(1, 101):
                wx.CallAfter(self.progress_gauge.SetValue, i)
                wx.MilliSleep(50)
            
            description = get_image_description(base64_image)
            
            if "error" in description:
                wx.CallAfter(self.description_txt.SetValue, description["error"]["message"])
            elif "choices" in description and len(description["choices"]) > 0:
                wx.CallAfter(self.description_txt.SetValue, description["choices"][0]["message"]["content"])
            else:
                wx.CallAfter(self.description_txt.SetValue, "Betimleme yapılamadı.")
        except Exception as e:
            wx.CallAfter(self.description_txt.SetValue, f"Hata: {str(e)}")
