from bs4 import BeautifulSoup
from google.cloud import storage
from google.oauth2 import service_account
import requests
import csv

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

credentials_dict = {
  "type": "service_account",
  "project_id": "bright-task-382122",
  "private_key_id": "44973ecdffc1b9762536c9f650f6ed0d9063fe9a",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDcV4l1N4NxZvNL\n9av6gbD4ZQFAhKGXVKK6Oixwv3fRhR23A3EXzypBYsneIS5VeLGJ6p+IAu39Q+jo\ngfay6fKKoNOoiw1okaS0qwL+lJEljRWX2W4m3v8kYdLAxCusCtt5gYFl3HJKwshz\nc+HRwkjyJXKSJRqVIHgssHrl0xPC9g/6k7Dw2p0k65wjgRFbYldnK6fwXdQ11Y3l\nWvzj7X9YxFNpwNX/NU89aZ8ETpmxbPUolr9xOiDDoMnioApWh/SqwcvTYiEgRrRy\nGPGtzFf31aN0H7+wND/HBnbogRulUgvQePI8xycIBICxLV2D2LNFSsjXWvbnKRmU\ng0QvtqvhAgMBAAECggEAE43RLQ3YJGA2hy8uK/UGd4S/L7KVhJCGQHCZMQhM4dMm\nZ+9uQeaooVTbBVN8gSlM2ChyL+fSpv831Cp0cjxAwfyzy+lLL1R9gWsLwPv+RY7X\ns7ogBGMV0Wy8/05pccMk5wuPKDMAEZJnp5dJGwxa3OJl4IJacZGIGK8wuOSahFqX\nors+AlAZbjbGP39PMbfK+87IvCiLRZ53UhtR6rZBtqypH3JsDolbn16eXSzCoAXy\nQoDUIf2SQ7Tb5334Zqe6yXjlrbs6N9SXWHz5cw4dwPkAcIt6XRscCOBjRwoGl2OT\nIzpSPrvozBReYW/Sz4Rc8xaq67ED+lurgfpMldzs4QKBgQD9OIDJKq0DPFAW76iP\n+1+p+dRNxws7iz/8zk49nTKMrMfFUAaKbDnrtPvMU9Yf3lE0/Se6gys5a34P81FD\nbTh/ZKRA7j/cJayxWtk7B/wIue43VzJskmj+R2FFesZns7dnNX6NMOyKL8hHak7i\n4nkrQo9kf1Qu5ov1yJLOVUSYHwKBgQDewqbEqyWwhPHyyqpvBNpT07vcrEJsYOmC\nRnissy3me3bA+pWE7fIjabHiXklMiotGqhC1OVbnSbygCaKW0VwSRZnh7pn/H0aX\n0bBPeMKKcKpw+YqZhGAoUmCyVY0HsF1Cw+/xJf4y2nkIx3nvNxDPKl0bs2hWHYEQ\nLkfaNCw7/wKBgAqPSaeZ9P8Wi8x5EBF5DSM8fOMFcu13wCJdxBuDq7D8H5SV4r/x\nBXVT5dA+isZncgGAsSBxCeNqHSazIedq7Zk6bDMc/GLE22/F9xskGRmQD2QVac/n\nRyObfG32UcHPV82hCHcA3Exi87our718bkskinBJcwxFpv6H779VBPhHAoGAPDoW\nir/XLdWT8NfYorGGMfniJfSw9Mpy99UD1XWQaGtjHSPi/xCyUd7GyHRDjx06ML3U\nTJsXIuttwzs3qV0rbolA5LP1EOQs2ulHqQT2XCW//1GIpp8CvIQhPrYgrj6ByIZf\nPizOgINPDA+aqRGTSt+iUtX71KSfe3d318gZWZMCgYBkXUf9rFCFOnpiSJiS1w/w\nrK47uTLzMtIjEK8cwd1IPczZM0jhrDEhiF8/DLdpfJ56xtrAbwkJL3Ok4CuMLDBS\nYJrZFbG1ocgczVjVSt4pY+EegV/vu4xKyjLF9oAa2/v+udqs8kxFSu6zkw6IAhya\niIsKWUf82qgQpUNUUYDRuQ==\n-----END PRIVATE KEY-----\n",
  "client_email": "aula-dataops@bright-task-382122.iam.gserviceaccount.com",
  "client_id": "112974487934322782561",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/aula-dataops%40bright-task-382122.iam.gserviceaccount.com"

}

try:

  """Uploads a file to the bucket."""
  credentials = service_account.Credentials.from_service_account_info(credentials_dict)
  storage_client = storage.Client(credentials=credentials)
  bucket = storage_client.get_bucket('atividade4') ### Nome do seu bucket
  blob = bucket.blob('artist-names.csv')

  pages = []
  names = "Name \n"

  for i in range(1, 5):
    url = 'https://web.archive.org/web/20121007172955/https://www.nga.gov/collection/anZ' + str(i) + '.htm'
    pages.append(url)

  for item in pages:
    page = requests.get(item)
    soup = BeautifulSoup(page.text, 'html.parser')

    last_links = soup.find(class_='AlphaNav')
    last_links.decompose()

    artist_name_list = soup.find(class_='BodyText')
    artist_name_list_items = artist_name_list.find_all('a')

    for artist_name in artist_name_list_items:
      names = names + artist_name.contents[0] + "\n"

    blob.upload_from_string(names, content_type="text/csv")

except Exception as ex:
  print(ex) 
