# 从命令行获得图片路径，压缩比率
# 压缩图片
# 将图片存储到命令行指定的位置
import argparse
# 创建解析器
parser = argparse.ArgumentParser()
# 添加参数选项
# 必写属性（位置属性）
parser.add_argument('imagePath', type=str, help='the path of the image')
parser.add_argument('scale', type=int, help='Compression Scale')
# 可选属性
parser.add_argument('-t', '--targetPath',\
                    type=str, help='the path of target')
# 解析命令行参数，返回一个命名空间， 如果想要使用变量，可用args.attr
args = parser.parse_args()
content = args.__dict__
for key, value in content.items():
    print('%s = %s' % (key, value))

# 获取图片路径
imagePath = content['imagePath']

# 获取目录下所有文件nn
import os.path
def getFileList(path, fileList):
    newPath = path
    if(os.path.isfile(path)):  # 如果该路径是文件
        fileList.append(path)  # 将该文件添加到列表
    elif(os.path.isdir(path)): # 如果该路径是目录
        for s in os.listdir(path): # 扫描该目录下的所有子目录
            newPath = os.path.join(path, s) # 原路径和子目录结合成新的路径
            # 递归遍历文件夹下所有子文件夹
            getFileList(newPath, fileList)
    return fileList

fileList = []
fileList =getFileList(imagePath, fileList)
print(fileList)

# 从文件列表中选出图片文件（.jpg或.png结尾）
import re
imageFileList = []
for item in fileList:
    pattern = re.compile(r'.*\.jpg\b')
    pic = re.findall(pattern, item) #利用正则表达式寻找.jpg结尾的文件
    if(pic):
        imageFileList.append(item)
    else:
        pic = re.findall(r'.*\.png\b', item) # 寻找.png结尾的文件
        if(pic):
            imageFileList.append(item)
print(imageFileList)

# 对每张图片都按照预定的比率进行压缩，并存储
scale = content['scale']
from PIL import Image
import math
index = 0
for im_path in imageFileList:
    im = Image.open(im_path) # 打开图片
    width, height = im.size  # 获取宽高
    # 压缩图片
    im_new = im.resize((math.floor(width/scale), \
                        math.floor(height/scale)))
    if(content['targetPath'] == None):# 如果未输入目标存储位置
        # 将图片保存在当前目录
        im_new.save(str(index)+'.png')# 以png格式保存缩略图
    else:
        objPath = content['targetPath']
        if(os.path.exists(objPath)):# 如果输入的目标存储路径存在
            im_new.save(os.path.join(objPath, str(index)+'.png'))
        else:# 如果目标路径不存在
            os.makedirs(objPath) # 创建目录
            print(u'目标存储路径不存在，已为之创建目录')
            im_new.save(os.path.join(objPath, str(index)+'.png'))
    index += 1
print(u'图片压缩完毕')
