# -*- coding: utf-8 -*-
answer = lambda C: sorted([(a, b, C-(120*a + 75*b)) for a in range(C//120 + 1) for b in range(C//75 + 1) if (120*a + 75*b) <= C], key=lambda x: x[2])[0]
print("a={}, b={} 时余额最少（为{}元）".format(answer(5000)[0], answer(5000)[1], answer(5000)[2]))
