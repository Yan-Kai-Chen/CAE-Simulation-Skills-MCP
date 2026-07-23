# Field and format policy

| Need | Preferred route | Notes |
|---|---|---|
| Nodal temperature | PATRAN NTL | Compact scalar export |
| Contact Pressure | PATRAN NTL | Set pressure/stress units explicitly |
| Full stress state | Abaqus INP + ASF | Preserve tensor components and connectivity |
| Displaced geometry | PATRAN displacement vector + reference mesh | A scalar total displacement is insufficient |
| Native contour media | Visual-Viewer Cast frames | Lock range before reapplying the palette |

Do not assume a part number or result filename is invariant across case
families. Inspect the loaded model and exported rows for each new family.

For batch processing, partition cases into non-overlapping lanes, use unique
manifests, make completed cases resumable and validate the final expected count
instead of relying on a visible GUI window.
