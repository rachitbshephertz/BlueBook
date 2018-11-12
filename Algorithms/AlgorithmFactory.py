from Algorithms import NaiveBayesGaussian as NB, NeuralNetwork as NW, LogisticsRegression as LR, SupportVectorMachine as SVM,\
    RandomForestClassifier as RF, NeuralNetwork as NN
from config import ConfigManager


class AlgorithmFactory(object):

    def __init__(self):
      pass

    def algorithm(self,algorithmSelect):
        if ConfigManager.algo_list.get(algorithmSelect) == 'LR':
            algoModelInstance = LR.LogisticsRegression()
        elif ConfigManager.algo_list.get(algorithmSelect) == 'NB':
            algoModelInstance = NB.NaiveBayesGaussian()
        elif ConfigManager.algo_list.get(algorithmSelect) == 'NN':
            algoModelInstance = NW.NeuralNetwork()
        elif ConfigManager.algo_list.get(algorithmSelect) == 'RF':
            algoModelInstance = RF.RandomForestClassifier()
        elif ConfigManager.algo_list.get(algorithmSelect) == 'SVM':
            algoModelInstance = SVM.SupportVectorMachine()
        elif ConfigManager.algo_list.get(algorithmSelect) == 'CNN':
            algoModelInstance = NN.NeuralNetwork()
        return algoModelInstance

