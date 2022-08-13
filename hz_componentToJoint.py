# Maya script that creates joints on each selected vertex or at the center of each selected edge or face.
# USAGE:
# copy this file in maya script folder and then run this code:
#   import hz_componentToJoint as c2j
#   c2j.componentToJoint()

import maya.cmds as cmds
import re


def componentToJoint():
    selection = cmds.ls(sl=1)
    if len(selection)<=0 : return 
    if cmds.objectType(selection[0]) != "mesh": return
    # return the selection as a list
    selList = getSelection()
    #print selList
    if len(selList) <= 0 : return
    componentType = selList[0][selList[0].index(".") + 1:selList[0].index("[")]
    componentCenters = []
    # if you selected a face or edge, make our joints at those component's centers
    cmds.select(cl=1)
    num = 0
    if componentType == "f" or componentType == "e":
        for c in selList:
            p = cmds.xform(c, q=1, t=1, ws=1)
            # find the average of all our x,y,z points. That's our center
            componentCenters.append([sum(p[0::3]) / len(p[0::3]),
                                     sum(p[1::3]) / len(p[1::3]),
                                     sum(p[2::3]) / len(p[2::3])])
            for loc in componentCenters:
                cmds.select(cmds.joint(n="joint#", p=loc, rad=.25), d=1)
                num += 1

    # else make a joint at the location of each vertex
    else:
        for c in selList:
            # make a joint at the position of each selected vertex
            cmds.select(cmds.joint(n="joint#", p=cmds.pointPosition(c), rad=.25), d=1)
            num += 1

    cmds.select( clear=True )
    print (str(num) + " joint(s) are placed on selected component(s) position. Done!"),
    return ""


def getSelection():
    # run before: cmds.selectPref(trackSelectionOrder = 1)
    components = cmds.ls(os=1)
    if len(components)<=0 : return []
    # expression_if_true if condition else expression_if_false
    #print components
    selList = []
    objName = components[0][0:components[0].index(".")]
    #print objName
    # go through every component in the list. If it is a single component ("pCube1.vtx[1]"), add it to the list. Else,
    # add each component in the index ("pCube1.vtx[1:5]") to the list
    for c in components:
        #print c
        strip = re.search(r"\[(\d+):(\d+)\]", c, re.I)
        if bool(strip):
            startComponent = int(strip.group(1))
            endComponent = int(strip.group(2))
            #startComponent = int(c[c.index("[") + 1: c.index(":")] or 0)
            #endComponent = int(c[c.index(":") + 1:c.index("]")] or 0)
            componentType = c[c.index(".") + 1:c.index("[")]
            while startComponent <= endComponent:
                selList.append(objName + "." + componentType + "[" + str(startComponent) + "]")
                startComponent += 1
        else:
            selList.append(c)

    return selList

