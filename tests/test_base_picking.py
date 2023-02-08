import uuid

from click.testing import CliRunner

from codecov_cli.commands.base_picking import pr_base_picking
from codecov_cli.main import cli
from codecov_cli.types import RequestError, RequestResult, RequestResultWarning


def test_base_picking_command(mocker):
    mocked_response = mocker.patch(
        "codecov_cli.services.commit.base_picking.send_put_request",
        return_value=RequestResult(status_code=200, error=None, warnings=[], text=""),
    )
    token = uuid.uuid4()
    runner = CliRunner()
    result = runner.invoke(
        pr_base_picking,
        [
            "-t",
            token,
            "--pr",
            "11",
            "--base-sha",
            "9a6902ee94c18e8e27561ce316b16d75a02c7bc1",
            "--service",
            "github",
            "--slug",
            "owner/repo",
        ],
    )
    assert result.exit_code == 0
    assert "info: Base picking finished successfully" in result.output
    mocked_response.assert_called_once()


def test_base_picking_command_slug_invalid(mocker):
    token = uuid.uuid4()
    runner = CliRunner()
    result = runner.invoke(
        pr_base_picking,
        [
            "-t",
            token,
            "--pr",
            "11",
            "--base-sha",
            "9a6902ee94c18e8e27561ce316b16d75a02c7bc1",
            "--service",
            "github",
            "--slug",
            "owner-repo",
        ],
    )
    assert result.exit_code == 0
    assert (
        "error: Slug is invalid. Slug should be in the form of owner_username/repo_name"
        in result.output
    )


def test_base_picking_command_warnings(mocker):
    mocked_response = mocker.patch(
        "codecov_cli.services.commit.base_picking.send_put_request",
        return_value=RequestResult(
            error=None,
            warnings=[RequestResultWarning(message="some random warning")],
            status_code=200,
            text="",
        ),
    )
    token = uuid.uuid4()
    runner = CliRunner()
    result = runner.invoke(
        pr_base_picking,
        [
            "-t",
            token,
            "--pr",
            "11",
            "--base-sha",
            "9a6902ee94c18e8e27561ce316b16d75a02c7bc1",
            "--service",
            "github",
            "--slug",
            "owner/repo",
        ],
    )
    assert result.exit_code == 0
    assert "info: Base picking process had 1 warning" in result.output
    assert "Warning 1: some random warning" in result.output
    assert "info: Base picking finished successfully" in result.output
    mocked_response.assert_called_once()


def test_base_picking_command_error(mocker):
    mocked_response = mocker.patch(
        "codecov_cli.services.commit.base_picking.send_put_request",
        return_value=RequestResult(
            status_code=401,
            error=RequestError(
                code="HTTP Error 401",
                description="Unauthorized",
                params={},
            ),
            warnings=[],
            text="",
        ),
    )
    token = uuid.uuid4()
    runner = CliRunner()
    result = runner.invoke(
        pr_base_picking,
        [
            "-t",
            token,
            "--pr",
            "11",
            "--base-sha",
            "9a6902ee94c18e8e27561ce316b16d75a02c7bc1",
            "--service",
            "github",
            "--slug",
            "owner/repo",
        ],
    )
    mocked_response.assert_called_once()
    print(result.output)
    assert result.exit_code == 0
    assert "error: Base picking failed: Unauthorized" in result.output
    assert "info: Base picking finished successfully" not in result.output
