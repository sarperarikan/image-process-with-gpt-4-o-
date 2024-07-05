import wx
import threading
from gpt_api import encode_image, get_image_description

class ImageDescriber(wx.Panel):
    def __init__(self, parent):
        super(ImageDescriber, self).__init__(parent)
        self.InitUI()

    def InitUI(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        self.file_picker = wx.FilePickerCtrl(self, message="Bir resim dosyası seçin", wildcard="JPEG files (*.jpg;*.jpeg)|*.jpg;*.jpeg")
        vbox.Add(self.file_picker, proportion=0, flag=wx.EXPAND|wx.ALL, border=10)
        
        self.describe_btn = wx.Button(self, label="Görseli Betimle")
        self.describe_btn.Bind(wx.EVT_BUTTON, self.OnDescribe)
        vbox.Add(self.describe_btn, proportion=0, flag=wx.EXPAND|wx.ALL, border=10)
        
        self.description_txt = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.TE_READONLY)
        vbox.Add(self.description_txt, proportion=1, flag=wx.EXPAND|wx.ALL, border=10)
        
        self.progress_gauge = wx.Gauge(self, range=100, style=wx.GA_HORIZONTAL)
        vbox.Add(self.progress_gauge, proportion=0, flag=wx.EXPAND|wx.ALL, border=10)
        
        self.SetSizer(vbox)
    
    def OnDescribe(self, event):
        image_path = self.file_picker.GetPath()
        
        if image_path:
            self.progress_gauge.SetValue(0)
            self.description_txt.SetValue("Betimleme hazırlanıyor...")
            threading.Thread(target=self.DescribeImage, args=(image_path,)).start()
        else:
            self.description_txt.SetValue("Lütfen bir resim dosyası seçin.")
    
    def DescribeImage(self, image_path):
        try:
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
