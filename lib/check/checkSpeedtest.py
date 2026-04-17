import os
import logging
import subprocess
import json
import asyncio
from aiohttp import ClientSession
from typing import Dict, List, Any
from pylibagent.check import CheckBase
from ..version import __version__ as version


IPERF3_SVR_URL = 'https://api.infrasonar.com/speedtest'
CONN_TIMEOUT = 10.0  # connection timeout


def run_speedtest(host: str, port: str, duration: int) -> dict[str, Any]:
    cmd = [
        'iperf3',
        '-c', host,
        '-p', str(port),
        '-J',
        '-t', f'{duration}'
    ]

    try:
        logging.debug(f'Start Speedtest for {host}:[{port}]...')
        process = subprocess.run(cmd,
                                 capture_output=True,
                                 text=True,
                                 check=True)
        logging.debug(f'Done Speedtest for {host}:[{port}]')
        data = json.loads(process.stdout)

        connected = data['start']['connected'][0]
        end_recv = data['end']['sum_received']
        end_send = data['end']['sum_sent']
        end_stream_sender = data['end']['streams'][0]['sender']

        # take host as name, new item when the host changes seems reasonable
        item = {
            'name': host,  # str
            'duration': duration,  # int
            'local_host': connected['local_host'],  # str
            'local_port': connected['local_port'],  # int
            'remote_host': connected['remote_host'],  # str
            'remote_port': connected['remote_port'],  # int
            'bits_per_second_recv': end_recv['bits_per_second'],  # float
            'bits_per_second_send': end_send['bits_per_second'],  # float
            'retransmits': end_send.get('retransmits', 0),  # int
            'max_latency_ms': end_stream_sender['max_rtt'] / 1000,  # float
            'min_latency_ms': end_stream_sender['min_rtt'] / 1000,  # float
        }
        return item

    except subprocess.CalledProcessError as e:
        raise Exception(f"Iperf3 error: {e.stderr}")


class CheckSpeedtest(CheckBase):
    key = 'speedtest'
    interval = int(os.getenv('CHECK_INTERVAL', '3600'))

    perf3_host = os.getenv('IPERF3_HOST', '')
    perf3_port = os.getenv('IPERF3_PORT', '5200-5209')
    time_param = int(os.getenv('TIME', '5'))

    @classmethod
    async def run(cls) -> Dict[str, List[Dict[str, Any]]]:
        if cls.interval == 0:
            raise Exception(f'{cls.key} is disabled')

        host = cls.perf3_host
        port = cls.perf3_port
        duration = cls.time_param

        if not host:
            logging.debug('Retrieving speedtest server...')
            try:
                async with ClientSession() as session:
                    async with session.get(url=IPERF3_SVR_URL) as resp:
                        svr = await resp.json()
                        host: str = svr['host']
                        port: str = svr['port']
                        duration: int = svr.get('time') or cls.time_param
            except Exception as e:
                raise Exception(f'Failed to read speedtest server: {str(e)}')

        loop = asyncio.get_running_loop()

        task = loop.run_in_executor(None, run_speedtest, host, port, duration)
        try:
            item = await asyncio.wait_for(task, timeout=duration+CONN_TIMEOUT)
        except asyncio.TimeoutError:
            raise Exception(f'Timed out: failed to connect to {host} [{port}]')

        state = {
            'speedtest': [{'name': 'speedtest', 'version': version}],
            'iperf3': [item]
        }
        return state
