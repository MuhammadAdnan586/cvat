# SPDX-License-Identifier: MIT

from collections.abc import Collection

from django.db.models import Count

from cvat.apps.engine.models import LabeledImage, LabeledShape, LabeledTrack

ANNOTATION_KINDS = {"shape": LabeledShape, "track": LabeledTrack, "tag": LabeledImage}


def count_annotations_by_label(
    task_id: int, kinds: Collection[str] = tuple(ANNOTATION_KINDS)
) -> dict[str, int]:
    """Number of annotations per label name in a task, for the given kinds of annotation."""

    totals: dict[str, int] = {}
    for kind in kinds:
        rows = (
            ANNOTATION_KINDS[kind]
            .objects.filter(job__segment__task_id=task_id)
            .values("label__name")
            .annotate(n=Count("id"))
            .order_by()
        )
        for row in rows:
            totals[row["label__name"]] = totals.get(row["label__name"], 0) + row["n"]
    return totals
