'''
HZAnimUtils.py



'''

import maya.cmds as mc
import maya.mel as mel
import math

__author__ = "Hamed Zandieh"
__copyright__ = "Copyright 2019, Hamed Zandieh"
__credits__ = ["Hamed Zandieh"]
__license__ = "PD"
__version__ = "0.0.1"
__maintainer__ = "Hamed Zandieh"
__email__ = "hamed.zandieh@gmail.com"
__status__ = "Production"


class Overlap(object):

    def __init__(self):
        self.Utils = Utils()
        self._pfx = 'HZOverlap'
        self.showUI()

    def showUI(self):
        pass

    def run(self, prefix=''):
        # must select last child first in order
        ctrls = mc.ls(orderedSelection=True)

        mc.undoInfo(openChunk=True)

        poses = []
        for lc in ctrls:
            poses.append(self.Utils.getWorldPos(lc))
        posLen = len(poses) + 1
        reversePoses = poses[::-1]
        reversePoses.append(poses[0])  # last joint added for correct oriient
        mc.select(clear=1)

        if not prefix:
            prefix = str(ctrls[0])
            prefix += "__HZ_"

        # create joints on poses
        joints = []
        joints_offGrp = ''
        if posLen > 2:
            # for lc in reversePoses:
            for x in range(0, posLen):
                jName = "%s_%d_joint" % (prefix, (x + 1))
                mc.joint(p=(reversePoses[x]), n=jName)
                joints.append(jName)
            mc.joint(joints[0], e=True, zso=True, oj="xyz", sao='yup', ch=1)
            lastjoitnTX = mc.getAttr("%s.tx" % joints[-2])
            # divide by 1 can be 2 or 4 depend on how much effect needed on last ctrl
            mc.setAttr("%s.tx" % joints[-1], lastjoitnTX / 1)
            reversePoses[-1] = self.Utils.getWorldPos(joints[-1])
            poses.insert(0, reversePoses[-1])
            mc.joint(joints[0], e=True, zso=True, oj="xyz", sao='yup', ch=1)
            mc.setAttr("%s.jointOrientX" % joints[-1], 0)
            mc.setAttr("%s.jointOrientY" % joints[-1], 0)
            mc.setAttr("%s.jointOrientZ" % joints[-1], 0)
            joints_offGrp = self.Utils.makeOffsetGrp(joints[0])
        mc.select(clear=1)

        nucleus = self.getActiveNucleus()
        if not nucleus:
            nucleus = self.createNucleus(
                name="%s_nucleus#" % prefix, setActive=1)
            mc.setAttr("%s.startFrame" % nucleus, 1)
            mc.setAttr("%s.frameJumpLimit" % nucleus, 1)
            mc.setAttr("%s.gravity" % nucleus, 0)  # defualt is 9.8
            mc.setAttr("%s.gravityDirectionY" % nucleus, 0)  # defualt is -1

        if posLen > 2:
            # use hair dynamics
            ikcurve = mc.curve(name="%s_ikcurve" % prefix, d=1, p=reversePoses)
            mc.rebuildCurve(ikcurve, rt=0, d=4, ch=1, rpo=1,
                            end=1, kep=1, kr=2, kcp=0, kt=0, tol=1e-008, s=0)

            mc.select(ikcurve, r=1)
            mel.eval("""makeCurvesDynamic 2 { "0", "0", "0", "1", "0"};""")
            allCurves = mc.ls("curve*", et="transform")
            lastCreatedCurve = allCurves[-1]
            ikDynCurve = mc.rename(lastCreatedCurve, prefix + '_curveDynamic#')
            dynCurveParent = mc.listRelatives(ikDynCurve, parent=True)
            lastHairSystem = mc.ls("hairSystem*", et="transform")
            lastCreatedHs = lastHairSystem[-3]
            firstHs = mc.rename(lastCreatedHs, prefix + '_HairSystem#')
            allFolli = mc.ls('follicle*', et='transform')
            # lenFolli = len(allFolli)
            lastFolli = allFolli[-1]  # mc.ls(allFolli[lenFolli-1])
            folName = mc.rename(lastFolli, prefix + '_follicle#')
            folParent = mc.listRelatives(folName, parent=True)
            mc.setAttr('%s.pointLock' % folName, 1)
            mc.parentConstraint(ctrls[-1], folName, mo=1)

            hairShape = mc.listRelatives(firstHs, s=True)[0]
            stiffness = 1
            curveAttract = 0.5
            mass = 1
            damp = 0.01
            friction = 0.5
            mc.setAttr(
                ('%s.stiffnessScale[0].stiffnessScale_FloatValue' % hairShape), stiffness)
            mc.setAttr(
                ('%s.stiffnessScale[1].stiffnessScale_FloatValue' % hairShape), stiffness / 2)
            mc.setAttr(('%s.startCurveAttract' % hairShape), curveAttract)
            mc.setAttr(('%s.mass' % hairShape), mass)
            mc.setAttr(('%s.damp' % hairShape), damp)
            mc.setAttr(('%s.attractionDamp' % hairShape), damp)
            mc.setAttr(('%s.friction' % hairShape), friction)
            # if make it on the curve has quick jumps
            mc.setAttr(('%s.noStretch' % hairShape), 0)

            ikhandle = mc.ikHandle(
                n="%s_ikHandle#" % prefix, sj=joints[0], ee=joints[-1], sol="ikSplineSolver", ccv=False, pcv=False, c=ikDynCurve)[0]

            mc.select(cl=1)
            alldynGrp = mc.group(name="%s_allDyn_grp" % prefix, em=1)
            mc.parent(nucleus, dynCurveParent, firstHs,
                      folParent, ikhandle, alldynGrp)

            #self.bakesimul(joints, ["rx", "ry", "rz"])
            #mc.delete(alldynGrp)
            #jlen = len(joints) - 1
            #for j in range(0, jlen):
            #    self.copyKeyframes(joints[j], [ctrls[jlen - j - 1]], attrList=["rx", "ry", "rz"])
            #mc.delete(joints_offGrp)

        else:
            # use particle dynamics
            lastChLoc = mc.spaceLocator()[0]
            lastChLocGoal = mc.spaceLocator()[0]
            mc.parentConstraint(ctrls[0], lastChLocGoal)

            particle = mc.nParticle(p=[poses[0]], c=1)
            particleShape = mc.listRelatives(particle, s=True)[0]
            mc.setAttr("%s.particleRenderType" % particleShape, 3)
            mc.connectAttr("%s.worldCentroid" %
                           particleShape, "%s.translate" % lastChLoc)
            mc.goal(particle, g=lastChLocGoal, w=0.5, utr=0)
            mc.setAttr("%s.goalWeight[0]" % particleShape, 0.5)
            mc.setAttr("%s.damp" % particleShape, 0.01)
            mc.setAttr("%s.friction" % particleShape, 0.5)

            mc.select(cl=1)
            alldynGrp = mc.group(name="%s_allDyn_grp" % prefix, em=1)
            mc.parent(nucleus, lastChLocGoal, particle, alldynGrp)

            self.bakesimul(lastChLoc, ["tx", "ty", "tz"])
            mc.delete(alldynGrp)
            self.copyKeyframes(lastChLoc, [ctrls[0]], attrList=[
                               "tx", "ty", "tz"])
            mc.delete(lastChLoc)

        mc.undoInfo(closeChunk=True)

    def bakesimul(self, objs, attrList, frameRange=(1, 120)):
        mc.bakeResults(objs, t=frameRange, sampleBy=1, simulation=True,
                       at=attrList, shape=False, minimizeRotation=True, disableImplicitControl=True)
        for o in objs:
            for attr in attrList:
                mc.filterCurve(["%s.%s" % (o, attr)], startTime=frameRange[0],
                               endTime=frameRange[1], f='simplify', timeTolerance=0.05, tolerance=0.01)
                # mc.filterCurve(["%s.%s" % (o, attr)],
                #               startTime=frameRange[0], endTime=frameRange[1], f='euler')
            mc.keyTangent(o, edit=True, t=frameRange, at=attrList,
                          inTangentType='spline', outTangentType='spline')

    def createNucleus(self, name='', setActive=True):
        if not name:
            name = 'nucleus#'
        nucleus = mc.createNode('nucleus', n=name)
        mc.connectAttr('time1.outTime', nucleus + '.currentTime')
        if setActive:
            self.setActiveNucleus(nucleus)
        return nucleus

    def getActiveNucleus(self):
        nucleus = mel.eval('getActiveNucleusNode(true,false)')
        return nucleus

    def setActiveNucleus(self, nucleus):
        if not self.Utils.isNType(nucleus, 'nucleus'):
            raise Exception('Object "' + nucleus +
                            '" is not a valid nucleus node!')
        mel.eval('source getActiveNucleusNode')
        mel.eval('setActiveNucleusNode("' + nucleus + '")')

    def getAnimationData(self, objs):
        obj = objs[0]
        animAttributes = mc.listAnimatable(obj)
        for attribute in animAttributes:
            numKeyframes = mc.keyframe(
                attribute, query=True, keyframeCount=True)
            if (numKeyframes > 0):
                print("---------------------------")
                print("Found ", numKeyframes, " keyframes on ", attribute)

                times = mc.keyframe(attribute, query=True, index=(
                    0, numKeyframes), timeChange=True)
                values = mc.keyframe(attribute, query=True, index=(
                    0, numKeyframes), valueChange=True)

                print('frame#, time, value')
                for i in range(0, numKeyframes):
                    print(i, times[i], values[i])

                print("---------------------------")

    def makeAnimLayer(self, layerName):
        baseAnimationLayer = mc.animLayer(query=True, root=True)
        foundLayer = False
        if (baseAnimationLayer is not None):
            childLayers = mc.animLayer(
                baseAnimationLayer, query=True, children=True)

            if (childLayers is not None) and (len(childLayers) > 0):
                if layerName in childLayers:
                    foundLayer = True
        if not foundLayer:
            mc.animLayer(layerName)
        else:
            print('Layer ' + layerName + ' already exists'),

    '''
    def copyKeyframes(self, objs):
        if (len(objs) < 0):
            mc.error('two object at least requared'),
        sourceObj = objs[0]
        animAttributes = mc.listAnimatable(sourceObj)
        for attribute in animAttributes:
            numKeyframes = mc.keyframe(
                attribute, query=True, keyframeCount=True)
            if (numKeyframes > 0):
                mc.copyKey(attribute)
            for obj in objs[1:]:
                mc.pasteKey(obj, attribute=self.getAttName(
                    attribute), option="replace")
                # mc.pasteKey(obj, attribute=self.getAttName(attribute), option="replace", animLayer="extraAnimation")
    '''

    def copyKeyframes(self, sourceObj, targetObjs,
                      attrList=["tx", "ty", "tz", "rx", "ry", "rz"],
                      frameRange=(1, 120),
                      mirror=False):
        # nowTime = mc.currentTime(q=1)
        if len(attrList) == 0:
            attrList = map(lambda x: x.split(
                '.')[-1], mc.listAnimatable(sourceObj))
        for attr in attrList:
            lenkf = mc.keyframe("%s.%s" % (sourceObj, attr),
                                query=1, keyframeCount=1)
            if (lenkf > 0):
                mc.copyKey(sourceObj, at=attr, time=(
                    frameRange[0], frameRange[1]))
                firstKeyVal = mc.keyframe("%s.%s" % (
                    sourceObj, attr), q=True, valueChange=True, time=(frameRange[0], frameRange[0]))[0]
                for trg in targetObjs:
                    if not mc.getAttr("%s.%s" % (trg, attr), lock=True):
                        mc.pasteKey(trg, at=attr, option="replace", valueOffset=(
                            -1 * firstKeyVal), time=(frameRange[0], frameRange[1]))
                        if mirror:
                            mc.scaleKey(trg, at=attr, valueScale=-1,
                                        time=(frameRange[0], frameRange[1]))


