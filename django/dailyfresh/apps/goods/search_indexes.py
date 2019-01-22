from haystack import indexes
# 导入模型类  需要以这个表中的数据来做
from goods.models import GoodsSKU
#指定对于某个类的某些数据建立索引
class GoodsSKUIndex(indexes.SearchIndex, indexes.Indexable):
    # 配置项 text 指的是索引字段  use_template=True 指定表中哪些字段来创建索引数据文件  是一个说明放在一个文件中
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        # 返回模型类
        return GoodsSKU

    # 建立索引所需要的数据
    def index_queryset(self, using=None):
        return self.get_model().objects.all()