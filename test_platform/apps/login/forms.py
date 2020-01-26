from django import forms


from .models import Profile, PostQuiz, Question

class RegisterForm(forms.Form):
    username = forms.CharField(label="Имя пользователя")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")
    email = forms.EmailField(label="Email", required=False)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput)

    def is_valid(self):
        valid = super(RegisterForm, self).is_valid()
        if self.cleaned_data['password'] != self.cleaned_data['password_confirm']:
            self.add_error("password_confirm", "Пароли не совпадают")
            return False
        return valid


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        exclude = ['user']

class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('question', 'option1', 'option2', 'option3', 'option4', 'answer')
        labels = {'option1': 'Вариант ответа №1', 'option2': 'Вариант ответа №2', 'option3': 'Вариант ответа №3', 'option4': 'Вариант ответа №4', 'answer': 'Правильный ответ'}
        widgets = {
            'option1': forms.TextInput(attrs = {'class': 'form-control form-control-sm' }),
            'option2': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'option3': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'option4': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'answer': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'question': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        }
        exclude = ['post_quiz']



class PostQuizForm(forms.ModelForm):

    class Meta:
        model = PostQuiz
        exclude = ['author']
