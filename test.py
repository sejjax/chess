class A:
    def __init__(self):
        print('A intialized')
        self.a = 'A'


class B:
    def __init__(self):
        print('B intialized')
        self.b = 'B'


class C(A, B):
    def __init__(self):
        A.__init__(self)
        B.__init__(self)
        print('C intialized')
        self.c = 'C'

        print(self.a)
        print(self.b)
        print(self.c)


C()
