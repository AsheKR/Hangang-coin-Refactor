from river.models import River


class TestRiverModel:

    def test_create_river_data_with_koreawqi(self):
        River.get_river_temperature()

        assert River.objects.count() == 1, 'River Data Crawling Failed'
