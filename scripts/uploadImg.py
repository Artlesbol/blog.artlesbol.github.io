import boto3
from botocore.config import Config
 
 
# 令牌值 【令牌名称root_token】
token = 'wF0gl4rrrEuRznf95woMtFVyLm3jpOlgU5rZLZnz'
# 你的 Cloudflare R2 访问密钥和秘密密钥
# 访问密钥 ID
access_key = 'd63da0ff8e3e1549d6df8ad592818bf7'
# 机密访问密钥
secret_key = '0f8cbda3bbe2321a2e474c20a4090dfe642378e8b3bb20379ca5f4dd1a1e50c4'
# 存储桶的 URL
url = 'https://28d5d85ca46fd48d3cc89291ea01fad0.r2.cloudflarestorage.com/blog'
 
 
# 创建一个 S3 客户端，这里指定了 R2 的端点
config = Config(signature_version='s3v4')
s3_client = boto3.client(
    's3',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    endpoint_url=url,
    config=config
)
# 你要上传到存储桶的名字
bucket_name = 'blog'
# 本地文件 文件名
file_path = 'MST.txt'
# 存储桶里的路径和文件名 此处可以重新命名上传后的文件名称，也可以添加文件夹
bucket_file_name = 'MST.txt'  
# 使用 S3 客户端上传文件
s3_client.upload_file(file_path, bucket_name, bucket_file_name)