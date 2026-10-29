# SPDX-License-Identifier: MIT

from django.db.models import Count

from cvat.apps.engine.models import LabeledImage, LabeledShape, LabeledTrack


def count_annotations_by_label(task_id: int) -> dict[str, int]:
    """Number of annotations per label name in a task: shapes, tracks and tags together."""

    totals: dict[str, int] = {}
    for model in (LabeledShape, LabeledTrack, LabeledImage):
        rows = (
            model.objects.filter(job__segment__task_id=task_id)
            .values("label__name")
            .annotate(n=Count("id"))
            .order_by()
        )
        for row in rows:
            totals[row["label__name"]] = totals.get(row["label__name"], 0) + row["n"]
    return totals
