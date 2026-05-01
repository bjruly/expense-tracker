# expense-tracker

Ứng dụng web theo dõi thu chi cá nhân — xây dựng bằng Python, Streamlit, SQLite.

Đây là project học tập cá nhân, viết từ đầu với mục tiêu tích hợp đồng thời nhiều kỹ thuật:
OOP, cơ sở dữ liệu quan hệ, giải thuật thống kê, và AI phân loại văn bản.
Không dùng framework nặng. Không abstraction thừa. Mỗi dòng code đều có lý do tồn tại.

---

## Stack

    Giao diện      Streamlit
    Backend        Python 3.11+
    Database       SQLite  (built-in, không cần server)
    Biểu đồ        Plotly
    Xuất file      pandas + openpyxl
    AI/ML          scikit-learn  (tùy chọn)
    Testing        pytest

---

## Cấu trúc thư mục

    expense-tracker/
    |
    +-- app.py                      Entry point. Chạy file này để khởi động app.
    +-- requirements.txt
    +-- .gitignore
    |
    +-- modules/                    Toàn bộ business logic nằm ở đây.
    |   +-- __init__.py
    |   +-- database.py             Kết nối SQLite, khởi tạo schema, seed data.
    |   +-- expense_manager.py      Class ExpenseManager — CRUD giao dịch.
    |   +-- analytics.py            Class Analytics — tổng hợp, thống kê.
    |   +-- budget_manager.py       Class BudgetManager — ngân sách & cảnh báo.
    |   +-- report_exporter.py      Xuất báo cáo ra CSV / Excel.
    |
    +-- pages/                      Multi-page Streamlit. Mỗi file = một trang.
    |   +-- 01_Dashboard.py
    |   +-- 02_Add_Expense.py
    |   +-- 03_History.py
    |   +-- 04_Budget.py
    |   +-- 05_Reports.py
    |
    +-- data/
    |   +-- expense.db              Tự sinh khi chạy lần đầu. Không commit lên Git.
    |
    +-- tests/
        +-- test_expense_manager.py
        +-- test_analytics.py
        +-- test_budget_manager.py

---

## Chạy ứng dụng

```bash
git clone https://github.com/<username>/expense-tracker.git
cd expense-tracker

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
streamlit run app.py
```

---

## Schema

```sql
CREATE TABLE categories (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name    TEXT    NOT NULL UNIQUE,
    icon    TEXT,
    color   TEXT
);

CREATE TABLE transactions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    amount      REAL    NOT NULL,
    category_id INTEGER REFERENCES categories(id),
    description TEXT,
    date        TEXT    NOT NULL,
    type        TEXT    CHECK(type IN ('expense', 'income')),
    created_at  TEXT    DEFAULT (datetime('now'))
);

CREATE TABLE budgets (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id   INTEGER REFERENCES categories(id),
    monthly_limit REAL    NOT NULL,
    month         TEXT    NOT NULL
);
```

---

## Tiến độ

    [ ] Giai đoạn 1 — Core          CRUD giao dịch, lịch sử, tổng thu/chi
    [ ] Giai đoạn 2 — Analytics     Biểu đồ cột, tròn, so sánh tháng
    [ ] Giai đoạn 3 — Budget        Ngân sách, cảnh báo 80% / 100%
    [ ] Giai đoạn 4 — Export & AI   Xuất Excel, tự phân loại giao dịch

---

## Nhật ký

**27/04/2026**
Khởi tạo project. Tạo cấu trúc thư mục, requirements.txt, .gitignore.
Push commit đầu tiên lên GitHub.

**28/04/2026**
Hoàn thành modules/database.py.
Viết get_connection(), create_tables(), seed_default_categories(), initialize_database().
Hiểu được Connection, Cursor, row_factory trong sqlite3.

**29/04/2026**
Review và sửa lại database.py sau khi nhận phản hồi.
Thêm type hint cho get_connection().
Đưa conn.close() ra ngoài khối logic chính, tránh resource leak.
Cập nhật schema cho đúng với project brief: đổi tên bảng, tên cột, kiểu dữ liệu.
Sửa lỗi cú pháp trong cursor.execute() của create_tables().
Tạo file modules/expense_manager.py với đầy đủ cấu trúc class.

**30/04/2026**
Hoàn thiện khung expense_manager.py.
Định nghĩa @dataclass Transaction và class ExpenseManager.
Viết skeleton các method: add_transaction(), get_transactions(), update_transaction(), delete_transaction().
Hiểu được @dataclass, cursor.lastrowid, **kwargs.

**01/05/2026**
Hoàn thành logic CRUD trong expense_manager.py.
Viết add_transaction() với INSERT và trả về Transaction object.
Viết get_transactions() với dynamic query, xử lý filters theo category_id và month.
Viết update_transaction() và delete_transaction(), kiểm tra kết quả qua cursor.rowcount.

---

*Sinh viên năm 2 — Python — Tích hợp OOP + CSDL + AI*
