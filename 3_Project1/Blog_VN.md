# Hồi quy tuyến tính

Trong thực tế công việc và cuộc sống hằng ngày, chúng ta thường xuyên đặt ra câu hỏi:

> **“Làm sao để dự đoán một giá trị chưa biết dựa trên những dữ liệu đã có?”**

Ví dụ, nếu bạn có dữ liệu về **giá vàng trong 12 tháng gần nhất**, làm sao để ước tính được giá vàng trong những tháng tiếp theo?

Đây chính là lúc các phương pháp **phân tích dữ liệu và học máy** phát huy tác dụng, trong đó **Hồi quy tuyến tính** là một trong những phương pháp đơn giản và phổ biến nhất.

## 1. Hồi quy tuyến tính là gì?

Hồi quy tuyến tính là một phương pháp dùng để **dự đoán biến phụ thuộc (Y)** dựa trên **biến độc lập (X)** thông qua một hàm tuyến tính.

Mô hình được biểu diễn bằng phương trình:

```math
y = f(x) = ax + b
```

Trong đó:

* `a`: Hệ số góc (slope), thể hiện mức độ ảnh hưởng của **X** lên **Y**
* `b`: Hệ số chặn (intercept)
* `x`: Biến độc lập
* `y`: Biến phụ thuộc

Phương trình này mô tả mối quan hệ giữa `X` và `Y` bằng **một đường thẳng** trên mặt phẳng tọa độ.

Trong lý tưởng, các điểm dữ liệu sẽ nằm chính xác trên một đường thẳng. Tuy nhiên, trong thực tế: dữ liệu thường bị nhiễu, bị ảnh hưởng bởi nhiều yếu tố bên ngoài hoặc các điểm dữ liệu phân bố rải rác. Do đó, các điểm hiếm khi nằm thẳng hàng hoàn toàn. Thay vào đó, chúng thường nằm **xung quanh một đường thẳng trung bình**.

Khi xây dựng mô hình hồi quy tuyến tính, mục tiêu của chúng ta là:

> Tìm ra một đường thẳng mô tả tốt nhất xu hướng của dữ liệu.

Cụ thể, đường thẳng này cần:

* Nằm gần với phần lớn các điểm dữ liệu.

* Giảm thiểu khoảng cách giữa giá trị thực tế và giá trị dự đoán.

* Làm cho sai số tổng thể nhỏ nhất.

Nói cách khác, chúng ta tìm kiếm **đường thẳng tối ưu** để đại diện cho dữ liệu.

Nhờ hồi quy tuyến tính, chúng ta có thể dự đoán xu hướng trong tương lai hay phân tích mối quan hệ giữa các biến nhằm hỗ trợ ra quyết định dựa trên dữ liệu. Một số ứng dụng phổ biến có thể kể đến như dự đoán giá vàng, giá cổ phiếu, ước tính doanh thu, phân tích hiệu suất học tập, dự báo như cầu thị trường, ...

Hồi quy tuyến tính là bước khởi đầu quan trọng trong lĩnh vực phân tích dữ liệu và học máy.
Mặc dù đơn giản, nhưng phương pháp này mang lại hiệu quả cao trong nhiều bài toán thực tế.

Với mục tiêu của là tối thiểu hóa sai số kết quả dự báo. Quá trình này được thực hiện thông qua hai công cụ then chốt: **Thước đo sự sai lệch** và **Thuật toán tối ưu**.

<div align="center">
  <img src="/static/uploads/20260201_225850_50a1e0c9.jpg" alt="Dữ liệu thực được chuyển thành biểu diễn số cho AI" width="700">
  <p><em>Ví dụ về đường thẳng tối ưu trong hồi quy tuyến tính.</em></p>
</div>

### 1.1. Thước đo sự sai lệch - Hầm mất mát (Loss Function)

Để biết đường thẳng dự báo đang "tệ" đến mức nào, chúng ta cần một công thức cụ thể để đo lường. Phổ biến nhất là **MSE (Mean Squared Error)** – Bình phương sai số trung bình.

- Cách hoạt động: Với mỗi điểm dữ liệu, máy tính sẽ tính khoảng cách từ điểm đó đến đường thẳng, sau đó bình phương lên (để loại bỏ dấu âm và nhấn mạnh các sai số lớn).
- Mục tiêu: Tổng tất cả các bình phương này càng nhỏ, đường thẳng càng "khớp" với thực tế.

