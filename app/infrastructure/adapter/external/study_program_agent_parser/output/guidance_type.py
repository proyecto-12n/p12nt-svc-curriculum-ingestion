from enum import StrEnum


class GuidanceType(StrEnum):
    DIDACTIC = "didactica"
    ASSESSMENT = "evaluacion"
    PLANNING = "planificacion"
    IMPLEMENTATION = "implementacion"
    TEACHER = "docente"
    TEACHER_OBSERVATION = "observacion_docente"
    OTHER = "otro"
