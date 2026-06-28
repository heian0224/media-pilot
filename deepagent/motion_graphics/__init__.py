"""HyperFrames motion-graphics composition engine (promoted from /tmp/gen_backlash_mg2.py).

12 component kinds (ring/cd/contrast/bignum/duo/flow/iconrow/statpair/quote/
spectrum/curve/card), single paused GSAP timeline (seek-safe), brand palette
applied via CSS color substitution. ``build_composition`` writes a complete
HyperFrames project (index.html + audio/ + scaffold) ready for `npx hyperframes render`."""
from .template import build_composition, CSS_COMPONENT_KINDS

__all__ = ["build_composition", "CSS_COMPONENT_KINDS"]
