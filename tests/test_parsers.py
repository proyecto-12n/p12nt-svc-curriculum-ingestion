# -*- coding: utf-8 -*-
import importlib.util
import sys
from unittest.mock import MagicMock

if importlib.util.find_spec("pymupdf") is None:
    sys.modules["pymupdf"] = MagicMock()

from domain.model.node import Node
from domain.model.resource_type import ResourceType
from infrastructure.adapter.outbound.http.parser.impl import (
    CurriculumNodeParser,
    ModalityNodeParser,
    SubjectNodeParser,
    GradeLevelNodeParser,
    StudyProgramRefNodeParser,
    StudyProgramNodeParser,
)


def test_curriculum_node_parser():
    parser = CurriculumNodeParser()
    html_content = """
    <html>
        <head><title>Test Title</title></head>
        <body>
            <h1>Bases Curriculares</h1>
            <div class="menu">
                <a href="/curriculum/educacion-parvularia">
                    <h3>Educacion Parvularia</h3>
                </a>
            </div>
        </body>
    </html>
    """
    node = Node(
        url="http://test.url/curr", type=ResourceType.HTML, content=html_content
    )
    curriculum, children = parser.parse(node, 0)

    assert curriculum.title == "Bases Curriculares"
    assert curriculum.content == html_content
    assert len(children) == 1
    assert children[0].url == "http://test.url/curriculum/educacion-parvularia"


def test_modality_node_parser():
    parser = ModalityNodeParser()
    html_content = """
    <html>
        <body>
            <h1>Educacion Parvularia</h1>
            <div class="subject">
                <a href="/curriculum/educacion-parvularia/desarrollo-personal-social">
                    <span class="subject-title">Desarrollo Personal</span>
                </a>
            </div>
        </body>
    </html>
    """
    node = Node(url="http://test.url/mod", type=ResourceType.HTML, content=html_content)
    modality, children = parser.parse(node, 123)

    assert modality.title == "Educacion Parvularia"
    assert modality.curriculum_id == 123
    assert modality.content == html_content
    assert len(children) == 1


def test_subject_node_parser():
    parser = SubjectNodeParser()
    html_content = """
    <html>
        <body>
            <h1>Matemáticas</h1>
            <div class="cursos-wrapper">
                <div class="grade-wrapper">
                    <a href="/curriculum/1o-6o-basico/matematicas/1-basico">1° Básico</a>
                </div>
            </div>
        </body>
    </html>
    """
    node = Node(url="http://test.url/sub", type=ResourceType.HTML, content=html_content)
    subject, children = parser.parse(node, 10)

    assert subject.title == "Matemáticas"
    assert subject.modality_id == 10
    assert subject.content == html_content
    assert len(children) == 1


def test_grade_level_node_parser():
    parser = GradeLevelNodeParser()
    html_content = """
    <html>
        <body>
            <h1>1 Básico</h1>
            <div class="three-grid-content">
                <div class="card--content">
                    <span class="badge">Programa de estudio</span>
                    <a href="/recursos/programa-estudio-matematica-1-basico">Programa</a>
                </div>
            </div>
        </body>
    </html>
    """
    node = Node(
        url="http://test.url/grade", type=ResourceType.HTML, content=html_content
    )
    grade, children = parser.parse(
        node,
        100,
    )

    assert grade.title == "1 Básico"
    assert grade.subject_id == 100
    assert grade.content == html_content
    assert len(children) == 1
    assert (
        children[0].url
        == "http://test.url/recursos/programa-estudio-matematica-1-basico"
    )


def test_study_program_ref_node_parser():
    parser = StudyProgramRefNodeParser()
    html_content = """
    <html>
        <body>
            <h1>Programa Matematica</h1>
            <a href="/sites/default/files/matematica.pdf">PDF Program</a>
        </body>
    </html>
    """
    node = Node(url="http://test.url/ref", type=ResourceType.HTML, content=html_content)
    ref, children = parser.parse(
        node,
        1000,
    )

    assert ref.title == "Programa Matematica"
    assert ref.grade_level_id == 1000
    assert ref.content == html_content
    assert len(children) == 1
    assert children[0].url == "http://test.url/sites/default/files/matematica.pdf"
    assert children[0].type == ResourceType.PDF


def test_study_program_node_parser():
    parser = StudyProgramNodeParser()
    pdf_content = b"PDF content bytes"
    node = Node(
        url="http://test.url/prog.pdf", type=ResourceType.PDF, content=pdf_content
    )
    program, children = parser.parse(
        node,
        2000,
    )

    assert program.study_program_ref_id == 2000
    assert program.title == "prog"
    assert program.content == pdf_content
    assert program.checksum != ""
    assert len(children) == 0

    # Test using PDF metadata title
    from unittest.mock import patch, MagicMock

    mock_doc = MagicMock()
    mock_doc.metadata = {"title": "My Extracted PDF Title"}
    mock_doc.__enter__.return_value = mock_doc

    with patch(
        "pymupdf.Document",
        return_value=mock_doc,
    ):
        program, children = parser.parse(
            node,
            2000,
        )
        assert program.title == "My Extracted PDF Title"
