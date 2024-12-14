import requests

base_url = "http://192.168.1.103:8001"
# GET /api/home
response_get = requests.get(base_url+"/api/home")
print("GET Response:", response_get.status_code, response_get.text)

# POST /api/retrieve
data_retrieve = {"index": 1}
response_post_retrieve = requests.post(
    base_url+"/api/retrieve",
    json=data_retrieve
)
print("POST Response (retrieve):", response_post_retrieve.status_code, response_post_retrieve.text)

# POST /api/generate
data_generate = {
    "patch_a": 1,
    "patch_b": 2,
    "model": ["batikgan_cl", "batikgan_sl"]
}
response_post_generate = requests.post(
    base_url+"/api/generate",
    json=data_generate
)
print("POST Response (generate):", response_post_generate.status_code, response_post_generate.text)
