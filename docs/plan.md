# Plan: Annotation Analytics

## Setup

- CPU: AMD Ryzen 5 7430U (6 cores, 12 threads)
- RAM: 7,583 MB (about 8 GB)
- OS: Microsoft Windows 11 Pro Education
- CVAT commit SHA: 4a09e27ff869b7aebbfdb07b29c4a34904a0221d
- Start time: 9:32 AM PKT, 29 Oct 2026 (time of "Acknowledged" reply)
- Deadline: 5:32 PM PKT, 29 Oct 2026
- Images in sample task: 500 (limited by disk space and 8 GB RAM)
- Annotations: instances_val2017.json, imported via COCO 1.0

## Note on time

Docker image pulls and dataset import run in the background and are not
counted, as the assessment states. Cloning the fork and writing this plan
happened after the start time and are counted.

## What I will build (in order)

| # | Item | Estimate |
|---|------|----------|
| 1 | Orient in codebase (models, auth, URLs) | 30 min |
| 2 | Django app `test`, endpoint: annotations per class (items 1, 5) | 1.5 h |
| 3 | UI page in cvat-ui, bar chart, empty and error states (items 2, 3, 4) | 2.5 h |
| 4 | One speed objective, measured 5 times (item 6) | 1 h |
| 5 | One filter or grouping (item 7) | 1 h |
| 6 | Decision record, docs, Loom, PR (item 10) | 1 h |
| | Buffer | 30 min |

## Decided to skip (unless time is left)

- Items 8 and 9 (WebSocket live updates and reconnect).
  Reason: items 1 to 4 are the floor, and I will not start item 8 before
  they work.

## Scope decisions

- The machine has about 8 GB RAM, so I will use 500 images, not the full 5,000.
- Decision: count LabeledShape, LabeledTrack and LabeledImage (tags) per
  Label. Skip LabeledInterval (audio only) and TrackedShape (a track is
  counted once, not once per frame). Reason: the abstract `Annotation` model
  in cvat/apps/engine/models.py gives all of them a `label` and a `job`.
- Label name is read through `label__name`, not through `Label.task`,
  because tasks inside a project take their labels from `Label.project`.

## Decision record

Written at the end of the work. The plan above is left as it was written; changes
to it are listed in the next section.

### Decision 1: where the page lives

- Taken: a page served by the new `test` Django app at
  `/api/tasks/<id>/annotation-counts/chart` (plain HTML and JavaScript, bars drawn
  with divs, calls the JSON endpoint with the user's session).
- Rejected: a React page inside cvat-ui, as planned in item 3.
- Why: when I had to decide, Windows reported about 0.8 GB of 7.4 GB RAM free with
  the Docker stack running. The running cvat_ui container is pre-built, so a new React
  page needs the webpack dev server. I judged that not feasible on this machine. I did
  not try it, so this is a judgement from the free-RAM number, not a measurement.
- What rejecting it cost: the page is not part of the real CVAT interface. There is no
  menu link to it, it does not reuse CVAT's components or styling, and it sits under
  `/api/` only because the proxy sends just `/api/*` to the Django server.

### Decision 2: how access to a task is checked

- Taken: a plain DRF `APIView` with `IsAuthenticated`, and an explicit call to
  `TaskPermission.create_scope_view(request, task).check_access()` inside `get()`.
  A missing login gives 401, a user without access to the task gives 403.
- Rejected: adding an action to `TaskViewSet`, or a new scope in
  `TaskPermission._get_scopes`, so the default `PolicyEnforcer` would do the check.
- Why: that means editing core engine files I did not write. My first version used the
  default `PolicyEnforcer` and returned a 500 (`'TaskAnnotationCountsView' object has no
  attribute 'detail'`), because it expects a ViewSet.
- What rejecting it cost: this view skips `PolicyEnforcer`, so any checks CVAT adds
  there (for example access-token plugin rules) do not run for it. I only tested with
  a normal login (basic auth), not with an access token.

### Decision 3: how the new code runs in Docker

- Taken: keep the pre-built images and bind-mount only `cvat/apps/test`, `cvat/urls.py`
  and `cvat/settings/base.py` into `cvat_server` with a compose override kept outside
  the repo.
- Rejected: rebuilding images through `docker-compose.dev.yml`.
- Why: that file rebuilds both `cvat_server` and `cvat_ui` from source. I judged that
  too slow for the time available on this machine; I did not time it.
- What rejecting it cost: the override file is not in the repository, so the way to
  run the code is written down below instead. The mounted settings and urls files must
  match the image; I compared them with the container copies at the start and they
  were identical.

## What changed from this plan

- Item 3: the page is not in cvat-ui (Decision 1). The estimate of 2.5 h no longer
  applies.
- Docker dev compose was replaced by a bind mount (Decision 3).
- Sample data: task 6 has 20 images, not 500, with 129 shapes, no tracks and no tags.
  Tracks and tags were only ever counted as zero, so that path has no non-zero test.
- Item 6: the 150 ms target was missed (median 400.5 ms). See objectives.md.
- Item 7: a `?type=shape,track,tag` filter was added to the endpoint. The page does not
  use it yet.
- Items 8 and 9 were skipped, as planned.

## Not reached

- Items 8 and 9 (live update over WebSocket, reconnect).
- A page inside cvat-ui.
- The filter in the page (it exists only in the API).
- An explanation of the 2098 ms outlier in the latency runs.
- Automated tests. Everything was checked by hand, evidence is in docs/evidence.
- Access-token authentication was not tested.

## How to run

    $env:CVAT_HOST="localhost"
    docker compose -f docker-compose.yml -f <path>\cvat-mount.yml up -d cvat_server

where cvat-mount.yml mounts three paths from this repository into the container:
`cvat/apps/test` to `/opt/cvat/cvat/apps/test`, `cvat/urls.py` to `/opt/cvat/cvat/urls.py`
and `cvat/settings/base.py` to `/opt/cvat/cvat/settings/base.py`. After a Python change run
`docker restart cvat_server` and wait about a minute.

- API: `GET /api/tasks/<id>/annotation-counts[?type=shape,track,tag]`
- Page: `/api/tasks/<id>/annotation-counts/chart`
