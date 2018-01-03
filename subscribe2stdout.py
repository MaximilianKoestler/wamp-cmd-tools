#!/usr/bin/env python3

# Copyright (c) Maximilian Köstler
# 3-clause BSD license
# https://license.koestler.hamburg

import argparse
import asyncio

from autobahn.wamp.types import SubscribeOptions
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner

def main(args):
    url = 'ws://{}:{}/ws'.format(args.host, args.port)
    print('Connecting to "{}".'.format(url))

    class EventPrinter(ApplicationSession):
        async def onJoin(self, details):

            for topic in args.topic:
                def onevent(*args, details=None):
                    print('>> {} >>'.format(details.topic), *args)

                print('Subscribing to topic "{}".'.format(topic))
                options = SubscribeOptions(details_arg='details', match='prefix')
                await self.subscribe(onevent, topic, options)

        def onDisconnect(self):
            print('Disconnecting.')
            asyncio.get_event_loop().stop()

    runner = ApplicationRunner(url=url, realm=args.realm)
    runner.run(EventPrinter)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Subscribe to a topic and print events to stdout.')
    parser.add_argument('host', type=str)
    parser.add_argument('port', type=int)
    parser.add_argument('realm', type=str)
    parser.add_argument('topic', type=str, nargs='+')

    main(parser.parse_args())
