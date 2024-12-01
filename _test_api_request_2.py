import requests
import sys

# コマンドライン引数でURLを受け取る
if len(sys.argv) < 2:
    print("Usage: python _test_api_request.py <URL>")
    sys.exit(0)

url = sys.argv[1].rstrip('/') + "/api/generate_report"

payload = {
    "output_id": 12345,
    "template_id": "12",
    "template_url":
    "https://my-excel-storage-bucket.s3.ap-northeast-1.amazonaws.com/sample_before_replace_template1.xlsx",
    "template_color": "xxx",
    "replace_info": {
        "(bk_cd1)": {
            "${chinryou_str}": ["22.6"],
            "${access_with_busstop}": ["京王バス46系 峰"],
            "${image_pos2,46,45,100%}": ["置換える文字列3", "11", "24"]
        },
        "(bk_cd2)": {
            "${置換えキー4}": ["置換える文字列4"],
            "${置換えキー5}": ["置換える文字列5"]
        }
    }
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
