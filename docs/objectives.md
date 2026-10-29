\# Objectives



\## MO-1

| Field | Entry |

|-------|-------|

| What is measured | Server response time of the per-class count endpoint for one task |

| How | \[to fill after the endpoint exists: tool and exact command] |

| Target | \[to fill after the first measurement, with the reason] |

| Conditions | Local Docker stack, 500 images from COCO val2017, Windows 11, nothing else running |

| Not included | First request after a cold start, video tasks |



\## Machine

\- CPU: AMD Ryzen 5 7430U (6 cores, 12 threads)

\- RAM: 7,583 MB (about 8 GB)

\- OS: Microsoft Windows 11 Pro Education

\- CVAT commit SHA: 4a09e27ff869b7aebbfdb07b29c4a34904a0221d



\## Results

(Raw output of 5 runs, median and spread, to be added.)


## MO-1: Endpoint latency

| Field | Entry |
|---|---|
| What is measured | Total response time of GET /api/tasks/6/annotation-counts, as seen by the client |
| How | `curl.exe -w "%{time_total}"` against http://localhost:8080, 1 warm-up request discarded, then 5 timed runs; raw output in docs/evidence/speed-raw.txt |
| Target | Median of 5 runs at or below 150 ms |
| Why this number | The page will render a chart from this one call; 150 ms keeps the call well under the point where a user notices a delay. It includes three count queries plus one OPA permission call, so it is not trivially met. |
| Conditions | Local Docker stack, task 6 (20 images, 129 annotations, no tracks or tags), authenticated as adnan, nothing else heavy running |
| Not included | First request after a server restart (cold start), tasks with many more annotations |

### MO-1 result (29 Oct 2026, local Docker stack)

Raw output: docs/evidence/speed-raw.txt. The first request (949 ms) was discarded as warm-up.
Five timed runs, in ms: 2098, 401, 407, 388, 363.
Median 400.5 ms, min 363 ms, max 2098 ms.

Target (median at or below 150 ms): MISSED, about 2.7 times over.
The 2098 ms run is an unexplained outlier; it is kept in the spread.
Cause of the miss: not yet established. See the baseline comparison below.
