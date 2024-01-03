# code done by team Hai, Phuong, Long, Khanh, Phat
from gekko import GEKKO
import numpy as np

# Số lượng phần tử trong các ma trận (m, n cần được xác định)
m, n = 5, 8  # Ví dụ, m = 5 và n = 8

# Khởi tạo mô hình
model = GEKKO(remote=False)

# Khởi tạo tham số với giá trị ngẫu nhiên (tuân theo các điều kiện đã nêu), các giá trị sẽ 0<=variables<=10
b = np.random.randint(0, 10, m)
s = np.random.randint(0, 10, m)

#tạo b>s
b = np.maximum(b, np.max(s, axis=0) + 1)
l = np.random.randint(0, 10, n)
q = np.random.randint(0, 10, n)

#tạo q>l
q = np.maximum(q, l + 1)
a = np.random.randint(0, 10, (n, m))
d = np.random.randint(0, 10, (2, n))

#cho giá trị x here-and-now, khởi tạo là biến random với giá trị 0<=x<=100
x = np.random.randint(0, 100, n)

# Khởi tạo biến
# x = [model.Var(lb=0) for i in range(m)]
y = [[model.Var(lb=0) for j in range(m)] for i in range(2)]
z = [[model.Var(lb=0) for j in range(n)] for i in range(2)]

# Xây dựng hàm mục tiêu
obj = sum([x[i] * b[i] for i in range(m)])
obj += sum([0.5 * (sum([(l[i] - q[i]) * z[h][i] for i in range(n)]) -
                   sum([s[j] * y[h][j] for j in range(m)])) for h in range(2)])

# constraint của mô hình
for i in range(2):
    for j in range(n):
        model.Equation(z[i][j] <= d[i][j])

for h in range(2):
    for j in range(m):
        model.Equation([y[h][j] == x[j] - sum(a[i][j] * z[h][i] for i in range(n))])  # Minimize objective



try:
    #giải mô hình
    model.Minimize(obj)
    model.options.IMODE = 1  # Tối ưu liên tục
    model.solve(disp=True)
    z_result = [[z[h][i].value[0] for i in range(n)] for h in range(2)]
    z_avg = []
    for i in range(n):
        z_avg.append((z_result[0][i] + z_result[1][i]) / 2)
    y_avg = []
    for i in range(m):
        y_avg.append((y[0][i] + y[1][i]) / 2)

    # in ra giá trị ngẫu nhiên
    print("The value of b:")
    print(b)
    print("\n")
    print("The value of l:")
    print(l)
    print("\n")
    print("The value of q:")
    print(q)
    print("\n")
    print("The value of s:")
    print(s)
    print("\n")
    print("The value of a:")
    print(a)
    print("\n")
    print("The value of d:")
    print(d)
    print("\n")
    # Hiện thị kết quả các biến quyết định
    print("The value of x:")
    print(x)
    print("\n")
    print("The value of y in the 1st scenario:")
    print(y[0])
    print("\n")
    print(z[0])
    print("The value of z in the 1st scenario:")
    print(z_result[0])
    print("\n")
    print("The value of y in the 2st scenario:")
    print(y[1])
    print("\n")
    print("The value of y in the 2st scenario:")
    print(z_result[1])
    print("\n")
    print("The average value of y:")
    print(y_avg)
    print("\n")
    print("The average value of z:")
    print(z_avg)
except:
    print("Solution Not Found")
