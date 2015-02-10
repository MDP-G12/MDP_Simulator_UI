class test:
    def __init__(self):
        self.a = [1, 2]

    def func(self):
        b = self.a
        # self.a = [1, 3]
        print(b)
        print(self.a==b)

a = test()
a.func()
