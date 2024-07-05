import wx
from image_describer import ImageDescriber
from camera_describer import CameraDescriber
from settings import SettingsPanel

class MainFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MainFrame, self).__init__(*args, **kw)
        self.InitUI()
    
    def InitUI(self):
        notebook = wx.Notebook(self)

        # Image Describer Tab
        image_describer_panel = ImageDescriber(notebook)
        notebook.AddPage(image_describer_panel, "Resim Betimle")

        # Camera Describer Tab
        camera_describer_panel = CameraDescriber(notebook)
        notebook.AddPage(camera_describer_panel, "Kameradan Betimle")

        # Settings Tab
        settings_panel = SettingsPanel(notebook)
        notebook.AddPage(settings_panel, "Ayarlar")

        # Set up the main frame
        self.SetTitle('Vision Sense')
        self.Centre()
        self.SetSize((600, 500))
        
        # Set the notebook as the frame's sizer
        self.SetSizer(notebook.GetSizer())

if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame(None)
    frame.Show()
    app.MainLoop()
