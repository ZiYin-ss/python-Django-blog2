from django import forms
from django.core.files.base import ContentFile
from slugify import slugify
from urllib import request
from .models import Image


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')

    def clean_url(self): # clean_xxx cleaned_data会自动调用的
        url = self.cleaned_data['url']
        # 验证扩展名
        valid_extensions = ['jpg', 'jpeg', 'png']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError("The  given  Url  does  not  match  valid  image extension.")
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        image = super(ImageForm, self).save(commit=False)
        image_url = self.cleaned_data['url']
        image_name = '{0}.{1}'.format(slugify(image.title), image_url.rsplit('.', 1)[1].lower())
        response = request.urlopen(image_url)
        #  上面四个都是铺垫的 就是说 这个才是真正保存图片 文件名 写入文件内容
        image.image.save(image_name, ContentFile(response.read()), save=False)

        if commit:
            image.save()

        return image
