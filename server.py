"""
Setup the means to pull icons and component definitions
"""
import json, os
from bottle import Bottle, request, response, run, static_file
app = Bottle()

pallets = {}
components = {}

def loadEverything():
    for name in os.listdir("palettes"):
            if(os.path.isdir):
                #add the pallet
                pallets[name] = {"components": {}}
                pallete_json = json.loads(open(os.path.abspath(os.path.join("palettes", name, "_config.pc"))).read())
                pallets[name]['SVGIcon'] = get_icon(pallete_json['SVGIcon'])
                pallets[name]['DisplayName'] = pallete_json['DisplayName']

                for component_file in os.listdir(os.path.join("palettes", name)):
                    #fo = open(os.path.join(base_path, "pallets", name, component_file))
                    #print os.path.exists(os.path.join("pallets", name, component_file))
                    if not component_file.endswith(".json"):
                        continue

                    json_data = open(os.path.abspath(os.path.join("palettes", name, component_file))).read()
                    c = json.loads(json_data)
                    components[c["componentID"]] = c
                    pallets[name]["components"][c["componentID"]] = c
 
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

@app.route('/component/<id>', method=['OPTIONS', 'GET'])
def get_component(id):
    return components[id]

@app.route('/palette/<name>', method=['OPTIONS', 'GET'])
def get_palette(name):
    return pallets[name]

@app.route('/palette', method=['OPTIONS', 'GET'])
def get_palettes():
    return json.dumps(pallets)
 
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