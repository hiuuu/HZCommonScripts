'''
//==============================================//
//                 H.Z.                         //
//             Lips rhuarb                      //
//                                              //
//       	 version 0.5                        //
//                                              //
//////////////////////////////////////////////////
prepare:
run this command on wav file:

E:\_DOWNLOADS_\rhubarb-lip-sync-1.10.0-win32\rhubarb.exe  "H:\mywork\2D_BilMangam\Episodes\Voice\SedaShahed_GH27_00;54.wav" -f dat --datFrameRate 25 --extendedShapes X -r phonetic -o "H:\mywork\2D_BilMangam\Episodes\Voice\SedaShahed_GH27_00;54.rhubarb.dat"


USAGE:

import HZ_lips_rhubarb as hzlips
reload(hzlips)
hzlips.HZ_lips_UI()
'''
import maya.cmds as cmds
import maya.mel as mel

'''
class HZ_lips_rhubarb(object):
  _instance = None

  def __init__(self):
      # do some configuration things
      # maybe load config from a file
      # or maybe load config from environment variables
      self.context = {}
      self.config = {}

  @classmethod 
'''  

def load_file( filePth, fileType = 'dat' ):
  global HZ_lips_rhubarb__data__
  cmds.textScrollList(HZ_lips_rhubarb_dataviewField, edit=True, removeAll=1 )
  if not filePth: return []
  HZ_lips_rhubarb__data__ = [line.strip().split() for line in open(filePth, 'r')]
  HZ_lips_rhubarb__data__.pop(0)
  if not HZ_lips_rhubarb__data__:
    cmds.textField(HZ_lips_rhubarb_filePathField, backgroundColor=(.8,0,0), edit=True, tx="Error in reading file!" )
  else:
    cmds.textField(HZ_lips_rhubarb_filePathField, edit=True, backgroundColor=(0,.6,0), fi=filePth )
    cmds.textScrollList(HZ_lips_rhubarb_dataviewField, edit=True, append=(map(str, HZ_lips_rhubarb__data__)) )
  #print('\n'.join(map(str, HZ_lips_rhubarb__data__)))
  return True

def phon_type_changed(methd):
  HZ_lips_rhubarb__phon_type_selector__ = methd
  #print "Current selection:", HZ_lips_rhubarb__phon_type_selector__

def setkey_phon(*_):
  frameRange = getSliderRange()
  offset = int(cmds.intField(HZ_lips_rhubarb_offsetField, query=True, value=True ))
  voiceoffset = int(cmds.intField(HZ_lips_rhubarb_voiceoffsetField, query=True, value=True ))

  if not HZ_lips_rhubarb__data__: 
    print("no Data Error"),
    return []
  if not HZ_lips_rhubarb__node__: 
    print("no node selected Error"),
    return

  result = {
    0: func_map_bilman, # result = func_map_bilman(data)
    1: func_map_advsklton,   # result = func_map_advsklton(data)
    2: func_map_cdkface,    # result = func_map_cdkface(data)
  }.get(HZ_lips_rhubarb__phon_type_selector__)(HZ_lips_rhubarb__node__, HZ_lips_rhubarb__data__, frameRange, offset, voiceoffset)
  return result

