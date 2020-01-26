from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.forms import formset_factory, inlineformset_factory


from .models import Profile, PostQuiz, Question
from .forms import RegisterForm, ProfileForm, PostQuizForm, QuestionForm

def edit(request, post_id):
    post = PostQuiz.objects.get(pk=post_id)
    quests = post.question.all()
    if request.method == 'POST':
        postf = PostQuizForm(request.POST, instance=post)
        if postf.is_valid():
            postf.save()
            messages.success(request, "Изменения сохранены!")
            return redirect(reverse('login:home'))
        else:
            messages.error(request, "Проверьте введенные данные! Там ошибка!")
            return render(request, 'quiz/edit_quiz.html', {'form': postf})
    else:
        postf = PostQuizForm(instance=post)
        questsf = QuestionFormSet(queryset=quests)
        return render(request, 'quiz/edit_quiz.html', {'formP':postf, 'formQ': questsf})

def newQuizAdd(request):
    QuestionFormSet = inlineformset_factory(PostQuiz, Question, form=QuestionForm, extra=1, max_num=10)
    if request.method == 'POST':
        text = request.POST['text']
        num = int(request.POST['num'])
        name_quiz = request.POST['quest1']
        p = PostQuiz.objects.create(text=text, author=request.user, name_quiz=name_quiz, num_of_quest=num)
        formset = QuestionFormSet(request.POST, initial=p)
        print()
        print(request.POST)
        print()

        if formset.is_valid():
            formset.save()
            messages.success(request, "Добавлена новая викторина!")
            return redirect(reverse('login:home'))

def NewQuiz(request):
    num = int(request.POST['num_of_quest'])
    if num == '':
        num = 5
    num = int(num)
    if num < 5:
        num = 5
    elif num > 10:
        num =10
    i = 1
    a = []
    while i != num+1:
        a.append(i)
        i +=1
    nums = a
    question_name = request.POST['question_name']
    text_quiz = request.POST['text_quiz']
    QuestionFormSet_factory = formset_factory(form=QuestionForm, can_order=True, extra=num, max_num=10)
    form = QuestionFormSet_factory()
    return render(request, 'quiz/newquiz.html', {'num': num, 'nums':nums, 'question_name':question_name, 'text_quiz':text_quiz, 'form':form })


class HomeView(TemplateView):
    template_name = "home.html"
    timeline_template_name = "timeline.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, self.template_name)

        if request.method == 'POST':
            form = PostQuizForm(request.POST, request.FILES)
            if form.is_valid():
                form.instance.author = request.user
                form.save()
                return redirect(reverse('login:home'))

        posts = PostQuiz.objects.all()
        quests = Question.objects.all()
        return render(request, self.timeline_template_name, {'posts': posts, 'quests':quests})


class RegisterView(TemplateView):
    template_name = "registration/register.html"

    def dispatch(self, request, *args, **kwargs):
        form = RegisterForm()
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                self.create_new_user(form)
                messages.success(request, "Вы успешно зарегистрировались!")
                return redirect(reverse("login"))

        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def create_new_user(self, form):
        email = None
        if 'email' in form.cleaned_data:
            email = form.cleaned_data['email']
        User.objects.create_user(form.cleaned_data['username'], email, form.cleaned_data['password'],
                                 first_name=form.cleaned_data['first_name'],
                                 last_name=form.cleaned_data['last_name'])


class LogoutView(View):
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return redirect("/")


class ProfileView(TemplateView):
    template_name = "registration/profile.html"

    def dispatch(self, request, *args, **kwargs):
        if not Profile.objects.filter(user=request.user).exists():
            return redirect(reverse("login:edit_profile"))
        context = {
            'selected_user': request.user
        }
        return render(request, self.template_name, context)

class EditProfileView(TemplateView):
    template_name = "registration/edit_profile.html"

    def dispatch(self, request, *args, **kwargs):
        form = ProfileForm(instance=self.get_profile(request.user))
        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES, instance=self.get_profile(request.user))
            if form.is_valid():
                form.instance.user = request.user
                form.save()
                messages.success(request, "Профиль успешно обновлен!")
                return redirect(reverse("login:profile"))
        return render(request, self.template_name, {'form': form})

    def get_profile(self, user):
        try:
            return user.profile
        except:
            return None