from repositories import canchas as repo


def test_eliminar_cancha_elimina_bloqueos_antes(monkeypatch):
    consultas = []

    class CursorFake:
        def execute(self, query, params):
            consultas.append((" ".join(query.split()), params))

    class ConexionFake:
        def __init__(self):
            self.commit_realizado = False
            self.rollback_realizado = False

        def cursor(self):
            return CursorFake()

        def commit(self):
            self.commit_realizado = True

        def rollback(self):
            self.rollback_realizado = True

        def close(self):
            pass

    conexion = ConexionFake()

    monkeypatch.setattr(
        "repositories.canchas.get_connection",
        lambda: conexion,
    )

    repo.eliminar(7)

    assert consultas[0] == (
        "DELETE FROM bloqueos WHERE id_cancha = %s",
        (7,),
    )
    assert consultas[1] == (
        "DELETE FROM canchas WHERE id = %s",
        (7,),
    )
    assert conexion.commit_realizado is True
    assert conexion.rollback_realizado is False
