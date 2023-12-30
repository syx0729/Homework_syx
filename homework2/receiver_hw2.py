from fastapi import FastAPI, File, UploadFile, Response, Form
from fastapi.responses import JSONResponse
import os
import time
import httpx

app = FastAPI()

@app.post("/")
async def upload_image(image: UploadFile = File(...), message: str = Form()):
    global save_path
    # 将上传的图片保存到本地
    file_bytes = image.file.read()
    image_path = r'./upload/images'
    if not os.path.exists(image_path):
        os.makedirs(image_path)

    image_name = 'syx_image'
    save_path = os.path.join(image_path, image_name)

    with open(save_path, 'wb') as f:
        f.write(file_bytes)

    # 对消息进行解密并打印出来
    decrypted_message = decrypt_message(message)
    print('解密后的消息：', decrypted_message)

    text_path = r'upload/message'
    if not os.path.exists(text_path):
        os.makedirs(text_path)

    text_path = os.path.join(text_path, 'text.txt')
    with open(text_path, 'wb') as file:
        file.write(decrypted_message.encode('unicode_escape'))

    image_server_url = 'http://192.168.1.17:8001/upload_image'
    image_response = httpx.post(image_server_url, files={'image': file_bytes})
    text_server_url = 'http://192.168.1.17:8002/upload_text'
    text_response = httpx.post(text_server_url, data={'message': decrypted_message})

    # 返回一个 JSON 响应
    return JSONResponse(content={
        'result': 'OK',
        'text_server_response': text_response.json(),
        'image_server_response': image_response.json()
    })


# 解密函数
def decrypt_message(encrypted_message):
    decrypted_message = ''
    for char in encrypted_message:
        decrypted_message += chr(ord(char) ^ 0xF0)
    return decrypted_message



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="192.168.1.17", port=8000)
