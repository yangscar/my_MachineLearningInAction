__author__ = 'neuralyang'
import matplotlib.pyplot as plt

decisionNode = dict(boxstyle="sawtooth", fc="0.8")
leafNode = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")


def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    createPlot.ax1.annotate(nodeTxt, xy=parentPt,
                            xycoords='axes fraction',
                            xytext=centerPt, textcoords='axes fraction',
                            va='center', ha='center', bbox=nodeType, arrowprops=arrow_args)


def plotMidText(childPt, parentPt, txtString):
    xMid = (parentPt[0]-childPt[0])/2.0 + childPt[0]
    yMid = (parentPt[1]-childPt[1])/2.0 + childPt[1]
    createPlot.ax1.text(xMid, yMid, txtString)


def plotTree(myTree, parentPt, nodeTxt):
    n_leafs = getNumLeafs(myTree)
    n_depth = getTreeDepth(myTree)
    root = myTree.keys()[0]
    kidPt = (plotTree.xOff + (1.0 + float(n_leafs))/ 2.0/ plotTree.totalW, plotTree.yOff)
    plotMidText(kidPt, parentPt, nodeTxt)
    plotNode(root, kidPt, parentPt, decisionNode)
    kids = myTree[root]
    plotTree.yOff -= 1.0/plotTree.totalD
    for key in kids.keys():
        print kids[key], plotTree.xOff, plotTree.yOff
        if type(kids[key]).__name__ == 'dict':
            plotTree(kids[key], kidPt, str(key))

        else:
            plotTree.xOff = plotTree.xOff + 1.0/ plotTree.totalW
            plotNode(kids[key], (plotTree.xOff, plotTree.yOff), kidPt, leafNode)
            plotMidText((plotTree.xOff, plotTree.yOff), kidPt, str(key))
    plotTree.yOff = plotTree.yOff + 1.0/plotTree.totalD



def getNumLeafs(myTree):
    n_leafs = 0
    root = myTree.keys()[0]
    kid = myTree[root]
    for key in kid.keys():
        if type(kid[key]).__name__ == 'dict':
            n_leafs += getNumLeafs(kid[key])
        else:
            n_leafs += 1
    return n_leafs


def getTreeDepth(myTree):
    max_depth = 0
    root = myTree.keys()[0]
    kid = myTree[root]
    for key in kid.keys():
        if type(kid[key]).__name__ == 'dict':
            this_depth = 1 + getTreeDepth(kid[key])
        else:
            this_depth = 1
        if this_depth > max_depth: max_depth = this_depth
    return max_depth


def createPlot(inTree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks = [], yticks= [])
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)
    plotTree.totalW = float(getNumLeafs(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))
    plotTree.xOff = -0.5/plotTree.totalW
    plotTree.yOff = 1.0
    plotTree(inTree, (0.5, 1) , '')
    #plotNode('a decision node', (.5, .1), (.1, .5), decisionNode)
    #plotNode('a leaf node', (.8, .1), (.3, .8), leafNode)
    plt.show()


def retrieveTree(i):
    listOfTrees = [{'no surfacing': {0: 'no', 1: {'flippers': \
                                                      {0: 'no', 1: 'yes'}}}},
                   {'no surfacing': {0: 'no', 1: {'flippers': \
                                                      {0: {'head': {0: 'no', 1: 'yes'}}, 1: 'no'}}}}
    ]
    return listOfTrees[i]