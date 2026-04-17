[![CI](https://github.com/infrasonar/speedtest-agent/workflows/CI/badge.svg)](https://github.com/infrasonar/speedtest-agent/actions)
[![Release Version](https://img.shields.io/github/release/infrasonar/speedtest-agent)](https://github.com/infrasonar/speedtest-agent/releases)

# InfraSonar Speedtest agent

Documentation: https://docs.infrasonar.com/collectors/agents/speedtest/

## Environment variables

Environment                 | Default                       | Description
----------------------------|-------------------------------|-------------------
`TOKEN`                     | _required_                    | Token to connect to.
`ASSET_ID`                  | `/data/.asset.json`           | Asset Id _or_ file where the Agent asset Id is stored _(must be a volume mount)_.
`API_URI`                   | https://api.infrasonar.com    | InfraSonar API.
`CHECK_INTERVAL`            | `3600`                        | Interval for the speedtest check in seconds.
`IPERF3_HOST`               | _empty_                       | Target IP/Host address for performance testing, for example: `ams.speedtest.clouvider.net`. If not given, the InfraSonar default will be used ([https://api.infrasonar.com/speedtest](https://api.infrasonar.com/speedtest)).
`IPERF3_PORT`               | _empty_                       | If empty, port `5200-5209` will be used unless specified by InfraSonar.
`TIME`                      | `5`                           | Time in seconds to transmit for.
`VERIFY_SSL`                | `1`                           | Verify SSL certificate, 0 _(=disabled)_ or 1 _(=enabled)_.
`LOG_LEVEL`                 | `warning`                     | Log level _(error, warning, info, debug)_.
`LOG_COLORIZED`             | `0`                           | Log colorized, 0 _(=disabled)_ or 1 _(=enabled)_.
`LOG_FMT`                   | `%y%m...`                     | Default format is `%y%m%d %H:%M:%S`.
