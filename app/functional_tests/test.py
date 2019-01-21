from app.functional_tests.base import FunctionalTest


class NewVisitorTest(FunctionalTest):

    def test_visit_our_site(self):
        # 홈페이지를 방문한다.
        self.browser.get(self.live_server_url)

        # 홈페이지의 타이틀이 한강 코인인것을 확인한다.

        # 현재 코인값과 대표값이 내려왔는지 확인한다.

        # 현재값과 대표값을 비교해서 등락률에 따른 색을 확인한다.

        # 현재값과 대표값을 비교해서 등락률에 따른 화살표 방향을 확인한다.

        # 모두 확인했으면 사이트를 종료한다.
