import requests
import sys

# コマンドライン引数でURLを受け取る
if len(sys.argv) < 2:
    print("Usage: python _test_api_request.py <URL>")
    sys.exit(0)

url = sys.argv[1].rstrip('/') + "/api/extract_placeholders"

payload = {
    "bucket_name": "my-excel-storage-bucket",
    "object_key": "sample_before_replace_template1.xlsx"
}

response = requests.post(url, json=payload)

# レスポンスの詳細を確認
print(f"Status Code: {response.status_code}")
print(f"Response Text: {response.text}")

# JSON形式のレスポンスの場合のみJSONパース
try:
    response_json = response.json()
    print(response_json)
except requests.exceptions.JSONDecodeError:
    print("The response is not in JSON format.")

