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