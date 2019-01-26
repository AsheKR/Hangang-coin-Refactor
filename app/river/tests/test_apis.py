import json

import pytest

from river.models import River


class TestCoinApi:

    @pytest.mark.smoke
    def test_retrieve_river_api(self, client):
        river = River.objects.create(temperature=2.8)

        json_data = json.loads(client.get('/api/river/').content.decode('utf8'))

        assert json_data['temperature'] == river.temperature
