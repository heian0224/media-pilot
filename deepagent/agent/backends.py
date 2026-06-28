"""Backend selection.

CompositeBackend routes ``/content/`` to the REAL workspace content/ dir, so
BOTH the framework's built-in write_file/read_file AND our explicit content_io
tools land real files under content/<slug>/. Ephemeral scratch (plans, offloaded
context) goes to the default StateBackend. This removes the ambiguity where a
subagent writing to ``/content/...`` would otherwise hit an in-memory virtual FS."""
from __future__ import annotations

from deepagents.backends import CompositeBackend, FilesystemBackend, StateBackend

from .. import config


def build_backend():
    return CompositeBackend(
        default=StateBackend(),
        routes={
            "/content/": FilesystemBackend(
                root_dir=config.MEDIA_CONTENT_DIR, virtual_mode=True
            ),
        },
    )
