from enum import StrEnum


class ActivityType(StrEnum):
    LEARNING = "aprendizaje"
    ASSESSMENT = "evaluacion"
    PROJECT = "proyecto"
    INTERDISCIPLINARY = "interdisciplinaria"
    OTHER = "otro"
