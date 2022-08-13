import maya.cmds as cmds
objs=cmds.ls(sl=1, tr=1, head=2) or []
if len(objs) != 2:
    cmds.warning("Please select 2 objects. Controller object should be first.")
else: 
    p1 = cmds.xform(objs[0], q=1, ws=1, t=1)
    p2 = cmds.xform(objs[1], q=1, ws=1, t=1)
    nam = "%s_%s_Line"%(objs[0],objs[1])
    crv=cmds.curve(p=[p1, p2], k=[0, 1], d=1, n=nam)
    cmds.cluster("%s.cv[0]"%crv, wn=(objs[0], objs[0]), bs=1, ar=1 )
    cmds.cluster("%s.cv[1]"%crv, wn=(objs[1], objs[1]), bs=1, ar=1 )         
    cmds.setAttr("%s.overrideEnabled"%crv, 1)
    cmds.setAttr("%s.overrideDisplayType"%crv, 1)
    cmds.setAttr("%s.overrideColor"%crv, 2)
    cmds.setAttr("%s.inheritsTransform"%crv, 0)
    expers = cmds.expression(name = "%sExpression"%nam, string = ".O[0] = (.I[0] && .I[1])")
    cmds.connectAttr("%s.v"%objs[0], "%s.input[0]"%expers, f=True)
    cmds.connectAttr("%s.v"%objs[1], "%s.input[1]"%expers, f=True)       
    cmds.connectAttr("%s.output[0]"%expers, "%s.v"%crv, f=True) 
    cmds.addAttr(crv, ln="length", at='double')
    cmds.setAttr('%s.length'%crv, k=True)
    crvInfoNode=cmds.createNode('curveInfo')
    cmds.connectAttr('%s.local'%crv, "%s.inputCurve"%crvInfoNode, f=1)
    cmds.connectAttr("%s.arcLength"%crvInfoNode, '%s.length'%crv, f=1)
    [cmds.setAttr("%s.%s%s"%(crv,a,b),l=1,k=0,cb=0) for a in "trs" for b in "xyz"]
    cmds.setAttr("%s.v"%crv, lock=1, keyable=0, channelBox=0)
    cmds.setAttr("%s.length"%crv, keyable=0, channelBox=1)
