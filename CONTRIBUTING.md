# Contributing to TuViMCP

Thank you for your interest in contributing to TuViMCP! We welcome contributions to improve horoscope calculation accuracy, support additional MCP features, refine documentation, and write test suites.

---

## Code of Conduct

Please be respectful and constructive in all communication, issues, and pull requests.

## Getting Started

### 1. Fork and Clone
Fork the repository on GitHub and clone it locally:
```bash
git clone https://github.com/your-username/TuViMCP.git
cd TuViMCP
```

### 2. Setup Development Environment
We recommend using a Python virtual environment.
```bash
# Create a virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows

# Install package in editable mode with test dependencies
pip install -e ".[test]"
```

### 3. Running Tests
We use `pytest` for unit testing. Before submitting any changes, make sure all tests pass:
```bash
pytest
```
If you add new features or fix bugs, please write matching unit tests inside the `tests/` directory.

---

## Development Guidelines

### Code Style
- Follow [PEP 8](https://peps.python.org/pep-0008/) style guidelines for Python code.
- Ensure your code is clean, readable, and properly documented with docstrings.
- Avoid introducing external runtime dependencies unless absolutely necessary. We prefer keeping TuViMCP lightweight.

### Database Operations
If you modify database structures:
- Ensure database modifications are safe and backward-compatible.
- Use a temporary SQLite database for unit tests (see `tests/test_tuvi.py` for how to use `TUVI_DB_PATH` environment override).

---

## Submission Process

1. **Create a Branch**: Create a feature branch with a descriptive name.
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. **Commit Changes**: Write clear, descriptive commit messages.
3. **Push and PR**: Push your branch to GitHub and open a Pull Request against the `main` branch.
4. **CI Verification**: Make sure the GitHub Actions CI pipeline passes successfully on your PR.

---

## Tài liệu tiếng Việt (Vietnamese Summary)

Chào mừng bạn đóng góp cho dự án TuViMCP! Quy trình đóng góp cơ bản bao gồm:
1. **Fork** dự án và nhân bản (clone) về máy cục bộ.
2. **Thiết lập môi trường** ảo Python: `python3 -m venv .venv`.
3. **Cài đặt chế độ chỉnh sửa** và thư viện kiểm thử: `pip install -e ".[test]"`.
4. **Chạy kiểm thử** bằng lệnh `pytest`. Hãy luôn đảm bảo tất cả kiểm thử vượt qua thành công trước khi gửi PR.
5. **Gửi PR** hướng về nhánh `main` kèm theo mô tả rõ ràng về thay đổi của bạn.
