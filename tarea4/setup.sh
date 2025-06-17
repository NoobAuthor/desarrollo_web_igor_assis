#!/bin/bash

# Setup script for Tarea 4 - Gestión de Actividades Recreativas
# This script automates the setup process for the Flask application

set -e  # Exit on any error

echo "=== Tarea 4 Setup Script ==="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running on supported OS
if [[ "$OSTYPE" != "linux-gnu"* ]] && [[ "$OSTYPE" != "darwin"* ]]; then
    print_warning "This script is designed for Linux/macOS. Windows users should run commands manually."
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.7+ first."
    exit 1
fi

print_status "Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 is not installed. Please install pip3 first."
    exit 1
fi

# Check if MySQL is installed
if ! command -v mysql &> /dev/null; then
    print_error "MySQL is not installed. Please install MySQL/MariaDB first."
    print_status "On Ubuntu/Debian: sudo apt-get install mysql-server"
    print_status "On macOS: brew install mysql"
    exit 1
fi

print_status "MySQL found: $(mysql --version)"

# Install Python dependencies
print_status "Installing Python dependencies..."
if pip3 install -r requirements.txt; then
    print_success "Python dependencies installed successfully"
else
    print_error "Failed to install Python dependencies"
    exit 1
fi

# Create static/fotos directory
print_status "Creating upload directory..."
mkdir -p static/fotos
chmod 755 static/fotos
print_success "Upload directory created"

# Database setup
echo ""
print_status "Setting up database..."
echo "Please enter your MySQL root password when prompted."

DB_USER="cc5002"
DB_PASS="programacionweb"
DB_NAME="tarea2"

# Create database user and grant privileges
print_status "Creating database user and privileges..."
mysql -u root -p << EOF
CREATE USER IF NOT EXISTS '${DB_USER}'@'localhost' IDENTIFIED BY '${DB_PASS}';
GRANT ALL PRIVILEGES ON *.* TO '${DB_USER}'@'localhost';
FLUSH PRIVILEGES;
EXIT
EOF

if [ $? -eq 0 ]; then
    print_success "Database user created successfully"
else
    print_error "Failed to create database user"
    exit 1
fi

# Create and populate database
print_status "Creating database schema..."
if mysql -u ${DB_USER} -p${DB_PASS} < database/tarea2.sql; then
    print_success "Main database schema created"
else
    print_error "Failed to create main database schema"
    exit 1
fi

print_status "Adding comments table..."
if mysql -u ${DB_USER} -p${DB_PASS} ${DB_NAME} < database/tabla-comentario.sql; then
    print_success "Comments table created"
else
    print_error "Failed to create comments table"
    exit 1
fi

print_status "Adding ratings table..."
if mysql -u ${DB_USER} -p${DB_PASS} ${DB_NAME} < database/tabla-nota.sql; then
    print_success "Ratings table created"
else
    print_error "Failed to create ratings table"
    exit 1
fi

print_status "Populating regions and communes..."
if mysql -u ${DB_USER} -p${DB_PASS} ${DB_NAME} < database/region-comuna.sql; then
    print_success "Regions and communes populated"
else
    print_error "Failed to populate regions and communes"
    exit 1
fi

# Ask if user wants sample data
echo ""
read -p "Do you want to populate the database with sample data for testing? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Creating sample data..."
    if python3 scripts/init_sample_data.py; then
        print_success "Sample data created successfully"
    else
        print_warning "Failed to create sample data, but the application should still work"
    fi
fi

# Final checks
echo ""
print_status "Running final checks..."

# Check if all required files exist
required_files=("app.py" "models.py" "templates/base.html" "static/style.css" "static/script.js")
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        print_success "✓ $file exists"
    else
        print_error "✗ $file is missing"
        exit 1
    fi
done

# Test database connection
if python3 -c "
import pymysql
try:
    conn = pymysql.connect(host='localhost', user='${DB_USER}', password='${DB_PASS}', database='${DB_NAME}')
    conn.close()
    print('Database connection successful')
except Exception as e:
    print(f'Database connection failed: {e}')
    exit(1)
"; then
    print_success "Database connection test passed"
else
    print_error "Database connection test failed"
    exit 1
fi

# Setup complete
echo ""
print_success "=== Setup Complete! ==="
echo ""
print_status "To start the application, run:"
echo "  python3 app.py"
echo ""
print_status "Then open your browser and go to:"
echo "  http://localhost:5000"
echo ""
print_status "Useful commands:"
echo "  • View logs: tail -f app.log (if logging is enabled)"
echo "  • Reset sample data: python3 scripts/init_sample_data.py"
echo "  • Check database: mysql -u ${DB_USER} -p${DB_PASS} ${DB_NAME}"
echo ""
print_status "For more information, see:"
echo "  • README.md - General documentation"
echo "  • SETUP.md - Detailed setup guide"
echo "  • docs/ - Additional documentation"
echo ""
print_success "Happy coding! 🚀"
