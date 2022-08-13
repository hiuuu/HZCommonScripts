from maya import cmds as MC, mel as MM

def one_undo(func):
    """Decorator - guarantee close chunk.
    type: (function) -> function
    """
    def func_wrapper(*args, **kwargs):
        # type: (*str, **str) -> None
        try:
            MC.undoInfo(openChunk=True)
            return func(*args, **kwargs)
        except Exception as e:
            raise e
        finally:
            MC.undoInfo(closeChunk=True)
    return func_wrapper

def hexcolor(s):
    s=s.upper()
    return float(int(s[:2], 16)) / 255, float(int(s[2:4], 16)) / 255, float(int(s[4:6], 16)) / 255 

def getFrameRange():
    gPlayBackSlider = MM.eval("$tmpVar=$gPlayBackSlider")
    if MC.timeControl(gPlayBackSlider, query=True, rangeVisible=True):
        frameRange = MC.timeControl(gPlayBackSlider, query=True, rangeArray=True)
        start = frameRange[0]
        end = frameRange[1]-1
    else:
        start = MC.playbackOptions(query=True, min=True)
        end = MC.playbackOptions(query=True, max=True)
    return start,end

class HZCRow:
    def __init__(self, parnt, colnum, customWidths = []):
        self.parnt = parnt
        self.colnum = len(customWidths) if customWidths else colnum
        self.cwidths = customWidths

    def __enter__(self):
        if not self.cwidths:
            colwid = [(i+1, int(300/self.colnum)) for i in range(self.colnum)]
        else:
            colwid = [(i+1, self.cwidths[i]) for i in range(self.colnum)]
        colatc = [(i+1, 'left', 5) for i in range(self.colnum)]
        #print (self.colnum, colwid, colatc)
        MC.rowLayout( parent=self.parnt, numberOfColumns=self.colnum, columnWidth=colwid, adjustableColumn=2, columnAlign=(1, 'left'), columnAttach=colatc )

    def __exit__(self, *args):
        MC.setParent( '..' )

