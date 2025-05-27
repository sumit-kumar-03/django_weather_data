# UK MetOffice Weather Data API

A Django REST API application for parsing, storing, and serving UK MetOffice weather data.

## Features

- **Data Parsing**: Parse UK MetOffice weather data format
- **Data Storage**: Store weather data in PostgreSQL database
- **REST API**: Comprehensive API with CRUD operations and analytics
- **Statistics**: Generate statistical analysis of weather data
- **Filtering**: Filter data by year, year ranges
- **Docker Support**: Containerized application with Docker Compose
- **Tests**: Comprehensive test suite
- **Admin Interface**: Django admin for data management

## Installation & Setup

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd weather-api-project
```

2. Copy environment file:
```bash
cp .env.example .env
```

3. Build and run with Docker Compose:
```bash
docker-compose up --build
```

4. Run migrations:
```bash
docker-compose exec web python manage.py migrate
```

5. Create superuser (optional):
```bash
docker-compose exec web python manage.py createsuperuser
```

### Manual Installation

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up PostgreSQL database and update `.env` file

4. Run migrations:
```bash
python manage.py migrate
```

5. Start development server:
```bash
python manage.py runserver
```

## Data Import

Import weather data using the management command:

```bash
# Using Docker
docker-compose exec web python manage.py import_weather_data /path/to/data/file.txt

# Manual installation
python manage.py import_weather_data /path/to/data/file.txt
```

Options:
- `--replace`: Replace existing data for duplicate years
- `--clear`: Clear all existing data before import

## API Endpoints

### Weather Data CRUD
- `GET /api/weather/` - List all weather data
- `POST /api/weather/` - Create new weather record
- `GET /api/weather/{id}/` - Get specific weather record
- `PUT /api/weather/{id}/` - Update weather record
- `DELETE /api/weather/{id}/` - Delete weather record

### Query Parameters
- `year`: Filter by specific year
- `year_from`: Filter from year
- `year_to`: Filter to year

### Analytics Endpoints
- `GET /api/weather/summary/` - Get summarized weather data
- `GET /api/weather/statistics/` - Get statistical analysis
- `GET /api/weather/{id}/monthly_breakdown/` - Get monthly breakdown for specific year

### Example API Responses

**List Weather Data:**
```json
{
  "count": 36,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "year": 1884,
      "january": 7.3,
      "february": 6.8,
      "march": 8.5,
      "april": 10.1,
      "may": 14.5,
      "june": 17.1,
      "july": 18.8,
      "august": 20.2,
      "september": 17.0,
      "october": 11.8,
      "november": 7.5,
      "december": 5.8,
      "winter": null,
      "spring": 11.02,
      "summer": 18.73,
      "autumn": 12.10,
      "annual": 12.14,
      "monthly_data": {
        "january": 7.3,
        "february": 6.8,
        // ... other months
      },
      "seasonal_data": {
        "winter": null,
        "spring": 11.02,
        "summer": 18.73,
        "autumn": 12.10
      },
      "created_at": "2024-01-01T12:00:00Z",
      "updated_at": "2024-01-01T12:00:00Z"
    }
  ]
}
```

**Statistics:**
```json
{
  "total_records": 36,
  "year_range": {
    "from": 1884,
    "to": 1919
  },
  "annual_statistics": {
    "avg_temperature": 11.75,
    "max_temperature": 12.87,
    "min_temperature": 10.81
  },
  "seasonal_statistics": {
    "winter": {
      "avg": 5.89,
      "max": 7.58,
      "min": 3.57
    },
    "spring": {
      "avg": 10.91,
      "max": 13.98,
      "min": 9.41
    },
    "summer": {
      "avg": 17.87,
      "max": 20.36,
      "min": 16.34
    },
    "autumn": {
      "avg": 12.08,
      "max": 13.68,
      "min": 10.37
    }
  },
  "extreme_years": {
    "hottest": {
      "year": 1893,
      "temperature": 12.87
    },
    "coldest": {
      "year": 1888,
      "temperature": 10.81
    }
  }
}
```

## Data Format

The application expects UK MetOffice data in the following format:

```
year    jan    feb    mar    apr    may    jun    jul    aug    sep    oct    nov    dec     win     spr     sum     aut     ann
1884    7.3    6.8    8.5   10.1   14.5   17.1   18.8   20.2   17.0   11.8    7.5    5.8     ---   11.02   18.73   12.10   12.14
1885    4.3    7.3    7.2   10.8   11.8   17.0   19.4   16.8   15.0    9.3    7.5    5.9    5.75    9.91   17.76   10.58   11.04
```

Where:
- `year`: Year of the data
- `jan-dec`: Monthly temperature averages
- `win,spr,sum,aut`: Seasonal averages
- `ann`: Annual average
- `---`: Missing data (stored as NULL)

## Testing

Run the test suite:

```bash
# Using Docker
docker-compose exec web python manage.py test

# Manual installation
python manage.py test
```

The test suite includes:
- Model tests
- Parser tests
- API endpoint tests
- Data validation tests

## Admin Interface

Access the Django admin at `/admin/` after creating a superuser:

```bash
# Using Docker
docker-compose exec web python manage.py createsuperuser

# Manual installation
python manage.py createsuperuser
```

## Architecture

### Components

1. **Models** (`weather_api/models.py`):
   - `WeatherData`: Main model for storing weather information

2. **Parsers** (`weather_api/parsers.py`):
   - `UKMetOfficeParser`: Parses UK MetOffice data format

3. **Views** (`weather_api/views.py`):
   - `WeatherDataViewSet`: REST API viewset with CRUD and analytics

4. **Serializers** (`weather_api/serializers.py`):
   - Data serialization for API responses

5. **Management Commands** (`weather_api/management/commands/`):
   - `import_weather_data`: Command for importing data files

### Database Schema

```sql
CREATE TABLE weather_data (
    id SERIAL PRIMARY KEY,
    year INTEGER UNIQUE NOT NULL,
    january FLOAT,
    february FLOAT,
    -- ... other months
    winter FLOAT,
    spring FLOAT,
    summer FLOAT,
    autumn FLOAT,
    annual FLOAT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

## Configuration

Key configuration options in `settings.py`:

- **Database**: PostgreSQL configuration
- **REST Framework**: Pagination and rendering settings
- **Static Files**: Handled by WhiteNoise
- **Time Zone**: UTC
- **Debug**: Controlled by environment variable

## Environment Variables

Create a `.env` file with:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=weather_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

## Production Deployment

For production deployment:

1. Set `DEBUG=False` in environment variables
2. Configure proper `SECRET_KEY`
3. Set up proper `ALLOWED_HOSTS`
4. Use production database settings
5. Configure reverse proxy (nginx/Apache)
6. Set up SSL certificates
7. Configure logging and monitoring

## API Usage Examples

### Filter by year range:
```bash
curl "http://localhost:8000/api/weather/?year_from=1890&year_to=1900"
```

### Get statistics:
```bash
curl "http://localhost:8000/api/weather/statistics/"
```

### Get monthly breakdown:
```bash
curl "http://localhost:8000/api/weather/1/monthly_breakdown/"
```

### Create new record:
```bash
curl -X POST "http://localhost:8000/api/weather/" \
  -H "Content-Type: application/json" \
  -d '{"year": 2023, "january": 5.5, "annual": 12.0}'
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes and add tests
4. Run the test suite
5. Submit a pull request

## License

This project is licensed under the MIT License.