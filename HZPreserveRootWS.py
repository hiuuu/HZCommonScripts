# creation date : 1 Jan, 2025
#
# Author :    Hamed Zandieh
# Contact :   hamed.zandieh@gmail.com
#
# Description :
#    This script preserve pose on root change
# How To use :
#    copy python file into maya script folder then run these lines:
# 
# import HZPreserveRootWS as hzprws
# hzprws.doAction("RootX_M","IK*","Pole*")
# 


import maya.cmds as mc
import maya.mel as mm
import maya.utils as ut
from contextlib import contextmanager

def one_undo(func):
    """Decorator - guarantee close chunk.
    type: (function) -> function
    """
    def func_wrapper(*args, **kwargs):
        # type: (*str, **str) -> None
        try:
            mc.undoInfo(openChunk=True)
            return func(*args, **kwargs)
        except Exception as e:
            raise e
        finally:
            mc.undoInfo(closeChunk=True)
    return func_wrapper
    
@contextmanager
def maintain_selection():
    sel = mc.ls(sl=True)
    try: yield
    finally: mc.select(sel) if sel else mc.select(cl=True)

def process_idle_events(max=15):
    # try: mc.timer(endTimer=1)
    # except: pass
    jlist = mc.evalDeferred(list=1)
    mc.timer(startTimer=1)
    while len(jlist) > 1:
        ut.processIdleEvents()
        jlist = mc.evalDeferred(list=1)
        if mc.timer(lap=1) > max:
            break
    mc.timer(endTimer=1)
    
def splitNS(name):
    '''
    Take the namespace on the string and return a tuple with the namespace in the first field, and the short name in the second
    
    @param name: name to separate namespace from
    @type: str
    
    @return: (namespace, baseName)
    @rtype: tuple(str, str)
    '''
    if not name: return None, None
    path = [x for x in name.split('|') if x]     # remove full paths
    name = path[-1]
    stack = [x for x in name.split(":") if x]
    if stack == []: return ("", "")
    if len(stack) == 1: return ("", stack[0])
    else: return (':'.join(stack[:-1]), stack[-1]) 

def getObjectsOfNS(namespace, filterOut=None):
    filterOut = filterOut if filterOut else []
    objects = set()
    namespaces = [namespace]
    for ns in namespaces:
        # get the objects in that namespace
        allObjects = set(mc.ls(f":{ns}:*"))
        # get the filter objects (objects of type that we dont want)
        filterObjects = set()
        for filterItem in filterOut:
            filterObjects.update(set(mc.ls(f":{ns}:*", type=filterItem)))
        # remove the filterObjects from allObjects and push them into the objects set
        objects.update(allObjects.difference(filterObjects))
    return objects

@one_undo
def preserve_pose_on_root_change(curr_frame, namespace, root, selectionFilters):
    mc.currentTime(curr_frame, u=True)
    process_idle_events()
    root = f"{namespace}:{root}"
    selectionFilters = [f"{namespace}:{name}" for name in selectionFilters]
    if not mc.objExists(root):
        raise ValueError(f"Main Root {root} not found")
    if not (keyframes := set(list(mc.keyframe(root, q=True, tc=True)))):
        raise ValueError(f"No keyframes on {root}")
    if not (prev_key := max((k for k in keyframes if k < curr_frame), default=None)):
        print(f"No previous keyframe for {root} in frame {curr_frame}. Action Skipped.")
        return
    if not (ctrls := [*mc.ls(selectionFilters, type='transform')]):
        raise ValueError("No IK or COG controls found")
    ctrls = [obj for obj in ctrls if mc.listRelatives(obj, shapes=True, type=['nurbsCurve'], fullPath=True)]
    print(ctrls)
    # Store world positions with temp locators
    temp_grp = mc.group(em=True, n=f"temp_HZPreserveRootWS_GRP_{curr_frame}")
    loc_pairs = [(ctrl, mc.parent(mc.spaceLocator(n=f"temp_{ctrl}_LOC")[0], temp_grp)[0]) for ctrl in ctrls]
    # Match locators to controls
    [mc.delete(mc.parentConstraint(ctrl, loc)) for ctrl, loc in loc_pairs]
    # Get and set root to prev key transform
    mc.currentTime(prev_key, u=True) # we need update be true to get values correctly
    root_pos = mc.xform(root, q=True, ws=True, t=True)
    root_rot = mc.xform(root, q=True, ws=True, ro=True)
    mc.currentTime(curr_frame, u=True)
    mc.xform(root, ws=True, t=root_pos, ro=root_rot)
    # Restore control positions
    #[mc.delete(mc.parentConstraint(loc, ctrl)) for ctrl, loc in loc_pairs] #constrants did not sets if inputs exists
    [mc.matchTransform(ctrl, loc, pos=True, rot=True) for ctrl, loc in loc_pairs]
    mc.delete(temp_grp)
    
def getKeysOfSelectedRange():
    timeLine = mm.eval("$tmpVar=$gPlayBackSlider")
    selectedRange = tuple(mc.timeControl(timeLine, query=True, rangeArray=True))
    selectedCurves = mc.timeControl(timeLine, query=True, animCurveNames=True)
    return sorted(set(list(mc.keyframe(selectedCurves, t=selectedRange, query=True, timeChange=True))))

def doAction(*wsctrls):
    sel = mc.ls(sl=True, head=1)
    if not sel: raise ValueError(f"unable to locate any selected main/root control!")
    selKeys = getKeysOfSelectedRange()
    namespace, rootName  = splitNS(sel[0])
    current_frame = mc.currentTime(q=True)
    with maintain_selection():
        for sk in selKeys:
            preserve_pose_on_root_change(sk, namespace, rootName, wsctrls)
    mc.currentTime(current_frame, u=True)