import json

import web

from .config import DEFAULT_MODE, TEMPLATE_DIR
from .utils import Update

render = web.template.render(TEMPLATE_DIR)

class WebServer():
    def __init__(self, data, port):
        self.data = data
        self.port = port
    def run(self, update_queue):
        self.update_queue = update_queue

        class Index:
            """Main Controls Page"""
            def GET(_):
                # the output mode is passed as an IntFlag
                mode = int(web.input().get('mode', DEFAULT_MODE))
                self.update_queue.append((Update.START, mode))
                return render.index(self.data)

        class Launch:
            """Initial Launch Screen"""
            def GET(_):
                return render.launch()

        class Style:
            """Endpoint for updating the foreground style"""
            def POST(_):
                target = json.loads(web.data().decode())
                style = target['style']
                part = target['part']
                if part == 'foreground':
                    self.update_queue.append((Update.FG_STYLE, style))
                elif part == 'background':
                    self.update_queue.append((Update.BG_STYLE, style))
                return web.OK()
        
        class Background:
            """Endpoint for updating the type of background handling"""
            def POST(_):
                state = web.data().decode() == 'true'
                self.update_queue.append((Update.BACKGROUND, state))
                return web.OK()
        
        class Exit:
            def POST(_):
                self.update_queue.append((Update.EXIT, None))
                self.app.stop()
                return web.OK()
        
        class Resolution:
            def POST(_):
                self.update_queue.append((Update.RESOLUTION, web.data().decode()))
                return web.OK()
        
        class BgType:
            def POST(_):
                self.update_queue.append((Update.BG_TYPE, web.data().decode()))
                return web.OK()

        urls = (
            # html sites
            '/controls', Index,
            '/launch', Launch,
            # change options
            '/style', Style,
            '/background', Background,
            '/exit', Exit,
            '/resolution', Resolution,
            '/bg_type', BgType,
            
        )

        # Set the port for launching the server
        import os
        os.environ["PORT"] = str(self.port)
        self.app = web.application(urls, globals())
        print('starting web server')
        self.app.run()
    def stop(self):
        self.app.stop()
