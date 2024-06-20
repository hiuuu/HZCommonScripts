import maya.cmds as cmds


def printAttributes(node, like=''):
    ''' Convinience function to print all the attributes of the given node.
        :param: node - Name of the Maya object.
        :param: like - Optional parameter to print only the attributes that have this
                       string in their nice names.
    '''
    heading = 'Node: %s' % node

    print()
    print('*' * (len(heading)+6))
    print('** %s **' % heading)
    print('*' * (len(heading)+6))
    attributes = cmds.listAttr(node)
    for attribute in attributes:
        attribute = attribute.split('.')[-1]
        longName = cmds.attributeQuery(attribute, node=node, longName=True)
        shortName = cmds.attributeQuery(attribute, node=node, shortName=True)
        niceName = cmds.attributeQuery(attribute, node=node, niceName=True)
        if like and (like.lower() not in shortName.lower()): continue
        heading = '\nAttribute: %s' % attribute
        print (heading)
        print ('-' * len(heading))
        print ('Long name: %s\nShort name: %s\nNice name: %s\n' % (longName, shortName, niceName))


printAttributes(cmds.ls(sl=True,head=1)[0], "bm")