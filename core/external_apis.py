from io import BytesIO

import requests


def download_file(file_url, headers=None):
    """
    download file
    :param file_url:
    :param headers:
    :return:
    """
    response = requests.get(file_url, headers=headers)
    response.raise_for_status()
    return BytesIO(response.content)


def upload_file(files, headers=None):
    """
    upload file
    :param files:
    :param headers:
    :return:
    """
    response = requests.post(f'{FILE_URL}/upload/doc',
                             files=files, headers=headers)
    response.raise_for_status()
    return response.json().get('url')
