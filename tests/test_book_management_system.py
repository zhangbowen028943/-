import tempfile
import unittest
from pathlib import Path

from book_management_system import Book, BookManager


class BookManagerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_file = Path(self.temp_dir.name) / "books.json"
        self.manager = BookManager(str(self.data_file))

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_add_and_list_books(self) -> None:
        self.manager.add_book(Book(isbn="978-7-111", title="算法导论", author="CLRS", year=2022, stock=2))
        books = self.manager.list_books()

        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].title, "算法导论")

    def test_borrow_and_return(self) -> None:
        self.manager.add_book(Book(isbn="978-7-222", title="数据库系统", author="Silberschatz", year=2021, stock=1))

        self.manager.borrow_book("978-7-222")
        self.assertEqual(self.manager.list_books()[0].stock, 0)

        self.manager.return_book("978-7-222")
        self.assertEqual(self.manager.list_books()[0].stock, 1)

    def test_search(self) -> None:
        self.manager.add_book(Book(isbn="978-7-333", title="Python编程", author="Guido", year=2020, stock=3))
        self.manager.add_book(Book(isbn="978-7-444", title="机器学习", author="Tom", year=2023, stock=2))

        result = self.manager.search("python")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].isbn, "978-7-333")

    def test_duplicate_isbn_should_fail(self) -> None:
        book = Book(isbn="978-7-555", title="操作系统", author="Tanenbaum", year=2019, stock=1)
        self.manager.add_book(book)

        with self.assertRaises(ValueError):
            self.manager.add_book(book)


if __name__ == "__main__":
    unittest.main()
