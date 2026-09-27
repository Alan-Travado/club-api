import unittest
from datetime import datetime, timedelta

from errors import ApiError
from services.estado_reserva import resolver_transicion

INICIO = datetime(2026, 10, 15, 18, 0, 0)
FIN = INICIO + timedelta(hours=2)


class TransicionesTest(unittest.TestCase):
    def test_repetir_no_modifica(self):
        antes = INICIO - timedelta(microseconds=1)
        self.assertFalse(resolver_transicion("confirmada", "confirmada", INICIO, FIN, antes))
        self.assertFalse(resolver_transicion("cancelada", "cancelada", INICIO, FIN, antes))
        self.assertFalse(resolver_transicion("finalizada", "finalizada", INICIO, FIN, FIN))

    def test_cancelar_solo_antes_del_inicio(self):
        self.assertTrue(
            resolver_transicion("confirmada", "cancelada", INICIO, FIN, INICIO - timedelta(microseconds=1))
        )
        with self.assertRaises(ApiError) as exc:
            resolver_transicion("confirmada", "cancelada", INICIO, FIN, INICIO)
        self.assertEqual(exc.exception.status, 409)

    def test_finalizar_desde_el_fin(self):
        with self.assertRaises(ApiError) as exc:
            resolver_transicion(
                "confirmada", "finalizada", INICIO, FIN, FIN - timedelta(microseconds=1)
            )
        self.assertEqual(exc.exception.status, 409)
        self.assertTrue(resolver_transicion("confirmada", "finalizada", INICIO, FIN, FIN))

    def test_cancelada_y_finalizada_no_cambian(self):
        for actual, nuevo in (
            ("cancelada", "confirmada"),
            ("cancelada", "finalizada"),
            ("finalizada", "confirmada"),
            ("finalizada", "cancelada"),
        ):
            with self.assertRaises(ApiError) as exc:
                resolver_transicion(actual, nuevo, INICIO, FIN, INICIO)
            self.assertEqual(exc.exception.status, 409)

    def test_estado_desconocido(self):
        with self.assertRaises(ApiError) as exc:
            resolver_transicion("confirmada", "expirada", INICIO, FIN, INICIO)
        self.assertEqual(exc.exception.status, 400)


if __name__ == "__main__":
    unittest.main()
