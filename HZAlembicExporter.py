import maya.cmds as cmds
import maya.mel as mel
import maya.utils as utl
import maya.api.OpenMaya as om2
import re, os

cmds.loadPlugin("AbcExport.mll", quiet=True)
def process_idle_events(max=15):
	jlist=cmds.evalDeferred(list=1)
	# '$list' contains all the current events/commands in the idle queue
	# The timer is here for safety
	# you could use a counter or the mel command 'progressWindow'
	cmds.timer(startTimer=1)
	while (len(jlist)>1):
		utl.processIdleEvents()
		# Idle events might spawn more idle events so we need to
		# loop until the list is empty
		jlist=cmds.evalDeferred(list=1)
		# Stop processing idle events after <max> seconds
		if cmds.timer(lap=1)>max: break
	cmds.timer(endTimer=1)

cmds.lockNode('initialShadingGroup', lu=0, l=0)
selection = cmds.ls(sl = True, tr=1)
for node in selection:
    cmds.lockNode(node, l=False)
selectedPolygons = cmds.filterExpand(selection, sm = 12)
cmds.select(selectedPolygons, r = True)
shapesInSel = cmds.ls(dag=1,o=1,s=1,sl=1)
shadingGrps = cmds.listConnections(shapesInSel,type='shadingEngine')
shadingGrps = list(set(shadingGrps))
cmds.select(cl=1)
#shaderGrps = cmds.ls("*:*SG?")
ass = {}
for i in range(len(shadingGrps)):
    shaders = cmds.ls(cmds.listConnections(shadingGrps[i]),materials=1)
    if re.search(r'eye(?!_)', shaders[0]): continue
    cmds.hyperShade(objects=shadingGrps[i])
    objWithMaterial = cmds.ls(sl=1)
    cmds.hyperShade(a="lambert1")
    cmds.select(cl=1)
    sels = []
    for j in range(len(objWithMaterial)):
        if 'f[' in objWithMaterial[j]:
            sels.append(objWithMaterial[j])
        else:
            sels.append(objWithMaterial[j]+".f[*]")
    ass[shadingGrps[i]] = sels
    cmds.select(cl=1)
process_idle_events()
for k, v in ass.items():
    cmds.select(v, r=1)
    cmds.hyperShade(a=k) 
process_idle_events(5)
cmds.select(selectedPolygons, r = True)
fullPathPolys = []
for dag in selectedPolygons:
    selList = om2.MSelectionList ()
    selList.add (dag)
    fullPathPolys.append(selList.getDagPath(0).fullPathName())
currentFileName = cmds.file(query=True, l=True)[0]
scene_path, scene_name = os.path.split(currentFileName) 
abcDir = os.path.join(scene_path, "ALEMBICS")
if not os.path.isdir(abcDir): os.mkdir(abcDir)  
alembicFile = os.path.join(abcDir, "%s.abc"%scene_name)
#startFrame, endFrame = (1,300)
startFrame = int(cmds.playbackOptions(query=True, min=True))
endFrame = int(cmds.playbackOptions(query=True, max=True))
roots = ""
for item in fullPathPolys: roots += " -root %s"%item
com = 'AbcExport -j "-frameRange %s %s -ro -stripNamespaces -uvWrite -writeFaceSets -writeUVSets -dataFormat ogawa %s -file \\"%s\\"";'%(startFrame,endFrame,roots,alembicFile.replace("\\", "/"))
print(com)
mel.eval(com)
cmds.select(cl=1)


############
"""
import pymel.core as pm
import maya.utils as utl
import maya.api.OpenMaya as om2
import os
import re

# Load plugin for Alembic export
pm.loadPlugin("AbcExport.mll", quiet=True)

def process_idle_events(max=15):
    jlist = pm.evalDeferred(list=1)
    pm.timer(startTimer=1)
    while len(jlist) > 1:
        utl.processIdleEvents()
        jlist = pm.evalDeferred(list=1)
        if pm.timer(lap=1) > max:
            break
    pm.timer(endTimer=1)

# Unlock initial shading group and selected nodes
pm.lockNode('initialShadingGroup', lock=False, unlock=True)
selected = pm.selected(type='transform')
for node in selected:
    pm.lockNode(node, lock=False)

# Filter and select polygons
selectedPolygons = pm.filterExpand(selected, sm=12)
pm.select(selectedPolygons, r=True)

# Get shading groups and materials
shapesInSel = pm.ls(dag=True, objects=True, shapes=True, sl=True)
shadingGrps = pm.listConnections(shapesInSel, type='shadingEngine')
shadingGrps = list(set(shadingGrps))
pm.select(clear=True)

# Store the assignment of materials
ass = {}
for shadingGrp in shadingGrps:
    shaders = pm.ls(pm.listConnections(shadingGrp), materials=True)
    if re.search(r'eye(?!_)', shaders[0]):
        continue
    pm.hyperShade(objects=shadingGrp)
    objWithMaterial = pm.ls(sl=True)
    pm.hyperShade(assign="lambert1")
    pm.select(clear=True)

    sels = [obj if 'f[' in obj else f"{obj}.f[*]" for obj in objWithMaterial]
    ass[shadingGrp] = sels
    pm.select(clear=True)

process_idle_events()

# Reassign materials
for shadingGrp, objs in ass.items():
    pm.select(objs, r=True)
    pm.hyperShade(assign=shadingGrp)

process_idle_events(5)

# Re-select original polygons
pm.select(selectedPolygons, r=True)

# Get the full paths of the selected polygons
fullPathPolys = [om2.MSelectionList().add(dag).getDagPath(0).fullPathName() for dag in selectedPolygons]

# Get the current file path
currentFileName = pm.file(q=True, l=True)[0]
scene_path, scene_name = os.path.split(currentFileName)

# Create Alembic directory if it doesn't exist
abcDir = os.path.join(scene_path, "ALEMBICS")
os.makedirs(abcDir, exist_ok=True)

# Define Alembic file path
alembicFile = os.path.join(abcDir, f"{scene_name}.abc")

# Get start and end frames
startFrame = int(pm.playbackOptions(q=True, min=True))
endFrame = int(pm.playbackOptions(q=True, max=True))

# Prepare the roots argument for Alembic export
roots = ' '.join([f"-root {item}" for item in fullPathPolys])

# Export Alembic
pm.mel.eval(f'AbcExport -j "-frameRange {startFrame} {endFrame} -ro -stripNamespaces -uvWrite -writeFaceSets -writeUVSets -dataFormat ogawa {roots} -file {alembicFile.replace("\\", "/")}"')

# Clear selection
pm.select(clear=True)
"""