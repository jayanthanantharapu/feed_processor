from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
import shutil
from django.views.generic import TemplateView
import plotly.offline as opy
import plotly.graph_objs as go
import plotly.plotly as py
# sentiment-analyser
from sentimentanalyser import train, test

# Create your views here.

def training_model(request):
	if request.method == 'GET':

	    template = loader.get_template('preprocessor/training_data_file_upload.html')	    
	    return HttpResponse(template.render({}, request))
	elif request.method == 'POST':

		myfile = request.FILES['labelled_file']
		fs = FileSystemStorage()
		fs.save(myfile.name, myfile)
		# setting labelled data to train model
		train_labelled_set(settings.MEDIA_ROOT+'/'+myfile.name, settings.TRAINED_SETS_ROOT)
		shutil.rmtree(settings.MEDIA_ROOT)
		# redirect
		return redirect('testing_trained_model')

def testing_trained_model(request):
	if request.method == 'GET':

	    template = loader.get_template('preprocessor/testing_trained_data.html')
	    context = update_context(settings.TRAINED_SETS_ROOT)
	    return HttpResponse(template.render(context, request))
	elif request.method == 'POST':

		myfile = request.FILES['unlabelled_set']
		fs = FileSystemStorage()
		fs.save(myfile.name, myfile)
		print(request.POST['trained_pkl'])
		# testing unlabelled data of train model
		data_result_df=test_unlabelled_set(
			settings.MEDIA_ROOT+'/'+myfile.name,
			request.POST['trained_pkl'],
			settings.TRAINED_SETS_ROOT
		)

		json_categ=get_categorical_in_json_generic(data_result_df,["SVM","Naive-Bayes"])
		
		sub_key_SVM=list(json_categ["SVM"].keys())
		sub_key_NB=list(json_categ["Naive-Bayes"].keys())

		values_SVM=list(json_categ["SVM"].values())
		values_NB=list(json_categ["Naive-Bayes"].values())

		# print(sub_key_SVM,
		# 	sub_key_NB,
		# 	values_NB,
		# 	values_SVM)



		graph_vals = {
		"sub_key_SVM": sub_key_SVM,
		"sub_key_NB": sub_key_NB,
		"values_SVM": values_SVM,
		"values_NB": values_NB
		}


		g = Graph() 
		context = g.get_context_data(graph_vals) 
		return render(request, 'preprocessor/tested_unlabelled_set_reports.html', context)

class Graph(TemplateView):
	template_name = 'graph.html'


	def get_context_data(self, graph_vals,**kwargs):
		context = super(Graph, self).get_context_data(**kwargs)

		'''
		{'sub_key_SVM': ['business', 'sport', 'entertainment', 'tech', 'politics'], 
		'sub_key_NB': ['business', 'sport', 'entertainment', 'tech', 'politics'], 
		'values_SVM': [25, 25, 20, 12, 17], 
		'values_NB': [26, 25, 20, 11, 17]}
		'''

		trace1 = go.Bar(
			x=graph_vals["sub_key_SVM"],
			y=graph_vals["values_SVM"],
			name='SVM'
		)

		trace2 = go.Bar(
			x=graph_vals["sub_key_SVM"],
			y=graph_vals["values_NB"],
			name='Naive-Bayes'
		)

	
		data = [trace1, trace2]



		# layout=go.Layout(title="Meine Daten", xaxis={'title':'x1'}, yaxis={'title':'x2'})

		layout = go.Layout(
			barmode='group'
		)

		figure=go.Figure(data=data,layout=layout)
		div = opy.plot(figure, auto_open=False, output_type='div')

		context['graph'] = div



		labels = ['Oxygen','Hydrogen','Carbon_Dioxide','Nitrogen']
		values = [4500,2500,1053,500]

		trace = go.Pie(labels=labels, values=values)

		# py.iplot([trace], filename='basic_pie_chart')

		div2 = opy.plot([trace], auto_open=False, output_type='div')
		print(div2)

		# div2 = opy.plot(fig, auto_open=False, output_type='div')
		context['graph2'] = div

		return context


def get_categorical_in_json_generic(df,list_of_models):
	dict_categories={}
	for model in list_of_models:
		categories=df[model].unique()
		dict_categories[model]={}
		for category in categories:
			count=df[df[model]==category].shape[0]
			dict_categories[model][category]=count
			print(count)
	return dict_categories
		
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
	return testedDataFrame

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