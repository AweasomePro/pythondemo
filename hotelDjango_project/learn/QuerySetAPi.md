# 数据库orm操作

##注意事项：

(1). 如果只是检查 Entry 中是否有对象，应该用 Entry.objects.all().exists()

(2). QuerySet 支持切片 Entry.objects.all()[:10] 取出10条，可以节省内存

(3). 用 len(es) 可以得到Entry的数量，但是推荐用 Entry.objects.count()来查询数量，后者用的是SQL：SELECT COUNT(*)

(4). list(es) 可以强行将 QuerySet 变成 列表
4. QuerySet 是可以用pickle序列化到硬盘再读取出来的

1
2
3
4
>>> import pickle
>>> query = pickle.loads(s)     # Assuming 's' is the pickled string.
>>> qs = MyModel.objects.all()
>>> qs.query = query            # Restore the original 'query'.
5. QuerySet 查询结果排序

作者按照名称排序

1
2
Author.objects.all().order_by('name')
Author.objects.all().order_by('-name') # 在 column name 前加一个负号，可以实现倒序
6. QuerySet 支持链式查询

1
2
3
4
5
Author.objects.filter(name__contains="WeizhongTu").filter(email="tuweizhong@163.com")
Author.objects.filter(name__contains="Wei").exclude(email="tuweizhong@163.com")

# 找出名称含有abc, 但是排除年龄是23岁的
Person.objects.filter(name__contains="abc").exclude(age=23)
7. QuerySet 不支持负索引

1
2
3
4
5
6
7
8
9
Person.objects.all()[:10] 切片操作，前10条
Person.objects.all()[-10:] 会报错！！！

# 1. 使用 reverse() 解决
Person.objects.all().reverse()[:2] # 最后两条
Person.objects.all().reverse()[0] # 最后一条

# 2. 使用 order_by，在栏目名（column name）前加一个负号
Author.objects.order_by('-id')[:20] # id最大的20条

8. QuerySet 重复的问题，使用 .distinct() 去重

一般的情况下，QuerySet 中不会出来重复的，重复是很罕见的，但是当跨越多张表进行检索后，结果并到一起，可以会出来重复的值（我最近就遇到过这样的问题）

qs1 = Pathway.objects.filter(label__name='x')
qs2 = Pathway.objects.filter(reaction__name='A + B >> C')
qs3 = Pathway.objects.filter(inputer__name='WeizhongTu')

# 合并到一起
qs = qs1 | qs2 | qs3
这个时候就有可能出现重复的

# 去重方法
qs = qs.distinct()

## 官方操作文档
 https://docs.djangoproject.com/en/dev/ref/models/querysets/