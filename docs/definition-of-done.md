# Definition of Done

Written before any code. Each line is ticked at the end with a number or a
link as evidence. A line with no evidence counts as unticked.

## Floor (items 1 to 4)

- [x] Endpoint returns correct per-class counts, checked against a known task.
  Evidence: task 6 total is 129, equal to the database count taken in the Django shell; the first 12 rows of known-counts.txt (taken before the endpoint was written) match the endpoint once label ids are mapped to names with docs/evidence/label-ids-task6.txt (401 person 53, 451 broccoli 13, 403 car 11, 450 orange 5, 457 chair 4, 428 tie 4, 402 bicycle 3, 415 bird 3, 455 donut 3, 426 umbrella 3, 460 bed 2, 437 skateboard 2). The remaining rows of that file were not compared. Files: docs/evidence/counts-task6-200.json, docs/evidence/known-counts.txt. Commits e4717c5, c60e889, 99c324b.
- [x] Page calls the endpoint and renders the counts as a graph.
  Evidence: docs/evidence/ui-chart.png (task 6, person is the longest bar at 53). Commit 7421142. Note: the page is served by the test app, not by cvat-ui (see plan, Decision 1).
- [x] Empty state (task with no annotations) handled.
  Evidence: docs/evidence/ui-empty.png (task 7, 1 image, no annotations). Commit 8f7efbc.
- [x] Failed request state handled.
  Evidence: docs/evidence/ui-error-404.png (task 9999, HTTP 404 with a Retry button). Commit 686846e.

## Access (item 5)

- [x] Request with no login is refused.
  Evidence: docs/evidence/no-login-401.txt (HTTP 401) and docs/evidence/ui-error-401.png.
- [x] User with no access to the task is refused.
  Evidence: docs/evidence/no-access-403.txt (user noaccess1, HTTP 403). Commit 0e4d210.

## Measured (item 6)

- [x] Speed objective measured 5 times, raw output saved.
  Evidence: docs/evidence/speed-raw.txt (first request discarded as warm-up, 5 timed runs), docs/evidence/baseline-raw.txt. Objective MO-1 was committed before measuring (1581852).
- [x] Target met, or missed with the reason written down.
  Evidence: missed. Median 400.5 ms against a target of 150 ms, min 363 ms, max 2098 ms. A light endpoint on the same machine has a median of 301.9 ms, so most of the time is shared request overhead. The 2098 ms outlier is unexplained. See docs/objectives.md (commits 15314a1, 80f4174).

## Extra (items 7 and 10)

- [x] One filter or grouping added, with the reason.
  Evidence: `?type=shape,track,tag`, commit 62d4f22. Files: docs/evidence/filter-shape.json (total 129), filter-track-tag.json (total 0), filter-invalid.json (400 with a message). Reason: the total mixes three annotation models, and the filter shows where a count comes from. The page does not use it.
- [x] Decision record written in the plan.
  Evidence: docs/plan.md, section "Decision record" (three decisions, each with what was taken, rejected and what rejecting cost).

## Stretch (items 8 and 9)

- [ ] Live update over WebSocket. Not done: skipped as planned, the floor was finished late.
- [ ] Page recovers after connection drop. Not done: depends on item 8.

## Honesty

- [x] Everything I did not finish is listed, with the reason.
  Evidence: docs/plan.md, section "Not reached".
- [x] Recording is 5 minutes or less and answers K1 to K4.
  Evidence: https://www.loom.com/share/095a838d44eb466b846f534fd98c7272
