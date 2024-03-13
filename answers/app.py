from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
import psycopg2
from urllib.parse import quote_plus

app = Flask(__name__)

# Set up Swagger documentation
SWAGGER_URL = '/api/docs'
API_URL = '/api/swagger.json'
swagger_ui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': 'Weather API'})
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# Connect to PostgreSQL database
params = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'password',
    'host': 'localhost',
}
conn = psycopg2.connect(**params)

# Define helper function for pagination
def paginate(items, offset, limit):
    return items[offset: offset + limit]

# @app.route('/api/swagger.json')
# def swagger():
#     return app.send_static_file('swagger.json')

# Define endpoint for /api/weather
@app.route('/api/weather')
def get_weather_data():
    # Get query parameters
    station_id = request.args.get('station_id')
    date = request.args.get('date')
    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 10))

    # Build SQL query
    sql = """
        SELECT * FROM weather_data
        WHERE (%s IS NULL OR station_id = %s)
        AND (%s IS NULL OR date = %s)
        ORDER BY date
    """
    params = [station_id, station_id, date, date]

    # Execute query
    cur = conn.cursor()
    cur.execute(sql, params)
    rows = cur.fetchall()

    # Paginate results
    paginated_rows = paginate(rows, offset, limit)

    # Build response
    results = []
    for row in paginated_rows:
        result = {
            'id': row[0],
            'station_id': row[1],
            'date': row[2].strftime('%Y-%m-%d'),
            'max_temperature': row[3],
            'min_temperature': row[4],
            'precipitation': row[5],
        }
        results.append(result)
    response = {'results': results}

    # Add pagination metadata
    response['metadata'] = {
        'offset': offset,
        'limit': limit,
        'total': len(rows),
    }

    return jsonify(response)

# Define endpoint for /api/weather/stats
@app.route('/api/weather/stats')
def get_weather_stats():
    # Get query parameters
    station_id = request.args.get('station_id')
    year = request.args.get('year')
    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 10))

    # Build SQL query
    sql = """
        SELECT * FROM weather_stats
        WHERE (%s IS NULL OR station_id = %s)
        AND (%s IS NULL OR year = %s)
        ORDER BY year
    """
    params = [station_id, station_id, year, year]

    # Execute query
    cur = conn.cursor()
    cur.execute(sql, params)
    rows = cur.fetchall()

    # Paginate results
    paginated_rows = paginate(rows, offset, limit)

    # Build response
    results = []
    for row in paginated_rows:
        result = {
            'id': row[0],
            'station_id': row[1],
            'year': row[2],
            'avg_max_temperature': row[3],
            'avg_min_temperature': row[4],
            'total_precipitation': row[5],
        }
        results.append(result)
    response = {'results': results}

    # Add pagination metadata
    response['metadata'] = {
        'offset': offset,
        'limit': limit,
        'total': len(rows),
    }

    # Return response
    return jsonify(response)

if __name__ == '__main__':
    app.run()
