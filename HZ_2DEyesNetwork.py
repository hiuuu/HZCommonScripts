import maya.cmds as cmds

grp = cmds.createNode('transform', name="customEyeControls_grp")

eyesLayeredShader = cmds.createNode('layeredShader', name='eyesLayeredShader#')
cmds.sets(renderable=True, empty=1, noSurfaceShader=True, name='%s2SG'%eyesLayeredShader)
cmds.connectAttr('%s.outColor'%eyesLayeredShader, '%s2SG.surfaceShader'%eyesLayeredShader, f=1)
cmds.setAttr("%s.inputs"%eyesLayeredShader, size=2)
cmds.setAttr("%s.inputs[0].color"%eyesLayeredShader, 1, 0, 0, type="float3")
cmds.setAttr("%s.inputs[0].transparency"%eyesLayeredShader, 1,1,1, type="float3")
cmds.setAttr("%s.inputs[1].color"%eyesLayeredShader, 1, 1, 1, type="float3")
cmds.setAttr("%s.inputs[1].transparency"%eyesLayeredShader, 0,0,0, type="float3")

eyeLayer_count = 6
eye_all_tex = cmds.createNode('layeredTexture', name="eyeAllLayeredTexture#")
cmds.setAttr("%s.inputs"%eye_all_tex, size=eyeLayer_count)
for lay in range(eyeLayer_count):
    cmds.setAttr("%s.inputs[%d].blendMode"%(eye_all_tex, eyeLayer_count), 1)
    cmds.setAttr("%s.inputs[%d].isVisible"%(eye_all_tex, eyeLayer_count), True)
cmds.setAttr("%s.inputs[0].color"%eye_all_tex, 0, 0, 1, type="float3")
cmds.setAttr("%s.inputs[1].color"%eye_all_tex, 1, 0, 0, type="float3")
cmds.removeMultiInstance("%s.inputs[6]"%eye_all_tex, b=True)

