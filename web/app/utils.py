import numpy as np
import base64
import random
from datetime import datetime
from PIL import Image
import onnxruntime as ort
from pathlib import Path
from django.conf import settings

def braycurtis(x, y):
    if x.shape != y.shape: 
        raise ValueError("Input vectors must have the same dimensions")
    numerator = np.sum(np.abs(x - y))
    denominator = np.sum(np.abs(x + y))
    if denominator == 0:
        return 0.0
    distance = numerator / denominator
    return distance

def get_image(index):
    npy_dir = Path(settings.BASE_DIR) / 'app' / 'npy'
    paths = np.load(npy_dir / 'paths_webp.npy')
    return paths[index]

# Home function utils
# webapp
def patch_home():
    npy_dir = Path(settings.BASE_DIR) / 'app' / 'npy'
    paths = np.load(npy_dir / 'paths_webp.npy')
    random.seed(3)
    random_index = random.sample(range(0,120), 18)
    paths = [paths[idx] for idx in random_index]
    return zip(paths, random_index)
# api
def api_patch_home():
    npy_dir = Path(settings.BASE_DIR) / 'app' / 'npy'
    paths = np.load(npy_dir / 'paths_webp.npy')
    random.seed(3)
    random_index = random.sample(range(0,120), 18)
    return random_index

# Select patch function utils
# webapp
def get_distinct(nested_list, index):
    seen = set()
    return [sublist for sublist in nested_list if not (sublist[index] in seen or seen.add(sublist[index]))]

def sort(res_list):
    res_list = sorted(res_list, key=lambda x: x[2])
    res_list = get_distinct(res_list, 1)
    return res_list

def retrieve(index):
    npy_dir = Path(settings.BASE_DIR) / 'app' / 'npy'
    features = np.load(npy_dir / 'features.npy')
    labels = np.load(npy_dir / 'labels.npy')
    paths = np.load(npy_dir / 'paths_webp.npy')
    query_features = features[int(index)]
    rank = []
    ind_data = 0
    for f in features:
        dist = braycurtis(query_features, f)
        rank.append([ind_data, labels[ind_data], dist])
        ind_data += 1
    rank = sort(rank)
    paths = [paths[f] for f in [rank[i][0] for i in range(len(rank[:4]))]]
    return zip(paths, [rank[i][0] for i in range(4)])

# api
def api_retrieve(index):
    npy_dir = Path(settings.BASE_DIR) / 'app' / 'npy'
    features = np.load(npy_dir / 'features.npy')
    labels = np.load(npy_dir / 'labels.npy')
    paths = np.load(npy_dir / 'paths_webp.npy')
    query_features = features[int(index)]
    rank = []
    ind_data = 0
    for f in features:
        dist = braycurtis(query_features, f)
        rank.append([ind_data, labels[ind_data], dist])
        ind_data += 1
    rank = sort(rank)
    return [rank[i][0] for i in range(4)]

# generate image function utils
# webapp
def preprocess(index):
    base_dir = Path(settings.BASE_DIR)
    paths = np.load(base_dir / 'app' / 'npy' / 'paths.npy')
    image_path = base_dir / 'staticfiles' / 'images' / 'patches' / paths[index]
    image = Image.open(image_path).convert('RGB')
    image = image.resize((128,128), Image.LANCZOS)
    image_array = np.array(image, dtype=np.float32)
    image_array = (image_array / 255.0 - 0.5) / 0.5
    #image_array = np.transpose(image_array, (2, 0, 1))
    image_array = np.expand_dims(image_array, axis=0)
    return image_array

def postprocess(output_image):
    base_dir = Path(settings.BASE_DIR)
    output_image = (output_image * 0.5 + 0.5) * 255
    output_image = np.clip(output_image, 0, 255).astype(np.uint8)
#    output_image = np.transpose(output_image, (1, 2, 0))
    output_image = Image.fromarray(output_image)

    current_dateTime = datetime.now()
    current_dateTime = current_dateTime.strftime('%d%m%y%H%M%S')
    result_name = "result-"+current_dateTime+".png"
    output_image.save(base_dir / 'staticfiles' / 'images' / 'results' / result_name)
    return result_name

def generate_image(patch_a, patch_b, model_name):
    base_dir = Path(settings.BASE_DIR)

    models = {
        'batikgan_sl': base_dir / 'app' / 'models' / 'batikgan_sl.onnx',
        'batikgan_cl': base_dir / 'app' / 'models' / 'batikgan_cl.onnx',
        'batikrvgan': base_dir / 'app' / 'models' / 'batikrvgan.onnx',    
    }

    patch_a = preprocess(patch_a)
    patch_b = preprocess(patch_b)
    
    session = ort.InferenceSession(models[model_name])
    input_name = [input_node.name for input_node in session.get_inputs()]
    output_name = session.get_outputs()[0].name
    
    input_dict = {
        input_name[0]: patch_a,
        input_name[1]: patch_b
    }

    outputs = session.run([output_name], input_dict)
    output_image = outputs[0][0]
    output_path = postprocess(output_image)
    return base_dir / 'staticfiles' / 'images' / 'results' / output_path

# api
def png_to_base64(png_file_path):
    """
    Convert a PNG image file to a Base64 encoded string.

    :param png_file_path: Path to the PNG image file
    :return: Base64 encoded string of the image
    """
    try:
        # Use pathlib to handle the file path
        png_path = Path(png_file_path)

        # Check if the file exists
        if not png_path.is_file():
            raise FileNotFoundError(f"The file {png_path} does not exist.")

        # Read the image file in binary mode
        with png_path.open("rb") as image_file:
            # Encode the binary data to Base64
            base64_encoded = base64.b64encode(image_file.read())

        # Convert the Base64 bytes to a string
        base64_string = base64_encoded.decode('utf-8')
        return base64_string

    except FileNotFoundError as fnf_err:
        print(fnf_err)
    except Exception as err:
        print(f"An error occurred: {err}")

def api_generate_image(patch_a, patch_b, model_name):
    base_dir = Path(settings.BASE_DIR)

    models = {
        'batikgan_sl': base_dir / 'app' / 'models' / 'batikgan_sl.onnx',
        'batikgan_cl': base_dir / 'app' / 'models' / 'batikgan_cl.onnx',
        'batikrvgan': base_dir / 'app' / 'models' / 'batikrvgan.onnx',    
    }

    patch_a = preprocess(patch_a)
    patch_b = preprocess(patch_b)
    
    session = ort.InferenceSession(models[model_name])
    input_name = [input_node.name for input_node in session.get_inputs()]
    output_name = session.get_outputs()[0].name
    
    input_dict = {
        input_name[0]: patch_a,
        input_name[1]: patch_b
    }

    outputs = session.run([output_name], input_dict)
    output_image = outputs[0][0]
    output_path = postprocess(output_image)
    output_path = base_dir / 'staticfiles' / 'images' / 'results' / output_path
    return png_to_base64(output_path)

