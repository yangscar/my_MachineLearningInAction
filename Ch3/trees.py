__author__ = 'neuralyang'

from math import log
import operator
import treePlotter


def calcShannonEnt(dataSet):
    n_entries = len(dataSet)
    label_counts = {}
    for vec in dataSet:
        cur_label = vec[-1]
        label_counts[cur_label] = label_counts.get(cur_label, 0) + 1
        # if cur_label not in label_counts.keys():
    shannonEnt = 0.0
    for key in label_counts:
        p = float(label_counts[key]) / n_entries
        shannonEnt -= p * log(p, 2)
    return shannonEnt


def createDataSet():
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]

    labels = ['no surfacing', 'flippers']
    return dataSet, labels


def splitDataSet(dataSet, axis, value):
    split_data = []
    for vec in dataSet:
        if vec[axis] == value:
            reduced_vec = vec[:axis]
            reduced_vec.extend(vec[axis + 1:])
            split_data.append(reduced_vec)
    return split_data


def chooseBestFeatureToSplit(dataSet):
    n_features = len(dataSet[0]) - 1
    base_entropy = calcShannonEnt(dataSet)  # origin entropy
    best_info_gain = 0.0
    best_feature = -1
    for i in range(n_features):
        feature_list = [example[i] for example in dataSet]
        unique_values = set(feature_list)
        new_entropy = 0.0
        for value in unique_values:
            subset = splitDataSet(dataSet, i, value)
            p = float(len(subset)) / len(dataSet)
            new_entropy += p * calcShannonEnt(subset)
        info_gain = base_entropy - new_entropy
        if info_gain > best_info_gain:
            best_info_gain = info_gain
            best_feature = i
    return best_feature


def majorityClass(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys(): classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(),
                              key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


def createTree(dataSet, labels):
    import copy
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    if len(dataSet[0]) == 1:  # remain only one feature
        return majorityClass(classList)  # determine by vote
    best_feature = chooseBestFeatureToSplit(dataSet)
    best_feature_label = labels[best_feature]
    my_tree = {best_feature_label: {}}
    del(labels[best_feature])
    feature_values = [example[best_feature] for example in dataSet]
    unique_values = set(feature_values)
    for value in unique_values:
        sub_labels = labels[:]
        my_tree[best_feature_label][value] = createTree(splitDataSet(dataSet, best_feature, value),
                                                        sub_labels)
    return my_tree

def classify(inputTree, featLabels, testVec):
    firstStr = inputTree.keys()[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    for key in secondDict.keys():
        if testVec[featIndex] == key:
            if type(secondDict[key]).__name__ == 'dict':
                classLabel = classify(secondDict[key], featLabels, testVec)
            else: classLabel = secondDict[key]
    return classLabel

def storeTree(inputTree, filename):
    import pickle
    fw = open(filename, 'w')
    pickle.dump(inputTree, fw)
    fw.close()

def grabTree(filename):
    import pickle
    fr = open(filename)
    return pickle.load(fr)




if __name__ == '__main__':
    my_data, my_labels = createDataSet()
    print my_data
    my_tree = createTree(my_data, my_labels)
    print my_tree
    my_tree['no surfacing'][3]='maybe'
    #my_tree = treePlotter.retrieveTree(0)
    #treePlotter.createPlot(my_tree)
    myDat, labels = createDataSet()
    #my_tree2 = treePlotter.retrieveTree(0)
    #classify(my_tree2, labels, [1, 0])
    print(classify(my_tree, labels, [3, 0]))