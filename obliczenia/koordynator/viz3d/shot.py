import sys, time, subprocess, os, json
from playwright.sync_api import sync_playwright
# VEND: katalog z pakietem three@0.128.0 (polecenie: npm pack three@0.128.0; tar -xzf three-0.128.0.tgz -C vendor)
ROOT=os.path.abspath('../../../model-3d'); VEND=os.path.abspath('vendor/package')
srv=subprocess.Popen([sys.executable,'-m','http.server','8765','--bind','127.0.0.1','--directory',ROOT],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
time.sleep(1.0)
shots=json.loads(sys.argv[1]) if len(sys.argv)>1 else [{"name":"desk","w":1280,"h":800}]
try:
    with sync_playwright() as p:
        b=p.chromium.launch(executable_path='/usr/bin/google-chrome',headless=True,args=['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist','--enable-webgl'])
        for s in shots:
            ctx=b.new_context(viewport={'width':s['w'],'height':s['h']},device_scale_factor=s.get('dpr',1),color_scheme=s.get('scheme','light'))
            page=ctx.new_page()
            logs=[]
            page.on('console',lambda m:logs.append(m.type+': '+m.text))
            page.on('pageerror',lambda e:logs.append('PAGEERROR: '+str(e)))
            def route(r):
                u=r.request.url
                if 'three.min.js' in u: r.fulfill(path=VEND+'/build/three.min.js',content_type='application/javascript')
                elif 'OrbitControls.js' in u: r.fulfill(path=VEND+'/examples/js/controls/OrbitControls.js',content_type='application/javascript')
                elif 'fonts.googleapis.com' in u or 'fonts.gstatic.com' in u: r.fulfill(status=200,content_type='text/css',body='')
                else: r.continue_()
            page.route('**/*',route)
            page.goto('http://127.0.0.1:8765/index.html')
            page.wait_for_function('window.__farm3d && window.__farm3d.ready',timeout=20000)
            page.wait_for_timeout(2500)
            for act in s.get('acts',[]):
                page.evaluate(act); page.wait_for_timeout(1200)
            (page.locator('#stage').screenshot(path=s['name']+'.png') if s.get('stage') else page.screenshot(path=s['name']+'.png'))
            print(s['name'],'logs:',logs[:12])
            ctx.close()
        b.close()
finally:
    srv.terminate()
