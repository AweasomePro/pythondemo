## model的操作
###新建一个对象的方法有以下几种：

Person.objects.create(name=name,age=age)

p = Person(name="WZ", age=23)

p.save()

p = Person(name="TWZ")

p.age = 23

p.save()

Person.objects.get_or_create(name="WZT", age=23)

这种方法是防止重复很好的方法，但是速度要相对慢些，返回一个元组，第一个为Person对象，第二个为True或False, 新建时返回的是True, 已经存在时返回False.



###获取对象有以下方法：

Person.objects.all()

Person.objects.all()[:10] 切片操作，获取10个人，不支持负索引，切片可以节约内存

Person.objects.get(name=name)

get是用来获取一个对象的，如果需要获取满足条件的一些人，就要用到filter

Person.objects.filter(name="abc") # 等于Person.objects.filter(name__exact="abc") 名称严格等于 "abc" 的人

Person.objects.filter(name__iexact="abc") # 名称为 abc 但是不区分大小写，可以找到 ABC, Abc, aBC，这些都符合条件



Person.objects.filter(name__contains="abc") # 名称中包含 "abc"的人

Person.objects.filter(name__icontains="abc") #名称中包含 "abc"，且abc不区分大小写



Person.objects.filter(name__regex="^abc") # 正则表达式查询

Person.objects.filter(name__iregex="^abc")# 正则表达式不区分大小写



filter是找出满足条件的，当然也有排除符合某条件的

Person.objects.exclude(name__contains="WZ") # 排除包含 WZ 的Person对象

Person.objects.filter(name__contains="abc").exclude(age=23) # 找出名称含有abc, 但是排除年龄是23岁的