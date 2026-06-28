"""CLI entrypoint: ``python -m deepagent run [--topic X | --auto [--dry-run]]``
and ``python -m deepagent schedule --cron "7 9 * * *"``.

The run command wires pre-run guardrails → (pick if --auto) → full pipeline →
post-run verification → structured log + optional webhook."""
from __future__ import annotations

import sys

import click

from . import config
from .agent import runner
from .scheduler import guardrails, notify, topic_selector


def _latest_today_slug() -> str:
    cands = sorted(
        [p for p in config.MEDIA_CONTENT_DIR.glob(f"{config.TODAY}-*") if p.is_dir()],
        key=lambda p: p.stat().st_mtime,
    )
    return cands[-1].name if cands else ""


@click.group()
def main() -> None:
    """media-pilot deepagent — turn a topic into ready-to-post content (+ video)."""


@main.command()
@click.option("--topic", default=None, help="Fixed topic to produce content for.")
@click.option("--auto", is_flag=True, help="Autonomously pick a trending topic (de-duped vs history).")
@click.option("--dry-run", is_flag=True, help="With --auto: only pick + log a topic, skip the pipeline.")
def run(topic: str | None, auto: bool, dry_run: bool) -> None:
    """Run the content pipeline once."""
    issues = guardrails.pre_run_checks()
    fatal = guardrails.fatal_issues(issues)
    if fatal:
        raise click.ClickException("ABORT (fatal): " + "; ".join(fatal))
    if issues:
        click.echo(f"warnings: {issues}", err=True)
    if not auto and not topic:
        raise click.UsageError("provide --topic <text> or --auto")

    mode = "auto" if auto else "topic"
    if auto:
        click.echo("selecting a trending topic...")
        pick = topic_selector.pick_auto_topic()
        topic = pick.get("topic") or ""
        click.echo(f"auto-picked: {topic}  ->  {pick.get('slug','')}")
        click.echo(f"reason: {pick.get('reason','')}")
        notify.notify(f"[media-pilot] auto-picked: {topic}")
        if dry_run or not topic:
            notify.log_run({"date": config.TODAY, "mode": "auto-dry-run", **pick})
            return

    click.echo(f"running pipeline for: {topic}")
    runner.run_topic(topic, verbose=False)
    slug = _latest_today_slug()
    report = guardrails.post_run_verify(slug) if slug else {"complete": False, "missing": ["unknown-slug"]}
    notify.log_run({"date": config.TODAY, "mode": mode, "topic": topic, "slug": slug, "report": report})
    notify.notify(f"[media-pilot] done: {topic} | complete={report.get('complete')} missing={report.get('missing', [])}")
    click.echo(f"done. slug={slug} complete={report.get('complete')} missing={report.get('missing', [])}")


@main.command()
@click.option("--cron", required=True, help='cron expr, e.g. "7 9 * * *" (daily 09:07)')
@click.option("--install/--no-install", default=False, help="Add to crontab (default: just print the line).")
def schedule(cron: str, install: bool) -> None:
    """Install (or just print) a crontab line that runs --auto on a schedule."""
    import subprocess

    config.LOG_DIR.mkdir(parents=True, exist_ok=True)
    line = (
        f'{cron} cd {config.WORKSPACE_ROOT} && {sys.executable} -m deepagent run --auto '
        f'>> {config.LOG_DIR}/media-pilot-cron.log 2>&1'
    )
    click.echo("crontab line:")
    click.echo("  " + line)
    if install:
        cur = subprocess.run(["crontab", "-l"], capture_output=True, text=True).stdout
        if line in cur:
            click.echo("already present in crontab.")
        else:
            subprocess.run(["crontab", "-"], input=cur + line + "\n", text=True)
            click.echo("installed into crontab.")
    else:
        click.echo("(not installed — pass --install to add, or paste the line into your crontab.)")


if __name__ == "__main__":
    main()
