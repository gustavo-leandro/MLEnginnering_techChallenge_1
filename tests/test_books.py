import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

client = TestClient(app)


# Mock para requests.get
class MockResponse:
    def __init__(self, text):
        self.text = text

    def raise_for_status(self):
        pass


@pytest.fixture
@patch("app.scraping.requests.get")
def test_post_books_scrape(mock_get):
    # Simula HTML mínimo para scraping
    html = """
    <html><body>
    <article class="product_pod"><h3><a href="book_1.html"></a></h3></article>
    </body></html>
    """
    book_html = """
    <html><body>
    <h1>Book Title</h1>
    <ul class="breadcrumb"><li></li><li></li><li>Fiction</li></ul>
    <p class="star-rating Three"></p>
    <div id="product_description"></div><p>Desc</p>
    <div class="item active"><img src="img.jpg"/></div>
    <table class="table table-striped">
    <tr><th>UPC</th><td>upc1</td></tr>
    <tr><th>Product Type</th><td>Book</td></tr>
    <tr><th>Price (excl. tax)</th><td>£10.00</td></tr>
    <tr><th>Price (incl. tax)</th><td>£12.00</td></tr>
    <tr><th>Tax</th><td>£2.00</td></tr>
    <tr><th>Availability</th><td>In stock (20 available)</td></tr>
    <tr><th>Number of reviews</th><td>5</td></tr>
    </table>
    </body></html>
    """
    mock_get.side_effect = [MockResponse(html), MockResponse(book_html)]
    response = client.post("/books/scrape", params={"pages": 1})
    assert response.status_code == 201
    assert isinstance(response.json(), list)
    assert response.json()[0]["title"] == "Book Title"


def test_get_books():
    response = client.get("/books/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_search_books_title_only():
    response = client.get("/api/v1/books/search", params={"title": "The Art of War"})
    assert response.status_code == 200
    data = response.json()
    assert all("The Art of War".lower() in book["title"].lower() for book in data)


def test_search_books_category_only():
    response = client.get("/api/v1/books/search", params={"category": "Philosophy"})
    assert response.status_code == 200
    data = response.json()
    assert all("Philosophy".lower() in book["category"].lower() for book in data)


def test_search_books_title_and_category():
    response = client.get(
        "/api/v1/books/search",
        params={"title": "The Art of War", "category": "Philosophy"},
    )
    assert response.status_code == 200
    data = response.json()
    for book in data:
        assert "The Art of War".lower() in book["title"].lower()
        assert "Philosophy".lower() in book["category"].lower()


def test_search_books_no_params():
    response = client.get("/api/v1/books/search")
    assert response.status_code == 200
    # Pode retornar todos os livros ou vazio, depende da implementação