### 1.2. Thuật toán tối ưu - Giảm độ dốc (Gradient Descent)

Sau khi đã có "thước đo" sai số, làm thế nào để điều chỉnh các hệ số `a` và `b` sao cho sai số giảm dần? Đây là lúc thuật toán Gradient Descent xuất hiện. Tưởng tượng bạn đang đứng trên đỉnh một thung lũng (nơi sai số đang rất cao) và mục tiêu của bạn là xuống đáy thung lũng (nơi sai số thấp nhất).
- Gradient (Độ dốc): Giúp máy tính biết hướng nào là hướng đi xuống. 
- Learning Rate (Tốc độ học): Là độ dài mỗi bước chân của bạn. Nếu bước quá dài, bạn có thể nhảy qua đáy; nếu quá ngắn, bạn sẽ đi rất chậm.

Để ví dụ cụ thể, dự án này tập trung về bài toán dự đoán điểm thi của học sinh dự trên bộ dữ liệu - Hiệu suất học tập của sinh viên.

## 2. Giới thiệu về bộ dữ liệu

### 2.1. Mục tiêu 

Mục tiêu của bài thực hành này là xây dựng một mô hình Hồi quy tuyến tính để dự đoán điểm số cuối cùng `final_score` của sinh viên dựa trên các yếu tố về thói quen học tập, các điểm số trong kì thi trước. Vì `final_score` là một biến liên tục nên đây là bài toán Hồi quy điển hình.

Chúng tôi sử dụng bộ dữ liệu **student_performance_interactions.csv**

Link: https://www.kaggle.com/datasets/spscientist/students-performance-in-exams

### 2.2. Tổng quan chung

<div align="center">
  <img src="/static/uploads/20260201_230414_0ee3c533.jpg" alt="Dữ liệu thực được chuyển thành biểu diễn số cho AI" width="700">
  <p><em>Tổng quan về bộ dữ liệu.</em></p>
</div>

**Kích thước**: 1000 dữ liệu của sinh viên và 18 cột dữ liệu

**Chất lượng**: Dữ liệu hoàn chỉnh, không có giá trị thiếu, sẵn sàng cho các bước xử lý tiếp theo

**Biến mục tiêu**: `final_score` (Điểm số thực tế từ 0 - 100)

### 2.3. Phân nhóm các biến độc lập

Để mô hình hồi quy đạt hiệu quả, chúng ta sẽ xem xét các nhóm đặc trưng sau để giải thích cho sự thay đổi của điểm số:

Nhóm Lịch sử học tập (4 biến):

- `previous_score`: Điểm trung bình tổng quát kỳ trước.
- `math_prev_score`: Điểm môn Toán kỳ trước.
- `science_prev_score`: Điểm môn Khoa học kỳ trước.
- `language_prev_score`: Điểm môn Ngôn ngữ kỳ trước.

Nhóm Hành vi học tập (3 biến):

- `daily_study_hours`: Số giờ tự học mỗi ngày.
- `attendance_percentage`: Tỷ lệ có mặt trên lớp (%).
- `homework_completion_rate`: Tỷ lệ hoàn thành bài tập về nhà (%).

Nhóm Lối sống & Sức khỏe (3 biến):
- `sleep_hours`: Số giờ ngủ mỗi đêm.
- `screen_time_hours`: Số giờ sử dụng thiết bị điện tử.
- `physical_activity_minutes`: Số phút hoạt động thể chất mỗi ngày.

Nhóm Tâm lý (2 biến):

- `motivation_score`: Chỉ số động lực học tập.
- `exam_anxiety_score`: Chỉ số lo lắng khi thi cử.

Nhóm Môi trường & Gia đình (2 biến - Cần mã hóa):

- `parent_education_level`: Trình độ học vấn phụ huynh (Định tính).
- `study_environment`: Môi trường học tập (Định tính: Quiet, Moderate, Noisy).

### 2.4. Các biến cần lạoi bỏ hoặc xử lý đặc biệt

Với bộ dữ liệu này, chúng ta sẽ loại bỏ các biến này để tránh sai số:

