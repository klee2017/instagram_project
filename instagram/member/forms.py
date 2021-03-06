from django import forms
from django.contrib.auth import get_user_model, authenticate, login as django_login
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class LoginForm(forms.Form):
    """
    is_valid()에서 주어진 username/password를 사용한 authenticate실행
    성공시 login(request)메서드를 사용할 수 있음
    """
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        self.user = authenticate(username=username, password=password)

        if not self.user:
            raise forms.ValidationError(
                'Invalid login credentials'
            )
        else:
            setattr(self, 'login', self._login)

    def _login(self, request):
        """
        django.contrib.auth.login(request)를 실행
        :param request: django.contrib.auth.login()에 주어질 HttpRequest객체
        :return: None
        """
        django_login(request, self.user)


# class SignupForm(forms.Form):
#     username = forms.CharField(
#         widget=forms.TextInput(
#             attrs={
#                 'class': 'form-control',
#             }
#         )
#     )
#     password = forms.CharField(
#         widget=forms.PasswordInput(
#             attrs={
#                 'class': 'form-control',
#             }
#         )
#     )
#
#     password2 = forms.CharField(
#         # required=False,
#         widget=forms.PasswordInput(
#             attrs={
#                 'class': 'form-control',
#             }
#         )
#     )
#
#     age = forms.IntegerField(
#         widget=forms.NumberInput(
#             attrs={
#                 'class': 'form-control',
#             }
#         )
#     )
#
#     def clean_username(self):
#         data = self.cleaned_data['username']
#         if User.objects.filter(username=data).exists():
#             raise forms.ValidationError('Username already exists')
#         return data
#
#     def clean_password2(self):
#         password = self.cleaned_data['password']
#         password2 = self.cleaned_data['password2']
#         if password != password2:
#             raise forms.ValidationError("Password1 and Password2 are not equal")
#         return password2
#
#     def clean(self):
#         if self.is_valid():
#             setattr(self, 'signup', self._signup)
#         return self.cleaned_data
#
#     def _signup(self):
#         username = self.cleaned_data['username']
#         password = self.cleaned_data['password']
#         age = self.cleaned_data['age']
#         return User.objects.create_user(
#             username=username,
#             password=password,
#             age=age,
#         )
class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        class_update_fields = ('password1', 'password2')
        for field in class_update_fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = User
        fields = (
            'username',
            'password1',
            'password2',
            'img_profile',
            'age',
        )
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'age': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                }
            ),
        }

