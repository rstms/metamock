#!/usr/bin/env python

import pytest
from click.testing import CliRunner
import shlex
from metamock import __version__, cli

@pytest.fixture
def runner():
    def _runner(cmd=[], **kwargs):
        if isinstance(cmd, str):
            cmd=shlex.split(cmd)
        cli_runner = CliRunner()
        assert isinstance(cmd, list)
        ret = cli_runner.invoke(cli, cmd, **kwargs) 
        assert ret.exit_code == 0, ret.output
        assert not ret.exception, str(ret.exception)
        return ret
    return _runner

def test_cli_version():
    assert cli.name == "metamock"
    assert __version__
    assert isinstance(__version__, str)


def test_cli_no_args(runner):
    result = runner()
    assert result.exit_code == 0, result
    assert "metamock" in result.output

def test_cli_help(runner):
    result = runner('--help')
    assert result.exit_code == 0, result
    assert "Show this message and exit." in result.output

def test_cli_configure(runner, shared_datadir):
    test_config = shared_datadir / 'default-config'
    assert test_config.is_file()
    test_out = test_config.read_text()

    ret = runner('configure')
    configure_out = ret.stdout

    assert configure_out == test_out

def test_cli_run_config(runner, shared_datadir):
    test_config = shared_datadir / 'default_config'
    result = runner(['--debug', '--config-file', test_config, 'run'])
    assert result.ok
