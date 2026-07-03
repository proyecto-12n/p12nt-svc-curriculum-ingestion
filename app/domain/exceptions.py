class DomainException(Exception):
    """Excepcion base de dominio"""

    pass


class EntityNotFoundException(DomainException):
    def __init__(self, entity_id: int):
        self.message = (
            f"Entity with id {entity_id} not found in domain curriculum_ingestion."
        )
        super().__init__(self.message)
