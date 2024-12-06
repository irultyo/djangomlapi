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
    patch_a, patch_b = int(requests.POST.get('select_image_patch')[0]), int(requests.POST.get('select_image_patch')[1])
    print(patch_a, patch_b)
    path_a, path_b = utils.get_image(patch_a), utils.get_image(patch_b) 
    print(path_a, path_b)

    paths = []
    for model_name in model_names:
        result = utils.generate_image(patch_a, patch_b, model_name)
        paths.append(result)

    data = zip(model_names, paths)
    return render(requests, 'result.html', locals())
