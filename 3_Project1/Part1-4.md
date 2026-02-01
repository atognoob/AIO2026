
# Dự án AI: Hồi quy Tuyến tính và Hiệu suất Học tập

## 2.1 Hồi quy tuyến tính (Linear Regression) là gì?

Trong thực tế công việc hằng ngày, câu hỏi "Làm sao để dự đoán một giá trị chưa biết dựa trên những dữ liệu đã có?" là điều mà ai cũng muốn có đáp án, ví dụ như ước tính giá vàng dựa trên dữ liệu 12 tháng qua.

Hồi quy tuyến tính là phương pháp dự đoán biến phụ thuộc () dựa trên giá trị của biến độc lập () thông qua phương trình gốc: . Mối quan hệ này được biểu diễn bằng một đường thẳng. Tuy nhiên, trong thực tế, dữ liệu thường nằm rải rác quanh đường thẳng chứ không thẳng hàng hoàn hảo. Mục tiêu của chúng ta là tìm ra đường thẳng có khoảng cách đến các điểm dữ liệu thực tế là nhỏ nhất để giảm thiểu sai số.

Để tối thiểu hóa sai số, quá trình này sử dụng hai công cụ then chốt: **Thước đo sự sai lệch** và **Thuật toán tối ưu**.

### a. Thước đo sự sai lệch - Hàm mất mát (Loss Function)

Để đo lường mức độ "tệ" của đường thẳng dự báo, chúng ta thường dùng **MSE (Mean Squared Error)** – Bình phương sai số trung bình. Máy tính sẽ tính khoảng cách từ mỗi điểm đến đường thẳng, sau đó bình phương lên để loại bỏ dấu âm và nhấn mạnh các sai số lớn. Tổng các bình phương này càng nhỏ, mô hình càng khớp với thực tế.

### b. Thuật toán tối ưu - Giảm độ dốc (Gradient Descent)

Để điều chỉnh các hệ số  và  sao cho sai số giảm dần, thuật toán **Gradient Descent** được sử dụng.

* 
**Gradient (Độ dốc):** Chỉ hướng để giảm sai số.


* 
**Learning Rate (Tốc độ học) :** Độ dài mỗi bước hiệu chỉnh; nếu quá dài có thể vượt qua đáy thung lũng (điểm tối ưu), nếu quá ngắn sẽ làm tốc độ học rất chậm.



---

## 2.2 Giới thiệu về bộ dữ liệu - Hiệu Suất Học Tập Của Sinh Viên

### 2.2.0. Mục tiêu

Xây dựng mô hình Hồi quy tuyến tính để dự đoán điểm số cuối cùng (`final_score`) của sinh viên dựa trên thói quen học tập và tâm lý. Vì `final_score` là biến liên tục, đây là bài toán Hồi quy điển hình.

### 2.2.1 Tổng quan chung

* 
**Kích thước:** 1.000 bản ghi và 18 cột dữ liệu hoàn chỉnh.


* 
**Biến mục tiêu:** `final_score` (0 - 100).



2.2.2 Phân nhóm các Biến độc lập 

* 
**Nhóm Lịch sử học tập:** `previous_score`, `math_prev_score`, `science_prev_score`, `language_prev_score`.


* 
**Nhóm Hành vi học tập:** `daily_study_hours`, `attendance_percentage`, `homework_completion_rate`.


* 
**Nhóm Lối sống & Sức khỏe:** `sleep_hours`, `screen_time_hours`, `physical_activity_minutes`.


* 
**Nhóm Tâm lý:** `motivation_score`, `exam_anxiety_score`.


* 
**Nhóm Môi trường (Cần mã hóa):** `parent_education_level`, `study_environment`.



2.2.3 Các biến cần loại bỏ 

Cần loại bỏ `student_id` (không ý nghĩa thống kê), `grade` và `pass_fail` (vì chúng là hệ quả trực tiếp từ `final_score`).

---

## 2.3 Mô hình hồi quy tuyến tính đơn biến (Simple linear regression)

Kiểm tra độ tương quan (correlation) cho thấy `previous_score` ảnh hưởng lớn nhất đến `final_score` ().

**Bảng hệ số tương quan Pearson với `final_score`:**

| Biến | Pearson Correlation |
| :--- | :--- |
| **previous_score** | **0.843755** |
| math_prev_score | 0.825755 |
| science_prev_score | 0.823998 |
| language_prev_score | 0.810688 |
| attendance_percentage | 0.737720 |
| daily_study_hours | 0.357275 |
| homework_completion_rate | 0.339800 |
| motivation_score | 0.255734 |
| physical_activity_minutes | -0.044330 |
| sleep_hours | 0.032623 |
| screen_time_hours | -0.029856 |



