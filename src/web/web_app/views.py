from django.shortcuts import render_to_response, redirect, render
from django.utils.html import format_html
from django.http.response import HttpResponse
from tweets import getTweets 

# Create your views here.
def index(request):
	return render_to_response("index.html")

def process(request):
	args = {}

	if 'screen_name' in request.POST: 
		screen_name = request.POST['screen_name']
		
		#try to find user
		try:
			user = getTweets.api.GetUser(screen_name = screen_name)
		except:
			args["error_message"] = "User not found"
			return render_to_response("index.html", args)

		#get output parameters	
		args["image_big"] = user.profile_image_url.replace("_normal", "_bigger")
		args["image_normal"] = user.profile_image_url
		args["name"] = user.name
		args["screen_name"] = user.screen_name
		args["description"] = user.description
		args["tweets"] = getTweets.api.GetUserTimeline(screen_name = user.screen_name, count = 20)
		
		#send arguments to results page
		return render_to_response("results.html", args)
	else:
		return redirect("/")