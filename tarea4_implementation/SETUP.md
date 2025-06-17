# Setup Guide - Tarea 4 Implementation

## Prerequisites

- Python 3.7+
- MySQL 5.7+ or MariaDB
- pip (Python package manager)

## Database Setup

1. **Create MySQL user and database:**
   ```sql
   CREATE USER 'cc5002'@'localhost' IDENTIFIED BY 'programacionweb';
   GRANT ALL PRIVILEGES ON *.* TO 'cc5002'@'localhost';
   FLUSH PRIVILEGES;
   ```

2. **Create and populate database:**
   ```bash
   # Create main database structure
   mysql -u cc5002 -p < tarea2.sql
   
   # Add comment table
   mysql -u cc5002 -p tarea2 < tabla-comentario.sql
   
   # Add rating table
   mysql -u cc5002 -p tarea2 < tabla-nota.sql
   
   # Populate regions and communes
   mysql -u cc5002 -p tarea2 < region-comuna.sql
   ```

## Python Environment Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create upload directory:**
   ```bash
   mkdir -p static/fotos
   ```

## Running the Application

1. **Start the Flask application:**
   ```bash
   python app.py
   ```

2. **Access the application:**
   - Open your browser and go to: http://localhost:5000

## Testing with Sample Data (Optional)

To populate the database with sample activities for testing:

```bash
python init_sample_data.py
```

This will create 5 sample activities with comments and ratings.

## Application Features

### New in Tarea 4:

1. **Rating System:**
   - Rate activities from 1-5 stars
   - View average ratings on listings
   - Rating statistics in charts

2. **Comment System:**
   - Add comments to activities
   - Real-time loading without page refresh
   - Comment validation

3. **Enhanced Statistics:**
   - New chart showing average ratings per activity
   - Updated existing charts

### Existing Features:

- Add new activities with photos and contact info
- Browse activities with pagination
- View detailed activity information
- Interactive region/commune selection
- Responsive design

## API Endpoints

### Comments API:
- `GET /api/comentarios/<activity_id>` - Get comments for activity
- `POST /api/comentarios/<activity_id>` - Add new comment

### Ratings API:
- `GET /api/notas/<activity_id>` - Get average rating for activity
- `POST /api/notas/<activity_id>` - Add new rating

### Statistics API:
- `GET /api/estadisticas/actividades_por_dia` - Activities by day
- `GET /api/estadisticas/actividades_por_tipo` - Activities by type
- `GET /api/estadisticas/actividades_por_horario_mes` - Activities by time/month
- `GET /api/estadisticas/promedio_notas` - Average ratings per activity

## File Structure

```
tarea4_implementation/
├── app.py                 # Main Flask application
├── models.py              # Database models
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── SETUP.md              # This setup guide
├── init_sample_data.py   # Sample data generator
├── static/
│   ├── style.css         # Styling
│   ├── script.js         # JavaScript functionality
│   └── fotos/            # Uploaded photos directory
├── templates/
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── agregar.html      # Add activity form
│   ├── listado.html      # Activity listing
│   ├── detalle.html      # Activity details with ratings/comments
│   └── estadisticas.html # Statistics with charts
├── tarea2.sql            # Main database schema
├── tabla-comentario.sql  # Comments table
├── tabla-nota.sql        # Ratings table
└── region-comuna.sql     # Chilean regions and communes data
```

## Troubleshooting

### Database Connection Issues:
- Verify MySQL is running
- Check username/password in app.py
- Ensure database 'tarea2' exists

### Photo Upload Issues:
- Ensure `static/fotos/` directory exists and is writable
- Check file permissions

### JavaScript/AJAX Issues:
- Check browser console for errors
- Verify all API endpoints are working
- Clear browser cache

## Development Notes

- The application uses Flask-SQLAlchemy for database operations
- CSRF protection is enabled for forms
- All AJAX operations include proper error handling
- File uploads are secured using werkzeug.secure_filename
- Rating validation ensures values are between 1-5
- Comment validation requires 3-80 characters for names and minimum 5 for text

## Production Considerations

For production deployment:
1. Change `app.secret_key` to a secure random value
2. Set `debug=False` in `app.run()`
3. Use a production WSGI server (gunicorn, uWSGI)
4. Configure proper database connection pooling
5. Implement proper logging
6. Add rate limiting for API endpoints
7. Use environment variables for sensitive configuration