def func_map_bilman(node, data, frameRange, offset = 0, voiceoffset = 0):
  lips_itt = 'linear'
  lips_ott = 'step'
  start = int(frameRange[0]) 
  end = int(frameRange[1]) 

  #print('\n'.join(map(str, data)))
  #print ("func_map_bilman begin: " + str(len(data)))
  #print ('\n'.join(map(str, frameRange)))

  #cmds.progressBar( prgsBarField, edit=True, beginProgress=True, isInterruptable=True, status='Setting Keys ...', maxValue= len(data) )

  cmds.setKeyframe( node, at='mode', v=0, t=offset+start-1, itt=lips_itt, ott=lips_ott )
  cmds.setKeyframe( node, at='scaleY', v=1, t=offset+start-1, itt=lips_itt, ott=lips_ott ) 
  
  for dataItem in data:
    if len(dataItem) != 2: continue

    phon = dataItem[1].capitalize()
    frm = int(dataItem[0]) + voiceoffset

    if (start > frm or frm > end): 
      # print ("bypass " + str(frm))
      continue
    
    #if cmds.progressBar(prgsBarField, query=True, isCancelled=True ) : break
    #cmds.progressBar(prgsBarField, edit=True, step=1)    
    
    '''
    result = {
      'A': lambda n,f,i,o: cmds.setKeyframe( n, at='mode', v=0, t=f, itt=i, ott=o )
      'B': lambda n,f,i,o: cmds.setKeyframe( n, at='mode', v=0, t=f, itt=i, ott=o )
      'C': lambda n,f,i,o: cmds.setKeyframe( n, at='mode', v=4, t=f, itt=i, ott=o )
      'D': lambda n,f,i,o: cmds.setKeyframe( n, at='mode', v=4, t=f, itt=i, ott=o )
      'E': lambda n,f,i,o: cmds.setKeyframe( n, at='mode', v=3, t=f, itt=i, ott=o )
      'F': lambda n,f,i,o: cmds.setKeyframe( n, at='mode', v=3, t=f, itt=i, ott=o )
      'G': lambda n,f,i,o: cmds.setKeyframe( n, at='mode', v=0, t=f, itt=i, ott=o )
      'H': lambda n,f,i,o: cmds.setKeyframe( n, at='mode', v=4, t=f, itt=i, ott=o )
      'X': lambda n,f,i,o: cmds.setKeyframe( n, at='mode', v=0, t=f, itt=i, ott=o )
    }.get(phon)(node,frm,lips_itt,lips_ott)
    '''
    if phon == 'A':
      cmds.setKeyframe( node, at='mode', v=1, t=offset+frm, itt=lips_itt, ott=lips_ott )
      cmds.setKeyframe( node, at='scaleY', v=1, t=offset+frm, itt=lips_itt, ott=lips_ott )
    elif phon == 'B':
      cmds.setKeyframe( node, at='mode', v=4, t=offset+frm, itt=lips_itt, ott=lips_ott )
      cmds.setKeyframe( node, at='scaleY', v=0.7, t=offset+frm, itt=lips_itt, ott=lips_ott )
    elif phon == 'C':
      cmds.setKeyframe( node, at='mode', v=4, t=offset+frm, itt=lips_itt, ott=lips_ott )
      cmds.setKeyframe( node, at='scaleY', v=1.2, t=offset+frm, itt=lips_itt, ott=lips_ott )
    elif phon == 'D':
      cmds.setKeyframe( node, at='mode', v=4, t=offset+frm, itt=lips_itt, ott=lips_ott )
      cmds.setKeyframe( node, at='scaleY', v=2, t=offset+frm, itt=lips_itt, ott=lips_ott )
    elif phon == 'E':
      cmds.setKeyframe( node, at='mode', v=3, t=offset+frm, itt=lips_itt, ott=lips_ott )
      cmds.setKeyframe( node, at='scaleY', v=1.4, t=offset+frm, itt=lips_itt, ott=lips_ott )
    elif phon == 'F':
      cmds.setKeyframe( node, at='mode', v=3, t=offset+frm, itt=lips_itt, ott=lips_ott )
      cmds.setKeyframe( node, at='scaleY', v=0.7, t=offset+frm, itt=lips_itt, ott=lips_ott )
    elif phon == 'G':
      cmds.setKeyframe( node, at='mode', v=1, t=offset+frm, itt=lips_itt, ott=lips_ott )
      cmds.setKeyframe( node, at='scaleY', v=1, t=offset+frm, itt=lips_itt, ott=lips_ott )
    elif phon == 'H':
      cmds.setKeyframe( node, at='mode', v=4, t=offset+frm, itt=lips_itt, ott=lips_ott )
      cmds.setKeyframe( node, at='scaleY', v=1, t=offset+frm, itt=lips_itt, ott=lips_ott )
    else: # X
      cmds.setKeyframe( node, at='mode', v=0, t=offset+frm, itt=lips_itt, ott=lips_ott )
      cmds.setKeyframe( node, at='scaleY', v=1, t=offset+frm, itt=lips_itt, ott=lips_ott )  
      
  cmds.setKeyframe( node, at='mode', v=0, t=offset+end+1, itt=lips_itt, ott=lips_ott )
  cmds.setKeyframe( node, at='scaleY', v=1, t=offset+end+1, itt=lips_itt, ott=lips_ott ) 
  
  #cmds.progressBar(prgsBarField, edit=True, endProgress=True)
  return True

