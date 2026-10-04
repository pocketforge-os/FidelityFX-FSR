# Provenance

| Field | Value |
| --- | --- |
| Canonical upstream | `https://github.com/GPUOpen-Effects/FidelityFX-FSR.git` |
| Upstream base | `a21ffb8f6c13233ba336352bdff293894c706575` |
| Licence | `license.txt` |
| PocketForge patch | Make CPU helpers inline and keep restrict qualifiers off returned pointers. |

The PocketForge patch series is based directly on the upstream commit above.
The FSR algorithm header remains unchanged. `tests/ffx_a_snapshot.py` verifies
the exact admitted `ffx_a.h` bytes and the two CPU portability properties.
