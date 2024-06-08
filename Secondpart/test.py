import torch
import torch.nn as nn
import torchvision
from torch.utils.data import DataLoader
import torch.optim as optim
from torch.optim import lr_scheduler
import torchvision.models as models

import argparse
import os
import cv2
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score
from sklearn import metrics
import numpy as np

from dataloader import get_loader
from mymodel import AdvancedTwoLayerCNN , AdvancedTwoLayerCNN_Atte, AdvancedTwoLayerCNN_NoAll, AdvancedTwoLayerCNN_RRDB

# frame-level 
def main():
		args = parse.parse_args()
		batch_size = args.batch_size
		model_path = args.model_path
		device = args.device
		torch.backends.cudnn.benchmark=True

		train_data, val_data, test_data, train_loader, val_loader, test_loader = get_loader(args)
		test_dataset_size = len(test_data)
		corrects = 0
		acc = 0

		model = eval(args.model)
		model.load_state_dict(torch.load(model_path))
		if isinstance(model, torch.nn.DataParallel):
			model = model.module
		model = model.to(device)
		model.eval()

		pred_labels = []
		target_labels = []
		probability = []
		with torch.no_grad():
			for item in test_loader:
				image, labels = item['image'].to(device), item['label'].to(device)
				outputs = model(image)

				_, preds = torch.max(outputs.data, 1)
				corrects += torch.sum(preds == labels.data).to(torch.float32)
				# print('Iteration Acc {:.4f}'.format(torch.sum(preds == labels.data).to(torch.float32)/batch_size))

				pred_labels.extend(preds.detach().cpu().numpy())
				target_labels.extend(labels.detach().cpu().numpy())

			acc = corrects / test_dataset_size
			preds_arr=np.array(pred_labels)
			labs_arr= np.array(target_labels)    
			# accs = accuracy_score(labs_arr, preds_arr)
			f1 = f1_score(labs_arr, preds_arr, average='macro')
			re = recall_score(labs_arr, preds_arr, average='macro')
			pr = precision_score(labs_arr, preds_arr, average='macro')

			# file.write('\npred_labels: {}\n'.format(pred_labels))
			# file.write('\ntarget_labels: {}\n'.format(target_labels))

			# print('pred_labels:',pred_labels)
			# print('target_labels:',target_labels)

		# file.write('\ntest_acc: {:.4f}, f1: {:.4f}, re: {:.4f}, pr: {:.4f}'.format(acc.detach().cpu().numpy(), f1, re, pr))
		print('test_acc:', acc.detach().cpu().numpy(), 'f1:', f1, 're:', re, 'pr:', pr)



if __name__ == '__main__':
	parse = argparse.ArgumentParser(
		formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parse.add_argument('--model_path', '-mp', type=str, default='/ssd6/Roy/DL/DL_hw2/Secondpart/output/resnet34/8_resnet34.pkl')
	parse.add_argument('--model', type=str, default='models.resnet34(pretrained=False)') # models.resnet34(pretrained=False)
	parse.add_argument('--batch_size', '-bz', type=int, default=64)

	# parse.add_argument('--model_path', '-mp', type=str, default='/ssd6/Roy/DL/DL_hw2/Secondpart/output/AdvancedTwoLayerCNN_3/best.pkl')
	# parse.add_argument('--model', type=str, default='AdvancedTwoLayerCNN()') # models.resnet34(pretrained=False)
	# parse.add_argument('--batch_size', '-bz', type=int, default=3)
	
	os.environ['CUDA_VISIBLE_DEVICES']='4' 
	parse.add_argument('--device', type=str, default="cpu")

	parse.add_argument('--image_size', type=int, default='256')
	parse.add_argument('--root_dir', type=str, default="/ssd6/Roy/DL/DL_hw2/dataset/images")
	parse.add_argument('--train_file_path', type=str, default="/ssd6/Roy/DL/DL_hw2/dataset/images/train.txt")
	parse.add_argument('--val_file_path', type=str, default="/ssd6/Roy/DL/DL_hw2/dataset/images/val.txt")
	parse.add_argument('--test_file_path', type=str, default="/ssd6/Roy/DL/DL_hw2/dataset/images/test.txt")
	
	device_ids = [0]
	main()