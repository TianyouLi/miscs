#include <iostream>

class A {
public:
    virtual int v(int i) { return i + 3; };
    virtual int vv(int i) { return i + 7; };
    int r(int i) { return i + 2 ; }
};


class B: public A {
public:
    int vv(int i) override { return i + 11; };
};


class C: public B {
public:
    int v(int i) override { return i + 3; };
};


void testA() {
    C c;
    A *a = &c;
    int total = 0;
    for (int i = 0; i < 2000000000; i++) {
        total += a->v(i);
        total += a->r(i);
    }
    std::cout << total;
}


void testB() {
    C c;
    A *a = &c;
    int total = 0;
    for (int i = 0; i < 1000000000; i++) {
        int k = i % 11;
        switch (total % 5) {
            case 0: total += (a->r(k)); break;
            case 1: total += (a->v(k)); break;
            case 2: total += (a->r(k)); break;
            case 3: total += (a->vv(k)); break;
            case 4: total += (a->v(k)); break;
        }
        total += a->v(i);
        total += a->r(i);
    }
    std::cout << total;
}

void testC() {
    C c;
    A *a = &c;
    int total = 0;
    for (int i = 0; i < 1000000000; i++) {
        int k = i % 11;
        switch (total % 3) {
            case 0: total += (a->vv(k)); break;
            case 1: total += (a->v(k)); break;
            case 2: total += (a->r(k)); break;
        }
        total += a->v(i);
        total += a->r(i);
    }
    std::cout << total;
}



int main() {
    testA();
    testB();
    testC();
    return 0;
}
