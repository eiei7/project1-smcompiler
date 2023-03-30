import matplotlib.pyplot as plt

# 设置全局字体
plt.rc('font', family='Times New Roman')

# 字体大小
font_size = 30

# 数据
left_num = [2, 4, 8, 16]
right_num = [1, 3, 5, 7]
comm_cost_request_left = [0.858, 1.542, 2.910, 5.642]
comm_cost_response_left = [1.146, 2.742, 5.478, 10.942]

comm_cost_request_right = [1.884, 1.882, 1.882, 1.880]
comm_cost_response_right = [3.426, 3.422, 3.422, 3.418]

plt.figure(figsize=(17, 6))
ax = plt.subplot(121)

plt.plot(left_num, comm_cost_request_left, linewidth=3, color='r', label="Request", marker='o', markersize=8)
plt.plot(left_num, comm_cost_response_left, linewidth=3, color='b', label="Response", marker='v', markersize=8)

# 线标签放置在坐上方
plt.legend(loc="upper left", fontsize=font_size)

# 设置坐标轴标签字号
plt.xticks(fontsize=font_size)
plt.yticks(fontsize=font_size)

# 设置坐标轴标签大小
ax.set_xlabel(..., fontsize=font_size)
ax.set_ylabel(..., fontsize=font_size)

# 坐标轴标签
plt.xlabel("Number of multiplication operations")
plt.ylabel("Comm-cost (kilo-bytes)")

ax = plt.subplot(122)
plt.plot(right_num, comm_cost_request_right, linewidth=3, color='r', label="Request", marker='o', markersize=8)
plt.plot(right_num, comm_cost_response_right, linewidth=3, color='b', label="Response", marker='v', markersize=8)
plt.ylim(0, 6.0)

# 线标签放置在坐上方
plt.legend(loc="upper left", fontsize=font_size)

# 设置坐标轴标签字号
plt.xticks(fontsize=font_size)
plt.yticks(fontsize=font_size)

# 设置坐标轴标签大小
ax.set_xlabel(..., fontsize=font_size)
ax.set_ylabel(..., fontsize=font_size)

# 坐标轴标签
plt.xlabel("Number of Scalars")
plt.ylabel("")

plt.subplots_adjust(top=0.95, bottom=0.16, left=0.07, right=0.994, hspace=0, wspace=0.15)
# 保存文件
plt.savefig('communication_cost_res_mul_increase_scalar_increase.png', dpi=600)
plt.show()
