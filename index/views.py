from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user
from django.contrib import messages
from .forms import UserForm,ProjectPicForm,CreateProjectForm
from .forms import EditProjectForm, ContactForm,EditPicsForm,EditProfileForm
from .models import User, Project, Comment, View

import random
from django.core.mail import send_mail, EmailMessage


def index(request):
	return render(request, 'index.html', {
		'title': 'Publish and share your portfolio',
		'page': 'Home',
		'profiles': User.objects.exclude(first_name__exact='').order_by('-last_login')[:5]
		})

def about(request):
	return render(request, 'about.html', {
		'title': 'About Projects',
		'page': 'About'
		})

def contact(request):
	if request.method=='POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			cont = form.save(commit=True)
			messages.success(request, 'Thanks for reaching out, we will get back to you via email')
			return redirect(contact)

		messages.error(request, 'Please ensure you fill all fields')
		return redirect(contact)

	contactdetails = {}
	if request.user.is_authenticated:
		contactdetails = User.objects.get(username=request.user.username)
	return render(request, 'contact.html', {
		'title': "Contact Project's team",
		'page': 'Contact',
		'contact': contactdetails
		})

def profile(request, username):
	if User.objects.filter(username=username):
		user = User.objects.get(username=username)
		if user.first_name=='':
			messages.error(request, 'Profile has not been completed. Please complete')
		return render(request, 'profile.html', {
			'title': user.first_name+ "'s Profile page",
			'page': 'Profile',
			'user': user,
			'profiles': User.objects.exclude(first_name__exact='').order_by('-last_login')[:5]
			})
	if request.user.is_authenticated and (not User.objects.filter(username=username)):
		messages.error(request, 'Incorrect profile link, please check your link')
	return redirect(index)

def defaultprofile(request):
	if User.objects.all():
		return redirect(profile, User.objects.all()[0].username)
	else:
		messages.error(request, 'No profile yet, be the first to create.')
		return redirect(signup)

def changepassword(request):
	if request.user.is_authenticated:
		if request.method=='POST':
			oldpass = request.POST['oldpass']
			password1 = request.POST['password1']
			password2 = request.POST['password2']

			if password2 and (password1==password2):
				user = User.objects.get(username=request.user.username)
				if user.check_password(oldpass):
					user.set_password(password1)
					user.save()

					messages.success(request, 'Password updated')
					return redirect(signin)
				else:
					messages.error(request, 'Old password is Incorrect')
			else:
				messages.error(request, 'Password mismatch')

			return redirect(changepassword)

		return render(request, 'changepass.html', {
			'title': request.user.username+': Change your password',
			'page': 'Profile'
			})

	return redirect(signin)

def forgotpass(request):
	if request.method=='POST':
		username = request.POST['username'].replace(' ', '')
		if username:
			if User.objects.filter(username=username):
				user = User.objects.get(username=username)
				newpass = random.randint(100000,10000000)
				message = "Hello, {}. Your new password is {}. \n Please ignore this message if you don't have a Project account".format(user.first_name, newpass)
				
				res = send_mail('Password reset', message, "ibdac2000@gmail.com",[user.email], fail_silently=True)
				if res==None:
					messages.error(request, 'Unable to reset password, please try again')
				else:
					print('Result: ',res)
					user.set_password(newpass)
					user.save()
					messages.success(request, 'New Password has been sent to your email')
				return redirect(forgotpass)
			else:
				messages.error(request, 'Username does not exist. Please check your letter case')
				return redirect(forgotpass)
		else:
			messages.error(request, 'Please enter the username you want to reset password')
			return redirect(signin)
	else:
		return render(request, 'forgotpass.html',{
			'title': 'Retrieve your Project Account'
			})


IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg', 'gif']

