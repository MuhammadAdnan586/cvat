# SPDX-License-Identifier: MIT

from django.urls import path

from .views import TaskAnnotationCountsView

urlpatterns = [
    path(
        "tasks/<int:task_id>/annotation-counts",
        TaskAnnotationCountsView.as_view(),
        name="task-annotation-counts",
    ),
]
