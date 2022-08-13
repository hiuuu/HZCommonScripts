# creation date : 25 May, 2022
#
# Author :    Hamed Zandieh
# Contact :   hamed.zandieh@gmail.com
#
# Description :
#    This script sets batch keyframes for multiple objects. Frame numbers can be pasted or type with space, comma or ... delimiter.
# How To use :
#    copy python file into maya script folder then run these lines:
# import HZBatchKeyframer
# HZBatchKeyframer.showUI()
# 

import maya.cmds as mc
from random import choice
import re
import ctypes

kernel32 = ctypes.windll.kernel32
kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
kernel32.GlobalLock.restype = ctypes.c_void_p
kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]
user32 = ctypes.windll.user32
user32.GetClipboardData.restype = ctypes.c_void_p

def get_clipboard_text():
    user32.OpenClipboard(0)
    try:
        if user32.IsClipboardFormatAvailable(1):
            data = user32.GetClipboardData(1)
            #user32.SetClipboardText(c) or user32.EmptyClipboard()
            data_locked = kernel32.GlobalLock(data)
            text = ctypes.c_char_p(data_locked)
            value = text.value
            kernel32.GlobalUnlock(data_locked)
            return value
    finally:
        user32.CloseClipboard()

def setKframes(*args):
    mc.currentUnit(time='pal')
    cam = mc.textScrollList("objsName", q=1, allItems=True)
    if not cam: 
        mc.warning("select objects")
        return
    excelcopypaste = mc.scrollField( "excelPaste",q=1, text=1)
    frms = [int(f) for f in re.findall("\d+", excelcopypaste)].sort()
    if not frms:
        mc.warning("no frame number found!")
        return
    for f in frms:
        mc.setKeyframe(t=(f,), shape=0, ott='linear', itt='linear',*cam)
    mc.playbackOptions(animationStartTime=min(frms))
    mc.playbackOptions(animationEndTime=max(frms))
    mc.playbackOptions(minTime=min(frms))
    mc.playbackOptions(maxTime=max(frms))
    mc.currentTime(frms[0]) 
    mc.select(cam, r=1)

def hzasgFrms(*args):
    mc.scrollField("excelPaste", e=1, cl=True)
    mc.scrollField("excelPaste", e=1, text=get_clipboard_text())

def hzasgNodes(*args):
    sl=mc.ls(sl=1, ni=True, o=True, r=True)
    mc.textScrollList("objsName", e=1, removeAll=True)
    if sl: mc.textScrollList("objsName", e=1, append=sl)

def hznodesDelItem( *args):
    selsCount = mc.textScrollList("objsName", q=1, numberOfSelectedItems=True)
    if selsCount > 0:
        sels = mc.textScrollList("objsName", q=1, selectIndexedItem=True)
        mc.textScrollList("objsName", e=1, deselectAll=True)
        mc.textScrollList("objsName", e=1, removeIndexedItem=sels)    
    
def showUI():    
    mc.window(title="Batch Keyframes", mxb=0, sizeable=0)
    mc.columnLayout(adjustableColumn=True, rowSpacing=5, columnOffset=['both',5])
    mc.text(l='H.Z. Batch Set Keyframes v1.0\n\n1.Choose Objects \n2.Paste or type frame numbers \n3.Hit the set button.' , 
            align='left', font='boldLabelFont')
    mc.separator(20)
    mc.textScrollList("objsName", h=50)
    mc.button(l="^^^ Add Selected Objects ^^^", h=20, c=hzasgNodes)
    mc.separator(20)
    mc.scrollField( "excelPaste", h=100, editable=True, wordWrap=False )
    mc.button(l="^^^ Paste Frame Numbers ^^^", h=20, c=hzasgFrms)
    mc.separator(20)
    mc.button(l="SET Keyframes", h=50, c=setKframes)
    mc.separator()
    mc.text(label="(C) hamed.zandieh@gmail.com", align='right', font='tinyBoldLabelFont')
    mc.showWindow()

if __name__ != "__main__":
    pass