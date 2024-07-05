import wx
import os

class SettingsPanel(wx.Panel):
    def __init__(self, parent):
        super(SettingsPanel, self).__init__(parent)
        self.InitUI()

    def InitUI(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        self.api_key_label = wx.StaticText(self, label="API Key:")
        vbox.Add(self.api_key_label, flag=wx.EXPAND|wx.ALL, border=10)
        
        self.api_key_text = wx.TextCtrl(self)
        vbox.Add(self.api_key_text, flag=wx.EXPAND|wx.ALL, border=10)
        
        self.save_btn = wx.Button(self, label="Kaydet")
        self.save_btn.Bind(wx.EVT_BUTTON, self.OnSave)
        vbox.Add(self.save_btn, flag=wx.EXPAND|wx.ALL, border=10)
        
        self.SetSizer(vbox)
        
        self.LoadAPIKey()

    def LoadAPIKey(self):
        if os.path.exists(".env"):
            with open(".env", "r") as f:
                for line in f:
                    if line.startswith("API_KEY="):
                        self.api_key_text.SetValue(line.strip().split("=")[1])

    def OnSave(self, event):
        api_key = self.api_key_text.GetValue()
        with open(".env", "w") as f:
            f.write(f"API_KEY={api_key}")
