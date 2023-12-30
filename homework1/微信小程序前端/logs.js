// logs.js
Page({
  data: {
    image: '',
    message: '',
  },
  takePhoto: function() {
    const ctx = wx.createCameraContext();
    ctx.takePhoto({
      quality: 'high',
      success: (res) => {
        this.setData({
          image: res.tempImagePath
        });
      }
    });
  },
  chooseImage:function(){
    var that = this;
    wx.chooseImage({
      count:1,
      success:function(res){
        var tempFilePath = res.tempFilePaths[0];
        that.setData({
          image:tempFilePath,
        });
      }
    });
  },
  onMessageInput: function(e) {
    this.setData({
      message: e.detail.value
    });
  },
  encryptMessage: function(message) {
    // 简单加扰加密，参考jpeg字段 (0x000000F0)
    let encryptedMessage = '';
    for (let i = 0; i < message.length; i++) {
      encryptedMessage += String.fromCharCode(message.charCodeAt(i) ^ 0xF0);
    }
    return encryptedMessage;
    //return message;
  },
  sendMessage: function() {
    // 对消息进行加扰加密
    let message = this.data.message;
    let encryptedMessage = this.encryptMessage(message);
    
    // 发送加密后的消息和图片
    wx.uploadFile({
      url: 'https://syx.mynatapp.cc/',
      filePath: this.data.image,
      name: 'image',
      formData: {
        message: encryptedMessage,
      },
      success: (res) => {
        console.log("success上传图片")
        console.log(res.data)
      },
      fail: (err) => {
        console.log("上传失败", err); // 输出上传失败的错误信息
      }
    })
  }
  
  
  
  
  
  
});
