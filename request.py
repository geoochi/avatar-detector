import requests

files = {'image': open('avatar1.png', 'rb')}
response = requests.post('http://127.0.0.1:5000/detect_avatar', files=files)

if response.status_code == 200:
    with open('result.jpg', 'wb') as f:
        f.write(response.content)
else:
    print(f'Error: {response.status_code}')
    print(response.text)
