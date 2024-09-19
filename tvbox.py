import boto3
from botocore.exceptions import NoCredentialsError
import os
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import sys

def delete_all_files_in_s3_bucket(bucket):
    """从 S3 桶中删除所有文件。

    :param bucket: S3 桶的名称
    :return: None
    """
    try:
        # 列出桶中的所有对象
        response = s3.list_objects_v2(Bucket=bucket)

        # 检查桶是否为空
        if 'Contents' not in response:
            print(f"桶 {bucket} 是空的，没有文件可以删除。")
            return

        # 收集要删除的对象
        objects_to_delete = [{'Key': obj['Key']} for obj in response['Contents']]

        for obj in objects_to_delete:
            # 删除对象
            s3.delete_object(Bucket=bucket, Key=obj['Key'])
            print(f"已成功删除 {obj['Key']} 。")

    except NoCredentialsError:
        print("凭证未找到")
    except Exception as e:
        print(f"删除失败: {e}")


def upload_file_to_s3(file_name, bucket, object_name=None):
    resp = s3.put_object(Bucket=bucket,
    Key=file_name, Body=open('tvbox/'+file_name, 'rb').read(), StorageClass='STANDARD')
    print(file_name + '上传成功')

def getdown(param):
    page = param.split("https://t.me/tvboxjk/")[1]
    url = f"https://tg.i-c-a.su/rss/tvboxjk?id={page}&limit=1"
    response = requests.get(url)
    tree = ET.ElementTree(ET.fromstring(response.text))
    root = tree.getroot()
    item = root.findall("channel")[0].find("item")
    return item.find("enclosure").attrib["url"]


def getData():
    data_list = []
    response = requests.get('https://tg.i-c-a.su/rss/TVBoxjkou/1')
    tree = ET.ElementTree(ET.fromstring(response.text))
    root = tree.getroot()
    for item in root.findall("channel")[0].findall("item"):
        data = {}
        title = item.find("title")
        if "软件名称" in title.text:
            data["title"] = title.text.replace("[Photo] ", "")
            cont_arr = item.find("description").text.split("\n<br />")
            soup = BeautifulSoup(cont_arr[len(cont_arr) - 1], 'html.parser')
            downurl = getdown(soup.find("a").attrs['href'])
            data["href"] = downurl
            data_list.append(data)
    return data_list


def download_ob(titile,url):
    response = requests.get(url)
    if response.status_code == 200:
        # 从 URL 中提取文件扩展名
        file_extension = url.split('.')[-1]

        # 构建文件名
        filename = f"{titile}.{file_extension}"
        # 保存图片
        with open('tvbox/'+filename, 'wb') as file:
            file.write(response.content)
        return filename
    else:
        return False


if __name__ == '__main__':

    # 检查传入的参数

    for i, arg in enumerate(sys.argv[1:], start=1):
        if i ==1:
            ACCESS_KEY = arg
        elif i ==2:
            SECRET_KEY = arg
        else:
            ENDPORT = arg
    BUCKET = 'fyy-tvbox'
    s3 = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        # 下面给出一个endpoint_url的例子
        endpoint_url=ENDPORT
    )
    if not os.path.exists("tvbox"):
        os.makedirs("tvbox")
    delete_all_files_in_s3_bucket(BUCKET)
    data_list = getData()
    for dat in data_list:
        file_name = download_ob(dat["title"],dat["href"])
        upload_file_to_s3(file_name, BUCKET)
