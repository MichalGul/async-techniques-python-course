import flask

import services.weather_service as weather_service
import services.sun_service as sun_service
import services.location_service as location_service

blueprint = flask.blueprints.Blueprint("city_api", "city_api")


@blueprint.route('/api/weather/<zip_code>/<country>', methods=['GET'])
def weather(zip_code: str, country: str):
    weather_data = weather_service.get_current(zip_code, country)
    if not weather_data:
        flask.abort(404)
    return flask.jsonify(weather_data)


@blueprint.route('/api/weather_geo/<lat>/<lon>', methods=['GET'])
async def weather_geo(lat: str, lon: str):
    weather_data = await weather_service.get_current_by_geo(lat, lon)
    if not weather_data:
        flask.abort(404)
    return flask.jsonify(weather_data)



@blueprint.route('/api/sun/<lat>/<long>', methods=['GET'])
async def sun(lat: str, long: str):
    sun_data = await sun_service.for_today(lat, long)
    if not sun_data:
        flask.abort(404)
    return flask.jsonify(sun_data)





@blueprint.route('/api/sun/<zip_code>/<country>', methods=['GET'])
def sun_by_zip(zip_code: str, country: str):
    lat, long = location_service.get_lat_long(zip_code, country)
    sun_data = sun_service.for_today(lat, long)
    if not sun_data:
        flask.abort(404)
    return flask.jsonify(sun_data)


