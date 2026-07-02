# -*- coding: utf-8 -*-
from app.domain.model.node import Node
from app.domain.model.resource_type import ResourceType
from app.infrastructure.adapter.outbound.http.parser.impl.curriculum_node_parser import (
    CurriculumNodeParser,
)
from app.infrastructure.adapter.outbound.http.parser.impl.modality_node_parser import (
    ModalityNodeParser,
)
from app.infrastructure.adapter.outbound.http.parser.impl.subject_node_parser import (
    SubjectNodeParser,
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
    curriculum, children = parser.parse(node)

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
    node = Node(
        url="http://test.url/mod", type=ResourceType.HTML, content=html_content
    )
    modality, children = parser.parse(
        node, parent_id=123, metadata={"curriculum": "Curr"}
    )

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
    node = Node(
        url="http://test.url/sub", type=ResourceType.HTML, content=html_content
    )
    subject, children = parser.parse(
        node, parent_id=10, metadata={"curriculum": "Curr", "modality": "Mod"}
    )

    assert subject.title == "Matemáticas"
    assert subject.modality_id == 10
    assert subject.content == html_content
    assert len(children) == 1
