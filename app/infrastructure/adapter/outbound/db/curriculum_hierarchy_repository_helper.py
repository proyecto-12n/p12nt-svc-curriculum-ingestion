# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Any, Callable, Optional, TypeVar

K = TypeVar("K")


class CurriculumHierarchyRepositoryHelper:
    @staticmethod
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
