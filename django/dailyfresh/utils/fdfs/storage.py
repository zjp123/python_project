from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client


class FdfsStorage(Storage):

    def _open(self, name):
        ''' 打开图片时调用'''
        pass

    def _save(self, name, content):
        ''' 上传图片时调用'''
        # name 上传图片的名字
        # content 包含上传图片内容的File对象

        # 创建一个上传对象
        client = Fdfs_client('./utils/fdfs/client.conf')
        # 上传到fdfs系统中
        res = client.upload_by_buffer(content.read())
        if res.get('Status') != 'Upload successed.':
            raise Exception('上传失败')

        filename = res.get('Remote file_id')

        return filename

    def exists(self, name):
        '''判断文件吗是否可用 实际判断不了，因为不在django服务器中'''
        return  False

    def url(self, name):

        '''返回文件url的路径'''
        return 'http://172.16.68.147:8888/'+name