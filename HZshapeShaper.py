# creation date : 2 May, 2022
#
# Author :    Hamed Zandieh
# Contact :   hamed.zandieh@gmail.com
#
# Description :
#    This script modify the shape of rig controls
# How To use :
#    copy python file into maya script folder then run these lines:
# 
# import HZshapeShaper as hzss
# hzss.HZshapeShaper().showUI()
# 

from pymel import core as PM

def one_undo(func):
    def func_wrapper(*args, **kwargs):
        with PM.UndoChunk():
            return func(*args, **kwargs)
    return func_wrapper

class HZshapeShaper:

    __version__ = '1.0.0'

    def __init__(self, *args):
        pass

    @staticmethod
    def hex2rgb(hex = str):
        if not hex: return [0,0,0]
        hex = hex.upper().split("#")[-1]
        lh = len(hex)
        if lh==3:  hex = iter(''.join([str(x) * 2 for x in hex]))
        elif lh<3: 
            from itertools import cycle, islice
            hex = iter(''.join(list(islice(cycle(hex), 6))))
        else: hex = iter(hex.ljust(6,'F')[:6])
        return [float(int("%s%s"%(a,b),16))/255 for a,b in zip(hex,hex)]  

    def showUI(self, *args):
        WINDOW_NAME = 'HZshapeShaperWindow'
        windowWidth = 200
        
        template = PM.uiTemplate('HZshapeShaperTemplate1', force=True)
        template.define(PM.button, width=windowWidth*0.99, height=25)
        template.define(PM.frameLayout, borderVisible=True, labelVisible=True, labelIndent=10,marginHeight=3,marginWidth=3)
        template.define(PM.columnLayout, rowSpacing=5, cal='center')
        template.define(PM.rowLayout, numberOfColumns=6, columnWidth6=[windowWidth*0.155 for i in range(6)], 
                                        adjustableColumn=3, columnAttach=[(i, 'both', 0) for i in range(1,7)])
        template.define(PM.floatSliderGrp, field=True, pre=1, cw3=(windowWidth*0.25, windowWidth*0.25, windowWidth*0.45))                                        
        colors = {'w':'3b3a30','x':'c94c4c','y':'b1cbbb','z':'92a8d1','xn':'9d2f2f','yn':'75a387','zn':'4b70b4', 'a':'deeaee','b':'eea29a'}
        rgb = lambda c: self.hex2rgb(colors.get(c) or c)

        if PM.window( WINDOW_NAME, exists=True ): PM.deleteUI( WINDOW_NAME )
        with PM.window(WINDOW_NAME, title="HZ.C.S.S. v" + self.__version__, maximizeButton=False, 
                        # menuBar=True, menuBarVisible=True,
                        sizeable=False, resizeToFitChildren=True, bgc=rgb('w')) as win:
            # with PM.menu():
            #     PM.menuItem(label='One')
            #     PM.menuItem(label='Two')
            #     with PM.subMenuItem(label='Sub'):
            #         PM.menuItem(label='A')
            #         PM.menuItem(label='B')
            #     PM.menuItem(label='Three')
            with template:
                with PM.frameLayout(borderVisible=False, labelVisible=False):
                    with PM.columnLayout():
                        with PM.rowLayout(numberOfColumns=2, cw2=[150,50], adjustableColumn=1):
                            PM.text(l="H.Z. Control Shape Shaper", font='tinyBoldLabelFont')
                            PM.button(l='About', h=15, w=10, bgc=rgb('80aaff'), 
                                        c= lambda *args: PM.layoutDialog(ui=self.showAbout,t='About', bgc=rgb('80aaff')) )
                        with PM.frameLayout(l="MOVE Curve Shape", font='smallFixedWidthFont'):
                            with PM.columnLayout():
                                self.tamount = PM.floatSliderGrp(l='Move ', min=0.1, max=10, value=0.2, step=0.1, pre=1)
                                with PM.rowLayout():
                                    PM.button(l="+X", c=PM.Callback(self.moveShape, 0), w=10, bgc=rgb('x'))
                                    PM.button(l="-X", c=PM.Callback(self.moveShape, 0,1), w=10, bgc=rgb('xn'))
                                    PM.button(l="+Y", c=PM.Callback(self.moveShape, 1), w=10, bgc=rgb('y'))
                                    PM.button(l="-Y", c=PM.Callback(self.moveShape, 1,1), w=10, bgc=rgb('yn'))
                                    PM.button(l="+Z", c=PM.Callback(self.moveShape, 2), w=10, bgc=rgb('z'))
                                    PM.button(l="-Z", c=PM.Callback(self.moveShape, 2,1), w=10, bgc=rgb('zn'))
                                PM.button(l="Back to Origin", c=PM.Callback(self.resetMoveShape), bgc=rgb('a'))
                        with PM.frameLayout(l="ROTATE Curve Shape", font='smallFixedWidthFont'):
                            with PM.columnLayout():
                                self.ramount = PM.floatSliderGrp(l='Degree ', min=0, max=180, value=90, step=5, pre=0)
                                with PM.rowLayout():
                                    PM.button(l="+X", c=PM.Callback(self.rotateShape, 0), w=10, bgc=rgb('x'))
                                    PM.button(l="-X", c=PM.Callback(self.rotateShape, 0,1), w=10, bgc=rgb('xn'))
                                    PM.button(l="+Y", c=PM.Callback(self.rotateShape, 1), w=10, bgc=rgb('y'))
                                    PM.button(l="-Y", c=PM.Callback(self.rotateShape, 1,1), w=10, bgc=rgb('yn'))
                                    PM.button(l="+Z", c=PM.Callback(self.rotateShape, 2), w=10, bgc=rgb('z'))
                                    PM.button(l="-Z", c=PM.Callback(self.rotateShape, 2,1), w=10, bgc=rgb('zn'))
                        with PM.frameLayout(l="SCALE Curve Shape", font='smallFixedWidthFont'):
                            with PM.columnLayout():
                                self.samount = PM.floatSliderGrp(l='Ratio ', min=0.1, max=2.0, value=1.1, step=0.1, pre=1)
                                self.saxis = PM.checkBoxGrp( numberOfCheckBoxes=4, 
                                                    cw5=(windowWidth*0.2,windowWidth*0.2,windowWidth*0.15,windowWidth*0.15,windowWidth*0.15), 
                                                    label='Axis:', labelArray4=['All', 'X', 'Y', 'Z'],
                                                    v1=True, on1=PM.Callback(self.scaleAllChange, 1), onc=PM.Callback(self.scaleAllChange, 0) )
                                self.scaleAllChange(1)
                                PM.button(l="Resize", c=PM.Callback(self.scaleShape), bgc=rgb('a'))
                        with PM.frameLayout(l="CUSTOM EDIT", font='smallFixedWidthFont'):
                            with PM.columnLayout():                           
                                PM.button(l="Select Control Shape Vertecies", bgc=rgb('b'), c=PM.Callback(self.selectVertecies), h=35 )

    @staticmethod
    def getImagePath(imageName, ext="png", imageFolder="."):
        import os
        # print ("file:", __file__)
        imageFile       = "%s.%s"%(imageName, ext)
        imgPath         = os.path.join(os.path.dirname(__file__),imageFolder, imageFile)
        return imgPath

    def showAbout(self, *args):
        import webbrowser, maya.cmds as MC
        DONATE_URL = "https://commerce.coinbase.com/checkout/75b5e1f7-d8f9-4adf-9812-b3ac3641e2f8"
        SITE_URL = "https://www.hashzee.xyz/hashzeeshapeshaper/"
        form = MC.setParent(q=True)
        MC.formLayout(form, edit=True, w=430)
        title = MC.text(label="HashZee Control Shape Shaper - Version %s" % self.__version__, font="boldLabelFont")
        more = MC.text(label="More info:")
        site = MC.text( label="<a href=\"%s\">HashZee C.S.S. website</a>" % SITE_URL, hyperlink=True, font='boldLabelFont')
        author = MC.text(label="Author: Hamed Zandieh")
        email = MC.text(
            label="<a href=\"mailto:hamed.zandieh@gmail.com/\">hamed.zandieh@gmail.com</a>", hyperlink=True, font='boldLabelFont')
        q1 = MC.text(label="Do you like HashZee C.S.S.?", w=210)
        img = MC.iconTextButton(label="Buy Me a Coffee!", style="iconOnly", command=lambda *args: webbrowser.open_new_tab(DONATE_URL),
                                   image=self.getImagePath("buy-me-a-coffee11"), highlightImage=self.getImagePath("buy-me-a-coffee12"),
                                   )
        elt = MC.text(label="I really appreciate\nthe support!")
        MC.formLayout( form, edit=True, attachForm=[(title, 'top', 10), (title, 'left', 10), 
                                                    (more, 'top', 40), (more, 'left', 10),
                                                    (site, 'top', 55), (site, 'left', 35),
                                                    (author, 'top', 85), (author, 'left', 10),
                                                    (email, 'top', 100), (email, 'left', 35),
                                                    (q1, 'top', 50),  (q1, 'left', 210),
                                                    (img, 'top', 70), (img, 'left', 210), 
                                                    (elt, 'top', 150), (elt, 'left', 30)
                                                    ] ,
                                                    attachPosition=[(img, 'right', 10, 100), (img, 'bottom', 10, 100)]
                                                    , h=200,w=430)

    def shapeVertecies(self):
        objects = PM.selected()
        if not objects:
            PM.warning('no selection found')
            return
        vrtcs = []
        sel_shapes = [s.getShapes() for s in objects]
        for obj in sel_shapes:
            for shp in obj:
                vrtcs.append(shp.cv)
        return vrtcs

    def selectVertecies(self):
        PM.select(self.shapeVertecies(), r=1)

    @one_undo
    def rotateShape(self, axis, neg=False):
        rot = [0,0,0]
        rot[axis] = self.ramount.getValue() * (-1.0 if neg else 1.0)
        PM.rotate(self.shapeVertecies(), rot , os=True, objectCenterPivot=True, forceOrderXYZ=True, euler=True)

    @one_undo
    def moveShape(self, axis, neg=False):
        val = [0,0,0]
        val[axis] = self.tamount.getValue() * (-1.0 if neg else 1.0)
        for vtx in self.shapeVertecies():
            PM.move(vtx, val , relative=True, objectSpace=True, worldSpaceDistance=True)
    
    @one_undo
    def resetMoveShape(self):
        objects = PM.selected()
        if not objects:
            PM.warning('no selection found')
            return
        try:
            PM.refresh(su=True)
            for obj in objects:
                cvs = [s.cv for s in obj.getShapes()]
                PM.select(cvs, r=1)
                bound = PM.exactWorldBoundingBox(cvs, ce=True, ii=True)
                bound_centre = [(bound[0] + bound[3])/2, (bound[1] + bound[4])/2, (bound[2] + bound[5])/2]
                PM.move((obj.getRotatePivot('world') - bound_centre),r=1,wd=1,os=1)
        except Exception as ex:
            raise ex
        finally:
            PM.select(objects, r=1)
            PM.refresh(su=False)

    @one_undo
    def scaleShape(self):
        a,x,y,z = self.saxis.getValueArray4()
        if a: x = y = z = 1
        amnt = self.samount.getValue()
        val = [amnt*x or 1,amnt*y or 1,amnt*z or 1]
        PM.scale(self.shapeVertecies(), val , relative=True, os=True, objectCenterPivot=True)

    def scaleAllChange(self, state):
        self.saxis.setValue1(state)
        if state is 1: self.saxis.setValueArray4((1,0,0,0))



if __name__ != "__main__":
    pass
