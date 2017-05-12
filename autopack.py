# coding=utf-8
import zipfile
import shutil
import os


def delete_file_folder(src):
    '''delete files and folders'''
    if os.path.isfile(src):
        try:
            os.remove(src)
        except:
            pass
    elif os.path.isdir(src):
        for item in os.listdir(src):
            itemsrc = os.path.join(src, item)
            delete_file_folder(itemsrc)
        try:
            os.rmdir(src)
        except:
            pass


# 创建一个空文件，此文件作为apk包中的空文件
src_empty_file = 'empty.txt'
f = open(src_empty_file, 'w')
f.close()

# 在渠道号配置文件中，获取指定的渠道号
# 修改channels.txt为对应的channel文件
channelFile = open('channels.txt', 'r')
channels = channelFile.readlines()
channelFile.close()
print('-' * 20, 'all channels', '-' * 20)
print(channels)
print('-' * 50)

# 获取当前目录下所有的apk文件
src_apks = []
print '当前目录下所有文件：' + os.listdir('.')
for file in os.listdir('.'):
    if os.path.isfile(file) and not str(os.path.basename(file)).startswith('.'):  # 过滤目录下的隐藏文件
        # print '---split ' + str(os.path.split(file))
        extension = os.path.splitext(file)[1][1:]
        if extension in 'apk':
            src_apks.append(file)

# 遍历所以的apk文件，向其压缩文件中添加渠道号文件
for src_apk in src_apks:
    src_apk_file_name = os.path.basename(src_apk)
    print('current apk name:', src_apk_file_name)
    temp_list = os.path.splitext(src_apk_file_name)
    src_apk_name = temp_list[0]
    src_apk_extension = temp_list[1]

    apk_names = src_apk_name.split('-')
    # print apk_names

    output_dir = 'outputDir' + '/'
    if os.path.exists(output_dir):
        delete_file_folder(output_dir)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    # 遍历从文件中获得的所以渠道号，将其写入APK包中
    for line in channels:
        target_channel = line.strip()
        # apk包采用appName-channelName-releaseType-versionName-versionCode的格式，根据实际情况自行修改
        target_apk = output_dir + apk_names[0] + "-" + target_channel + "-" + apk_names[2] + apk_names[3] + apk_names[4] + src_apk_extension
        shutil.copy(src_apk, target_apk)
        zipped = zipfile.ZipFile(target_apk, 'a', zipfile.ZIP_DEFLATED)
        empty_channel_file = "META-INF/channel_{channel}".format(channel=target_channel)
        zipped.write(src_empty_file, empty_channel_file)
        zipped.close()

print('-' * 50)
print('repackaging is over ,total package: ', len(channels))
input('\npackage over...')
