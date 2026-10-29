\# Plan: Annotation Analytics



\## Setup

\- CPU: AMD Ryzen 5 7430U (6 cores, 12 threads)

\- RAM: 7,583 MB (about 8 GB)

\- OS: Microsoft Windows 11 Pro Education

\- CVAT commit SHA: 4a09e27ff869b7aebbfdb07b29c4a34904a0221d

\- Start time: 9:32 AM PKT, 29 Oct 2026 (time of "Acknowledged" reply)

\- Deadline: 5:32 PM PKT, 29 Oct 2026

\- Images in sample task: 500 (limited by disk space and 8 GB RAM)

\- Annotations: instances\_val2017.json, imported via COCO 1.0



\## Note on time

Docker image pulls and dataset import run in the background and are not

counted, as the assessment states. Cloning the fork and writing this plan

happened after the start time and are counted.



\## What I will build (in order)

| # | Item | Estimate |

|---|------|----------|

| 1 | Orient in codebase (models, auth, URLs) | 30 min |

| 2 | Django app `test`, endpoint: annotations per class (items 1, 5) | 1.5 h |

| 3 | UI page in cvat-ui, bar chart, empty and error states (items 2, 3, 4) | 2.5 h |

| 4 | One speed objective, measured 5 times (item 6) | 1 h |

| 5 | One filter or grouping (item 7) | 1 h |

| 6 | Decision record, docs, Loom, PR (item 10) | 1 h |

| | Buffer | 30 min |



\## Decided to skip (unless time is left)

\- Items 8 and 9 (WebSocket live updates and reconnect).

&#x20; Reason: items 1 to 4 are the floor, and I will not start item 8 before

&#x20; they work.



\## Scope decisions

\- The machine has about 8 GB RAM, so I will use 500 images, not the full 5,000.

\- Decision: count LabeledShape, LabeledTrack and LabeledImage (tags) per

&#x20; Label. Skip LabeledInterval (audio only) and TrackedShape (a track is

&#x20; counted once, not once per frame). Reason: the abstract `Annotation` model

&#x20; in cvat/apps/engine/models.py gives all of them a `label` and a `job`.

\- Label name is read through `label\_\_name`, not through `Label.task`,

&#x20; because tasks inside a project take their labels from `Label.project`.



\## Decision record

(To be added at the end.)