### 2.3.1 Giải thích toán học

Phương trình mô hình:
$$y = w_1x + w_0 + \epsilon$$
Trong đó:
$y$: Giá trị cần dự đoán (Label/Target).

$x$: Dữ liệu đầu vào (Feature).

$w_1$: Hệ số góc (Weight/Slope), thể hiện mức độ ảnh hưởng của $x$ lên $y$.

$w_0$: Hệ số chặn (Bias/Intercept), là giá trị của $y$ khi $x = 0$.

$\epsilon$: Sai số ngẫu nhiên (Noise).


Để đánh giá một đường thẳng là "tốt" hay "xấu", chúng ta cần một thước đo sai số, gọi là Hàm mất mát (Loss Function).

Với mỗi điểm dữ liệu $(x_i, y_i)$, ta tính giá trị dự đoán $\hat{y}_i$:
$$\hat{y}_i = w_1x_i + w_0$$

Mục tiêu của chúng ta là tìm w1 và w0 sao cho khoảng cách giữa $\hat{y}$ (giá trị dự đoán) và y $y$ (giá trị thực tế) là nhỏ nhất

Để tính khoảng cách, ta có thể dùng MAE hoặc MSE

Trong trường hợp này, ta áp dụng MSE

Hàm mất mát theo biến w1, w0 phải đạt giá trị cực tiểu

$$L(w) = \frac{1}{2n} \sum (y - \hat{y})^2 = \frac{1}{2n} \sum (y - w_1x - w_0)^2$$


## 3.1 Tính trực tiếp

Để đạt giá trị cực tiểu, đạo hàm của hàm L(w) =0

Đạo hàm theo $w_1$: $D_{w1} = \frac{-2}{n} \sum_{i=1}^{n} x_i(y_i - \hat{y}_i) =0$

Đạo hàm theo $w_0$: $D_{w0} = \frac{-2}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i) =0$ 

$$\Leftrightarrow w_0 = \bar{y} - w_1\bar{x} \quad (2)$$

Thay (2) vào phương trình $D_{w1} = 0$ (1), ta tìm được:

$$w_1 = \frac{\sum_{i=1}^{n} (x_i - \bar{x})(y_i - \bar{y})}{\sum_{i=1}^{n} (x_i - \bar{x})^2}$$

Sau khi có $w_1$, ta tính $w_0$:
$$w_0 = \bar{y} - w_1\bar{x}$$


Phương pháp này được gọi là **Normal Equation (Phương trình chuẩn)**. Nó cho phép tìm ra giá trị tối ưu của $w_1, w_0$ chỉ qua một bước tính toán đại số mà không cần vòng lặp. Giá trị này sẽ đóng vai trò là **Benchmark (Mốc chuẩn)** để chúng ta đánh giá độ chính xác của thuật toán Gradient Descent ở phần tiếp theo.


### 3.2 Quy trình tối ưu hóa (Gradient Descent)

**Tại sao chọn Gradient Descent thay vì Normal Equation?**
* **Độ phức tạp tính toán:** Normal Equation yêu cầu tính ma trận nghịch đảo với độ phức tạp $O(n^3)$. Khi số lượng đặc trưng hoặc dữ liệu lên đến hàng triệu, việc này trở nên cực kỳ chậm và tốn bộ nhớ. Gradient Descent có chi phí thấp hơn nhiều và hoạt động tốt trên dữ liệu lớn.
* **Tính tổng quát:** Gradient Descent có thể áp dụng cho hầu hết các thuật toán học máy khác (như Neural Networks), nơi mà không có công thức nghiệm đóng (closed-form solution) như Linear Regression.


Cách làm trên tốn nhiều tài nguyên 

Đạo hàm theo $w_1$: $D_{w1} = \frac{-2}{n} \sum_{i=1}^{n} x_i(y_i - \hat{y}_i)$

Đạo hàm theo $w_0$: $D_{w0} = \frac{-2}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)$

Cập nhật giá trị

$w_1 = w_1 - \alpha \times D_{w1}$

$w_0 = w_0 - \alpha \times D_{w0}$

Lặp lại nhiều lần (epochs) cho đến khi sai số không còn giảm đáng kể.


## 4. Hồi quy tuyến tính đa biến (Multiple Linear Regression)

Trong thực tế, một kết quả thường bị chi phối bởi nhiều nguyên nhân. Do đó, ta mở rộng mô hình từ 1 biến $x$ thành nhiều biến đặc trưng.

