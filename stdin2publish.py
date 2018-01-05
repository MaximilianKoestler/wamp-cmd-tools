#!/usr/bin/env python3

# Copyright (c) Maximilian Köstler
# 3-clause BSD license
# https://license.koestler.hamburg

import argparse
import asyncio
import sys

from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner

def main(args):
    url = 'ws://{}:{}/ws'.format(args.host, args.port)
    print('Connecting to "{}".'.format(url))

    class EventPublisher(ApplicationSession):
        async def onJoin(self, details):
            for line in sys.stdin:
                for topic in args.topic:
                    self.publish(topic, line.strip())

        def onDisconnect(self):
            print('Disconnecting.')
            asyncio.get_event_loop().stop()

    runner = ApplicationRunner(url=url, realm=args.realm)
    runner.run(EventPublisher)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Publish lines from stdin to a topic.')
    parser.add_argument('host', type=str)
    parser.add_argument('port', type=int)
    parser.add_argument('realm', type=str)
    parser.add_argument('topic', type=str, nargs='+')

    main(parser.parse_args())
