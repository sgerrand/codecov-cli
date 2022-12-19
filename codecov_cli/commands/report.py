import logging
import uuid

import click

from codecov_cli.fallbacks import CodecovOption, FallbackFieldEnum
from codecov_cli.services.report import create_report_logic

logger = logging.getLogger("codecovcli")


@click.command()
@click.option(
    "--commit-sha",
    help="Commit SHA (with 40 chars)",
    cls=CodecovOption,
    fallback_field=FallbackFieldEnum.commit_sha,
    required=True,
)
@click.option(
    "--code", help="The code of the report. If unsure, leave default", default="default"
)
@click.option(
    "--slug",
    cls=CodecovOption,
    fallback_field=FallbackFieldEnum.slug,
    help="owner/repo slug used instead of the private repo token in Self-hosted",
    envvar="CODECOV_SLUG",
    required=True,
)
@click.option(
    "--service",
    help="Git service provider, e.g. github",
    cls=CodecovOption,
    fallback_field=FallbackFieldEnum.service,
)
@click.option(
    "-t",
    "--token",
    help="Codecov upload token",
    type=click.UUID,
    envvar="CODECOV_TOKEN",
)
@click.pass_context
def create_report(
    ctx, commit_sha: str, code: str, slug: str, service: str, token: uuid.UUID
):
    logger.debug(
        "Starting create report process",
        extra=dict(
            extra_log_attributes=dict(
                commit_sha=commit_sha, code=code, slug=slug, service=service
            )
        ),
    )
    res = create_report_logic(commit_sha, code, slug, service, token)
    if not res.error:
        logger.info("Finished creating report successfully")
        logger.info(res.text)