### 4.1 Giải thích toán học (Dạng ma trận)

Hồi quy tuyến tính đa biến với $p$ biến đầu vào có phương trình hồi quy cho từng điểm dữ liệu:
$$ \hat{y}_i = w_0 + w_1 x_{i1} + \dots + w_p x_{ip} = \mathbf{w}^\top \mathbf{x}_i $$
Trong đó $\mathbf{x}_i$ là véc-tơ đại diện cho quan sát thứ $i$: $(1, x_{i1}, \dots, x_{ip})$ (đã thêm số 1 ở đầu để tính $w_0$).

**Biểu diễn cho toàn bộ tập dữ liệu:**
Ký hiệu $\bar{\mathbf{X}}$ là ma trận mở rộng kích thước $n \times (p+1)$ (với $n$ là số quan sát).
$$ \hat{\mathbf{y}} = \bar{\mathbf{X}}\mathbf{w} = \begin{bmatrix} 1 & x_{11} & \dots & x_{1p} \\ \vdots & \vdots & \ddots & \vdots \\ 1 & x_{n1} & \dots & x_{np} \end{bmatrix} \begin{bmatrix} w_0 \\ w_1 \\ \vdots \\ w_p \end{bmatrix} $$

**Hàm mất mát (MSE):**
Véc-tơ sai số $\mathbf{e} = \mathbf{y} - \hat{\mathbf{y}}$.
$$ \mathcal{L}(\mathbf{w}) = \frac{1}{2n} \sum_{i=1}^n (y_i - \hat{y}_i)^2 = \frac{1}{2n} ||\bar{\mathbf{X}}\mathbf{w} - \mathbf{y}||_2^2 = \frac{1}{2n} (\mathbf{y} - \bar{\mathbf{X}}\mathbf{w})^\top (\mathbf{y} - \bar{\mathbf{X}}\mathbf{w}) $$

**Đạo hàm và Nghiệm:**
Đạo hàm theo $\mathbf{w}$:
$$ \nabla \mathcal{L}(\mathbf{w}) = \frac{1}{n} \bar{\mathbf{X}}^\top (\bar{\mathbf{X}}\mathbf{w} - \mathbf{y}) $$

Phương trình nghiệm đóng (Normal Equation):
$$ \mathbf{w} = (\bar{\mathbf{X}}^\top \bar{\mathbf{X}})^{-1} \bar{\mathbf{X}}^\top \mathbf{y} $$

### 4.2 Chuẩn bị dữ liệu

Dựa trên phân tích mã nguồn từ notebook `linear_regression1.ipynb`, quy trình chuẩn bị dữ liệu được thực hiện như sau:

*   **Biến mục tiêu (Target - y):** `final_score`
*   **Biến đầu vào (Features - X):** 12 biến số học (numerical features).
    *   Các cột dữ liệu không cần thiết hoặc chưa được xử lý mã hóa (`student_id`, `grade`, `pass_fail`, `parent_education_level`, `study_environment`) đã bị loại bỏ.
    *   Danh sách 12 đặc trưng được sử dụng: `previous_score`, `math_prev_score`, `science_prev_score`, `language_prev_score`, `daily_study_hours`, `attendance_percentage`, `homework_completion_rate`, `sleep_hours`, `screen_time_hours`, `physical_activity_minutes`, `motivation_score`, `exam_anxiety_score`.

### 4.3 Tự triển khai Gradient Descent

Trước khi sử dụng thư viện, chúng ta tự xây dựng hàm `linear_regression_gd` để hiểu rõ cơ chế hoạt động của thuật toán Gradient Descent với nhiều biến số.
  
* **Khởi tạo:** Trọng số $w$ được khởi tạo bằng 0.
* **Vòng lặp (Epochs):**
    * **Tính giá trị dự đoán:** $\hat{y} = Xb \cdot w$
    * **Tính sai số:** $error = \hat{y} - y$
    * **Tính Gradient:** $\nabla w = \frac{2}{n} Xb^T \cdot error$
    * **Cập nhật trọng số:** $w = w - \alpha \cdot \nabla w$
    * **Kiểm tra điều kiện dừng sớm (early stopping)** nếu sự thay đổi loss không đáng kể.

### 4.4 Triển khai với Scikit-Learn

Thay vì tự tính toán các đạo hàm phức tạp cho nhiều biến, ta sử dụng thư viện `scikit-learn` đã được tối ưu hóa cao.

Kết quả đánh giá mô hình sẽ cung cấp các chỉ số như MSE, RMSE, MAE và $R^2$ Score để cho thấy mức độ phù hợp của mô hình đa biến so với đơn biến.

