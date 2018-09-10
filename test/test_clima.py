from unittest import TestCase
import responses
from ..model.clima import (
    URL,
    read_clima
)
from .fixtures import metar1


class Clima(TestCase):
    @responses.activate
    def test_read(self):
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
