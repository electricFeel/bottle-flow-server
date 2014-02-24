"""
Setup the means to pull icons and component definitions
"""
import json, os
from bottle import Bottle, request, response, run, static_file
app = Bottle()

pallets = {};
components = {};

pallets = {}
components = {}

def loadEverything():
    for name in os.listdir("palettes"):
            if(os.path.isdir):
                #add the pallet
                pallets[name] = {}
                for component_file in os.listdir(os.path.join("palettes", name)):
                    #fo = open(os.path.join(base_path, "pallets", name, component_file))
                    #print os.path.exists(os.path.join("pallets", name, component_file))
                    json_data = open(os.path.abspath(os.path.join("palettes", name, component_file))).read()
                    c = json.loads(json_data)
                    components[c["componentID"]] = c
                    pallets[name][c["componentID"]] = c
 
@app.hook('after_request')
def enable_cors():
    """
    You need to add some headers to each request.
    Don't use the wildcard '*' for Access-Control-Allow-Origin in production.
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
 

@app.route('/icon/<name>', method=['OPTIONS', 'GET'])
def get_icon(name):
    return static_file(name, root='icons/')
 
@app.route('/icon', method=['OPTIONS', 'GET'])
def get_icon():
    return """
    <?xml version="1.0" encoding="utf-8"?>

<!-- License Agreement at http://iconmonstr.com/license/ -->

<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
     width="512px" height="512px" viewBox="0 0 512 512" style="enable-background:new 0 0 512 512;" xml:space="preserve">
<path id="gamepad-2-icon" d="M432,255.744v140H80v-140H432z M462,225.744H50v200h412V225.744z M195,339.244h-31.5v31.5h-27v-31.5
    H105v-27h31.5v-31.5h27v31.5H195V339.244z M276,370.744h-40v-15h40V370.744z M339.25,343.744c-9.94,0-18-8.061-18-18
    c0-9.941,8.06-18,18-18c9.941,0,18,8.059,18,18C357.25,335.684,349.191,343.744,339.25,343.744z M388.75,343.744
    c-9.94,0-18-8.061-18-18c0-9.941,8.06-18,18-18c9.941,0,18,8.059,18,18C406.75,335.684,398.691,343.744,388.75,343.744z
     M265.688,194.782v10.962H245.39v-10.962c0-26.72-8.237-31.061-37.144-36.433c-44.346-8.243-58.861-23.196-51.254-72.094
    l20.108,2.807c-6.104,38.547,2.114,43.245,34.854,49.33C237.162,143.076,265.688,149.078,265.688,194.782z"/>
</svg>

     """

@app.route('/component/<id>', method=['OPTIONS', 'GET'])
def get_component(id):
    return components[id]

@app.route('/pallet/<name>', method=['OPTIONS', 'GET'])
def get_pallet(name):
    return pallets[name]

 
if __name__ == '__main__':
    #load all of the pallets and then all of the components
    loadEverything()
    

    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("--host", dest="host", default="localhost",
                      help="hostname or ip address", metavar="host")
    parser.add_option("--port", dest="port", default=8080,
                      help="port number", metavar="port")

    (options, args) = parser.parse_args()
    run(app, host=options.host, port=int(options.port), debug=True)