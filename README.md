[![CI](https://github.com/infrasonar/speedtest-agent/workflows/CI/badge.svg)](https://github.com/infrasonar/speedtest-agent/actions)
[![Release Version](https://img.shields.io/github/release/infrasonar/speedtest-agent)](https://github.com/infrasonar/speedtest-agent/releases)

# InfraSonar Speedtest agent

## Environment variables

Environment                 | Default                       | Description
----------------------------|-------------------------------|-------------------
`TOKEN`                     | _required_                    | Token to connect to.
`ASSET_ID`                  | `/data/.asset.json`           | Asset Id _or_ file where the Agent asset Id is stored _(must be a volume mount)_.
`API_URI`                   | https://api.infrasonar.com    | InfraSonar API.
`CHECK_INTERVAL`            | `300`                         | Interval for the speedtest check in seconds.
`NO_DOWNLOAD`               | `0`                           | Do not perform download test _(1 will disable the download test)_.
`NO_UPLOAD`                 | `0`                           | Do not perform upload test _(1 will disable the upload test)_.
`SINGLE`                    | `0`                           | Only use a single connection instead of multiple. This simulates a typical file transfer.
`SOURCE`                    | _null_                        | Source IP address to bind to _(not required)_.
`TIMEOUT`                   | `10`                          | HTTP timeout in seconds.
`SECURE`                    | `0`                           | Use HTTPS instead of HTTP when communicating with speedtest.net operated servers.
`VERIFY_SSL`                | `1`                           | Verify SSL certificate, 0 _(=disabled)_ or 1 _(=enabled)_.
`LOG_LEVEL`                 | `warning`                     | Log level _(error, warning, info, debug)_.
`LOG_COLORIZED`             | `0`                           | Log colorized, 0 _(=disabled)_ or 1 _(=enabled)_.
`LOG_FMT`                   | `%y%m...`                     | Default format is `%y%m%d %H:%M:%S`.
