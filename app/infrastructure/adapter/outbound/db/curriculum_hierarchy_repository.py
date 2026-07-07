# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Any, Callable, Protocol, Optional, TypeVar, List

K = TypeVar("K")


class CurriculumHierarchyRepository(Protocol[K]):
    async def find_by_id(self, id: int) -> Optional[K]:
        pass

    async def find_by_url(self, url: str) -> Optional[K]:
        pass

    async def list(self, parent_id: Optional[int] = None) -> List[K]:
        pass

    async def save(self, knowledge: K) -> K:
        pass


def save_hierarchy_model(
    session: Any,
    model: K,
    statement: Any,
    fields: tuple[str, ...],
    before_commit: Optional[Callable[[Any], None]] = None,
) -> K:
    persisted_model = session.exec(statement).first()
    if persisted_model:
        for field in fields:
            setattr(persisted_model, field, getattr(model, field))
    else:
        persisted_model = model.__class__(
            id=model.id,
            **{field: getattr(model, field) for field in fields},
        )
        session.add(persisted_model)

    if before_commit is not None:
        before_commit(persisted_model)

    session.commit()
    session.refresh(persisted_model)
    model.id = persisted_model.id
    return model
