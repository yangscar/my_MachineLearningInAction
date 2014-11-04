__author__ = 'neuralyang'
from numpy import *
import os
import operator


def createDataSet():
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels


def classify0(inX, dataSet, labels, k):
    m = dataSet.shape[0]
    diff_mat = tile(inX, (m, 1)) - dataSet
    sq_diff_mat = diff_mat ** 2
    sq_distances = sq_diff_mat.sum(axis=1)
    distances = sq_distances ** 0.5
    sortedDistIndices = distances.argsort()
    classCount = {}
    for i in range(k):
        label = labels[sortedDistIndices[i]]
        classCount[label] = classCount.get(label, 0) + 1
    sortedClassCount = sorted(classCount.iteritems(),
                              key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


def file2matrix(filename):
    f = open(filename)
    arrayOLines = f.readlines()
    n_lines = len(arrayOLines)
    returnMat = zeros((n_lines, 3))
    classLabels = []
    idx = 0
    i_label = 0
    label_map = {}
    for line in arrayOLines:
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[idx, :] = listFromLine[0:3]
        if not label_map.get(listFromLine[-1]):
            label_map[listFromLine[-1]] = i_label
            i_label += 1
        classLabels.append(label_map[listFromLine[-1]])
        idx += 1
    return returnMat, classLabels


def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals, (m, 1))
    normDataSet = normDataSet / tile(ranges, (m, 1))
    return normDataSet, ranges, minVals


def datingClassTest():
    hoRatio = 0.2
    datingDataMat, datingLabels = file2matrix('datingTestSet.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    n_test_vectors = int(m * hoRatio)
    error_count = 0
    for i in range(n_test_vectors):
        classifier_result = classify0(normMat[i, :], normMat[n_test_vectors:m, :], \
                                      datingLabels[n_test_vectors:m], 3)
        print "the classifier came back with: %d, the real answer is: %d" \
              % (classifier_result, datingLabels[i])
        if classifier_result != datingLabels[i]:
            error_count += 1
    print "the total error rate is: %.8f" % (float(error_count) / n_test_vectors)


def classifyPerson():
    result_list = ['not at all', 'in small doses', 'in large doses']
    percent_time_play = float(raw_input( \
        "percentage of time spent playing video games?"))
    frequent_flier = float(raw_input("frequent flier miles earned per year?"))
    ice_cream = float(raw_input("liters of ice cream consumed per year?"))
    datingDataMat, datingLabels = file2matrix('datingTestSet.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    input_arr = array([frequent_flier, percent_time_play, ice_cream])
    classfier_result = classify0((input_arr - minVals)/ ranges, normMat, datingLabels, 3)
    print "You will probably like this person: ", result_list[classfier_result-1]


def img2vector(filename):
    vec = zeros((1, 32**2))
    fr = open(filename)
    for i in range(32):
        line_str = fr.readline()
        for j in range(32):
            vec[0,32*i+j] = int(line_str[j])
    return vec


def handwritingClassTest():
    # train data
    hw_labels = []
    trainingFileList = os.listdir("trainingDigits")
    m = len(trainingFileList)
    training_mat = zeros((m,1024))
    for i in range(m):
        file_name = trainingFileList[i]
        class_num = int(file_name.split('.')[0].split('_')[0])
        hw_labels.append(class_num)
        training_mat[i, :] = img2vector('trainingDigits/%s'% file_name)
    # test data
    testFileList = os.listdir('testDigits')
    error_count = 0
    m_test = len(testFileList)
    for i in range(m_test):
        file_name = testFileList[i]
        class_num = int(file_name.split('.')[0].split('_')[0])
        vector2test = img2vector('testDigits/%s' % file_name)
        class_res = classify0(vector2test, training_mat, hw_labels, 5)
        print "the classifier came back with: %d, the real answer is: %d"\
                % (class_res, class_num)
        if class_res != class_num: error_count+=1
    print "\n the total number of errors is %d" % error_count
    print "\n the total error rate is: %f" % (float(error_count)/m_test)




if __name__ == "__main__":
    group, labels = createDataSet()
    print classify0([0, 0], group, labels, 3)
    datingDataMat, datingLabels = file2matrix('datingTestSet.txt')
    print datingLabels[0:20]

    import matplotlib
    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(datingDataMat[:, 1], datingDataMat[:, 2],
               15.0 * array(datingLabels), array(datingLabels))
    #plt.show()
    #datingClassTest()
    #classifyPerson()
    #test_vec = img2vector('testDigits/0_13.txt')
    #print test_vec[0,0:31]

    handwritingClassTest()