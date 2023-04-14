from core import process, predict

#原始文件的路径、检测模型、文件类型是否符合标准ext
# id part
def c_main(path, model, ext):
    # image_data包含data_path（文件路径）, file_name（文件名）
    # 原始文件路径
    image_data = process.pre_process(path)
    # type：int；检测目标的大小，
    # image_info = predict.predict(image_data, model, ext)
    img_z, image_info, id_info = predict.predict(image_data, model, ext)
    # 得到文件的新的文件名，预测后的图片信息
    # return image_data[1] + '.' + ext, image_info
    return image_data[1] + '.' + ext, img_z, image_info,id_info

# menu part
def b_main(path,model,ext):
    image_data = process.pre_process(path)
    img_z, image_info = predict.predict_main(image_data, model, ext)
    return image_data[1] + '.' + ext, img_z, image_info

# receipt part
def a_main(path,model,ext):
    image_data = process.pre_process(path)
    img_z, image_info ,receipt_info= predict.predict_receipt(image_data, model, ext)
    return image_data[1] + '.' + ext, img_z, image_info, receipt_info

# ticket part
def d_main(path,model,ext):
    image_data = process.pre_process(path)
    img_z, image_info ,ticket_info= predict.predict_ticket(image_data, model, ext)
    return image_data[1] + '.' + ext, img_z, image_info, ticket_info

# business part
def e_main(path,model,ext):
    image_data = process.pre_process(path)
    img_z, image_info, business_info = predict.predict_business(image_data, model, ext)
    return image_data[1] + '.' + ext, img_z, image_info, business_info



if __name__ == '__main__':
    pass
