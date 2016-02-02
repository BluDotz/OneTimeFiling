import os
import wx
import json
 
try:
    import qrcode
except ImportError:
    qrcode = None
 
 
########################################################################
class QRPanel(wx.Panel):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        self.photo_max_size = 240
        sp = wx.StandardPaths.Get()
        self.defaultLocation = sp.GetDocumentsDir()
 
        img = wx.EmptyImage(240,240)
        self.imageCtrl = wx.StaticBitmap(self, wx.ID_ANY,
                                         wx.BitmapFromImage(img))
 
        qrServerLbl = wx.StaticText(self, label="Server:")
        self.qrServerTxt = wx.TextCtrl(self, value="", size=(200,-1))
        qrUserLbl = wx.StaticText(self, label="User:")
        self.qrUserTxt = wx.TextCtrl(self, value="", size=(200,-1))
        qrPasswordLbl = wx.StaticText(self, label="Password:")
        self.qrPasswordTxt = wx.TextCtrl(self, value="", style=wx.TE_PASSWORD, size=(200,-1))
 
        qrcodeBtn = wx.Button(self, label="Create QR")
        qrcodeBtn.Bind(wx.EVT_BUTTON, self.onUseQrcode)
 
 
        # Create sizer
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        parameterSizer = wx.GridSizer(rows=3, cols=2)
        parameterSizer.Add(qrServerLbl)
        parameterSizer.Add(self.qrServerTxt)
        parameterSizer.Add(qrUserLbl)
        parameterSizer.Add(self.qrUserTxt)
        parameterSizer.Add(qrPasswordLbl)
        parameterSizer.Add(self.qrPasswordTxt)
        
#         qrDataSizer = wx.BoxSizer(wx.HORIZONTAL)
#         locationSizer = wx.BoxSizer(wx.HORIZONTAL)
        qrBtnSizer = wx.BoxSizer(wx.VERTICAL)
 
#         qrDataSizer.Add(qrDataLbl, 0, wx.ALL, 5)
#         qrDataSizer.Add(self.qrDataTxt, 1, wx.ALL|wx.EXPAND, 5)
#         self.mainSizer.Add(wx.StaticLine(self, wx.ID_ANY),
#                            0, wx.ALL|wx.EXPAND, 5)
#         self.mainSizer.Add(qrDataSizer, 0, wx.EXPAND)
        self.mainSizer.Add(parameterSizer, 0, wx.EXPAND)
        self.mainSizer.Add(self.imageCtrl, 0, wx.ALL, 5)
#         locationSizer.Add(instructLbl, 0, wx.ALL, 5)
#         locationSizer.Add(self.qrPhotoTxt, 0, wx.ALL, 5)
#         locationSizer.Add(browseBtn, 0, wx.ALL, 5)
#         self.mainSizer.Add(locationSizer, 0, wx.ALL, 5)
#         self.mainSizer.Add(self.defaultLocationLbl, 0, wx.ALL, 5)
 
        qrBtnSizer.Add(qrcodeBtn, 0, wx.ALL, 5)
        self.mainSizer.Add(qrBtnSizer, 0, wx.ALL|wx.CENTER, 10)
 
        self.SetSizer(self.mainSizer)
        self.Layout()
 
 
    #----------------------------------------------------------------------
    def onUseQrcode(self, event):
        """
        https://github.com/lincolnloop/python-qrcode
        """
        parameters = {}
        parameters['server'] = self.qrServerTxt.GetValue()
        parameters['user'] = self.qrUserTxt.GetValue()
        parameters['password'] = self.qrPasswordTxt.GetValue()

        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(json.dumps(parameters))
        qr.make(fit=True)
        im = qr.make_image()
 
        qr_file = os.path.join(".", "qr.jpg")
        img_file = open(qr_file, 'wb')
        im.save(img_file, 'JPEG')
        img_file.close()
        self.showQRCode(qr_file)
 
 
    #----------------------------------------------------------------------
    def showQRCode(self, filepath):
        """"""
        img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
        # scale the image, preserving the aspect ratio
        W = img.GetWidth()
        H = img.GetHeight()
        if W > H:
            NewW = self.photo_max_size
            NewH = self.photo_max_size * H / W
        else:
            NewH = self.photo_max_size
            NewW = self.photo_max_size * W / H
        img = img.Scale(NewW,NewH)
 
        self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
        self.Refresh()
 
 
########################################################################
class QRFrame(wx.Frame):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="QR Code Viewer", size=(550,500))
        panel = QRPanel(self)
 
if __name__ == "__main__":
    app = wx.App(False)
    frame = QRFrame()
    frame.Show()
    app.MainLoop()