eyeBallColor = cmds.createNode('phong', name='eyesballMat#')
cmds.setAttr("%s.frozen"%eyeBallColor, 0)
cmds.setAttr("%s.refractionLimit"%eyeBallColor, 6)
cmds.setAttr("%s.refractiveIndex"%eyeBallColor, 1)
cmds.setAttr("%s.refractions"%eyeBallColor, 0)
cmds.setAttr("%s.diffuse"%eyeBallColor, 0.8000000119)
cmds.setAttr("%s.rayDirectionX"%eyeBallColor, 0)
cmds.setAttr("%s.rayDirectionY"%eyeBallColor, 0)
cmds.setAttr("%s.rayDirectionZ"%eyeBallColor, 1)
cmds.setAttr("%s.colorR"%eyeBallColor, 0.8974279761)
cmds.setAttr("%s.colorG"%eyeBallColor, 0.8974279761)
cmds.setAttr("%s.colorB"%eyeBallColor, 0.78204)
cmds.setAttr("%s.transparencyR"%eyeBallColor, 0)
cmds.setAttr("%s.transparencyG"%eyeBallColor, 0)
cmds.setAttr("%s.transparencyB"%eyeBallColor, 0)
cmds.setAttr("%s.ambientColorR"%eyeBallColor, 0)
cmds.setAttr("%s.ambientColorG"%eyeBallColor, 0)
cmds.setAttr("%s.ambientColorB"%eyeBallColor, 0)
cmds.setAttr("%s.incandescenceR"%eyeBallColor, 0)
cmds.setAttr("%s.incandescenceG"%eyeBallColor, 0)
cmds.setAttr("%s.incandescenceB"%eyeBallColor, 0)
cmds.setAttr("%s.translucence"%eyeBallColor, 0)
cmds.setAttr("%s.translucenceFocus"%eyeBallColor, 0.5)
cmds.setAttr("%s.translucenceDepth"%eyeBallColor, 0.5)
cmds.setAttr("%s.glowIntensity"%eyeBallColor, 0)
cmds.setAttr("%s.vrOverwriteDefaults"%eyeBallColor, 0)
cmds.setAttr("%s.vrFillObject"%eyeBallColor, 0)
cmds.setAttr("%s.vrEdgeWeight"%eyeBallColor, 0)
cmds.setAttr("%s.vrEdgeColorR"%eyeBallColor, 0.5)
cmds.setAttr("%s.vrEdgeColorG"%eyeBallColor, 0.5)
cmds.setAttr("%s.vrEdgeColorB"%eyeBallColor, 0.5)
cmds.setAttr("%s.vrEdgeStyle"%eyeBallColor, 0)
cmds.setAttr("%s.vrEdgePriority"%eyeBallColor, 0)
cmds.setAttr("%s.vrHiddenEdges"%eyeBallColor, 0)
cmds.setAttr("%s.vrHiddenEdgesOnTransparent"%eyeBallColor, 0)
cmds.setAttr("%s.vrOutlinesAtIntersections"%eyeBallColor, 1)
cmds.setAttr("%s.materialAlphaGain"%eyeBallColor, 1)
cmds.setAttr("%s.hideSource"%eyeBallColor, 0)
cmds.setAttr("%s.surfaceThickness"%eyeBallColor, 0)
cmds.setAttr("%s.shadowAttenuation"%eyeBallColor, 0.5)
cmds.setAttr("%s.lightAbsorbance"%eyeBallColor, 0)
cmds.setAttr("%s.chromaticAberration"%eyeBallColor, 0)
cmds.setAttr("%s.pointCameraX"%eyeBallColor, 1)
cmds.setAttr("%s.pointCameraY"%eyeBallColor, 1)
cmds.setAttr("%s.pointCameraZ"%eyeBallColor, 1)
cmds.setAttr("%s.normalCameraX"%eyeBallColor, 1)
cmds.setAttr("%s.normalCameraY"%eyeBallColor, 1)
cmds.setAttr("%s.normalCameraZ"%eyeBallColor, 1)
cmds.setAttr("%s.matteOpacityMode"%eyeBallColor, 2)
cmds.setAttr("%s.matteOpacity"%eyeBallColor, 1)
cmds.setAttr("%s.hardwareShaderR"%eyeBallColor, 0)
cmds.setAttr("%s.hardwareShaderG"%eyeBallColor, 0)
cmds.setAttr("%s.hardwareShaderB"%eyeBallColor, 0)
cmds.setAttr("%s.rsRefractionSamples"%eyeBallColor, 1)
cmds.setAttr("%s.reflectionLimit"%eyeBallColor, 1)
cmds.setAttr("%s.specularColorR"%eyeBallColor, 0.3675279915)
cmds.setAttr("%s.specularColorG"%eyeBallColor, 0.3675279915)
cmds.setAttr("%s.specularColorB"%eyeBallColor, 0.3675279915)
cmds.setAttr("%s.reflectivity"%eyeBallColor, 0.5)
cmds.setAttr("%s.reflectedColorR"%eyeBallColor, 0)
cmds.setAttr("%s.reflectedColorG"%eyeBallColor, 0)
cmds.setAttr("%s.reflectedColorB"%eyeBallColor, 0)
cmds.setAttr("%s.triangleNormalCameraX"%eyeBallColor, 0)
cmds.setAttr("%s.triangleNormalCameraY"%eyeBallColor, 1)
cmds.setAttr("%s.triangleNormalCameraZ"%eyeBallColor, 0)
cmds.setAttr("%s.reflectionSpecularity"%eyeBallColor, 1)
cmds.setAttr("%s.rsReflectionSamples"%eyeBallColor, 1)
cmds.setAttr("%s.cosinePower"%eyeBallColor, 65.65811157)

