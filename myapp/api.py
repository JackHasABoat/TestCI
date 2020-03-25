# Simple Code
import logging, logging.handlers
import traceback
import yaml
from flask import Flask, request, abort, Response, stream_with_context
from werkzeug.datastructures import Headers
from io import StringIO

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

thePropertyFile = "properties.yml"

theProperties = yaml.load(open(thePropertyFile, 'r'))
theAppPath = theProperties['api']['path']
thePortNumber = int(theProperties['api']['port'])
logger.info('The application path is %s, the port number is %s' % (theAppPath, thePortNumber))

app = Flask(__name__, static_url_path='%s/static' % (theAppPath))

@app.route('/')
def hello_world():
    return 'Hey, we have Flask in a Docker container!\n'

# Healthy Check
# Test with http://localhost:5000/health
@app.route('/health', methods=['GET'])
def healthChecking():
    return 'Version 0.10\n', 200

# Get the mail users' server and mailfile info by Customer ID
# Test with http://localhost:5000/download/abc/123?extension=txt
@app.route('/download/<string:theName>/<int:theID>', methods=['GET'])
def downloadFile(theName, theID):
    logger.info('Preparing downloading data for %s with ID %s ...' % (theName, theID))

    try:
        if request.args.get('extension', '') == 'txt':
            logger.info('Preparing txt file contents...')

            def generate():
                try:
                    contentsBody = StringIO()

                    contentsBody.write(
                        '"ItemID", "Name","Available"\n')

                    yield contentsBody.getvalue()

                    contentsBody.seek(0)
                    contentsBody.truncate(0)

                    for item in range(10):
                        row = []
                        row.append(str(item))
                        row.append("Item Name Is " +str(item))
                        row.append("Yes")
                        contentsBody.write('"' + '","'.join(row) + '"\n')

                        yield contentsBody.getvalue()
                        contentsBody.seek(0)
                        contentsBody.truncate(0)
                except:
                    logger.error('File creation exception: %s' % (traceback.format_exc()))

            headers = Headers()
            headers.set('Content-Disposition', 'attachment', filename='%s.txt' % (str(theID)))
            return Response(stream_with_context(generate()), mimetype='text/txt', headers=headers)

        else:
            raise Exception('None txt files are not supported.')

    except:
        logger.warning(
            'Exception in downloadFile. Stack trace is: %s' % (traceback.format_exc()))
        abort(404)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=thePortNumber, debug=False, threaded=True)
