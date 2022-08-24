import maya.cmds as cmds
def getSetChild(parentset):
    cmds.select(parentset, noExpand=True, r=1)
    set1 = cmds.ls(selection=True, type="objectSet")[0]
    if set1:
        res = {set1: {}}
        lvl = cmds.sets(set1, q=True)
        if lvl:
            for l in lvl:
                if cmds.objectType(l, isType="objectSet"):
                    child = getSetChild(l)
                    if child:
                        res[set1].update(child)
                else:
                    if not "members" in res[set1]:
                        res[set1]["members"] = []
                    res[set1]["members"].append(l)
            return res
    return {}

def createSet(setdict, prnt=None):
    for k in setdict.keys():
        set1 = cmds.sets(n=k, em=1)
        if "members" in setdict[k]:
            for m in setdict[k]["members"]:
                cmds.sets(m, add=set1)
        else:
            cmds.sets( createSet(setdict[k], set1) , include=set1)
        if prnt:
            cmds.sets( set1 , include=prnt)


import os
dicdata = []
seletedSets = cmds.ls(sl=1, sets=1)
for s in seletedSets: dicdata.append(getSetChild(s) )
# print (dicdata)
scene_path, scene_name = os.path.split(cmds.file(query=True, l=True)[0])
fileName = os.path.join(scene_path , dicdata[0].keys()[0].lower() + ".py")
save_string = """import sys
sys.dont_write_bytecode=True
import maya.cmds as B
A={}
def E(A,P=0):
	F='members'
	for C in A.keys():
		D=B.sets(n=C,em=1)
		if F in A[C]:
			for G in A[C][F]:
				try:B.sets(G,add=D)
				except:pass
		else:B.sets(E(A[C],D),include=D)
		if P:B.sets(D,include=P)
for a in A: E(a)
""".format(dicdata)
with open(fileName, 'w') as outfile:
    outfile.write(save_string)
print (fileName)
