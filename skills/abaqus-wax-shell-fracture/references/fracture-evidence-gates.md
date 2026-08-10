# XFEM fracture evidence gates

Keep these statements separate:

- positive face-connected STATUSXFEM: numerical initiation morphology;
- positive CSDMG/CRKOPEN: resolved cohesive damage and opening;
- CSDMG equal to one: fully degraded cohesive surface point;
- STATUSXFEM near one: fully cracked element under the extractor definition;
- one fully cracked face-connected component touching both loaded inner and
  physical exterior surfaces: topology-verified through-thickness vent.

Do not merge the gates into one event time. Intact stresses after damage begins
are an unrelieved load envelope, not a post-crack stress field.
Do not call a numerical activation time a calibrated experimental crack time
unless material/contact parameters and experiments support that calibration.

After a verified vent, preserve pressure continuity and label any hydraulic
feedback as reduced-order unless a fully coupled fluid-fracture solve is used.
Distinguish pressure reduction from structural opening reduction. During
unloading, decreasing CRKOPEN with an irreversible connected crack topology is
closure, not healing.

Preserve failed trials, datachecks, manifests, pressure histories, candidate
definitions, compact extraction files, figures and energy checks.
