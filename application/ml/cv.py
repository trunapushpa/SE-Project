import os
import json
import torch
import numpy as np
from PIL import Image
from torchvision import transforms
from .mobilenet import mobilenet_v2


'''
	Helper function to classify the given input image using ImageNet classification
	Args:
		fpath: 	(string) image file file
	Return
		feat: 	(numpy.float32 array) image features
		output:	(numpy.float32 array) class probabilities
'''
def predict(fpath):
	model = mobilenet_v2(pretrained=True).eval()
	input_image = Image.open(fpath).convert('RGB')
	preprocess = transforms.Compose([
		transforms.Resize(256),
		transforms.CenterCrop(224),
		transforms.ToTensor(),
		transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
	])
	input_tensor = preprocess(input_image)
	input_batch = input_tensor.unsqueeze(0)

	with torch.no_grad():
		feat, output = model(input_batch)
		output = torch.nn.functional.softmax(output[0], dim=0)
		feat, output = torch.squeeze(feat), torch.squeeze(output)
		feat = np.array([x.item() for x in feat], dtype=np.float32)
		output = np.array([x.item() for x in output], dtype=np.float32)

	return feat, output


'''
	Returns classes labels for class indexes
	Args:
		ind: (numpy.int array) indexes
	Return
		classes: (list) corresponding class labels 

'''
def ind_to_class(ind):
	fpath = os.path.join(os.getcwd(), 'application/ml', 'imagenet_classes.json')
	with open(fpath) as fp:
		data = json.load(fp)
	classes = [data[str(i)] for i in ind]
	return classes


'''
	Returns topk predictions for the input image
	Args:
		fpath: 	(string) image file path
	Return
		p: 		 (list) top-k class probabilites
		classes: (list) corresponding class labels 

'''
def topk(fpath, k=1):
	if k <= 1000 and k > 0:
		feat, preds = predict(fpath)
		ind = np.argpartition(preds, -k)[-k:]
		ind = ind[np.argsort(preds[ind])]
		classes = ind_to_class(ind)
		p = list(preds[ind])
		return p[::-1], classes[::-1]
	else:
		raise AssertionError("k should be <= 1000.")

'''
	Returns features for the given image file
	Args:
		fpath: (string) image file path
	Return
		feat: 		 (np.float32) feature vector
		class_label: (string) class label
'''
def extract_feature(fpath):
	feat, preds = predict(fpath)
	class_label = ind_to_class([np.argmax(preds)])[0]
	return feat, class_label
