import pymel.core as pm
'''*********************************************
Description:
HZTransferAttr Transfers the custom attributes
on a selected object to another selected object

General Description:
Transfers the custom attributes on a selected object to another
selected object including min/max ranges, the default value etc.
The current values of the attributes will also be tranfered.

How to Use:
1) select the object with the Attributes you want to transfer,
then the object you want the attributes transfered too.
2) run HZTransferAttr()

***********************************************'''
def HZTransferAttr():
	selectedObj=pm.ls(sl=1, head=2)
	userAttributes=pm.listAttr(selectedObj[0], userDefined=1)
	attribute = ""
	attrType = []
	attrRange = []
	attrMulti = 0
	attrListParent = []
	attrListDefault = []
	attrParam=""
	for attribute in userAttributes:
		attrParam=""
		if pm.attributeQuery(attribute, node=selectedObj[0], exists=1):
			attrType=pm.ls(((selectedObj[0] + "." + str(attribute))), showType=1)
		if pm.attributeQuery(attribute, node=selectedObj[0], rangeExists=1):
			attrRange=pm.attributeQuery(attribute, node=selectedObj[0], range=1)
			attrParam+=(" -min " + str(attrRange[0]) + " -max " + str(attrRange[1]))
		attrMulti=int(pm.attributeQuery(attribute, node=selectedObj[0], multi=1))
		if attrMulti: attrParam+=" -m"
		attrListParent=pm.attributeQuery(attribute, node=selectedObj[0], listParent=1)
		if attrListParent and len(attrListParent)>0:
			attrParam+=(" -p " + attrListParent[0])
		if attrType[1] == "string":
			attrParam=(("addAttr -ln " + str(attribute) + " -dt \"" + attrType[1] + "\"") + attrParam + (" -keyable true " + selectedObj[1] + ";\n"))
			pm.mel.eval(attrParam)
		elif attrType[1] == "enum":
			enum_string = pm.attributeQuery(attribute, node=selectedObj[0], listEnum=True)[0]
			pm.addAttr(selectedObj[1], longName=str(attribute), attributeType="enum", enumName=enum_string, keyable=True)
		else:
			attrListDefault=pm.attributeQuery(attribute, node=selectedObj[0], listDefault=1)
			if len(attrListDefault) == 1: attrParam+=(" -dv " + str(attrListDefault[0]))
			attrParam=(("addAttr -ln " + str(attribute) + " -at " + attrType[1]) + attrParam + (" -keyable true " + selectedObj[1] + ";\n"))
			pm.mel.eval(attrParam)
		
	for attribute in userAttributes:
		if pm.attributeQuery(attribute, node=selectedObj[0], exists=1):
			attrType=pm.ls(((selectedObj[0] + "." + str(attribute))), showType=1)
		if attrType[1] == "string":
			pm.setAttr((selectedObj[1] + "." + str(attribute)), (pm.getAttr(selectedObj[0] + "." + str(attribute))), type=attrType[1])
		elif attrType[1] == "double3":
			pass
		elif attrType[1] == "enum":
			pass
		else:
			pm.setAttr((selectedObj[1] + "." + str(attribute)), (pm.getAttr(selectedObj[0] + "." + str(attribute))))

HZTransferAttr()
