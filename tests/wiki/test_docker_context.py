# Copyright 2026 Federico Cesarini, Marco Sassarini
# SPDX-License-Identifier: AGPL-3.0-or-later

"""The Docker build context: every file the Dockerfile copies gets past .dockerignore's allowlist."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_every_file_the_dockerfile_copies_is_let_into_the_build_context() -> None:
    allowed = {line[1:].strip().rstrip("/") for line in (ROOT / ".dockerignore").read_text().splitlines() if line.startswith("!")}
    copied = [
        source
        for line in (ROOT / "Dockerfile").read_text().splitlines()
        if line.startswith("COPY ") and "<<" not in line  # a heredoc brings its own text
        for source in line.split()[1:-1]
        if not source.startswith("--")
    ]

    assert copied, "no COPY found in the Dockerfile"
    assert [s for s in copied if s.rstrip("/") not in allowed] == []
    assert all((ROOT / s).exists() for s in copied)