def func_map_advsklton(data):
  return True
  
 
def func_map_cdkface(data):
  return True

def HZ_lips_UI():
  global HZ_lips_rhubarb_filePathField
  global HZ_lips_rhubarb_rangBeginField
  global HZ_lips_rhubarb_rangEndField
  global HZ_lips_rhubarb_offsetField
  global HZ_lips_rhubarb_dataviewField
  global HZ_lips_rhubarb_nodeField
  global HZ_lips_rhubarb_voiceoffsetField
  global HZ_lips_rhubarb__phon_type_selector__
  global HZ_lips_rhubarb__data__
  global HZ_lips_rhubarb__node__
  
  HZ_lips_rhubarb__phon_type_selector__ = 0
  HZ_lips_rhubarb__data__ = []
  HZ_lips_rhubarb__node__ = '' 

  #check to see if window exists   
  if cmds.window ("HZLipsUI", exists = True):
    cmds.deleteUI("HZLipsUI")
    
  window = cmds.window( "HZLipsUI", title='H.Z. Lips Rhubarb',widthHeight=(500.0, 320.0))
  #cmds.frameLayout( label="windowTitle", cl=True )
  form = cmds.formLayout(numberOfDivisions=100)
  
  # Creating Element load
  object = cmds.button( label="Load rhubarb 'dat' File...", w=168, h=34, command = lambda _: load_file(cmds.fileDialog( dm='*.dat' )))
  cmds.formLayout( form, edit=True, attachForm=[( object, 'top', 41), ( object, 'left', 171)] )
  #=========================================
  # Creating Element set_Key
  object = cmds.button( label="< SET KEY >", backgroundColor=(.2,.3,.4), w=323, h=34, command = setkey_phon)
  cmds.formLayout( form, edit=True, attachForm=[( object, 'top', 252), ( object, 'left', 9)] )
  #=========================================
  # Creating Element from
  object = cmds.text( label="Frame Range", w=88, h=34)
  cmds.formLayout( form, edit=True, attachForm=[( object, 'top', 129), ( object, 'left', 12)] )
  #=========================================
  # Creating Element offset
  object = cmds.text( label="Frame Offset", w=88, h=34)
  cmds.formLayout( form, edit=True, attachForm=[( object, 'top', 212), ( object, 'left', 12)] )
  #=========================================  
  # Creating Element voiceoffset
  object = cmds.text( label="Voice Offset", w=88, h=34)
  cmds.formLayout( form, edit=True, attachForm=[( object, 'top', 212), ( object, 'left', 182)] )
  #=========================================    
  # Creating Element to
  object = cmds.text( label="To", w=48, h=34)
  cmds.formLayout( form, edit=True, attachForm=[( object, 'top', 129), ( object, 'left', 170)] )  
  #=========================================
  # Creating Element dataview
  HZ_lips_rhubarb_dataviewField = cmds.textScrollList( w=147, h=277)
  cmds.formLayout( form, edit=True, attachForm=[( HZ_lips_rhubarb_dataviewField, 'top', 2), ( HZ_lips_rhubarb_dataviewField, 'left', 348)] )
  #=========================================
  # Creating Element totxt
  HZ_lips_rhubarb_rangEndField = cmds.intField( w=68, h=34, value=0)
  cmds.formLayout( form, edit=True, attachForm=[( HZ_lips_rhubarb_rangEndField, 'top', 128), ( HZ_lips_rhubarb_rangEndField, 'left', 220)] )
  #=========================================
  # Creating Element prgsbar
  #prgsBarField = cmds.progressBar( w=335, h=34)
  #cmds.formLayout( form, edit=True, attachForm=[( prgsBarField, 'top', 252), ( prgsBarField, 'left', 4)] )
  #=========================================
  # Creating Element methid
  object = cmds.radioButtonGrp( labelArray3=["bilmangam", "advskeleton", "cdkface"], numberOfRadioButtons = 3,
                                          columnWidth1 = (120), columnWidth2 = [120, 120], columnWidth3= [120, 120, 120], columnWidth4 = [75, 75, 75, 75],
                                          w=327, h=36, sl=1,
                                          onCommand1 = lambda _: phon_type_changed(0),
                                          onCommand2 = lambda _: phon_type_changed(1),
                                          onCommand3 = lambda _: phon_type_changed(2)
                                        )
  cmds.formLayout( form, edit=True, attachForm=[( object, 'top', 87), ( object, 'left', 11)] )
  HZ_lips_rhubarb__phon_type_selector__ = 0
  #=========================================
  # Creating Element Load_file
  HZ_lips_rhubarb_filePathField = cmds.textField( backgroundColor=(0.25,0.25,0.25), text="No Data File Loaded!", ed=0, w=331, h=34)
  cmds.formLayout( form, edit=True, attachForm=[( HZ_lips_rhubarb_filePathField, 'top', 3), ( HZ_lips_rhubarb_filePathField, 'left', 7)] )
  #=========================================
  # Creating Element fromtxt
  HZ_lips_rhubarb_rangBeginField = cmds.intField( w=68, h=34, v=0)
  cmds.formLayout( form, edit=True, attachForm=[( HZ_lips_rhubarb_rangBeginField, 'top', 128), ( HZ_lips_rhubarb_rangBeginField, 'left', 105)] )
  #=========================================
  # Creating Element ofsettxt
  HZ_lips_rhubarb_offsetField = cmds.intField( w=68, h=34, v=0)
  cmds.formLayout( form, edit=True, attachForm=[( HZ_lips_rhubarb_offsetField, 'top', 212), ( HZ_lips_rhubarb_offsetField, 'left', 105)] )
  #=========================================  
  # Creating Element voiceofsettxt
  HZ_lips_rhubarb_voiceoffsetField = cmds.intField( w=68, h=34, v=0)
  cmds.formLayout( form, edit=True, attachForm=[( HZ_lips_rhubarb_voiceoffsetField, 'top', 212), ( HZ_lips_rhubarb_voiceoffsetField, 'left', 268)] )
  #=========================================   
  # Creating Element nodetxt
  HZ_lips_rhubarb_nodeField = cmds.textField( w=248, h=34, text='', ed=False)
  cmds.formLayout( form, edit=True, attachForm=[( HZ_lips_rhubarb_nodeField, 'top', 170), ( HZ_lips_rhubarb_nodeField, 'left', 12)] )
  #=========================================
   # Creating Element select_node
  object = cmds.button( label="<<< Node", w=68, h=34, command = select_node)
  cmds.formLayout( form, edit=True, attachForm=[( object, 'top', 170), ( object, 'left', 268)] )
  #=========================================
 
  cmds.setParent( '..' )
  cmds.setParent( '..' )
  cmds.showWindow( window )    
      
    
