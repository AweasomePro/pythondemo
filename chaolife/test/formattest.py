class User():
    def __init__(self,name,age):
        self.name = name
        self.age = age

xiaoming = User('小明',12)

print(xiaoming.name,xiaoming.age)
res =  '{name},hsh{age},{test}'.format_map(vars(xiaoming),)
print(res)