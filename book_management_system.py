"""简单的图书管理系统（命令行版）。"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List


@dataclass
class Book:
    """图书实体。"""

    isbn: str
    title: str
    author: str
    year: int
    stock: int = 1


class BookManager:
    """图书管理器，负责增删改查和借还逻辑。"""

    def __init__(self, data_file: str = "books.json") -> None:
        self.data_path = Path(data_file)
        self._books: Dict[str, Book] = {}
        self.load()

    def add_book(self, book: Book) -> None:
        if book.isbn in self._books:
            raise ValueError(f"ISBN {book.isbn} 已存在")
        self._books[book.isbn] = book
        self.save()

    def remove_book(self, isbn: str) -> None:
        if isbn not in self._books:
            raise KeyError(f"未找到 ISBN {isbn}")
        del self._books[isbn]
        self.save()

    def update_stock(self, isbn: str, delta: int) -> None:
        book = self._get_book(isbn)
        new_stock = book.stock + delta
        if new_stock < 0:
            raise ValueError("库存不足")
        book.stock = new_stock
        self.save()

    def borrow_book(self, isbn: str) -> None:
        self.update_stock(isbn, -1)

    def return_book(self, isbn: str) -> None:
        self.update_stock(isbn, 1)

    def list_books(self) -> List[Book]:
        return sorted(self._books.values(), key=lambda b: b.title)

    def search(self, keyword: str) -> List[Book]:
        k = keyword.lower()
        return [
            b
            for b in self.list_books()
            if k in b.title.lower() or k in b.author.lower() or k in b.isbn.lower()
        ]

    def load(self) -> None:
        if not self.data_path.exists():
            return
        content = json.loads(self.data_path.read_text(encoding="utf-8"))
        self._books = {item["isbn"]: Book(**item) for item in content}

    def save(self) -> None:
        payload = [asdict(book) for book in self.list_books()]
        self.data_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _get_book(self, isbn: str) -> Book:
        if isbn not in self._books:
            raise KeyError(f"未找到 ISBN {isbn}")
        return self._books[isbn]


def _print_books(books: List[Book]) -> None:
    if not books:
        print("暂无图书。")
        return

    print("\nISBN            标题                     作者            年份    库存")
    print("-" * 72)
    for b in books:
        print(f"{b.isbn:<15} {b.title:<24} {b.author:<14} {b.year:<6} {b.stock}")


def main() -> None:
    manager = BookManager()

    menu = """
==== 图书管理系统 ====
1. 添加图书
2. 删除图书
3. 借阅图书
4. 归还图书
5. 查询图书
6. 显示全部图书
0. 退出
"""

    while True:
        print(menu)
        choice = input("请选择功能：").strip()

        try:
            if choice == "1":
                isbn = input("ISBN: ").strip()
                title = input("书名: ").strip()
                author = input("作者: ").strip()
                year = int(input("出版年份: ").strip())
                stock = int(input("库存: ").strip() or "1")
                manager.add_book(Book(isbn=isbn, title=title, author=author, year=year, stock=stock))
                print("添加成功。")
            elif choice == "2":
                manager.remove_book(input("请输入 ISBN: ").strip())
                print("删除成功。")
            elif choice == "3":
                manager.borrow_book(input("请输入 ISBN: ").strip())
                print("借阅成功。")
            elif choice == "4":
                manager.return_book(input("请输入 ISBN: ").strip())
                print("归还成功。")
            elif choice == "5":
                result = manager.search(input("关键字: ").strip())
                _print_books(result)
            elif choice == "6":
                _print_books(manager.list_books())
            elif choice == "0":
                print("已退出。")
                break
            else:
                print("无效输入，请重试。")
        except Exception as exc:  # 命令行程序需要友好提示
            print(f"操作失败: {exc}")


if __name__ == "__main__":
    main()
