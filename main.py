# -*- coding:utf-8 -*-
"""Expose API to clients."""
from __future__ import absolute_import
from __future__ import unicode_literals
import gevent
from gevent import monkey
monkey.patch_all()
from kits.create_app import app
from kits import initialize
from config.conf import conf
from sync_to_node import sync_poller
from callback import callback_poller


if __name__ == '__main__':
    initialize(["entrance", "logger", "mysql", "redis"])
    # gevent.spawn(sync_poller).start()
    # gevent.spawn(callback_poller).start()
    conf['logger'].info("Listen on port %d..." % conf['port'])
    app.run(host="0.0.0.0", port=conf['port'], debug=conf['env']['debug'])
