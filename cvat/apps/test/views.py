# SPDX-License-Identifier: MIT

from django.views.generic import TemplateView
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cvat.apps.engine.models import Task
from cvat.apps.engine.permissions import TaskPermission

from .counts import ANNOTATION_KINDS, count_annotations_by_label


class TaskAnnotationCountsView(APIView):
    # The default PolicyEnforcer needs a ViewSet (view.detail, iam_permission_class).
    # This is a plain APIView, so the task-level OPA check is done explicitly in get().
    permission_classes = [IsAuthenticated]

    def get(self, request, task_id: int):
        task = get_object_or_404(Task, pk=task_id)

        permission = TaskPermission.create_scope_view(request, task)
        if not permission.check_access().allow:
            raise PermissionDenied("You do not have access to this task.")

        requested = request.query_params.get("type")
        kinds = requested.split(",") if requested else list(ANNOTATION_KINDS)
        unknown = sorted(set(kinds) - set(ANNOTATION_KINDS))
        if unknown:
            raise ValidationError(
                f"Unknown type(s): {', '.join(unknown)}. Allowed: {', '.join(ANNOTATION_KINDS)}."
            )

        counts = count_annotations_by_label(task.id, kinds)
        return Response(
            {
                "task_id": task.id,
                "types": kinds,
                "total": sum(counts.values()),
                "counts": [
                    {"label": label, "count": count}
                    for label, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
                ],
            }
        )


class TaskAnnotationCountsPageView(TemplateView):
    template_name = "test/annotation_counts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_id"] = kwargs["task_id"]
        return context
