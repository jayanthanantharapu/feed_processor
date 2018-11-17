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
		train_labelled_set(settings.MEDIA_ROOT+'/'+myfile.name, settings.MEDIA_ROOT)
		# render html
		template = loader.get_template('preprocessor/testing_trained_data.html')
	    context = {"trained_sets": os.listDir(settings.TRAINED_SETS__ROOT)}
	    return HttpResponse(template.render(context, request))

def testing_trained_model(request):
	if request.method == 'GET':
	    template = loader.get_template('preprocessor/testing_trained_data.html')
	    context = {"trained_sets": os.listDir(settings.TRAINED_SETS__ROOT)}
	    return HttpResponse(template.render(context, request))
	elif request.method == 'POST':
		request.POST['unlabelled_set']
		# testing unlabelled data of train model
		# render html
		template = loader.get_template('preprocessor/tested_unlabelled_set_reports.html')
	    context = {}
	    return HttpResponse(template.render(context, request))

### Sentiment Analysis 

def train_labelled_set(filename, output_dir):
	trainObj=train.Train()
	trainObj.train_file_model(filePath, output_dir)

def test_unlabelled_set(test_filename, test_referenced_file, output_dir):
	testObj=test.TestData()
	testedDataFrame=testObj.test_model(
		"",
		test_filename,
		test_referenced_file,
		output_dir
	)