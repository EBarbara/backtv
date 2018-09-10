from unittest import TestCase, mock
import responses
from model.clima import (
    URL,
    read_clima
)
from model.tests.fixtures import metar1


class Clima(TestCase):
    @responses.activate
    @mock.patch("model.clima.jsonify", return_value={"temperature": "26.0"})
    def test_read(self, _jsonify):
        responses.add(
            responses.GET,
            URL,
            body=metar1
        )

        retorno = read_clima()

        self.assertEqual(
            retorno,
            {"temperature": "26.0"}
        )
