import cv2

# 预测图片和数据
def predict(dataset, model, ext):
    global img_y
    # 把中文的文件名转化为python可读文件名
    x = dataset[0].replace('\\', '/')
    y = x
    file_name = dataset[1]
    print(x)
    print(file_name)
    x = cv2.imread(x)
    # ima_y预测图片；image_info预测图片的信息（放入表格中）
    # img_y, image_info = model.init_model(y)
    # image_info排除
    img_y, image_info, id_info = model.init_model(y)

    # 将预测后的图片放置tmp/draw中
    # "{} {}".format("hello", "world")    ： 不设置指定位置，按默认顺序
    # 'hello world'
    # 把img_y写到文件夹中
    # if cv2.imwrite('./tmp/draw/{}.{}'.format(file_name, ext), img_y):
    #     raise Exception('保存图片时出错.Error saving the picture.')
    img_z = cv2.imwrite('./tmp/draw/{}.{}'.format(file_name, ext), img_y)
    # return image_info
    return img_z,image_info, id_info

def predict_main(dataset, model, ext):
    global img_y
    x = dataset[0].replace('\\', '/')
    y = x
    file_name = dataset[1]
    print(x)
    print(file_name)
    x = cv2.imread(x)
    img_y, image_info = model.main_model(y)
    img_z = cv2.imwrite('./tmp/draw/{}.{}'.format(file_name, ext), img_y)
    return img_z, image_info

def predict_receipt(dataset, model, ext):
    global img_y
    x = dataset[0].replace('\\', '/')
    y = x
    file_name = dataset[1]
    print(x)
    print(file_name)
    x = cv2.imread(x)
    img_y, image_info, receipt_info = model.fapiao__model(y)
    img_z = cv2.imwrite('./tmp/draw/{}.{}'.format(file_name, ext), img_y)
    return img_z, image_info , receipt_info

def predict_ticket(dataset, model, ext):
    global img_y
    x = dataset[0].replace('\\', '/')
    y = x
    file_name = dataset[1]
    print(x)
    print(file_name)
    x = cv2.imread(x)
    img_y, image_info, ticket_info = model.ticket__model(y)
    img_z = cv2.imwrite('./tmp/draw/{}.{}'.format(file_name, ext), img_y)
    return img_z, image_info , ticket_info

def predict_business(dataset, model, ext):
    global img_y
    x = dataset[0].replace('\\', '/')
    y = x
    file_name = dataset[1]
    print(x)
    print(file_name)
    x = cv2.imread(x)
    img_y, image_info, business_info = model.business__model(y)
    img_z = cv2.imwrite('./tmp/draw/{}.{}'.format(file_name, ext), img_y)
    return img_z, image_info , business_info
