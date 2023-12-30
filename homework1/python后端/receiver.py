from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse

app = FastAPI()


@app.post("/")
async def upload_image(image: UploadFile = File(...), message: str = Form()):
    # 将上传的图片保存到本地
    file_bytes = image.file.read()
    tempfile = 'syx.jpg'
    with open(tempfile, 'wb') as f:
        f.write(file_bytes)

    # 对消息进行解密并打印出来
    decrypted_message = decrypt_message(message)
    print('解密后的消息：', decrypted_message)


    file_path =  r'C:/Users/jiang/PycharmProjects/pythonProject_syx/text.txt'


    save_str_to_file(decrypted_message, file_path)

    # 返回一个 JSON 响应
    return JSONResponse(content={'result': 'OK'})



# 解密函数
def decrypt_message(encrypted_message):
    decrypted_message = ''
    for char in encrypted_message:
        decrypted_message += chr(ord(char) ^ 0xF0)
    return decrypted_message

def save_str_to_file(string, file_path):
    with open(file_path, 'w') as file:
        file.write(string)



