import os
from pylibagent.agent import Agent
from lib.check.checkSpeedtest import CheckSpeedtest
from lib.version import __version__ as version


if __name__ == '__main__':
    # Update ASSET_ID and set a default for the speedtest agent
    ASSET_ID = os.getenv('ASSET_ID', '/data/.asset.json')
    os.environ['ASSET_ID'] = ASSET_ID

    checks = [CheckSpeedtest]
    Agent('speedtest', version).start(checks, asset_kind='Speed')
