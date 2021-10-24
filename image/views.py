import os
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .forms import ImageForm
from .models import Image


@login_required(login_url='/account/login/')
@csrf_exempt
@require_POST
def upload_image(request):
    form = ImageForm(data=request.POST)
    if form.is_valid():
        new_item = form.save(commit=False)
        new_item.user = request.user
        new_item.save()
        # 这个地方是先保存了三个字段 title url 和描述
        #  然后form表单中调用了image.image.save方法保存了图片 因为在模型类的upload_to设置了保存路径 在根目录下面
        #  在调用了模型类的save方法保存了slug 然后created是模型类的父类的save保存的
        #  至此保存了六个 然后在保存user 就可以了

        # return JsonResponse({'status': "1"})
        return HttpResponse("1")
    else:
        # return JsonResponse({'status': "0"})
        return HttpResponse("0")


@login_required(login_url='/account/login/')
def list_images(request):
    images = Image.objects.filter(user=request.user)
    return render(request, 'image/list_images.html', {"images": images})


@login_required(login_url='/account/lobin/')
@require_POST
@csrf_exempt
def del_image(request):
    image_id = request.POST['image_id']
    try:
        image = Image.objects.get(id=image_id)
        # V:\Python文件\Django\Simple-blogging-system\python-blog2\image\views.py
        # 获取当前文件名的绝对路径 一直到文件名
        # print(os.path.abspath(__file__))
        #  获取到文件路径 就是上面的上一级目录
        # V:\Python文件\Django\Simple-blogging-system\python-blog2\image
        # print(os.path.dirname(os.path.abspath(__file__)))
        # V:\Python文件\Django\Simple-blogging-system\python-blog2
        # print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        d = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        #  V:\Python文件\Django\Simple-blogging-system\python-blog2  images/2021/10/24/Tu-Zi.jpg
        tu_jpg = os.path.join(d, "\media\\" + str(image.image).replace('/','\\'))
        if os.path.isfile(tu_jpg):
            os.remove(tu_jpg)
        image.delete()
        return JsonResponse({'status': "1"})
    except:
        return JsonResponse({'status': "2"})