def editprofile(request):
	if request.user.is_authenticated:
		if request.method=='POST':
			form = EditProfileForm(request.POST)
			if form.is_valid():
				user = User.objects.get(username=request.user.username)
				
				user.first_name = form.cleaned_data['first_name']
				user.last_name = form.cleaned_data['last_name']
				user.email = form.cleaned_data['email']
				user.phonenum = form.cleaned_data['phonenum']
				user.about = form.cleaned_data['about']
				user.job_title = form.cleaned_data['job_title']
				user.job_description = form.cleaned_data['job_description']
				user.nationality = form.cleaned_data['nationality']
				user.contact_address = form.cleaned_data['contact_address']
				
				pictureForm = EditPicsForm(request.POST,request.FILES)
				if pictureForm.is_valid():
					img_type = str(request.FILES['profilePics']).split('.')[-1].lower()
					resume_type = str(request.FILES['resume']).split('.')[-1].lower()
					
					if (not resume_type=='pdf') and (img_type not in IMAGE_FILE_TYPES):
						messages.error(request, 'Image must be a jpeg, png or jpg file while resume should be in pdf file format')
						print(resume_type, img_type)
					else:
						user.profilePics = request.FILES['profilePics']
						user.resume = request.FILES['resume']
						user.save()
						print('He want to upload')

					messages.success(request ,'Your profile has been updated, you are now ready to share your portfolio')
					return redirect(profile,request.user.username)
				elif user.profilePics:
					user.save()
					return redirect(profile, request.user.username)
					
			messages.error(request, 'Please fill all fields')
			return redirect(editprofile)

		return render(request, 'editprofile.html', {
			'title': request.user.username+': Edit Profile',
			'page': 'Profile',
			'user': User.objects.get(username=request.user.username)
			})

	messages.error(request, 'Please ensure you are logged in.')
	return redirect(signin)

def addproject(request):
	if request.user.is_authenticated:
		if request.method=='POST':
			if not User.objects.get(username=request.user.username).first_name:
				messages.error(request, 'Please complete your profile before saving a project')
				return redirect(editprofile)

			form = CreateProjectForm(request.POST, request.FILES)
			# print('Form')
			# print(form)
			if form.is_valid():
				project = form.save(commit=True)
				propics = ProjectPicForm(request.POST, request.FILES)
				
				if propics.is_valid():
					if not propics.cleaned_data['picture']=='defaultproject.jpg':
						project.picture = request.FILES['picture']
						project.save()

				messages.success(request, 'New Project created')
				return redirect(addproject)
				# user = User.objects.get(username=request.user.username)
				# pro = Project.objects.create(\
				# 	user=user,title=request.POST['title'],short_desc=request.POST['POST'])

			print(form.errors)
			messages.error(request, 'Please fill required fields')
			return redirect(addproject)

		return render(request, 'addproject.html', {
			'title': 'Add new project to your portfolio',
			'page': 'Project'
			})

	messages.error(request, 'Please ensure you are logged in.')
	return redirect(index)


def deleteproject(request, id):
	if request.user.is_authenticated:
		if Project.objects.filter(id=id):
			project = Project.objects.get(id=id)
			if project.user.username == request.user.username:
				project.delete()
				messages.success(request, 'Project deleted')
				return redirect(projects, request.user.username)

			else: messages.error(request, 'Unauthorize access')

		else: messages.error(request, 'Project does not exist')

	return redirect(index)


def editproject(request, id):
	if request.user.is_authenticated:
		if Project.objects.filter(id=id):
			project = Project.objects.get(id=id)
			if project.user.username == request.user.username:
				if request.method=='POST':
					editform = EditProjectForm(request.POST, request.FILES)
					if editform.is_valid():
						edit = editform.save(commit=False)
						edit.id = id
						edit.user = project.user
						edit.pub_date = project.pub_date
						if request.FILES:
							edit.picture = request.FILES['picture']
						else:
							edit.picture = project.picture
						edit.save()

						print('Edited')
						messages.success(request, 'Project Edited')

					else: messages.error(request, 'Please fill required fields')

					return redirect(projects, project.user.username)
				else:
					return render(request, 'editproject.html', {
						'title': 'Edit '+project.title,
						'page': 'Project',
						'project': project
						})

			else: messages.error(request, 'Unauthorize access')

		else: messages.error(request, 'Project does not exist')

	return redirect(index)

