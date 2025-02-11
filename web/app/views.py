from django.shortcuts import render
from . import utils

def home(requests):
    product_name="Batik RVGAN"
    patches = utils.patch_home()
    return render(requests, 'home.html', locals())

def select_patch(requests):
    product_name="Batik RVGAN"
    index = requests.POST.get('index')
    patches = utils.retrieve(index)
    return render(requests, 'select_patch.html', locals())

def result(requests):
    product_name = "Batik RVGAN"   
    model_names = requests.POST.getlist('model_name')
    patches = requests.POST.getlist('select_image_patch')
    patch_a, patch_b = int(patches[0]), int(patches[1])
    path_a, path_b = utils.get_image(patch_a), utils.get_image(patch_b) 
    base64_images = []
    for model_name in model_names:
        result = utils.generate_image(patch_a, patch_b, model_name) 
        base64_images.append(result)
    data = zip(model_names, base64_images)
    return render(requests, 'result.html', locals())
