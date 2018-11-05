#!/usr/bin/python2

from __future__ import division

import sys
import string
import math

def RemovePunctuation( word ):
    return word.translate(None, string.punctuation).translate(None, string.digits).lower()

def CalculateFeatures( InputFile, OutFile, Vocab ):
	Features = []
	with open( InputFile, 'r' ) as inFile:
		for line in inFile:
			global MatrixPreTrain
			global MatrixPreTest
			global TotalRecordsTrain
			global TotalRecordsTest
			global TotalBadTrain
			global TotalGoodTrain

			lines = line.split('\t')
			classifier = int(lines[1].replace('\n', '').replace(' ', ''))

			FeaturesVector = [0] * (len(Vocab) + 1)
			FeaturesVector[len(Vocab)] = classifier

			for word in lines[0].split():
				cleanWord = RemovePunctuation(word)
				index = Vocab.index(cleanWord) if cleanWord in Vocab else None
				if index != None:
					FeaturesVector[index] = 1

			Features.append(FeaturesVector)

			if ( InputFile == "trainingSet.txt" ):
				TotalRecordsTrain += 1
				MatrixPreTrain.append(FeaturesVector)
				if ( classifier == 0 ):
					TotalBadTrain += 1
				elif ( classifier == 1 ):
					TotalGoodTrain += 1
			elif ( InputFile == "testSet.txt" ):
				TotalRecordsTest += 1
				MatrixPreTest.append(FeaturesVector)

			open( OutFile, 'a' ).write("%s\n" % (','.join(map(str,FeaturesVector))))
	
	return Features

def PredictClassifier( Features, Vocab, ProbabilityValues ):
	Predictions = []
	
	for feature in Features:
		Predicts = [0, 0]
		Index = 0
		for value in feature:
			if ( Index != len(Vocab) ):
				if ( value == 1 ):
					Predicts[0] += ProbabilityValues[Index][0]
					Predicts[1] += ProbabilityValues[Index][2]
				elif ( value == 0 ):
					Predicts[0] += ProbabilityValues[Index][1]
					Predicts[1] += ProbabilityValues[Index][3]
			Index += 1
		if ( Predicts[0] > Predicts[1] ):
			Predictions.append(1)
		else:
			Predictions.append(0)
	return Predictions

def CalculateAccuracy( Features, Predictions, Total ):
	Index = 0
	Correct = 0
	for feature in Features:
		classifier = feature[len(feature) - 1]
		if ( Predictions[Index] == classifier ):
			Correct += 1
		Index += 1
	return (Correct / Total) * 100.0
					

if ( __name__ == "__main__" ):
	MatrixPreTrain = []
	MatrixPreTest = []
	TotalRecordsTrain = 0
	TotalRecordsTest = 0
	TotalBadTrain = 0
	TotalGoodTrain = 0

	PreprocessedTrain = "preprocessed_train.txt"
	PreprocessedTest = "preprocessed_test.txt"
	
	open( PreprocessedTrain, 'w' ).close()
	open( PreprocessedTest, 'w' ).close()

	Vocab = []
	with open("trainingSet.txt", 'r') as inFile:
		for line in inFile:
			for word in line.split():
				cleanWord = RemovePunctuation(word).lower()
				if cleanWord not in Vocab:
					Vocab.append(cleanWord)

	Vocab.sort()
	Vocab.append("classlabel")

	open( PreprocessedTrain, 'a' ).write("%s\n" % ','.join(Vocab))
	open( PreprocessedTest, 'a' ).write("%s\n" % ','.join(Vocab))

	TrainingFeatures = CalculateFeatures( "trainingSet.txt", PreprocessedTrain, Vocab)
	TrainBadLog = math.log(TotalBadTrain / TotalRecordsTrain)
	TrainGoodLog = math.log(TotalGoodTrain / TotalRecordsTrain)

	TestingFeatures = CalculateFeatures( "testSet.txt", PreprocessedTest, Vocab)

	ProbabilityValues = [([0] * 4) for x in xrange(len(Vocab))]
	IndexWord = 0

	for word in Vocab:
		for row in MatrixPreTrain:
			val = row[IndexWord]
			classifier = row[len(Vocab)]
			
			if ( val == 0 ):
				if ( classifier == 0 ):
					ProbabilityValues[IndexWord][3] += 1
				elif ( classifier == 1 ):
					ProbabilityValues[IndexWord][1] += 1
			elif( val == 1 ):
				if ( classifier == 0 ):
					ProbabilityValues[IndexWord][2] += 1
				elif ( classifier == 1 ):
					ProbabilityValues[IndexWord][0] += 1

		ProbabilityValues[IndexWord][0] = math.log((ProbabilityValues[IndexWord][0] + 1) / (TotalGoodTrain + 2))
		ProbabilityValues[IndexWord][1] = math.log((ProbabilityValues[IndexWord][1] + 1) / (TotalGoodTrain + 2))
		ProbabilityValues[IndexWord][2] = math.log((ProbabilityValues[IndexWord][2] + 1) / (TotalBadTrain + 2))
		ProbabilityValues[IndexWord][3] = math.log((ProbabilityValues[IndexWord][3] + 1) / (TotalBadTrain + 2))
		IndexWord += 1

	TrainPredictions = PredictClassifier( MatrixPreTrain, Vocab, ProbabilityValues )
	TestPredictions = PredictClassifier( MatrixPreTest, Vocab, ProbabilityValues )
	TrainingAccuracy = CalculateAccuracy( MatrixPreTrain, TrainPredictions, TotalRecordsTrain )
	TestingAccuracy = CalculateAccuracy( MatrixPreTest, TestPredictions, TotalRecordsTest )

	print "Training Accuracy\t= %f" % TrainingAccuracy
	print "Testing Accuracy\t= %f" % TestingAccuracy

	Results = open( "results.txt", 'w' )
	Results.write( "Training Accuracy\t= %f\n" % TrainingAccuracy )
	Results.write( "Testing Accuracy\t= %f\n" % TestingAccuracy )
	Results.close()
