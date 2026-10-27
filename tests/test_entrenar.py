"""Entrenamiento y reanudación (docs/04_entrenamiento_y_busqueda.md)."""
import numpy as np
import pytest

from quickdraw import entrenar as T
from quickdraw.config import Config


def cache_sintetica(n, semilla):
    """n dibujos de 2 trazos con imágenes al azar y 30 etiquetas."""
    rng = np.random.default_rng(semilla)
    K = np.full(n, 2, dtype=np.int32)
    return {"imagenes": rng.integers(0, 256, (2 * n, 28, 28), dtype=np.uint8),
            "inicio": np.arange(n, dtype=np.int64) * 2, "K": K,
            "etiqueta": np.arange(n, dtype=np.int64) % 30, "indice": np.arange(n)}


def test_reanudar_tras_un_corte_da_lo_mismo(tmp_path, monkeypatch):
    """Si Colab corta a mitad del entrenamiento, al retomar desde el checkpoint
    se obtiene exactamente el mismo historial que sin corte (incluido dropout)."""
    cfg = Config(lote=64, paciencia=10)
    ent, val = cache_sintetica(256, 0), cache_sintetica(64, 1)
    kw = dict(esquema="prefijos", objetivo="final", dropout=0.3, epocas=3, verbose=False)
    _, sin_corte = T.entrenar("M2", ent, val, cfg, ruta=tmp_path / "a", **kw)

    original, llamadas = T.objetivo_validacion, []
    def corte(*a, **k):
        llamadas.append(1)
        if len(llamadas) == 2:                 # se corta durante la segunda época
            raise KeyboardInterrupt
        return original(*a, **k)
    monkeypatch.setattr(T, "objetivo_validacion", corte)
    with pytest.raises(KeyboardInterrupt):
        T.entrenar("M2", ent, val, cfg, ruta=tmp_path / "b", **kw)
    monkeypatch.setattr(T, "objetivo_validacion", original)
    _, con_corte = T.entrenar("M2", ent, val, cfg, ruta=tmp_path / "b", **kw)

    assert [h["perdida"] for h in con_corte] == [h["perdida"] for h in sin_corte]


def test_modelos_con_otros_datos_detienen_antes_de_la_busqueda(tmp_path):
    import json
    from dataclasses import replace
    cfg = Config(ruta_trabajo=tmp_path)
    carpeta = tmp_path / "modelos" / "M2_s0"
    carpeta.mkdir(parents=True)
    (carpeta / "hiperparametros.json").write_text(json.dumps(T.huella_datos(cfg)))
    T.verificar_modelos_guardados(cfg)                       # mismos datos: sigue
    with pytest.raises(RuntimeError, match="grosor"):
        T.verificar_modelos_guardados(replace(cfg, grosor=10))
