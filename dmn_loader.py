''' This is dataset loader file to load the bAbI dataset. '''
import re
import numpy as np
from glob import glob
from torch.utils.data import Dataloader
from torch.utils.data.dataset import Dataset
from torch.utils.data.dataloader import default_collate

class adict(dict):
	def __init__(self, *args, **kargs):
		dict.__init__(self, *args, **kargs)
		self.__dict__ = self

def pad_collate(batch):
	max_len_ques = float('-inf')
	max_sen_len_context = float('-inf')
	max_len_context = float('-inf')
	
	for item in batch:
		contexts, ques, _ = item
		if len(contexts) > max_len_context:
			max_len_context = len(contexts)
		if len(ques) > max_len_ques:
			max_len_ques = len(ques)
		for sen in contexts:
			if(len(sen) > max_sen_len_context):
				max_sen_len_context = len(sen)
	max_len_context = min(max_len_context, 70)
	for idx, item in enumerate(batch): # Going through each example in the batch which contains their ow context, question and answer.
		context_i, question, answer = item
		context_i = context[-max_len_context:] #???
		context = np.zeros((max_len_context, max_sen_len_context))
		for i, sen in enumerate(context_i): # going through ith context containing max_len_context sentences and a question
			context[i] = np.pad(sen, (0, max_sen_len_context-len(sen)), 'constant', constant_values=0)
		question = np.pad(question, (0, max_len_ques-len(question)), 'constant', constant_values=0)
		batch[idx] = (context, question, answer)
		
	return default_collate(batch)

class BabiDataSet(Dataset):
	def __init__(self, task_id, mode='train'):
		self.mode = mode
		self.vocab_path = 'dataset/babi{}_vocab.pkl'.format(task_id)
		train_data, test_data = get_train_test(task_id) # Get raw train_data and test_data from babi dataset
		self.QA = adict()
		self.QA.VOCAB = {'<PAD>': 0, '<EOS>':1}
		self.QA.INV_VOCAB = {0:'<PAD>', 1:'<EOS>'}
		self.train = self.get_processed_data(train_data)
		self.val = [self.train[i][int(9*len(self.train[i])/10:] for i in range(3)] # splitting into 90/10 train/val dataset
		self.train = [self.train[i][:int(9*len(self.train[i])/10] for i in range(3)] # splitting into 90/10 train/val dataset
		self.test = self.get_processed_data(test_data)
	
	def set_mode(self, mode):
		self.mode = mode #????
		
	def __len__(self):
		if self.mode == 'train':
			return len(self.train[0])
		elif self.mode == 'val':
			return len(self.val[0])
		elif self.mode == 'test':
			return len(self.test[0])
		else:
			print ("Invalid Mode!")
			return
	
	def __getdata__(self, index):
		if self.mode == 'train':
			contexts, questions, answers = self.train
		elif self.mode == 'val':
			contexts, questions, answers = self.val
		elif self.mode == 'test':
			contexts, questions, answers = self.test
		
		return contexts[index], questions[index], answers[index]
	
	def get_processed_data(self, raw_data):
		''' TO DO '''

	def build_vocab(self, token):
		''' TO DO '''
	
	
	
def get_train_test(task_id):
	paths = glob('data/en-10k/qa{}_*'.format(task_id))
	for path in paths:
		if 'train' in path;
			with open(path, 'r') as f:
				train = f.read()
		elif 'test' in path:
			with open(path, 'r') as f:
				test = f.read()
	
	return train, test
	