cmds.connectAttr("%s.outColor"%eye_all_tex, "%s.inputs[0].color"%eyesLayeredShader)
cmds.connectAttr("%s.outTransparency"%eye_all_tex, "%s.inputs[0].transparency"%eyesLayeredShader)
cmds.connectAttr("%s.outColor"%eyeBallColor, "%s.inputs[1].color"%eyesLayeredShader)
cmds.connectAttr("%s.outTransparency"%eyeBallColor, "%s.inputs[1].transparency"%eyesLayeredShader)
cmds.connectAttr("%s.outGlowColor"%eyeBallColor, "%s.inputs[1].glowColor"%eyesLayeredShader)

#######################
### Eyelashes Setup ###
#######################
posIndex = -1
for pos in "UD":
    posIndex += 1
    eyelash_ctl = cmds.createNode('transform', parent=grp, name="eyeLash_%s_ctl"%pos)
    cmds.addAttr(eyelash_ctl, longName="map", attributeType="enum", enumName="Straight:ArcUp:ArcDn", keyable=True)
    cmds.addAttr(eyelash_ctl, longName="shown", attributeType="bool", defaultValue="on", keyable=True)
    #cmds.connectAttr("%s.shown"%eyelash_ctl, "%s.inputs[%d].isVisible"%(eye_all_tex, posIndex))
    eyelash_prj = cmds.createNode('projection', name="eyelash_%s_projection#"%pos)
    cmds.setAttr("%s.defaultColor"%eyelash_prj, 0, 0, 0, type="float3")
    cmds.setAttr("%s.projType"%eyelash_prj, 1)
    cmds.connectAttr("%s.outTransparencyR"%eyelash_prj, "%s.inputs[%d].alpha"%(eye_all_tex, posIndex))
    eyelash_3dtex = cmds.createNode('place3dTexture',  parent=eyelash_ctl, name="eyeLash_%s_place3dTexture#"%pos)
    cmds.connectAttr("%s.worldInverseMatrix"%eyelash_3dtex, "%s.placementMatrix"%eyelash_prj)
    eyeLash_p2d = cmds.createNode('place2dTexture', name="eyeLash_%s_place2dTexture#"%pos)
    cmds.setAttr("%s.wrapU"%eyeLash_p2d, False)
    cmds.setAttr("%s.wrapV"%eyeLash_p2d, False)
    cmds.setAttr("%s.coverageU"%eyeLash_p2d, 10)
    cmds.setAttr("%s.coverageV"%eyeLash_p2d, 10)
    cmds.setAttr("%s.translateFrameU"%eyeLash_p2d, -4.5)
    cmds.setAttr("%s.translateFrameV"%eyeLash_p2d, -3.5)
    eyeLash_ramp = cmds.createNode('ramp', name="eyeLash_%s_ramp#"%pos)
    cmds.setAttr("%s.defaultColor"%eyeLash_ramp, 1, 1, 1, type="float3")
    cmds.setAttr("%s.type"%eyeLash_ramp, 4)
    cmds.setAttr("%s.interpolation"%eyeLash_ramp, 0)
    cmds.setAttr("%s.invert"%eyeLash_ramp, 0)
    cmds.setAttr("%s.colorEntryList"%eyeLash_ramp, size=2)
    cmds.setAttr("%s.colorEntryList[0].position"%eyeLash_ramp, 0)
    cmds.setAttr("%s.colorEntryList[0].color"%eyeLash_ramp, 1, 1, 1, type="float3")
    cmds.setAttr("%s.colorEntryList[1].position"%eyeLash_ramp, 0.5)
    cmds.setAttr("%s.colorEntryList[1].color"%eyeLash_ramp, 0, 0, 0, type="float3") 
    cmds.connectAttr("%s.outColor"%eyeLash_ramp, "%s.transparency"%eyelash_prj)
    cmds.connectAttr("%s.outUV"%eyeLash_p2d, "%s.uvCoord"%eyeLash_ramp)
    cmds.connectAttr("%s.outUvFilterSize"%eyeLash_p2d, "%s.uvFilterSize"%eyeLash_ramp)
    cmds.setDrivenKeyframe("%s.invert"%eyeLash_ramp, cd="%s.map"%eyelash_ctl, itt='linear', ott='step', dv=0, v=1 )
    cmds.setDrivenKeyframe("%s.type"%eyeLash_ramp, cd="%s.map"%eyelash_ctl, itt='linear', ott='step', dv=0, v=5 )
    cmds.setDrivenKeyframe("%s.type"%eyeLash_ramp, cd="%s.map"%eyelash_ctl, itt='linear', ott='step', dv=1, v=4 )
    cmds.setDrivenKeyframe("%s.type"%eyeLash_ramp, cd="%s.map"%eyelash_ctl, itt='linear', ott='step', dv=2, v=4 )
    if (posIndex == 0):   # up eyelash
        cmds.setDrivenKeyframe("%s.invert"%eyeLash_ramp, cd="%s.map"%eyelash_ctl, itt='linear', ott='step', dv=1, v=1 )
        cmds.setDrivenKeyframe("%s.invert"%eyeLash_ramp, cd="%s.map"%eyelash_ctl, itt='linear', ott='step', dv=2, v=0 )
        cmds.setDrivenKeyframe("%s.offsetV"%eyeLash_p2d, cd="%s.map"%eyelash_ctl, itt='linear', ott='step', dv=0, v=-0.70 )
        cmds.setDrivenKeyframe("%s.offsetV"%eyeLash_p2d, cd="%s.map"%eyelash_ctl, itt='linear', ott='step', dv=1, v=0.40 )
        cmds.setDrivenKeyframe("%s.offsetV"%eyeLash_p2d, cd="%s.map"%eyelash_ctl, itt='linear', ott='step', dv=2, v=1.72 )
    elif (posIndex == 1):  # dn eyelash
        cmds.setDrivenKeyframe("%s.invert"%eyeLash_ramp, cd="%s.map"%eyelash_ctl, itt='linear', ott='step', dv=1, v=0 )
        cmds.setDrivenKeyframe("%s.invert"%eyeLash_ramp, cd="%s.map"%eyelash_ctl, itt='linear', ott='step', dv=2, v=1 )
        cmds.setDrivenKeyframe("%s.offsetV"%eyeLash_p2d, cd="%s.map"%eyelash_ctl, itt='linear', ott='step', dv=0, v=1.90 )
        cmds.setDrivenKeyframe("%s.offsetV"%eyeLash_p2d, cd="%s.map"%eyelash_ctl, itt='linear', ott='step', dv=1, v=2.50 )
        cmds.setDrivenKeyframe("%s.offsetV"%eyeLash_p2d, cd="%s.map"%eyelash_ctl, itt='linear', ott='step', dv=2, v=1.82 )

