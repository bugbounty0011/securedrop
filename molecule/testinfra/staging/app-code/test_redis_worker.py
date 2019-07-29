import pytest
import re


testinfra_hosts = ["app-staging"]
securedrop_test_vars = pytest.securedrop_test_vars


@pytest.mark.parametrize(
    "config_line",
    [
        "[program:securedrop_worker]",
        "command=/opt/venvs/securedrop-app-code/bin/rqworker",
        "directory={}".format(securedrop_test_vars.securedrop_code),
        (
            'environment=PYTHONPATH="/var/www/securedrop:'
            '/opt/venvs/securedrop-app-code/lib/python3.5/site-packages"'
        ),
        "autostart=true",
        "autorestart=true",
        "startretries=3",
        "stderr_logfile=/var/log/securedrop_worker/rqworker.err",
        "stdout_logfile=/var/log/securedrop_worker/rqworker.out",
        "user={}".format(securedrop_test_vars.securedrop_user),
    ],
)
def test_redis_worker_configuration(host, config_line):
    """
    Ensure SecureDrop Redis worker config for supervisor service
    management is configured correctly.
    """
    f = host.file("/etc/supervisor/conf.d/securedrop_worker.conf")
    # Config lines may have special characters such as [] which will
    # throw off the regex matching, so let's escape those chars.
    regex = re.escape(config_line)
    assert f.contains("^{}$".format(regex))


def test_redis_worker_config_file(host):
    """
    Ensure SecureDrop Redis worker config for supervisor service
    management has proper ownership and mode.

    Using separate test so that the parametrization doesn't rerun
    the file mode checks, which would be useless.
    """
    f = host.file("/etc/supervisor/conf.d/securedrop_worker.conf")
    assert f.is_file
    assert f.mode == 0o644
    assert f.user == "root"
    assert f.group == "root"
