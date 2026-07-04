# -*- coding: utf-8 -*-
from infrastructure.util.id_generator import generate_id


def test_generate_id_is_deterministic():
    id1 = generate_id("Bases Curriculares", "Educación Parvularia")
    id2 = generate_id("Bases Curriculares", "Educación Parvularia")
    assert id1 == id2


def test_generate_id_returns_integer():
    val = generate_id("Artes Visuales")
    assert isinstance(val, int)
    assert val > 0