def select_node(*_):
  global HZ_lips_rhubarb__node__
  selected = cmds.ls( selection=True )
  HZ_lips_rhubarb__node__ = str(selected[0])
  cmds.textField(HZ_lips_rhubarb_nodeField, edit=True, backgroundColor=(0,.6,0), tx= HZ_lips_rhubarb__node__ )
    
def close_window(*_):
  cmds.deleteUI("HZLipsUI")                          # deletes the window above


def getSliderRange(*_):
  fromfield = int(cmds.intField(HZ_lips_rhubarb_rangBeginField, query=True, value=True ))
  tofield = int(cmds.intField(HZ_lips_rhubarb_rangEndField,  query=True, value=True ))
  gPlaybackSlider = mel.eval("global string $gPlayBackSlider; $gPlayBackSlider = $gPlayBackSlider;")
  if tofield > 0:
    return [fromfield, tofield]  
  elif cmds.timeControl(gPlaybackSlider, query=True, rangeVisible=True):
    highlightedRange = cmds.timeControl(gPlaybackSlider, query=True, rangeArray=True)
    highlightedRange[-1] -= (1)
    return highlightedRange
  else:
    start = cmds.playbackOptions( q=True,min=True )
    end  = cmds.playbackOptions( q=True,max=True )
    return [start, end]
  