from django import forms
from .models import *
from django.core.exceptions import ValidationError


class AddAplForm(forms.ModelForm):
    class Meta:
        model = Aplication
        fields = ('name', 'description', 'Category', 'photo_file')
        enctype = "multipart/form-data"


class AppListForm(forms.ModelForm):

    def clean(self):
        status = self.cleaned_data.get('status')
        comment = self.cleaned_data.get('comment')
        photo_file2 = self.cleaned_data.get('photo_file2')
        if self.instance.status != 'new':
            raise forms.ValidationError({'status': 'Статус можно сменить только у новой заявки'})
        if status == 'new' and comment:
            raise forms.ValidationError({'comment': 'К новой заявке нельзя добавить комментарий'})
        if status == 'haired' and not comment:
            raise forms.ValidationError({'comment': 'Нужно указать комментарий для заявки принятой в работу'})
        if status == 'done' and not photo_file2:
            raise forms.ValidationError({'photo_file2': 'Нужно добавить фотографию для выполненой заявки'})


class Reg_Form(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label='Введите пороль')
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label='Повторите пороль')
    confirm = forms.BooleanField(required=True, label='Согласие на обработку пресоональных данных')
    email = forms.EmailField(widget=forms.EmailInput(), label='Введите почту')

    class Meta:
        model = User
        fields = ['name', 'surname', 'patronymic', 'username', 'email', 'password', 'confirm_password', 'confirm']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            self.add_error('confirm_password', 'Пароли не совпадают.')
        return cleaned_data

    def clean_name(self):
        ALLOWED_CHARS = 'йцукенгшщзхъэждлорпавыфячсмитьбюёЁЙЦУКЕНГШЩЗХЪЭЖДЛОРПАВЫФЯЧСМИТЬБЮ -'
        name = self.cleaned_data['name']
        if not (set(name)) <= set(ALLOWED_CHARS):
            raise ValidationError('Имя должно состоять из кириллических букв, дефиса и пробелов.')
        return name

    def clean_surname(self):
        ALLOWED_CHARS = 'йцукенгшщзхъэждлорпавыфячсмитьбюёЁЙЦУКЕНГШЩЗХЪЭЖДЛОРПАВЫФЯЧСМИТЬБЮ -'
        surname = self.cleaned_data['surname']
        if not (set(surname)) <= set(ALLOWED_CHARS):
            raise ValidationError('Фамилия должна состоять из кириллических букв, дефиса и пробелов.')
        return surname

    def clean_patronymic(self):
        ALLOWED_CHARS = 'йцукенгшщзхъэждлорпавыфячсмитьбюёЁЙЦУКЕНГШЩЗХЪЭЖДЛОРПАВЫФЯЧСМИТЬБЮ -'
        patronymic = self.cleaned_data['patronymic']
        if not (set(patronymic)) <= set(ALLOWED_CHARS):
            raise ValidationError('Отчество должно состоять из кириллических букв, дефиса и пробелов.')
        return patronymic

    def clean_username(self):
        ALLOWED_CHARS = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890-'
        username = self.cleaned_data['username']
        if not (set(username)) <= set(ALLOWED_CHARS):
            raise ValidationError('Логин должен состоять только из латинских букв, цифр и дефиса.')
        if User.objects.filter(username=username).exists():
            self.add_error('username', 'Пользователь с таким логином уже существует.')
        return username


STATUS_CHOISE = [
    ('new', 'Новая'),
    ('haired', 'Принято в работу'),
    ('done', 'Выполнено'),
    ('all', 'Все заявки')
]


class AppListFormFilter(forms.Form):
    status = forms.ChoiceField(choices=STATUS_CHOISE, label='Отсортировать по статусу ', initial='All')


class AppListHandleForm(forms.ModelForm):
    name = forms.CharField(disabled=True, label='Имя заявки')
    description = forms.CharField(disabled=True, label='Описание')
    photo_file = forms.ImageField(disabled=True, label='Фото заявки')
    status = forms.ChoiceField(choices=[('done', 'Выполнено'), ('haired', 'Принято в работу')],
                               label='Изменить статус на ')
    Category = forms.ModelChoiceField(queryset=Category.objects.all(), disabled=True, label='Категория')
    photo_file2 = forms.ImageField(disabled=False, label='Фото готовой заявки', required=True)
    comment = forms.CharField(disabled=False, label='Комментарий', required=True)

    def clean(self):
        status = self.cleaned_data.get('status')
        comment = self.cleaned_data.get('comment')
        photo_file2 = self.cleaned_data.get('photo_file2')
        if self.instance.status != 'new':
            raise forms.ValidationError({'status': 'Статус можно сменить только у новой заявки'})
        if status == 'new' and comment:
            raise forms.ValidationError({'comment': 'К новой заявке нельзя добавить комментарий'})
        if status == 'haired' and not comment:
            raise forms.ValidationError({'comment': 'Нужно указать комментарий для заявки принятой в работу'})
        if status == 'done' and not photo_file2:
            raise forms.ValidationError({'photo_file2': 'Нужно добавить фотографию для выполненой заявки'})

    class Meta:
        model = Aplication
        fields = ['name', 'description', 'photo_file', 'status', 'Category', 'photo_file2', 'comment']
        enctype = "multipart/form-data"


class CategoryList(forms.ModelForm):
    name = forms.CharField(max_length=250, label='Новая категория', required=True)

    class Meta:
        model = Category
        fields = ['name']
