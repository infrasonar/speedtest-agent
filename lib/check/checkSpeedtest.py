import os
import asyncio
import logging
from typing import Dict, List, Any
from pylibagent.check import CheckBase
from speedtest import (
    Speedtest,
    ConfigRetrievalError,
    ServersRetrievalError,
    InvalidServerIDType,
    HTTP_ERRORS,
    NoMatchedServers)
from ..version import __version__ as version


class CheckSpeedtest(CheckBase):
    key = 'speedtest'
    interval = int(os.getenv('CHECK_INTERVAL', '3600'))

    download = not bool(int(os.getenv('NO_DOWNLOAD', '0')))
    upload = not bool(int(os.getenv('NO_UPLOAD', '0')))
    single = bool(int(os.getenv('SINGLE', '0')))
    source = os.getenv('SOURCE', None)
    timeout = int(os.getenv('TIMEOUT', '10'))
    secure = bool(int(os.getenv('SECURE', '0')))

    @classmethod
    async def run(cls) -> Dict[str, List[Dict[str, Any]]]:
        if cls.interval == 0:
            raise Exception(f'{cls.key} is disabled')

        logging.debug('Retrieving speedtest.net configuration...')
        try:
            speedtest = Speedtest(
                source_address=cls.source,
                timeout=cls.timeout,
                secure=cls.secure
            )
        except (ConfigRetrievalError,) + HTTP_ERRORS as e:
            msg = str(e) or type(e).__name__
            raise Exception(f'Cannot retrieve speedtest configuration: {msg}')

        cl = speedtest.config['client']
        item = {
            'name': 'speedtest',
            'from': f'{cl["isp"]} ({cl["ip"]})',
        }

        logging.debug(f'Testing from {item["from"]}...')
        logging.debug('Retrieving speedtest.net server list...')
        try:
            speedtest.get_servers()
        except NoMatchedServers:
            raise Exception('No matched servers')
        except (ServersRetrievalError,) + HTTP_ERRORS:
            msg = str(e) or type(e).__name__
            raise Exception(f'Cannot retrieve speedtest server list: {msg}')
        except InvalidServerIDType:
            raise Exception(
                f'Server Id is an invalid server type, must be an int')

        logging.debug('Selecting best server based on ping...')
        speedtest.get_best_server()

        results = speedtest.results

        item['destination'] = destination = \
            f"{results.server['sponsor']} ({results.server['name']})"
        item['distance'] = d = results.server['d']
        item['latency'] = latency = results.server['latency']

        logging.debug(
            f"Hosted by {destination} [{d:.02f} km]: {latency:.03f} ms")

        if cls.download:
            logging.debug('Testing download speed')
            speedtest.download(threads=(None, 1)[cls.single])
            item['download'] = v = results.download

            logging.debug(f'Download: {(v / 1_000_000.0):.2f} Mbit/s')
        else:
            logging.debug('Skipping download test')

        if cls.upload:
            logging.debug('Testing upload speed')
            speedtest.upload(threads=(None, 1)[cls.single])
            item['upload'] = v = results.upload
            logging.debug(f'Upload: {(v / 1_000_000.0):.2f} Mbit/s')
        else:
            logging.debug('Skipping upload test')

        item['bytes_received'] = results.bytes_received
        item['bytes_sent'] = results.bytes_sent

        item['version'] = version

        state = {'speedtest': [item]}
        return state
