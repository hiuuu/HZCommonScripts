from maya import cmds as MC, mel as MM

def one_undo(func):
    def func_wrapper(*args, **kwargs):
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

class HZwheelRigger:

    def __init__(self, *args):
        pass

    def showUI(self, *args):
        WINDOW_NAME = "HZwheelRiggerWindow"
        if MC.window(WINDOW_NAME, exists = True): MC.deleteUI(WINDOW_NAME)
        window = MC.window( WINDOW_NAME, title = "H.Z. Wheel Rigger")
        form = MC.formLayout(numberOfDivisions=10)

        _ = MC.text( label="Wheel Diameter:", align='left', w=100, h=25)
        MC.formLayout( form, edit=True, attachForm=[( _, 'top', 12), ( _, 'left', 5)] )
        #=========================================
        self.txt_diam = MC.floatField( pre=3, w=100, h=25)
        MC.formLayout( form, edit=True, attachForm=[( self.txt_diam, 'top', 12), ( self.txt_diam, 'left', 100)] )
        #=========================================
        _ = MC.button(c=self.btn_diam_push, label="<<< Calculate", w=100, h=25)
        MC.formLayout( form, edit=True, attachForm=[( _, 'top', 12), ( _, 'left', 220)] )
        #=========================================
        self.rdio_dir = MC.radioButtonGrp( label='Wheel Direction:', numberOfRadioButtons=3, labelArray3=['X', 'Y', 'Z'], cw4= [100,35,35,35], cl4=['left','left','left','left'],  sl=3, w=320)
        MC.formLayout( form, edit=True, attachForm=[( self.rdio_dir, 'top', 53), ( self.rdio_dir, 'left', 5)] )
        #=========================================
        self.rdio_rot = MC.radioButtonGrp( label='Wheel Rotation:', numberOfRadioButtons=3, labelArray3=['X', 'Y', 'Z'], cw4= [100,35,35,35], cl4=['left','left','left','left'],  sl=1, w=320)
        MC.formLayout( form, edit=True, attachForm=[( self.rdio_rot, 'top', 92), ( self.rdio_rot, 'left', 5)] )
        #=========================================
        _ = MC.text( label="Auto Switch:", align='left', w=100, h=25)
        MC.formLayout( form, edit=True, attachForm=[( _, 'top', 133), ( _, 'left', 5)] )
        #=========================================
        self.txt_asw = MC.textField( w=100, h=25)
        MC.formLayout( form, edit=True, attachForm=[( self.txt_asw, 'top', 133), ( self.txt_asw, 'left', 100)] )
        #=========================================
        _ = MC.button( c=self.btn_asw_push,  label="<<< Assign", w=100, h=25)
        MC.formLayout( form, edit=True, attachForm=[( _, 'top', 133), ( _, 'left', 220)] )
        #=========================================
        _ = MC.text( label="Global Scale:", align='left', w=100, h=25)
        MC.formLayout( form, edit=True, attachForm=[( _, 'top', 173), ( _, 'left', 5)] )
        #=========================================
        self.txt_gsc = MC.textField( w=100, h=25)
        MC.formLayout( form, edit=True, attachForm=[( self.txt_gsc, 'top', 173), ( self.txt_gsc, 'left', 100)] )
        #=========================================
        _ = MC.button( c=self.btn_gsc_push,  label="<<< Assign", w=100, h=25)
        MC.formLayout( form, edit=True, attachForm=[( _, 'top', 173), ( _, 'left', 220)] )
        #=========================================
        _ = MC.button( c=self.btn_create_push, backgroundColor=hexcolor('92a8d1'), label="Create H.Z. Auto Wheel", w=200, h=34)
        MC.formLayout( form, edit=True, attachForm=[( _, 'top', 215), ( _, 'left', 65)] )
        #=========================================

        MC.setParent( '..' )
        MC.setParent( '..' )
        MC.showWindow( window )
        MC.window( window, edit=True, widthHeight=(330.0, 270.0))

    def parentOffset(self, node, suffix = '_offset#' ):
        node = str(node)
        grp=str(MC.group(name=(node + suffix), empty=1))
        MC.parent(grp,  node)
        MC.setAttr((grp + ".t"),  0, 0, 0, type='double3')
        MC.setAttr((grp + ".r"),  0, 0, 0, type='double3')
        MC.setAttr((grp + ".s"),  1, 1, 1, type='double3')
        seletedParent=MC.listRelatives(node,  p=1, path=1)
        if seletedParent:
            MC.parent(grp, seletedParent[0])
        else:
            MC.parent(grp,  w=1)
        MC.parent(node, grp)
        MC.setAttr((node + ".t"), 0, 0, 0, type='double3')
        MC.setAttr((node + ".r"), 0, 0, 0, type='double3')
        MC.setAttr((node + ".s"), 1, 1, 1, type='double3')
        return grp

    def shapeParent(self, obj, crvShp = None):
        if crvShp: temp = crvShp
        else: temp=MC.circle( c=(0, 0, 0), ch=1, d=3, ut=0, sw=360, s=8, r=1, tol=0.01, nr=(1, 0, 0))[0]
        #print ('mioo', obj,  MC.getAttr(obj+".t"))
        MC.delete(MC.pointConstraint(obj, temp , weight = 1,mo = False))
        if MC.getAttr(obj+".t") == [(0.0, 0.0, 0.0)]: 
            MC.makeIdentity(temp, apply=True, t=1, r=1, s=1, n=0)
        shape=MC.listRelatives(temp, s=1, f=1)
        MC.parent(shape[0], obj, s=1, r=1)
        MC.delete(temp)
        shape=MC.listRelatives(obj, s=1, f=1)
        for sh in shape:
            MC.rename(sh,  (str(obj) + "Shape"))

    def shapeReplace(self, obj, crvShp = None):
        shape=MC.listRelatives(obj, s=1, f=1)
        if shape:  MC.delete(shape)
        self.shapeParent(obj, crvShp)

    def btn_diam_push(self, *args):
        target=MC.ls(type='transform', sl=1, head=1)
        if target:
            min=MC.getAttr("%s.boundingBoxMinY"%target[0])
            max=MC.getAttr("%s.boundingBoxMaxY"%target[0])
            res = (max - min) 
            MC.floatField(self.txt_diam, e=1, v=res)
            return res
        return None

    def btn_asw_push(self, *args):
      pass

    def btn_gsc_push(self, *args):
      pass

    @one_undo
    def btn_create_push(self, *args):
        target=MC.ls(type='transform', sl=1, head=1)
        if target: target = target[0]
        else:
            MC.warning('Select Wheel Object.')
            return False
        diam = MC.floatField(self.txt_diam, q=True, v=True)
        switch = MC.textField(self.txt_asw, q=True, text=True)
        gscale = MC.textField(self.txt_gsc, q=True, text=True)
        direc = '_xyz'[MC.radioButtonGrp(self.rdio_dir,q=True,sl=True)]
        rotat = '_xyz'[MC.radioButtonGrp(self.rdio_rot,q=True,sl=True)]

        moveNode = self.parentOffset(target, '_move')
        rotNode = self.parentOffset(target, '_rot')
        offsetNode = self.parentOffset(target, '_offset')
        MC.select([moveNode, rotNode, offsetNode], r=1)
        MM.eval('CenterPivot;')

        if not diam:
            diam = self.btn_diam_push()
        MC.addAttr(moveNode, ln='wheelDiam', at='float', dv=diam)
        MC.setAttr("%s.wheelDiam"%(moveNode), k=True)
        radiu = "%s.wheelDiam"%(moveNode)

        _ = MC.curve(p =[(-0.5, 0.0, 0.0), (-0.5, 0.0, 1.0), (0.5, 0.0, 1.0), (0.5, 0.0, 0.0), 
                                    (1.0, 0.0, 0.0), (0.0, 0.0, -1.0), (-1.0, 0.0, 0.0), (-0.5, 0.0, 0.0)],
                                    per = False, d=1, k=[0, 1, 2, 3, 4, 5, 6, 7])
        self.shapeReplace(moveNode, _)
        self.shapeReplace(offsetNode)

        if not switch:
            MC.addAttr(moveNode, min=0, ln="autoSwitch", max=1, at="double", dv=1)
            MC.setAttr("%s.autoSwitch"%(moveNode), k=True)
            switch = "%s.autoSwitch"%(moveNode)
        if not gscale:
            gscale = "%s.s%s"%(moveNode, direc)

        worldRefLoc = MC.spaceLocator(n='%s_worldRefLoc'%target, a=True)[0]
        worldref = "%sShape"%worldRefLoc
        MC.setAttr("%s.v"%worldRefLoc, 0)
        MC.setAttr("%s.localScale"%worldref, 0,0,0, type='double3')
        MC.delete(MC.pointConstraint(moveNode, worldRefLoc  , weight = 1,mo = False))
        MC.setAttr("%s.t%s"%(worldRefLoc,direc), MC.getAttr("%s.t%s"%(worldRefLoc, direc)) - 1)
        
        _ = MC.spaceLocator(n='%s_directionRefLoc'%target, a=True)[0]
        directionRef = "%sShape"%_
        MC.parent(_ , moveNode)
        MC.delete(MC.pointConstraint(moveNode, _  , weight = 1,mo = False))
        MC.setAttr("%s.t%s"%(_, direc), MC.getAttr("%s.t%s"%(_, direc)) + 1)
        MC.setAttr("%s.v"%_, 0)
        MC.setAttr("%s.localScale"%directionRef, 0,0,0, type='double3')

        decMx01 = MC.createNode('decomposeMatrix', name='%sDecMx'%target)
        MC.connectAttr("%s.worldMatrix[0]"%moveNode, "%s.inputMatrix"%decMx01, f=True)

        MC.connectAttr("%s.outputRotate"%decMx01, "%s.r"%worldRefLoc, f=True)

        dist01 = MC.createNode("distanceBetween", name="%sDistance01"%target)
        MC.connectAttr("%s.worldMatrix[0]"%moveNode, "%s.inMatrix2"%dist01, f=True)
        MC.connectAttr("%s.worldMatrix[0]"%worldref, "%s.inMatrix1"%dist01, f=True)

        wheelVecPMA = MC.createNode("plusMinusAverage", name="%sWheelVectorPMA"%target)
        MC.setAttr("%s.operation"%wheelVecPMA, 2)
        MC.connectAttr("%s.worldPosition[0]"%directionRef, "%s.input3D[0]"%wheelVecPMA, f=True)
        MC.connectAttr("%s.outputTranslate"%decMx01, "%s.input3D[1]"%wheelVecPMA, f=True)
        
        motionVecPMA = MC.createNode("plusMinusAverage", name="%sMotionVecPMA"%target)
        MC.setAttr("%s.operation"%motionVecPMA, 2)
        MC.connectAttr("%s.worldPosition[0]"%worldref, "%s.input3D[0]"%motionVecPMA, f=True)
        MC.connectAttr("%s.outputTranslate"%decMx01, "%s.input3D[1]"%motionVecPMA, f=True)

        dotProd = MC.createNode("vectorProduct", name="%sVectorProduct"%target)
        MC.setAttr("%s.operation"%dotProd, 1)
        MC.setAttr("%s.normalizeOutput"%dotProd, 1)       
        MC.connectAttr("%s.output3D"%motionVecPMA, "%s.input1"%dotProd, f=True)
        MC.connectAttr("%s.output3D"%wheelVecPMA, "%s.input2"%dotProd, f=True)

        dotXDisMD = MC.createNode("multiplyDivide", name="%sDotXDisMD"%target)
        MC.setAttr("%s.operation"%dotXDisMD, 1)
        MC.connectAttr("%s.distance"%dist01, "%s.input1X"%dotXDisMD, f=True)
        MC.connectAttr("%s.outputX"%dotProd, "%s.input2X"%dotXDisMD, f=True)

        expers = MC.expression(name = "%sExpression"%target, string = ".O[0]  = ((.I[0] * (360 / (3.1415 * ((.I[1] * .I[3] ) + 0.00001) ))) % 360) * .I[2]")
        MC.connectAttr("%s.outputX"%dotXDisMD, "%s.input[0]"%expers, f=True)
        MC.connectAttr(radiu, "%s.input[1]"%expers, f=True)
        MC.connectAttr(switch, "%s.input[2]"%expers, f=True)       
        MC.connectAttr(gscale, "%s.input[3]"%expers, f=True) 
        MC.connectAttr("%s.output[0]"%expers, "%s.r%s"%(rotNode, rotat), f=True)        

        MC.select(moveNode)
        return True


if __name__ != "__main__":
    pass