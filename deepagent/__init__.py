"""media-pilot — autonomous self-media content engine.

Two front-ends share one core:
  * Claude Code plugin  (skills/ + hooks/)            — interactive, in-REPL
  * Standalone agent    (``python -m media_pilot``)   — deepagents, cron-driven

The core (brand, prompts, tools, motion-graphics template, agent wiring) lives in
this package. Brand identity is NEVER baked in — it is read from an external
``brand.md`` (see ``brand.example.md``), so the repo stays brand-neutral / open.
"""
__version__ = "0.2.0"
