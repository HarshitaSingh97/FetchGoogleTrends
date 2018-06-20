#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request, Response, redirect
import sys
import time
from PygTrends import fetchtrends

appy = Flask(__name__)

@appy.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@appy.route('/', methods=['POST','GET'])
def index():
    try:
        keywords = request.args['keywords']
        kw_list = keywords.split(',')
        latitude = request.args['latitude']
        longitude = request.args['longitude']
        fromtime = request.args.get('from')
        totime = request.args.get('to')
        if(fromtime!=None and totime!=None):
            timeframe=fromtime+" "+totime
        else:
            timeframe=None
        if(timeframe==None):
            try:
                fetch_instance = fetchtrends(kw_list,latitude,longitude)
            except:
                return '''Append a list of 'keywords', 'latitude', 'longitude', 'from' (YYYY-MM-DD) and 'to' (YYYY-MM-DD) to the URL. 'from' and 'to' are optional.'''

        else:
            try:
                fetch_instance = fetchtrends(kw_list,latitude,longitude,timeframe)
            except:
                return '''Append a list of 'keywords', 'latitude', 'longitude', 'from' (YYYY-MM-DD) and 'to' (YYYY-MM-DD) to the URL. 'from' and 'to' are optional.'''
        df=""
        try:
            df=fetch_instance.fetch()
        except:
            time.sleep(60)
            df=fetch_instance.fetch()
        finally:
            if (len(df)==0):
                abort(404)
            jsondf=df.to_json()
            return '''{}'''.format(jsondf)
    except:
        return '''Append a list of 'keywords', 'latitude', 'longitude', 'from' (YYYY-MM-DD) and 'to' (YYYY-MM-DD) to the URL. 'from' and 'to' are optional.'''
header_text = '''
    <html>\n<head> <title>PyGT API</title> </head>\n<body>'''
instructions = '''
    <p><em>Hint</em>: This is a RESTful web service! Append a list of 'keywords', 'latitude', 'longitude', 'from' (YYYY-MM-DD) and 'to' (YYYY-MM-DD) to the URL (for example: <code>/?keywords=keywrd&latitude=0.0&longitude=0.0&from=2000-01-01&to=2010-01-01/code>) to get Google Trends data for a specific keyword, location and timeframe.</p>\n'''
footer_text = '</body>\n</html>'

if __name__ == '__main__':
    appy.run(threaded=True)
