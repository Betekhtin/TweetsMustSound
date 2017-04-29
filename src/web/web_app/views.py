from django.shortcuts import render_to_response, redirect, render
from django.utils.html import format_html
from django.http.response import HttpResponse
from tweets import getTweets 

# Create your views here.
def index(request):
	return render_to_response("index.html")

def process(request):
	args = {}
	screen_name = request.POST['screen_name']
	if screen_name == "":
		args["error_message"] = "Field is empty" 
		return render_to_response("index.html", args)
	try:
		user = getTweets.api.GetUser(screen_name = screen_name)
	except:
		args["error_message"] = "User not found"
		return render_to_response("index.html", args)
	args["image"] = user.profile_image_url
	args["name"] = user.name
	args["screen_name"] = user.screen_name
	args["description"] = user.description
	print(user)
	return render_to_response("results.html", args)