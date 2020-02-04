import argparse
import logging

from async_savers import AsyncSaverZMQWorker


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', '-ip', type=str, default='127.0.0.1')
    parser.add_argument('--port', '-p', type=str, default='5000')
    args = parser.parse_args()

    logging.info('Running AsyncSaverZMQWorker...')
    worker = AsyncSaverZMQWorker(args.ip, args.port)
    worker.start()