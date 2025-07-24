import matplotlib.pyplot as plt

# 创建图形
plt.figure(figsize=(3, 1), facecolor="black")  # 设置背景颜色为黑色
plt.text(0.5, 0.5, r"$Z = X' U$", fontsize=30, color="white", ha='center', va='center')

# 隐藏坐标轴
plt.axis("off")

# 保存图像
plt.savefig("pca_equation.png", dpi=300, bbox_inches='tight', facecolor="black")

# 显示图像
plt.show()