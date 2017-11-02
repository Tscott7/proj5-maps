"""
Very simple Flask web site, with a map that uses geolocation to find the user
and places 3 markers on the map based on what is in the map.html file
Sources:
    https://developers.google.com/maps/documentation/javascript/examples/infowindow-simple
    https://developers.google.com/maps/documentation/javascript/examples/place-details
    https://stackoverflow.com/questions/36892826/click-on-google-maps-api-and-get-the-address
    https://developers.google.com/maps/documentation/javascript/examples/map-geolocation
    https://stackoverflow.com/questions/36892826/click-on-google-maps-api-and-get-the-address
    https://developers.google.com/maps/documentation/javascript/importing_data
    https://developers.google.com/maps/documentation/javascript/examples/infowindow-simple
    http://jsbeautifier.org/
    http://jinja.pocoo.org/docs/2.9/templates/
    https://stackoverflow.com/questions/15321431/how-to-pass-a-list-from-python-by-jinja2-to-javascript
    https://stackoverflow.com/questions/30578251/jinja2-string-variable-with-a-space-not-reading-correctly-in-classname
"""


import flask
import logging
import arrow      # Replacement for datetime, based on moment.js

# Our own modules
import pre        # Preprocess markers file
import config     # Configure from configuration files or command line


###
# Globals
###
app = flask.Flask(__name__)
if __name__ == "__main__":
    configuration = config.configuration()
else:
    # If we aren't main, the command line doesn't belong to us
    configuration = config.configuration(proxied=True)

if configuration.DEBUG:
    app.logger.setLevel(logging.DEBUG)

# Pre-processed markers is global, so be careful to update
# it atomically in the view functions.
#
markers = pre.process(open(configuration.MAP))
api_key = configuration.API_KEY


###
# Pages
# Each of these transmits the default "200/OK" header
# followed by html from the template.
###

@app.route("/")
@app.route("/index")
def index():
    """Main application page; most users see only this"""
    app.logger.debug("Main page entry")
    flask.g.markers = markers  # To be accessible in Jinja2 on page
    flask.g.api_key = api_key
    return flask.render_template('map.html')


@app.route("/refresh")
def refresh():
    """Admin user (or debugger) can use this to reload the markers."""
    app.logger.debug("Refreshing markers")
    global markers
    markers = pre.process(open(configuration.MAP))
    return flask.redirect(flask.url_for("index"))

### Error pages ###
#   Each of these transmits an error code in the transmission
#   header along with the appropriate page html in the
#   transmission body


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.g.linkback = flask.url_for("index")
    return flask.render_template('404.html'), 404


@app.errorhandler(500)
def i_am_busted(error):
    app.logger.debug("500: Server error")
    return flask.render_template('500.html'), 500


@app.errorhandler(403)
def no_you_cant(error):
    app.logger.debug("403: Forbidden")
    return flask.render_template('403.html'), 403


#################
#
# Functions used within the templates
#
#################

@app.template_filter('fmtdate')
def format_arrow_date(date):
    try:
        normal = arrow.get(date)
        return normal.format("ddd MM/DD/YYYY")
    except:
        return "(bad date)"


#
# If run as main program (not under gunicorn), we
# turn on debugging.  Connects to anything (0.0.0.0)
# so that we can test remote connections.
#
if __name__ == "__main__":
    app.run(port=configuration.PORT, host="0.0.0.0")
