import exifread
import os, time

'''
    获取文件夹中的文件信息，并依次传递入
    图片传递单元，并提供文件格式、拍摄日期
    （创建日期）、文件名等内容以供生成处理
    后的文件。
'''

import os
import exifread


def getExif(pathname, FIELD = 'EXIF DateTimeOriginal'):
    fd = open(pathname, 'rb')
    tags = exifread.process_file(fd)
    fd.close()

    if FIELD in tags:
        time_name = str(tags[FIELD]).replace(':', '').replace(' ', '_').split(".")[0]
        return True, time_name
    else:
        return False, ""


def TimeStampToTime(timestamp, asfilename=False):
    # 把时间戳转化为时间: 1479264792 to 2016-11-16 10:53:12
    timeStruct = time.localtime(timestamp)
    s=time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)
    if asfilename:
        return s.replace('-','').replace(' ','_').replace(':','')
    else:
        return s


def get_FileCreateTime(filePath, asfilename=False):
    # 获取文件的创建时间
    filePath = str(filePath)
    t = os.path.getctime(filePath)
    return TimeStampToTime(t, asfilename)


def reconstrut_filename(filePath, newPath):
    '''
    Due to the way Windows and Linux contruct the path differently,
    this function only works on Windows("C:\\1\1" "\root\1").

    1) call getExif()
    2) if 1 returns False: call get_FileCreateTime()->TimeStampToTime()
    3) collect first part(p2) name based on 1/2
    4) splice the p2 with pathname(p1) and original file name(p3)
    5) if name is duplicated, add a number(0-9) to the symbol position
       ==> p1\p2_(symbol:e for exif, p for replaced-by-timestamp)_p3
        eg.im\19700101_000000_e0_test.jpg
    6) rename old file with new name
    '''

    exif_valid, fname_p2= getExif(filePath)
    if not exif_valid:fname_p2= get_FileCreateTime(filePath, asfilename=True)

    if newPath=='':pname_p1 = '\\'.join(os.path.splitext(filePath)[0].split('\\')[0:-1])
    else:pname_p1='\\'.join(newPath.split('\\'))
    oname_p3 = os.path.splitext(filePath)[0].split('\\')[-1] + os.path.splitext(filePath)[1]
    if exif_valid:symbol_code='e'
    else:symbol_code='p'
    duplicated=0
    while duplicated<=9:
        new_name= pname_p1 + '\\' +fname_p2+'_'+symbol_code+str(duplicated)+'_'+oname_p3
        if not os.path.exists(new_name):break
        duplicated+=1
    if duplicated>9: return False
    print(filePath,new_name)
    os.rename(filePath, new_name)
    return True

'''
            
        for filename in os.listdir('.'):
            if os.path.isfile(filename):
                getExif(filename)
                '''

print(reconstrut_filename(r'C:\Users\Administrator\Desktop\Documents\python_work\cours_image\im\1.jpg'))