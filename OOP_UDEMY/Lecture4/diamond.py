class A:
    def method(self):
        print("This method belongs to A")

class B(A):
    def method(self):
        print("This method belongs to B")

class C(A):
    def method(self):
        print("This method belongs to C")

# the method calls depends upon the method overriding order.
class D(B,C):
    pass

d = D()
d.method()