eyesValsU = [0.0,0.125,0.25,0.375,0.5,0.625,0.75,0.875] # 8x8 houses each 1024x1024 pixels
eyesValsV = [0.0,0.125,0.25,0.375,0.5,0.625,0.75,0.875]
sideIndex = 1
for side in "RL":
    sideIndex += 1
    specA_ctl = cmds.createNode('transform', parent=grp, name="specA_%s_ctl"%side)
    cmds.addAttr(specA_ctl, longName="shown", attributeType="double", minValue=0, maxValue=1, defaultValue=1, keyable=True)
    specB_ctl = cmds.createNode('transform', parent=grp, name="specB_%s_ctl"%side)
    cmds.addAttr(specB_ctl, longName="shown", attributeType="double", minValue=0, maxValue=1, defaultValue=1, keyable=True)
    eye_ctl = cmds.createNode('transform', parent=grp, name="eye_%s_ctl"%side)
    cmds.addAttr(eye_ctl, longName="map", attributeType="enum", 
                enumName="eyeDefault:eyeClosedBig:eyeClosedMid:eyeClosedSmall:eyeHappyBig:eyeHappyMid:" 
                + "eyeHappySmall:eyeMountUp:eyeMountDn:eyeStraight:eyeBlink:eyeCross:eyeSpiral:eyeHeart", keyable=True)
    
    ##############################
    ### 2D eyes Textures Setup ###
    ##############################
    eye2D_col_prj = cmds.createNode('projection', name="eye2D_col_%s_projection#"%side)
    cmds.setAttr("%s.defaultColor"%eye2D_col_prj, 0, 0, 0, type="float3")
    cmds.setAttr("%s.projType"%eye2D_col_prj, 1)
    cmds.connectAttr("%s.outColor"%eye2D_col_prj, "%s.inputs[%d].color"%(eye_all_tex, sideIndex))
    cmds.connectAttr("%s.outTransparencyR"%eye2D_col_prj, "%s.inputs[%d].alpha"%(eye_all_tex, sideIndex))
    eye2D_col_tex = cmds.createNode('place3dTexture',  parent=eye_ctl, name="eye2D_col_%s_place3dTexture#"%side)
    cmds.connectAttr("%s.worldInverseMatrix"%eye2D_col_tex, "%s.placementMatrix"%eye2D_col_prj)
    eye2D_col_col = cmds.createNode('file', name="eye2D_col_%s_file#"%side)
    cmds.setAttr("%s.defaultColor"%eye2D_col_col, 0, 0, 0, type="float3")
    cmds.setAttr("%s.fileTextureName"%eye2D_col_col, "H:/OURWORK/BAD_CARS/ASSETS/CHR/COMMON/SHA/eyeExpressions_col_v004.png", type="string")
    eye2D_col_msk = cmds.createNode('file', name="eye2D_msk_%s_file#"%side)
    cmds.setAttr("%s.defaultColor"%eye2D_col_msk, 0, 0, 0, type="float3")
    cmds.setAttr("%s.fileTextureName"%eye2D_col_msk, "H:/OURWORK/BAD_CARS/ASSETS/CHR/COMMON/SHA/eyeExpressions_msk_v004.png", type="string")
    eye2D_col_p2d = cmds.createNode('place2dTexture', name="eye2D_col_%s_place2dTexture#"%side)
    cmds.setAttr("%s.wrapU"%eye2D_col_p2d, False)
    cmds.setAttr("%s.wrapV"%eye2D_col_p2d, False)
    cmds.setAttr("%s.repeatUV"%eye2D_col_p2d, 0.125, 0.125, type="float2")
    cmds.connectAttr("%s.outColor"%eye2D_col_col, "%s.image"%eye2D_col_prj)
    cmds.connectAttr("%s.outColor"%eye2D_col_msk, "%s.transparency"%eye2D_col_prj)
    for fiNode in [eye2D_col_col, eye2D_col_msk]:
        cmds.connectAttr("%s.c"%eye2D_col_p2d, "%s.c"%fiNode)
        cmds.connectAttr("%s.tf"%eye2D_col_p2d, "%s.tf"%fiNode)
        cmds.connectAttr("%s.rf"%eye2D_col_p2d, "%s.rf"%fiNode)
        cmds.connectAttr("%s.mu"%eye2D_col_p2d, "%s.mu"%fiNode)
        cmds.connectAttr("%s.mv"%eye2D_col_p2d, "%s.mv"%fiNode)
        cmds.connectAttr("%s.s"%eye2D_col_p2d, "%s.s"%fiNode)
        cmds.connectAttr("%s.wu"%eye2D_col_p2d, "%s.wu"%fiNode)
        cmds.connectAttr("%s.wv"%eye2D_col_p2d, "%s.wv"%fiNode)
        cmds.connectAttr("%s.re"%eye2D_col_p2d, "%s.re"%fiNode)
        cmds.connectAttr("%s.of"%eye2D_col_p2d, "%s.of"%fiNode)
        cmds.connectAttr("%s.r"%eye2D_col_p2d, "%s.ro"%fiNode)
        cmds.connectAttr("%s.n"%eye2D_col_p2d, "%s.n"%fiNode)
        cmds.connectAttr("%s.vt1"%eye2D_col_p2d, "%s.vt1"%fiNode)
        cmds.connectAttr("%s.vt2"%eye2D_col_p2d, "%s.vt2"%fiNode)
        cmds.connectAttr("%s.vt3"%eye2D_col_p2d, "%s.vt3"%fiNode)
        cmds.connectAttr("%s.vc1"%eye2D_col_p2d, "%s.vc1"%fiNode)
        cmds.connectAttr("%s.o"%eye2D_col_p2d, "%s.uv"%fiNode)
        cmds.connectAttr("%s.ofs"%eye2D_col_p2d, "%s.fs"%fiNode)
    i,j,k = (0,0,len(eyesValsU))
    for valV in eyesValsV:
        for valU in eyesValsU:
            cmds.setDrivenKeyframe( '%s.offsetU'%eye2D_col_p2d,cd='%s.map'%eye_ctl,itt='linear',ott='step', dv=(i), v=(valU) )
            cmds.setDrivenKeyframe( '%s.offsetV'%eye2D_col_p2d,cd='%s.map'%eye_ctl,itt='linear',ott='step', dv=(j*k), v=(valV) )
            i += 1
        j += 1
    cmds.setAttr("%s.visibility"%eye2D_col_tex, 0)
    if side == "L":
        cmds.setAttr("%s.sx"%eye2D_col_tex, -1)

    #########################################
    ### 2D eyes Popil and Speculars Setup ###
    #########################################
    eye3DShown_cond = cmds.createNode('condition', name="eye3D_shown_%s_condition#"%side)
    cmds.setAttr("%s.operation"%eye3DShown_cond, 1)  # op => not equals
    cmds.setAttr("%s.secondTerm"%eye3DShown_cond, 0)  
    cmds.setAttr("%s.colorIfTrueR"%eye3DShown_cond, 0)  
    cmds.setAttr("%s.colorIfFalseR"%eye3DShown_cond, 1)  
    cmds.connectAttr("%s.outColorR"%eye3DShown_cond, "%s.inputs[%d].isVisible"%(eye_all_tex, sideIndex+2))
    cmds.connectAttr("%s.map"%eye_ctl, "%s.firstTerm"%eye3DShown_cond)
    eye3D_col_tex = cmds.createNode('layeredTexture', name="eye3D_col_%s_layeredTexture#"%side)
    cmds.setAttr("%s.inputs"%eye3D_col_tex, size=3)
    cmds.setAttr("%s.inputs[0].blendMode"%eye3D_col_tex, 1)
    cmds.setAttr("%s.inputs[0].isVisible"%eye3D_col_tex, True)
    cmds.setAttr("%s.inputs[1].blendMode"%eye3D_col_tex, 1)
    cmds.setAttr("%s.inputs[1].isVisible"%eye3D_col_tex, True)
    cmds.setAttr("%s.inputs[2].blendMode"%eye3D_col_tex, 1)
    cmds.setAttr("%s.inputs[2].isVisible"%eye3D_col_tex, True)
    cmds.connectAttr("%s.outColor"%eye3D_col_tex, "%s.inputs[%d].color"%(eye_all_tex, sideIndex+2))
    cmds.connectAttr("%s.outAlpha"%eye3D_col_tex, "%s.inputs[%d].alpha"%(eye_all_tex, sideIndex+2))
    secIndex = -1
    for sec in ['specA', 'sepcB', 'popil']:
        secIndex += 1
        sec_prj = cmds.createNode('projection', name="%s_%s_projection#"%(sec, side))
        cmds.setAttr("%s.defaultColor"%sec_prj, 0, 0, 0, type="float3")
        cmds.setAttr("%s.projType"%sec_prj, 1)
        cmds.connectAttr("%s.outColor"%sec_prj, "%s.inputs[%d].color"%(eye3D_col_tex, secIndex))
        cmds.connectAttr("%s.outTransparencyR"%sec_prj, "%s.inputs[%d].alpha"%(eye3D_col_tex, secIndex))    
        sec_tex = cmds.createNode('place3dTexture', name="%s_%s_place3dTexture#"%(sec, side))
        cmds.connectAttr("%s.worldInverseMatrix"%sec_tex, "%s.placementMatrix"%sec_prj)
        sec_p2d = cmds.createNode('place2dTexture', name="%s_%s_place2dTexture#"%(sec, side))
        cmds.setAttr("%s.wrapU"%sec_p2d, False)
        cmds.setAttr("%s.wrapV"%sec_p2d, False) 
        sec_ramp = cmds.createNode('ramp', name="%s_%s_ramp#"%(sec, side))
        cmds.setAttr("%s.defaultColor"%sec_ramp, 0, 0, 0, type="float3")
        cmds.setAttr("%s.type"%sec_ramp, 4)
        cmds.setAttr("%s.interpolation"%sec_ramp, 0)
        cmds.setAttr("%s.invert"%sec_ramp, 0)
        cmds.setAttr("%s.colorEntryList"%sec_ramp, size=2)
        cmds.setAttr("%s.colorEntryList[0].position"%sec_ramp, 0)
        cmds.setAttr("%s.colorEntryList[0].color"%sec_ramp, 1, 1, 1, type="float3")
        cmds.setAttr("%s.colorEntryList[1].color"%sec_ramp, 0, 0, 0, type="float3") 
        cmds.connectAttr("%s.outColor"%sec_ramp, "%s.transparency"%sec_prj)
        cmds.connectAttr("%s.outUV"%sec_p2d, "%s.uvCoord"%sec_ramp)
        cmds.connectAttr("%s.outUvFilterSize"%sec_p2d, "%s.uvFilterSize"%sec_ramp)
        cmds.setAttr("%s.visibility"%sec_tex, 0)
        if secIndex == 0 :  #"specA":
            cmds.setAttr("%s.invert"%sec_prj, 1)
            cmds.setAttr("%s.colorEntryList[1].position"%sec_ramp, 0.2)
            cmds.connectAttr("%s.shown"%specA_ctl, "%s.cgr"%sec_prj)
            cmds.connectAttr("%s.shown"%specA_ctl, "%s.cgg"%sec_prj)
            cmds.connectAttr("%s.shown"%specA_ctl, "%s.cgb"%sec_prj) 
            cmds.parent( sec_tex, specA_ctl )          
            cmds.parent( specA_ctl, eye_ctl )          
        elif secIndex == 1 :  #"specB":
            cmds.setAttr("%s.invert"%sec_prj, 1)
            cmds.setAttr("%s.colorEntryList[1].position"%sec_ramp, 0.17)
            cmds.connectAttr("%s.shown"%specB_ctl, "%s.cgr"%sec_prj)
            cmds.connectAttr("%s.shown"%specB_ctl, "%s.cgg"%sec_prj)
            cmds.connectAttr("%s.shown"%specB_ctl, "%s.cgb"%sec_prj)
            cmds.parent( sec_tex, specB_ctl )
            cmds.parent( specB_ctl, eye_ctl )
        elif secIndex == 2 :  #"popil":
            cmds.setAttr("%s.colorEntryList[1].position"%sec_ramp, 0.7) 
            cmds.setAttr("%s.translateFrame"%sec_p2d, 0.15, 0, type="float2")
            cmds.setAttr("%s.coverage"%sec_p2d,  0.75, 1, type="float2")
            cmds.parent( sec_tex, eye_ctl )


pp_geo,_  = cmds.polyPlane(cuv=2, sy=3, sx=3, h=8, ch=1, w=8, ax=(0, 1, 0))
cmds.setAttr("%s.rotateX"%pp_geo, 90)
cmds.sets(forceElement='%s2SG'%eyesLayeredShader, e=1)
cmds.move( -1.5, 0, 0, grp+'|eye_R_ctl', r=1, os=1, wd=1)
cmds.move( 1.5, 0, 0, grp+'|eye_L_ctl', r=1, os=1, wd=1)
cmds.group(grp, pp_geo)