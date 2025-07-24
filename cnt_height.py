bpd = 9.2
hc = 33.0
ac = 34.1
fl= 6.9

ret = 1.3596 - 0.00386*ac *fl+ 0.0064 *hc+ 0.0424 *ac+ 0.174 *fl
import math
print(10**ret)

ret2 = 1.07 * (hc*ac*fl)**0.31
print(ret2)

