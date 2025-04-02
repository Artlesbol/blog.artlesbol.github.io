import boto3
from botocore.config import Config
import os
import re

# 从 r2_key.yaml 文件中加载 R2 配置信息
import yaml

r2_key_path = f"{os.path.dirname(__file__)}/r2_key.yaml"

with open(r2_key_path, 'r', encoding='utf-8') as key_file:
    r2_config = yaml.safe_load(key_file)

access_key = r2_config['access_key']
secret_key = r2_config['secret_key']
url = r2_config['url']

visit_url = 'https://r2.artlesbol.top'
bucket_name = 'blog'

# 创建 S3 客户端
config = Config(signature_version='s3v4')
s3_client = boto3.client(
    's3',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    endpoint_url=url,
    config=config
)


def upload_to_r2(local_file_path, bucket_file_name):
    """上传文件到 R2"""
    try:
        s3_client.upload_file(local_file_path, bucket_name, bucket_file_name)
        print(f"Uploaded {local_file_path} to {bucket_file_name}")
        return f"{visit_url}/{bucket_name}/{bucket_file_name}"
    except Exception as e:
        print(f"Failed to upload {local_file_path}: {e}")
        return None

def process_directory(base_dir):
    """遍历目录并处理 attachment 文件夹和 .md 文件"""
    for root, dirs, files in os.walk(base_dir):
        if 'attachment' in dirs:
            attachment_dir = os.path.join(root, 'attachment')
            md_files = [f for f in files if f.endswith('.md')]

            # 上传 attachment 目录中的文件
            for file_name in os.listdir(attachment_dir):
                local_file_path = os.path.join(attachment_dir, file_name)
                bucket_file_name = f"content/img/{file_name}"
                bucket_file_name = bucket_file_name.replace("\\", "/")  # 替换为 R2 兼容路径
                r2_url = upload_to_r2(local_file_path, bucket_file_name)
                print(r2_url)

                # 替换同级 .md 文件中的图片路径
                if r2_url:
                    for md_file in md_files:
                        md_file_path = os.path.join(root, md_file)
                        replace_image_path(md_file_path, file_name, r2_url)

def replace_image_path(md_file_path, file_name, r2_url):
    """替换 .md 文件中的图片路径为 R2 路径"""
    try:
        with open(md_file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 替换图片路径
        updated_content = re.sub(
            #匹配图片路径，如：img src="attachment/d8fc267508bb5e274aaf90b19d486d3d.webp"
            fr'img src="attachment/{file_name}"',
            f'img src="{r2_url}"',
            content
        )

        with open(md_file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        print(f"Updated image path in {md_file_path}")
    except Exception as e:
        print(f"Failed to update {md_file_path}: {e}")

if __name__ == "__main__":
    content_dir = os.path.join(os.path.dirname(__file__), "../content")
    process_directory(content_dir)