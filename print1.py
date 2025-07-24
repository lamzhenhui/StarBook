# 给定的测量值
bpd = 9.2
hc = 33.0
ac = 34.1
fl = 6.9

# Hadlock公式计算胎儿体重
estimated_weight = 1.02 * (ac * bpd * fl) ** 0.425 * (hc) ** 0.3

print(f"估算的胎儿体重: {estimated_weight:.2f} 克")