class HZCycleMaker:

    def __init__(self, *args):
        pass

    def showUI(self, *args):
        WINDOW_NAME = "HZCycleMakerWindow"
        if MC.window(WINDOW_NAME, exists = True): MC.deleteUI(WINDOW_NAME)
        window = MC.window( WINDOW_NAME, title = "H.Z. Cycle Maker")
        form = MC.columnLayout( columnAttach=('both', 5), rowSpacing=10, columnWidth=300 )

        self.chk_extract = MC.checkBox( ann="Main Keyframes will be Removed", l="Extract Animation (optional)", align='left' )
        #=========================================
        with HZCRow(form, 3):
            MC.text(l="Distane:")
            self.txt_dist = MC.floatField(pre=3, v=40)
            MC.button(h=20, c=self.hzDist_help, l="?", ann="Show Help", w=50)            
        #=========================================
        with HZCRow(form, 4, [55,75,20,110]):
            MC.text(l="Forward:")
            self.chk_nega = MC.checkBox( label='Negative', align='left' )
            MC.text(l="")
            self.rdio_dir = MC.radioButtonGrp(numberOfRadioButtons=3, labelArray3=['X', 'Y', 'Z'], cw3= [35,35,35], cl3=['left','left','left'],  sl=3)
        #=========================================
        with HZCRow(form, 5, [75,50,25,50,50]):
            MC.text(l="Frame From:", w=75)
            self.txt_animfrom = MC.intField( w=50, v=1)
            MC.text(l="To:", w=25)
            self.txt_animto = MC.intField( w=50, v=25)
            MC.button(h=20, c=self.hzfromTo, l="<<<", ann="Fill From Timeline", w=50)
        #=========================================
        with HZCRow(form, 3):
            MC.text(bgc=hexcolor('cccccc'), l="System Prefix:")
            self.txt_sym = MC.textField(tx="HZAC1")
            MC.button(h=20, c=self.hzdelSys, l="X", backgroundColor=hexcolor('c94c4c'), ann="Delete Current System", w=50)
        #=========================================
        with HZCRow(form, 3):
            MC.text(l="Animated Nodes:")
            self.txt_nds = MC.textScrollList( numberOfRows=5, allowMultiSelection=True, 
                                                            deleteKeyCommand = self.hznodesDelItem, doubleClickCommand = self.hznodesDelItem)
            MC.button(h=20, c=self.hzasgNodes, l="<<<", w=50)
        #=========================================
        with HZCRow(form, 3):
            MC.text(l="Parent Ctrl:")
            self.txt_mnc = MC.nameField()
            MC.button(h=20, c=self.hzasgMnc, l="<<<", w=50)
        #=========================================
        with HZCRow(form, 3):
            MC.text(l="Path Curve (opt):")
            self.txt_pcrv = MC.nameField()
            MC.button(h=20, c=self.hzasgPCrv, l="<<<", w=50)
        #=========================================
        MC.button(c=self.hzmaker, l="Create H.Z. Auto Cycle", backgroundColor= hexcolor('92a8d1') , w=240)

        MC.setParent( '..' )
        MC.setParent( '..' )
        MC.showWindow( window )
        MC.window( window, edit=True, widthHeight=(300.0, 340.0))

    def hzasgMnc(self, *args):
        sl=MC.ls(sl=1, ni=True, o=True, r=True)
        if sl: MC.nameField(self.txt_mnc, e=1, object=sl[0])

    def hzasgNodes(self, *args):
        sl=MC.ls(sl=1, ni=True, o=True, r=True)
        MC.textScrollList(self.txt_nds, e=1, removeAll=True)
        if sl: MC.textScrollList(self.txt_nds, e=1, append=sl)

    def hznodesDelItem(self, *args):
        selsCount = MC.textScrollList(self.txt_nds, q=1, numberOfSelectedItems=True)
        if selsCount > 0:
            sels = MC.textScrollList(self.txt_nds, q=1, selectIndexedItem=True)
            MC.textScrollList(self.txt_nds, e=1, deselectAll=True)
            MC.textScrollList(self.txt_nds, e=1, removeIndexedItem=sels)

    def hzasgPCrv(self, *args):
        cfrv=MC.ls(sl=1, ni=True, o=True, r=True)
        if cfrv: MC.nameField(self.txt_pcrv, e=1, object=cfrv[0])

    def hzdelSys(self, txSym=None):
        if not txSym:
            txSym =str(MC.textField(self.txt_sym, q=1, tx=1))+ "__"
        oldsys = MC.ls("%s*" % txSym)
        if oldsys:
            MC.delete("%s*" % txSym)

    def hzDist_help(self, *args):
        MC.warning("Distance Help:\n" 
                +"white: 63 -> 21F \n" 
                +"sharkito: 21.1 -> 9F \n" 
                +"sharkira: 41.5 -> 16F \n" 
                +"mommyShark: 45.5 -> 17F  && 9.1 -> 17F \n"
                ,'i')

    def hzfromTo(self, *args):
        strt,end = getFrameRange()
        MC.intField(self.txt_animfrom, e=1, v=strt)
        MC.intField(self.txt_animto, e=1, v=end)
    
    @one_undo
    def hzmaker(self, *args):
        forwardUp = 'Y'
        forward = 'Z'
        forwardMD = 1
        dirIdx = MC.radioButtonGrp(self.rdio_dir, q=1, sl=1)
        if dirIdx == 1:
            forward = 'X'
            forwardUp = 'Y'
        elif dirIdx == 2:
            forward = 'Y'
            forwardUp = 'Z'
        if MC.checkBox(self.chk_nega, q=1, v=1):
            forwardMD = -1
        extract = MC.checkBox(self.chk_extract, q=True, v=True)
        txMnc =MC.nameField(self.txt_mnc, q=1, object=1)
        txDis =float(MC.floatField(self.txt_dist, q=1, v=1))
        txAnimFrom =int(MC.intField(self.txt_animfrom, q=1, v=1))
        txAnimTo =int(MC.intField(self.txt_animto, q=1, v=1))
        txSym =str(MC.textField(self.txt_sym, q=1, tx=1)) + "__"
        cfrv = MC.nameField(self.txt_pcrv, q=1, object=1)
        curv = (cfrv and MC.objExists(cfrv))
        txKey = MC.textScrollList(self.txt_nds, q=1, allItems=True)
        if not txKey:
            MC.warning('No animation found!')
            return
        # make sure the txMnc is not inside the txKey list
        txKey = ["%s"%t for t in txKey if not t == txMnc]
        self.hzdelSys(txSym)
        #__________________CreateControllerNode
        mainController = MC.createNode('transform', n=txSym + "HZAutoCycle#_ctrl")
        MC.addAttr(mainController, min=0, ln="auto", max=1, at="double", dv=1)
        MC.addAttr(mainController, ln="distance",  at="double")
        for b in 'trs':
            for a in 'xyz':
                MC.setAttr("%s.%s%s" % (mainController,b,a) , k=False, l=True)
        MC.setAttr("%s.v" % (mainController)  , k=False)
        MC.setAttr("%s.auto" % (mainController) , k=True)
        MC.setAttr("%s.distance" % (mainController) , k=True)
        MC.setAttr("%s.ove" % (mainController), True)
        MC.setAttr("%s.ovc" % (mainController), 30)
        mainControllerShape1 = MC.curve(p =[(0, 1, 1), (0, 0, 2), (1, 0, 1), (0, 1, 1), 
                                    (0.0, 0.0, 0.0), (1.0, 0.0, 1.0), (0, 0.0, 2.0), (-1, 0.0, 1.0),
                                    (0.0, 0.0, 0.0),(0.0, 1.0, 1.0),(-1, 0.0, 1.0),(0.0, -1, 1.0),
                                    (0.0, 0.0, 2.0),(-1, 0.0, 1.0),(0.0, 0.0, 0.0),(0.0, -1, 1),(1.0, 0.0, 1.0)],
                                    per = False, d=1, k=[0, 1, 2, 3, 4, 5, 6, 7, 8 ,9 ,10,11,12,13,14,15,16])
        MC.setAttr("%s.v" % (mainControllerShape1), k=False)
        MC.xform(mainControllerShape1, centerPivots=True)
        MC.xform(mainControllerShape1, os=1, t=(0,0,0))
        txMncBB = MC.xform(txMnc, q=1, bb=1)
        scalePercent = 0.1+ (abs(txMncBB[3] - txMncBB[0]) * 0.01)
        MC.setAttr("%s.scale" % (mainControllerShape1), scalePercent,scalePercent,scalePercent, type='double3')
        MC.makeIdentity(mainControllerShape1, apply=True)
        MC.parent(MC.listRelatives(mainControllerShape1, path=1, s=1) , mainController, s=1, r=1)
        MC.delete(mainControllerShape1)
        shapes=MC.listRelatives(mainController, s=1, f=1)
        for shp in shapes:
            MC.rename(shp,  (str(mainController) + "Shape"))
        #_____eos_____________CreateControllerNode 
        if curv:
            MC.createNode('curveInfo', n=(txSym + "crvInf"))
            MC.connectAttr((cfrv + ".worldSpace"), (txSym + "crvInf.inputCurve"), f=1)    
        MC.setAttr("%s.distance" % (mainController), txDis)
        MC.createNode('multiplyDivide', n=(txSym + "time_MD"))
        MC.createNode('unitToTimeConversion', n=(txSym + "time_MD_UTTC"))
        MC.setAttr((txSym + "time_MD.input2X"), (abs(txAnimTo - txAnimFrom)))
        MC.setAttr((txSym + "time_MD_UTTC.conversionFactor"), 200)
        MC.connectAttr((txSym + "time_MD.outputX"), (txSym + "time_MD_UTTC.input"))   
        dirLoc = MC.spaceLocator(n='%s_directionRefLoc'%txSym, a=True)[0]
        directionRef = "%sShape"%dirLoc
        MC.delete(MC.pointConstraint(txMnc, dirLoc  , weight = 1,mo = False))
        MC.setAttr("%s.t%s"%(dirLoc, forward.lower() ), MC.getAttr("%s.t%s"%(dirLoc, forward.lower() )) + 1)
        MC.setAttr("%s.v"%dirLoc, 0)
        MC.setAttr("%s.localScale"%directionRef, 0,0,0, type='double3')
        MC.group([mainController, dirLoc], p=str(txMnc), n="%s_grp"  % (mainController)) 
        MC.select(cl=1)
        awlayer = self.createAnimLayer(txKey, namePrefix = txSym)
        rootLayer = MC.animLayer(query=True, root=True) or 'BaseAnimation'
        MC.connectAttr((mainController + ".auto"), (awlayer + ".weight"),  f=1)
        self.selectAnimLayer(awlayer)  
        MC.cutKey(iub=1, *txKey)
        self.selectAnimLayer(rootLayer)
        for ctrl in txKey:
            self.copyAnimation(source=ctrl, destination=ctrl, start=txAnimFrom, end=txAnimTo, destinationLayer=awlayer, sourceLayer=rootLayer)
        if extract:
            self.selectAnimLayer(rootLayer)  
            MC.cutKey(t=(txAnimFrom, txAnimTo), iub=1, *txKey)
        layerAnimCurves = MC.animLayer(awlayer, query=True, animCurves=True) 
        #print (layerAnimCurves)
        for lac in layerAnimCurves:
            MC.setAttr((str(lac) + ".preInfinity"), 3)
            MC.setAttr((str(lac) + ".postInfinity"), 3)
            MC.connectAttr((txSym + "time_MD_UTTC.output"), (str(lac) + ".input"), f=1)
        if curv:
            MC.addAttr(mainController, ci=True, min=0, ln="curve_path", max=100, at="double", sn="curve_path")
            MC.setAttr("%s.curve_path" % (mainController), k=True)
            MC.select(txMnc, r=1)
            MC.select(cfrv, add=1)
            MC.pathAnimation(upAxis=forwardUp.lower() , fractionMode=True, 
                endTimeU=MC.playbackOptions(query=1, maxTime=1), 
                startTimeU=MC.playbackOptions(minTime=1, query=1), 
                n=(txSym + "motionPath"), worldUpType="vector", 
                inverseUp=False, 
                inverseFront=False, 
                follow=True, 
                bank=False, 
                followAxis=forward.lower(), 
                worldUpVector=(0, 1, 0) )
            MC.createNode('unitConversion', n=(txSym + "utC"))
            MC.setAttr((txSym + "utC.conversionFactor"),  0.01)
            MC.connectAttr((mainController + ".curve_path"), (txSym + "utC.input"),  f=1)
            MC.connectAttr((txSym + "utC.output"), (txSym + "motionPath.uValue"),  f=1)
            MC.createNode('multiplyDivide', n=(txSym + "Steps_MD"))
            MC.setAttr((txSym + "Steps_MD.operation"),  2)
            MC.createNode('multiplyDivide', n=(txSym + "Position_MD"))
            MC.connectAttr((txSym + "crvInf.arcLength"), (txSym + "Steps_MD.input1X"),  f=1)
            MC.connectAttr((mainController + ".distance"), (txSym + "Steps_MD.input2X"), f=1)
            MC.connectAttr((txSym + "Steps_MD.outputX"), (txSym + "Position_MD.input1X"), f=1)
            MC.connectAttr((txSym + "utC.output"), (txSym + "Position_MD.input2X"), f=1)
            MC.connectAttr((txSym + "Position_MD.outputX"), (txSym + "time_MD.input1X"), f=1) 
        else:
            worldRefLoc = MC.spaceLocator(n='%s_worldRefLoc'%txSym, a=True)[0]
            worldref = "%sShape"%worldRefLoc
            MC.delete(MC.pointConstraint(txMnc, worldRefLoc  , weight = 1,mo = False))
            MC.setAttr("%s.t%s"%(worldRefLoc,  forward.lower()), MC.getAttr("%s.t%s"%(worldRefLoc,  forward.lower() )) - 1)
            MC.setAttr("%s.v"%worldRefLoc, 0)
            MC.setAttr("%s.localScale"%worldref, 0,0,0, type='double3')
            decMx01 = MC.createNode('decomposeMatrix', name='%sDecMx'%txSym)
            MC.connectAttr("%s.worldMatrix[0]"%txMnc, "%s.inputMatrix"%decMx01, f=True)
            MC.connectAttr("%s.outputRotate"%decMx01, "%s.r"%worldRefLoc, f=True)
            dist01 = MC.createNode("distanceBetween", name="%sDistance01"%txSym)
            MC.connectAttr("%s.worldMatrix[0]"%txMnc, "%s.inMatrix2"%dist01, f=True)
            MC.connectAttr("%s.worldMatrix[0]"%worldref, "%s.inMatrix1"%dist01, f=True)
            wheelVecPMA = MC.createNode("plusMinusAverage", name="%sWheelVectorPMA"%txSym)
            MC.setAttr("%s.operation"%wheelVecPMA, 2)
            MC.connectAttr("%s.worldPosition[0]"%directionRef, "%s.input3D[0]"%wheelVecPMA, f=True)
            MC.connectAttr("%s.outputTranslate"%decMx01, "%s.input3D[1]"%wheelVecPMA, f=True)
            motionVecPMA = MC.createNode("plusMinusAverage", name="%sMotionVecPMA"%txSym)
            MC.setAttr("%s.operation"%motionVecPMA, 2)
            MC.connectAttr("%s.worldPosition[0]"%worldref, "%s.input3D[1]"%motionVecPMA, f=True)
            MC.connectAttr("%s.outputTranslate"%decMx01, "%s.input3D[0]"%motionVecPMA, f=True)
            dotProd = MC.createNode("vectorProduct", name="%sVectorProduct"%txSym)
            MC.setAttr("%s.operation"%dotProd, 1)
            MC.setAttr("%s.normalizeOutput"%dotProd, 1)       
            MC.connectAttr("%s.output3D"%motionVecPMA, "%s.input1"%dotProd, f=True)
            MC.connectAttr("%s.output3D"%wheelVecPMA, "%s.input2"%dotProd, f=True)
            dotXDisMD = MC.createNode("multiplyDivide", name="%sDotXDisMD"%txSym)
            MC.setAttr("%s.operation"%dotXDisMD, 1)
            MC.connectAttr("%s.distance"%dist01, "%s.input1X"%dotXDisMD, f=True)
            MC.connectAttr("%s.outputX"%dotProd, "%s.input2X"%dotXDisMD, f=True)
            forwardMDN = MC.createNode('multiplyDivide', name="%sforwardMDN"%txSym)
            MC.setAttr("%s.operation"%forwardMDN,  1)
            MC.connectAttr("%s.outputX"%dotXDisMD, "%s.input1X"%forwardMDN,  f=True)
            MC.setAttr("%s.input2X"%forwardMDN, forwardMD)
            stepMD = MC.createNode('multiplyDivide', name="%sStepsMD"%txSym) 
            MC.setAttr("%s.operation"%stepMD,  2)
            MC.connectAttr("%s.outputX"%forwardMDN, "%s.input1X"%stepMD,  f=True)
            MC.connectAttr((mainController + ".distance"), "%s.input2X"%stepMD, f=True)
            positionMD = MC.createNode('multiplyDivide', name="%sPositionMD"%txSym)
            MC.setAttr("%s.operation"%positionMD,  1)
            MC.connectAttr("%s.outputX"%stepMD, "%s.input1X"%positionMD, f=True)
            MC.connectAttr((mainController + ".auto"), "%s.input2X"%positionMD, f=True)
            MC.connectAttr("%s.outputX"%positionMD, (txSym + "time_MD.input1X"), f=True) 
        MC.select(txMnc)
        return True

    def createAnimLayer(self, nodes=None, name=None, namePrefix='', override=True):
        '''
        Create an animation layer, add nodes, and select it.
        '''

        #if there's no layer name, generate one
        if not name:
            if namePrefix:
                namePrefix+='_'
            if nodes:
                shortNodes = MC.ls(nodes, shortNames=True)
                shortNodes = [x.rpartition(':')[-1] for x in shortNodes]
                #if there's just one node, use it's name minus the namespace
                if len(shortNodes) == 1:
                    name = namePrefix+shortNodes[0]
                elif ':' in nodes[0]:
                    #otherwise use the namespace if it has one
                    name = namePrefix + nodes[0].rsplit('|',1)[-1].rsplit(':',1)[0]
            if not name:
                if not namePrefix:
                    namePrefix = 'hz_'
                name = namePrefix+'animLayer'

        layer = MC.animLayer(name, override=override, 
                excludeScale=True, excludeVisibility=True, excludeBoolean=True
                , excludeDynamic=True, excludeEnum = True )

        #add the nodes to the layer
        if nodes:
            sel = MC.ls(sl=True)
            MC.select(nodes)
            MC.animLayer(layer, edit=True, addSelectedObjects=True)
            if sel:
                MC.select(sel)
            else:
                MC.select(clear=True)

        #select the layer
        self.selectAnimLayer(layer)
        return layer

    def selectAnimLayer(self, animLayer=None):
        '''
        Select only the specified animation layer
        '''
        #deselect all layers
        for each in MC.ls(type='animLayer'):
            MC.animLayer(each, edit=True, selected=False, preferred=False)
        if animLayer:
            MC.animLayer(animLayer, edit=True, selected=True, preferred=True)

    def minimizeRotationCurves(self, obj):
        '''
        Sets rotation animation to the value closest to zero.
        '''

        rotateCurves = MC.keyframe(obj, attribute=('rotateX','rotateY', 'rotateZ'), query=True, name=True)

        if not rotateCurves or len(rotateCurves) < 3:
            return

        keyTimes = MC.keyframe(rotateCurves, query=True, timeChange=True)
        tempFrame = sorted(keyTimes)[0] - 1

        #set a temp frame
        MC.setKeyframe(rotateCurves, time=(tempFrame,), value=0)

        #euler filter
        MC.filterCurve(rotateCurves)

        #delete temp key
        MC.cutKey(rotateCurves, time=(tempFrame,))

    def copyAnimation(self, source=None, destination=None, pasteMethod='replace', offset=0, start=None, end=None, sourceLayer=None, destinationLayer=None):
        '''
        Actually do the copy and paste from one node to another. If start and end frame is specified,
        set a temporary key before copying, and delete it afterward.
        '''
        
        if destinationLayer:
            MC.select(destination)
            MC.animLayer(destinationLayer, edit=True, addSelectedObjects=True)
     
        if sourceLayer:
            self.selectAnimLayer(sourceLayer)  
         
        #we want to make sure rotation values are within 360 degrees, so we don't get flipping when blending layers.
        self.minimizeRotationCurves(source)
        #minimizeRotationCurves(destination)
        
        if pasteMethod=='replaceCompletely' or not start or not end:
            MC.copyKey(source, al = sourceLayer)
            MC.pasteKey(destination, option=pasteMethod, timeOffset=offset, al=destinationLayer)
        else:

            #need to do this per animation curve, unfortunately, to make sure we're not adding or removing too many keys
            animCurves = MC.keyframe(source, query=True, name=True)
            if not animCurves:
                return
            
            #story cut keytimes as 2 separate lists means we only have to run 2 cutkey commands, rather than looping through each
            cutStart = list()
            cutEnd = list()
            for curve in animCurves:
            
                #does it have keyframes on the start and end frames?
                startKey = MC.keyframe(curve, time=(start,), query=True, timeChange=True)
                endKey = MC.keyframe(curve, time=(end,), query=True, timeChange=True)

                #if it doesn't set a temporary key for start and end
                #and store the curve name in the appropriate list
                if not startKey:
                    MC.setKeyframe(curve, time=(start,), insert=True)
                    cutStart.append(curve)
                if not endKey: 
                    MC.setKeyframe(curve, time=(end,), insert=True)
                    cutEnd.append(curve)
                
            MC.copyKey(source, time=(start,end), al=sourceLayer)
            MC.pasteKey(destination, option=pasteMethod, time=(start,end), copies=1, connect=0, timeOffset=offset, al=destinationLayer)

            #if we set temporary source keys, delete them now
            if cutStart:
                MC.cutKey(cutStart, time=(start,))
            if cutEnd:
                MC.cutKey(cutEnd, time=(end,))

if __name__ != "__main__":
    pass