- `student_id`: Mã định danh (Không có ý nghĩa thống kê, cần loại bỏ khi huấn luyện).
- `grade`: Xếp loại (A, B, C...). Biến này được tính trực tiếp từ final_score nên không dùng làm đầu vào để dự đoán final_score.
- `pass_fail`: Đạt/Trượt (0 hoặc 1). Tương tự như grade, biến này là hệ quả của điểm số, không phải nguyên nhân.

## 3. Mô hình hồi quy tuyến tính đơn biến (Simple linear Regression)

Đầu tiên, sau khi loại bỏ các biến ta kiểm tra correlation và thấy `previous_score` ảnh hưởng lớn nhất đến `final_score`.

```python
target = 'final_score'
cols_to_check = list(df.columns[3:15])

corrs = {}
for col in cols_to_check:
    series = pd.to_numeric(df[col], errors='coerce')
    corr = df[target].corr(series)
    corrs[col] = corr

corr_df = pd.DataFrame.from_dict(corrs, orient='index', columns=['pearson_corr'])
corr_df = corr_df.sort_values('pearson_corr', key=lambda x: x.abs(), ascending=False)

print(corr_df)

correlation_results = corr_df
```

```
# Result
previous_score                 0.843755
math_prev_score                0.825755
science_prev_score             0.823998
language_prev_score            0.810688
attendance_percentage          0.737720
pass_fail                      0.484865
daily_study_hours              0.357275
homework_completion_rate       0.339800
motivation_score               0.255734
physical_activity_minutes     -0.044330
sleep_hours                    0.032623
screen_time_hours             -0.029856
```

### 3.1. Giải thích cách làm toán học

Phương trình của mô hình hồi quy tuyến tính đơn biến là:
$$y = w_1x + w_0 + \epsilon$$
Trong đó:

$y$: Giá trị cần dự đoán (Label/Target).

$x$: Dữ liệu đầu vào (Feature).

$w_1$: Hệ số góc (Weight/Slope), thể hiện mức độ ảnh hưởng của $x$ lên $y$.

$w_0$: Hệ số chặn (Bias/Intercept), là giá trị của $y$ khi $x = 0$.

$\epsilon$: Sai số ngẫu nhiên (Noise).

Với mỗi điểm dữ liệu $(x_i, y_i)$, ta tính giá trị dự đoán $\hat{y}_i$:
$$\hat{y}_i = w_1x_i + w_0$$
Mục tiêu của chúng ta là tìm $w_1$ và $w_0$ sao cho khoảng cách giữa $\hat{y}$ (giá trị dự đoán) và $y$ (giá trị thực tế) là nhỏ nhất.

Chúng ta sẽ sử dụng hàm MSE (Mean Square Error) làm hàm mất mát. Hàm số này có giá trị bằng trung bình của tổng bình phương sai số giữa giá trị dự báo và ground truth.

Hàm mất mát theo biến $w_1$, $w_0$ phải đạt giá trị cực tiểu:
$$L(w) = \frac{1}{2n} \sum (y - \hat{y})^2 = \frac{1}{2n} \sum (y - w_1x - w_0)^2$$

Để đạt giá trị cực tiểu, đạo hàm của hàm L(w) =0

Đạo hàm theo $w_1$: 
$$D_{w1} = \frac{-2}{n} \sum_{i=1}^{n} x_i(y_i - \hat{y}_i) =0 \quad (1)$$

Đạo hàm theo $w_0$: $$D_{w0} = \frac{-2}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i) =0$$

$$\Leftrightarrow w_0 = \bar{y} - w_1\bar{x} \quad (2)$$

Thay (2) vào (1), ta tìm được:

$$w_1 = \frac{\sum_{i=1}^{n} (x_i - \bar{x})(y_i - \bar{y})}{\sum_{i=1}^{n} (x_i - \bar{x})^2}$$

Sau khi có $w_1$, ta tính $w_0$:
$$w_0 = \bar{y} - w_1\bar{x}$$


Phương pháp này được gọi là **Normal Equation (Phương trình chuẩn)**. Nó cho phép tìm ra giá trị tối ưu của $w_1, w_0$ chỉ qua một bước tính toán đại số mà không cần vòng lặp. Giá trị này sẽ đóng vai trò là **Benchmark (Mốc chuẩn)** để chúng ta đánh giá độ chính xác của thuật toán Gradient Descent ở phần tiếp theo.