class Utils(object):
    def __init__(self):
        pass

    def getObjectAttributeFromFull(self, fullString):
        parts = fullString.split("|")
        return parts[-1]

    def makeOffsetGrp(self, object, name="", prefix="", orient=False, scale=False):
        if name:
            offsetGrp = mc.group(n=name, em=1)
        else:
            if not prefix:
                prefix = self.removeSuffix(object)
            offsetGrp = mc.group(n=prefix + "_Offgrp", em=1)
        objectParents = mc.listRelatives(object, p=1)
        if objectParents:
            mc.parent(offsetGrp, objectParents[0])
        mc.delete(mc.pointConstraint(object, offsetGrp))
        if orient:
            mc.delete(mc.orientConstraint(object, offsetGrp))
        if scale:
            mc.delete(mc.scaleConstraint(object, offsetGrp))
        mc.parent(object, offsetGrp)
        return offsetGrp

    def removeSuffix(self, name):
        edits = name.split("_")
        if len(edits) < 2:
            return name
        suffix = "_" + edits[-1]
        nameNoSuffix = name[: -len(suffix)]
        return nameNoSuffix

    def snap(self, object, parentObj, t=True, o=False, s=False):
        mc.delete(mc.pointConstraint(parentObj, object))
        if o:
            mc.delete(mc.orientConstraint(parentObj, object))
        if s:
            mc.delete(mc.scaleConstraint(parentObj, object))
        mc.makeIdentity(object, apply=True, translate=t, rotate=o, scale=s)

    def mag(self, v=[]):
        return math.sqrt(pow(v[0], 2) + pow(v[1], 2) + pow(v[2], 2))

    def centerPivot(self, objs):
        # bbox = mc.exactWorldBoundingBox(obj)
        # bottom = [(bbox[0] + bbox[3])/2, bbox[1], (bbox[2] + bbox[5])/2]
        # mc.xform(obj, piv=bottom, ws=True)
        mc.select(clear=True)
        if not isinstance(objs, list):
            objs = [objs]
        for o in objs:
            mc.select(o, add=True)
        mel.eval("CenterPivot;")
        mc.select(clear=True)

    def searchReplace(self, objList, serch, repl):
        for each in objList:
            newname = str(each).replace(serch, repl)
            each.rename(newname)

    def midpoint(self, p1, p2):
        return tuple(
            [((p1[0] + p2[0]) / 2), ((p1[1] + p2[1]) / 2), ((p1[2] + p2[2]) / 2)]
        )

    def makeGuideLine(self, obj1, obj2):
        obj1Pos = self.getWorldPos(obj1)
        obj2Pos = self.getWorldPos(obj2)
        crv = mc.curve(n=("%s_Guideline_curve" % obj1),
                       d=1, p=[obj1Pos, obj2Pos])
        clust1 = mc.cluster("%s.cv[0]" % crv, n=(
            "%s_GuidelineHandle" % obj1))[1]  # handle
        mc.pointConstraint(obj1, clust1)
        clust2 = mc.cluster("%s.cv[1]" % crv, n=(
            "%s_GuidelineHandle" % obj2))[1]
        mc.pointConstraint(obj2, clust2)
        mc.setAttr("%s.v" % clust1, 0, lock=1)
        mc.setAttr("%s.v" % clust2, 0, lock=1)
        mc.setAttr("%s.overrideEnabled" % crv, 1)
        mc.setAttr("%s.overrideDisplayType" % crv, 1)
        mc.setAttr("%s.overrideColor" % crv, 2)
        mc.setAttr("%s.inheritsTransform" % crv, 0)
        mc.connectAttr("%s.v" % obj1, "%s.v" % crv)
        grp = mc.group(crv, clust1, clust2, n=("%s_Guideline_grp" % obj1))
        return grp

    def getWorldPos(self, obj):
        objLoc = mc.spaceLocator()[0]
        mc.delete(mc.pointConstraint(obj, objLoc))
        X, Y, Z = mc.xform(objLoc, ws=1, q=1, rp=1)
        mc.delete(objLoc)
        return tuple([X, Y, Z])

    def getWorldRot(self, obj):
        X, Y, Z = mc.xform(obj, q=1, ws=1, ro=1)
        euX = (math.sin(X) + math.sin(Z)) - \
            (math.cos(X) + math.sin(Y) + math.cos(Z))
        euY = (math.sin(X) + math.cos(Y)) - \
            (math.cos(X) + math.sin(Y) + math.sin(Z))
        euZ = (-1 * math.cos(X)) + math.cos(Y)
        return tuple([euX, euY, euZ])

    def getBoundingBox(self, obj):
        bb = mc.xform(obj, q=1, bb=1)
        bbx = bb[3] - bb[0]
        bby = bb[4] - bb[1]
        bbz = bb[5] - bb[2]
        return tuple([bbx, bby, bbz])

    def isNType(self, nNode, nType):
        '''
        Check if the specified object is a nucleus compatible nDynamics node
        '''
        # Check object exists
        if not mc.objExists(nNode):
            return False
        # Check shape
        if mc.objectType(nNode) == 'transform':
            nNode = mc.listRelatives(nNode, s=True, ni=True, pa=True)[0]
        if mc.objectType(nNode) != nType:
            return False

        # Return result
        return True
