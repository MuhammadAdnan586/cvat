# SPDX-License-Identifier: MIT

from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from cvat.apps.engine.models import Task
from cvat.apps.engine.permissions import TaskPermission

from .counts import count_annotations_by_label


class TaskAnnotationCountsView(APIView):
    def get(self, request, task_id: int):
        task = get_object_or_404(Task, pk=task_id)

        permission = TaskPermission.create_scope_view(request, task)
        if not permission.check_access().allow:
            raise PermissionDenied("You do not have access to this task.")

        counts = count_annotations_by_label(task.id)
        return Response(
            {
                "task_id": task.id,
                "total": sum(counts.values()),
                "counts": [
                    {"label": label, "count": count}
                    for label, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
                ],
            }
        )
