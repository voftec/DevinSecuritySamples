import os
import runpy
import sys

import flask
import pytest

APP_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app.py'))


@pytest.fixture
def run_kwargs(monkeypatch):
    captured = {}

    def fake_run(self, *args, **kwargs):
        captured['args'] = args
        captured['kwargs'] = kwargs

    monkeypatch.setattr(flask.Flask, 'run', fake_run)
    monkeypatch.delitem(sys.modules, 'app', raising=False)
    return captured


def test_entrypoint_disables_debug_and_binds_localhost(run_kwargs, monkeypatch):
    monkeypatch.delenv('HOST', raising=False)
    monkeypatch.delenv('PORT', raising=False)

    runpy.run_path(APP_PATH, run_name='__main__')

    assert run_kwargs['kwargs']['debug'] is False
    assert run_kwargs['kwargs']['host'] == '127.0.0.1'
    assert run_kwargs['kwargs']['port'] == 5000


def test_entrypoint_ignores_debug_env_vars(run_kwargs, monkeypatch):
    monkeypatch.setenv('FLASK_DEBUG', '1')
    monkeypatch.setenv('FLASK_ENV', 'development')

    runpy.run_path(APP_PATH, run_name='__main__')

    assert run_kwargs['kwargs']['debug'] is False


def test_run_config_honours_host_and_port(monkeypatch):
    monkeypatch.setenv('HOST', '10.0.0.5')
    monkeypatch.setenv('PORT', '8080')

    from app import run_config

    assert run_config() == ('10.0.0.5', 8080)
