from unittest import TestCase
import responses
from ..model.clima import (
    URL,
    read
)


class Clima(TestCase):
    @responses.activate
    def test_read(self):
        responses.add(
            responses.GET,
            URL,
            json={"retorno": "yay"}
        )

        retorno = read()

        self.assertEqual(
            retorno,
            {"temperature": "NULL"}
        )