def defaultproject(request):
	if Project.objects.all():
		return redirect(projects, Project.objects.all()[0].user.username)

	messages.error(request, 'No project yet')
	return redirect(index)


def projects(request, username):
	if User.objects.filter(username=username):
		user = User.objects.get(username=username)
		return render(request, 'projects.html', {
			'title': user.first_name+"'s Projects",
			'page': 'Project',
			'user': user
			})

	messages.error(request, 'Ooops, Porfolio projects not found')
	return redirect(index)


def project(request, id):
	if Project.objects.filter(id=id):
		project = Project.objects.get(id=id)
		viewed = None
		if request.user.is_authenticated:
			user = request.user.username
			if (not user==project.user.username) and (not View.objects.filter(project=project, user=user)):
				View.objects.create(project=project, user=user)
				viewed = True
		else:
			user = 'Anonymous'
			View.objects.create(project=project, user=user)
			viewed = True


		if viewed: # If the a view object is created
			if project.user.email:
				mes = "<h2>Hello {}.</h2>  \
					<p>We trust you are doing good. Just want to inform you that your project titled {} \
					got a new view from {}</p> <br/> <p>Team Project.<p/>".format(project.user.username, project.title, user)
				
				email = EmailMessage("Project view", mes, "ibdac2000@gmail.com",[project.user.email])
				email.content_subtype = "html"
				res = email.send(fail_silently=True)

		return render(request, 'project.html', {
			'title': project.title+' by '+project.user.username,
			'page': 'Project',
			'project': project
			})

	messages.error(request, 'Ooops, Project not found')
	return redirect(index)

def commentproject(request, id):
	if request.user.is_authenticated:
		if request.method=='POST':
			comment = request.POST['comment']
			if not comment:
				messages.error(request, 'Please fill the comment field')
				return redirect(project, id)

			if Project.objects.filter(id=id):
				user = User.objects.get(username=request.user.username)
				p = Project.objects.get(id=id)
				comment = Comment.objects.create(project=p,author=user,comment=comment)
				messages.success(request, 'Project Commented')

				# Creating a new comment for the project author
				# slug = '/project/{}'.format(id)
				# message = "{} write a comment on your project titled {}".format(user.username,p.title)
				# Notification.objects.create(user=p.user, message=message, slug=slug)
			
				if p.user.email:
					mes = "<h2>Hello {}.</h2>  \
						<p>We trust you are doing good. Just want to inform you that your project titled {} \
						got a new comment from {}</p> <br/> <p>Team Project.<p/>".format(p.user.username, p.title, user.username)
					
					email = EmailMessage("New comment on your portfolio on Project", mes, "ibdac2000@gmail.com",[p.user.email])
					email.content_subtype = "html"
					res = email.send(fail_silently=True)
				return redirect(project, id)

			messages.error(request, 'Ooops, Project not found')
			return redirect(project, id)


	messages.error(request, 'Please ensure you are logged in.')
	return redirect(signin)

def signin(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			if user.is_active:
				login_user(request, user)
				
				return redirect(profile, username)
				
			messages.error(request, 'Your account has been disabled')
				
		else:
			messages.error(request, 'Invalid login')
		
		return redirect(signin)
	else:
		return render(request, 'login.html', {
			'title': 'Sign in to share your portfolio',
			'page': 'Login'
			})

def signup(request):
	if request.method=='POST':
		if not request.POST['password'] == request.POST['password2']:
			messages.error(request, 'Password chosen mismatch. Please try again')
			return redirect(signup)

		if User.objects.filter(username=request.POST['username']):
			messages.error(request, 'Username you chose has been taken')
			return redirect(signup)

		form = UserForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user.set_password(password)

			user.save()
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login_user(request, user)
				
				messages.success(request, 'Please complete your profile to make it visible')
				return redirect(editprofile)
		
		messages.error(request, 'Please ensure the all the field are filled')
		return redirect(signup)
	else:
		return render(request, 'register.html', {
			'title': 'Create and Share your portfolio round the world',
			'page': 'Register'
			})


def logout(request):
	logout_user(request)
	return redirect(signin)