### 3.2. Quy trình tối ưu hóa (Gradient Descent)

**Tại sao chọn Gradient Descent thay vì Normal Equation?**
* **Độ phức tạp tính toán:** Normal Equation yêu cầu tính ma trận nghịch đảo với độ phức tạp $O(n^3)$. Khi số lượng đặc trưng hoặc dữ liệu lên đến hàng triệu, việc này trở nên cực kỳ chậm và tốn bộ nhớ. Gradient Descent có chi phí thấp hơn nhiều và hoạt động tốt trên dữ liệu lớn.
* **Tính tổng quát:** Gradient Descent có thể áp dụng cho hầu hết các thuật toán học máy khác (như Neural Networks), nơi mà không có công thức nghiệm đóng (closed-form solution) như Linear Regression.


Cách làm trên tốn nhiều tài nguyên:

Đạo hàm theo $w_1$: $D_{w1} = \frac{-2}{n} \sum_{i=1}^{n} x_i(y_i - \hat{y}_i)$

Đạo hàm theo $w_0$: $D_{w0} = \frac{-2}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)$

Cập nhật giá trị

$$w_1 = w_1 - \alpha \times D_{w1}$$

$$w_0 = w_0 - \alpha \times D_{w0}$$

Lặp lại nhiều lần (epochs) cho đến khi sai số không còn giảm đáng kể.

## 4. Hồi quy tuyến tính đa biến (Multiple Linear Regression)

Trong thực tế, một kết quả thường bị chi phối bởi nhiều nguyên nhân. Do đó, ta mở rộng mô hình từ 1 biến $x$ thành $n$ biến đặc trưng $x_1, x_2, ..., x_n$.

Phương trình tổng quát:
$$y = w_0 + w_1x_1 + w_2x_2 + ... + w_nx_n + \epsilon$$

### 4.1 Chuẩn bị dữ liệu

Dựa trên phân tích mã nguồn từ notebook `linear_regression1.ipynb`, quy trình chuẩn bị dữ liệu được thực hiện như sau:

*   **Biến mục tiêu (Target - y):** `final_score`
*   **Biến đầu vào (Features - X):** 12 biến số học (numerical features).
    *   Các cột dữ liệu không cần thiết hoặc chưa được xử lý mã hóa (`student_id`, `grade`, `pass_fail`, `parent_education_level`, `study_environment`) đã bị loại bỏ.
    *   Danh sách 12 đặc trưng được sử dụng: `previous_score`, `math_prev_score`, `science_prev_score`, `language_prev_score`, `daily_study_hours`, `attendance_percentage`, `homework_completion_rate`, `sleep_hours`, `screen_time_hours`, `physical_activity_minutes`, `motivation_score`, `exam_anxiety_score`.

### 4.2 Tự triển khai Gradient Descent

Trước khi sử dụng thư viện, chúng ta tự xây dựng hàm `linear_regression_gd` để hiểu rõ cơ chế hoạt động của thuật toán Gradient Descent với nhiều biến số.
  
* **Khởi tạo:** Trọng số $w$ được khởi tạo bằng 0.
* **Vòng lặp (Epochs):**
    * **Tính giá trị dự đoán:** $\hat{y} = Xb \cdot w$
    * **Tính sai số:** $error = \hat{y} - y$
    * **Tính Gradient:** $\nabla w = \frac{2}{n} Xb^T \cdot error$
    * **Cập nhật trọng số:** $w = w - \alpha \cdot \nabla w$
    * **Kiểm tra điều kiện dừng sớm (early stopping)** nếu sự thay đổi loss không đáng kể.

### 4.3 Triển khai với Scikit-Learn

Thay vì tự tính toán các đạo hàm phức tạp cho nhiều biến, ta sử dụng thư viện `scikit-learn` đã được tối ưu hóa cao.


## 5. Code

Dưới đây là link github chứa chi tiết code về dự án Hồi quy tuyến tính sử dụng hồi quy tuyến tính đơn biến, hồi quy tuyến tính đa biến và triển khai với Scikit-Learn dựa trên thư viện có sẵn trong python. Các bạn có thể xem và tham khảo:

https://github.com/atognoob/AIO2026/tree/main/3_Project1