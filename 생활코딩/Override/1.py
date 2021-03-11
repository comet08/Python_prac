class C1:
    def m(self):
        return 'parent'

class C2(C1):
    def m(self):

        return 'child' +  super().m()

o = C2()
print(o.m())