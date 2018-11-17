from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
# sentiment-analyser
from sentimentanalyser import train

# Create your views here.

def training_model(request):
	if request.method == 'GET':
	    template = loader.get_template('preprocessor/training_data_file_upload.html')
	    context = {}
	    return HttpResponse(template.render(context, request))
	elif request.method == 'POST':
		myfile = request.FILES['labelled_file']
		fs = FileSystemStorage()
		fs.save(myfile.name, myfile)
		# setting labelled data to train model
		train_labelled_set(settings.MEDIA_ROOT+'/'+myfile.name, settings.TRAINED_SETS_ROOT)
		os.rmdir(settings.MEDIA_ROOT)
		# redirect
		return HttpResponseRedirect(reverse('testing_trained_model'))

def testing_trained_model(request):
	if request.method == 'GET':
	    template = loader.get_template('preprocessor/testing_trained_data.html')
	    context = update_context(settings.TRAINED_SETS_ROOT)
	    return HttpResponse(template.render(context, request))
	elif request.method == 'POST':
		myfile = request.POST['unlabelled_set']
		fs = FileSystemStorage()
		fs.save(myfile.name, myfile)
		# testing unlabelled data of train model
		test_unlabelled_set(
			settings.MEDIA_ROOT+'/'+myfile.name,
			request.POST['trained_pkl'],
			settings.TRAINED_SETS_ROOT
		)
		# render html
		template = loader.get_template('preprocessor/tested_unlabelled_set_reports.html')
		context = {}
		return HttpResponse(template.render(context, request))

### Sentiment Analysis 

def train_labelled_set(filename, output_dir):
	trainObj=train.Train()
	trainObj.train_file_model(filename, output_dir)

def test_unlabelled_set(test_filename, test_referenced_file, output_dir):
	testObj=test.TestData()
	testedDataFrame=testObj.test_model(
		"",
		test_filename,
		test_referenced_file,
		output_dir
	)

class Trained_Files:
	"""docstring for Trained_Files"""
	def __init__(self, name):
		self.name = name;

def update_context(train_location):
	folder_list = os.listdir(train_location)
	folder_obj_list = []
	for folder in folder_list:
		folder_obj_list.append(Trained_Files(folder))
	context = {"folder_list": folder_obj_list}
	return context