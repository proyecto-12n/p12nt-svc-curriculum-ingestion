# -*- coding: utf-8 -*-
import importlib.util
import sys
from unittest.mock import MagicMock

import pytest

from domain.model import CurriculumHierarchyType
from domain.model.scrap_resource import ScrapResource

if importlib.util.find_spec("pymupdf") is None:
    sys.modules["pymupdf"] = MagicMock()

from domain.model.resource_type import ResourceType
from infrastructure.adapter.outbound.http.parser.impl import (
    CurriculumScrapResourceParser,
    ModalityScrapResourceParser,
    SubjectScrapResourceParser,
    GradeLevelScrapResourceParser,
    StudyProgramRefScrapResourceParser,
    StudyProgramScrapResourceParser,
)


@pytest.mark.asyncio
async def test_curriculum_node_parser():
    parser = CurriculumScrapResourceParser()
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
    resource = ScrapResource(
        url="https://test.url/curr", type=ResourceType.HTML, content=html_content
    )

    edge = await parser.get_edge(resource)

    assert edge.url == "https://test.url/curr"
    assert edge.type == ResourceType.HTML
    assert edge.hierarchy == CurriculumHierarchyType.CURRICULUM

    assert edge.title == "Bases Curriculares"
    assert edge.content == html_content

    children = [x async for x in parser.get_children(resource)]
    assert len(children) == 1
    assert children[0].url == "/curriculum/educacion-parvularia"
    assert children[0].type == ResourceType.HTML
    assert children[0].hierarchy == CurriculumHierarchyType.MODALITY


@pytest.mark.asyncio
async def test_modality_node_parser():
    parser = ModalityScrapResourceParser()
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
    resource = ScrapResource(
        url="https://test.url/mod", type=ResourceType.HTML, content=html_content
    )
    edge = await parser.get_edge(resource)

    assert edge.url == "https://test.url/mod"
    assert edge.type == ResourceType.HTML
    assert edge.hierarchy == CurriculumHierarchyType.MODALITY

    assert edge.title == "Educacion Parvularia"
    assert edge.content == html_content

    children = [x async for x in parser.get_children(resource)]
    assert len(children) == 1
    assert (
        children[0].url == "/curriculum/educacion-parvularia/desarrollo-personal-social"
    )
    assert children[0].type == ResourceType.HTML
    assert children[0].hierarchy == CurriculumHierarchyType.SUBJECT


@pytest.mark.asyncio
async def test_subject_node_parser():
    parser = SubjectScrapResourceParser()
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
    resource = ScrapResource(
        url="https://test.url/sub", type=ResourceType.HTML, content=html_content
    )
    edge = await parser.get_edge(resource)

    assert edge.url == "https://test.url/sub"
    assert edge.type == ResourceType.HTML
    assert edge.hierarchy == CurriculumHierarchyType.SUBJECT

    assert edge.title == "Matemáticas"
    assert edge.content == html_content

    children = [x async for x in parser.get_children(resource)]
    assert len(children) == 1
    assert children[0].url == "/curriculum/1o-6o-basico/matematicas/1-basico"
    assert children[0].type == ResourceType.HTML
    assert children[0].hierarchy == CurriculumHierarchyType.GRADE_LEVEL


@pytest.mark.asyncio
async def test_grade_level_node_parser():
    parser = GradeLevelScrapResourceParser()
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
    resource = ScrapResource(
        url="https://test.url/grade", type=ResourceType.HTML, content=html_content
    )

    edge = await parser.get_edge(resource)

    assert edge.url == "https://test.url/grade"
    assert edge.type == ResourceType.HTML
    assert edge.hierarchy == CurriculumHierarchyType.GRADE_LEVEL

    assert edge.title == "1 Básico"
    assert edge.content == html_content

    children = [x async for x in parser.get_children(resource)]
    assert len(children) == 1
    assert children[0].url == "/recursos/programa-estudio-matematica-1-basico"
    assert children[0].type == ResourceType.HTML
    assert children[0].hierarchy == CurriculumHierarchyType.STUDY_PROGRAM_REF


@pytest.mark.asyncio
async def test_study_program_ref_node_parser():
    parser = StudyProgramRefScrapResourceParser()
    html_content = """
    <html>
        <body>
            <h1>Programa Matematica</h1>
            <a href="/sites/default/files/matematica.pdf">PDF Program</a>
        </body>
    </html>
    """
    resource = ScrapResource(
        url="https://test.url/ref", type=ResourceType.HTML, content=html_content
    )
    edge = await parser.get_edge(resource)

    assert edge.url == "https://test.url/ref"
    assert edge.type == ResourceType.HTML
    assert edge.hierarchy == CurriculumHierarchyType.STUDY_PROGRAM_REF

    assert edge.title == "Programa Matematica"
    assert edge.content == html_content

    children = [x async for x in parser.get_children(resource)]
    assert len(children) == 1
    assert children[0].url == "/sites/default/files/matematica.pdf"
    assert children[0].type == ResourceType.PDF
    assert children[0].hierarchy == CurriculumHierarchyType.STUDY_PROGRAM


@pytest.mark.asyncio
async def test_study_program_node_parser():
    parser = StudyProgramScrapResourceParser()
    pdf_content = b"PDF content bytes"
    resource = ScrapResource(
        url="https://test.url/prog.pdf", type=ResourceType.PDF, content=pdf_content
    )
    edge = await parser.get_edge(resource)

    assert edge.title == "prog"
    assert edge.content == pdf_content

    children = []
    async for child in parser.get_children(resource):
        children.append(child)
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
        edge = await parser.get_edge(resource)
        assert edge.title == "My Extracted PDF Title"

    # Test URL-encoded filename fallback (%20 → space)
    encoded_resource = ScrapResource(
        url="https://test.url/Programa%20de%20Estudio%201%C2%BA.pdf",
        type=ResourceType.PDF,
        content=pdf_content,
    )
    edge = await parser.get_edge(encoded_resource)
    assert edge.title == "Programa de Estudio 1º"
