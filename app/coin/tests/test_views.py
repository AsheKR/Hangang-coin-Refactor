

class TestCoinView:

    def test_home_page_returns_correct_html(self, client):
        response = client.get('/')
        assert response.status_code == 200
