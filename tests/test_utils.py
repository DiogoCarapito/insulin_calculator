from utils.utils import calculo_insulina


def test_calculo_insulina():
    assert calculo_insulina(12, 50, 59, 120, "↗ subir", 50) == 0
