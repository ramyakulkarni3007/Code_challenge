import os
import psycopg2
import datetime
import logging

# Set up logging
logging.basicConfig(filename='weather_data_ingestion.log', level=logging.INFO)

def connect_to_database():
    """Connect to the PostgreSQL database"""
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="password",
        host="localhost"
    )
    return conn

def create_weather_data_table(conn):
    """Create the weather_data table"""
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS weather_data (
        id SERIAL PRIMARY KEY,
        station_id VARCHAR(255),
        date DATE,
        max_temperature FLOAT,
        min_temperature FLOAT,
        precipitation FLOAT
            );
    """)
    conn.commit()
    cur.close()

def create_weather_stats_table(conn):
    """Create the weather_stats table"""
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS weather_stats (
        id SERIAL PRIMARY KEY,
        station_id VARCHAR(255),
        year INTEGER,
        avg_max_temperature FLOAT,
        avg_min_temperature FLOAT,
        total_precipitation FLOAT
            );
    """)
    conn.commit()
    cur.close()

def insert_weather_data(conn, filename):
    """Insert weather data from a file into the database"""
    # Check which files have already been processed
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT station_id FROM weather_data")
    processed_files = set([row[0] for row in cur.fetchall()])
    # Specify the directory where the weather data files are stored
    directory = 'wx_data'

    # Start time
    start_time = datetime.datetime.now()
    logging.info(f"Started ingesting weather data at {start_time}")

    # Iterate over each file in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".txt") and filename[:-4] not in processed_files:
            with open(os.path.join(directory, filename), "r") as f:
                data = []
                for line in f:
                    # Extract the data from the line and check for missing values
                    fields = line.strip().split("\t")
                    if len(fields) == 4:
                        date, max_temp, min_temp, precipitation = fields
                        if max_temp != "-9999" and min_temp != "-9999" and precipitation != "-9999":
                            # Add the data to the list
                            data.append((filename[:-4], date, int(max_temp), int(min_temp), int(precipitation)))
                # Remove duplicates from the data
                data = list(set(data))
                # Insert the data into the database
                cur.executemany("INSERT INTO weather_data (station_id, date, max_temperature, min_temperature, precipitation) VALUES (%s, %s, %s, %s, %s)", data)
                conn.commit()
                # Log the number of records ingested
                logging.info(f"Ingested {len(data)} records from {filename}")

    # End time
    end_time = datetime.datetime.now()
    logging.info(f"Finished ingesting weather data at {end_time}")
    # Log the total time taken
    logging.info(f"Total time taken: {end_time - start_time}")
    # Close the database connection
    cur.close()

def calculate_weather_stats(conn):
    """Calculate and store weather statistics in the database"""
    cur = conn.cursor()
    query = """
        INSERT INTO weather_stats (
            station_id, 
            year, 
            avg_max_temperature, 
            avg_min_temperature, 
            total_precipitation
        )
        SELECT 
            station_id,
            EXTRACT(year FROM date) AS year,
            AVG(max_temperature)/10 AS avg_max_temperature,
            AVG(min_temperature)/10 AS avg_min_temperature,
            SUM(precipitation)/100 AS total_precipitation
        FROM 
            weather_data
        GROUP BY 
            station_id, 
            year;
    """
    cur.execute(query)
    conn.commit()
    cur.close()

if __name__ == '__main__':
    conn = connect_to_database()
    create_weather_data_table(conn)
    for filename in os.listdir("wx_data"):
        insert_weather_data(conn, filename)
    create_weather_stats_table(conn)
    calculate_weather_stats(conn)
    conn.close()

