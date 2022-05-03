#!/bin/env python
# -*- coding: iso-8859-1 -*-
import wx
class MyDialog(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title)
        self.parent = parent
        self.Bind(wx.EVT_CLOSE, self.OnClose)
   
    def OnClose(self, event):
        self.parent.OnSupButton(event)       
       
class MyFrame(wx.Frame):
    def __init__(self, parent, ID, title):
        wx.Frame.__init__(self, parent, ID, title, size = (200,100))
       
        self.mybutton = wx.Button(self, wx.NewId(), "Initial" )
       
        self.Bind(wx.EVT_BUTTON, self.OnInitialButton, id = self.mybutton.GetId())
       
        self.dlg = None
       
        self.Show(True)
       
    def OnInitialButton(self, event):
        self.mybutton.SetLabel("\'Sup" )
        self.Bind(wx.EVT_BUTTON, self.OnSupButton, id = self.mybutton.GetId())
        self.dlg = MyDialog(self, -1, "Test Dialog" )
        self.dlg.Show(True)
       
    def OnSupButton(self, event):
        self.mybutton.SetLabel("Initial" )
        self.Bind(wx.EVT_BUTTON, self.OnInitialButton, id = self.mybutton.GetId())
        if self.dlg:
            self.dlg.Destroy()
   
app = wx.PySimpleApp()
frame = MyFrame(None, -1, "Test Frame" )
app.MainLoop()