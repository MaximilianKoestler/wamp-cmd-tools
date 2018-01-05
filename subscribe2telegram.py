#!/usr/bin/env python3

# Copyright (c) Maximilian Köstler
# 3-clause BSD license
# https://license.koestler.hamburg

import argparse
import asyncio
import telegram

from autobahn.wamp.types import SubscribeOptions
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner

def main(args):
    url = 'ws://{}:{}/ws'.format(args.host, args.port)
    print('Connecting to "{}".'.format(url))

    with open ('token.txt', 'r') as tokenfile:
        token = tokenfile.read().strip()

    bot = telegram.Bot(token=token)
    chat_id = args.telegram

    class EventPrinter(ApplicationSession):
        async def onJoin(self, details):

            for topic in args.topic:
                def onevent(*args, details=None):
                    
                    text = 'Received event on topic "{}"'.format(details.topic) + '\n' + ' '.join(args)
                    bot.send_message(chat_id=chat_id, text=text)

                print('Subscribing to topic "{}".'.format(topic))
                options = SubscribeOptions(details_arg='details', match='prefix')
                await self.subscribe(onevent, topic, options)

        def onDisconnect(self):
            print('Disconnecting.')
            asyncio.get_event_loop().stop()

    runner = ApplicationRunner(url=url, realm=args.realm)
    runner.run(EventPrinter)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Subscribe to a topic and print events to a telegram chat.')
    parser.add_argument('host', type=str)
    parser.add_argument('port', type=int)
    parser.add_argument('realm', type=str)
    parser.add_argument('telegram', type=str)
    parser.add_argument('topic', type=str, nargs='+')

    main(parser.parse_args())
