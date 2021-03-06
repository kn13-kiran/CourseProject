from abc import ABCMeta
import metapy

class MenuClassifier(object):
	__metaclass__ = ABCMeta

	def __init__(self, configFile):
		self.invertedIndex = metapy.index.make_inverted_index(configFile)
		self.fwdIndex = metapy.index.make_forward_index(configFile)

		# Define multi class data set
		self.multiClassDataset = metapy.classify.MulticlassDataset(self.fwdIndex)
		self.classifier = metapy.classify.NaiveBayes(self.multiClassDataset, alpha=0.01, beta=0.01)

	def score(self, link_text, page_title, body_text):
		doc = metapy.index.Document()
		doc.content(link_text + page_title + body_text)
		docvec = self.fwdIndex.tokenize(doc)
		label = self.classifier.classify(docvec)
		if label == "MenuPage":
			return 1.0
		else:
			return 0.
