import requests
import sys
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openpyxl
import boto3
import re
from io import BytesIO
from dotenv import load_dotenv
import os

# ロギングの設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# .envファイルの読み込み
load_dotenv()

# 環境変数の取得
AWS_ACCESS_KEY = os.getenv("MY_AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("MY_AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("MY_AWS_REGION", "ap-northeast-1")

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello from Vercel!"}

# Boto3クライアントの作成
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

# 正規表現でプレースホルダを見つけるパターン
PLACEHOLDER_PATTERN = re.compile(r'\$\{[a-zA-Z0-9_]+\}')

class ExtractPlaceholdersRequest(BaseModel):
    bucket_name: str
    object_key: str

@app.post("/api/extract_placeholders")
async def extract_placeholders(request: ExtractPlaceholdersRequest):
    change_key_list = {}

    try:
        logging.info(f"Extracting placeholders from bucket: {request.bucket_name}, object: {request.object_key}")
        # S3からExcelファイルを取得
        response = s3_client.get_object(Bucket=request.bucket_name, Key=request.object_key)
        excel_file = BytesIO(response['Body'].read())
        workbook = openpyxl.load_workbook(excel_file, data_only=False)

        # 各シートからプレースホルダを抽出
        for sheet_name in workbook.sheetnames:
            logging.info(f"Processing sheet: {sheet_name}")
            sheet = workbook[sheet_name]
            placeholders = set()

            # セルからプレースホルダを抽出
            for row in sheet.iter_rows():
                for cell in row:
                    if isinstance(cell.value, str):
                        found_placeholders = PLACEHOLDER_PATTERN.findall(cell.value)
                        if found_placeholders:
                            logging.info(f"Found placeholders in cell: {found_placeholders}")
                        placeholders.update(found_placeholders)

            # 図形からプレースホルダを抽出（オプション）
            if sheet._drawing is not None:
                for drawing in sheet._drawing._drawings:
                    if hasattr(drawing, 'text'):
                        found_placeholders = PLACEHOLDER_PATTERN.findall(drawing.text)
                        if found_placeholders:
                            logging.info(f"Found placeholders in drawing: {found_placeholders}")
                        placeholders.update(found_placeholders)

            if placeholders:
                change_key_list[sheet_name] = list(placeholders)

        # 成功時のレスポンス
        logging.info(f"Successfully extracted placeholders: {change_key_list}")
        return {
            "template_id": request.object_key.split('/')[-1].split('.')[0],
            "change_key_list": change_key_list
        }

    except Exception as e:
        logging.error(f"Error processing Excel file: {e}")
        # 失敗時のレスポンス
        return {
            "template_id": request.object_key.split('/')[-1].split('.')[0],
            "error": [str(e)],
            "change_key_list": {}
        }

# ローカル実行用
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

