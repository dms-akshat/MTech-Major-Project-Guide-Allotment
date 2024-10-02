pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
#!/bin/bash

# A shell script to automatically create a Django superuser if it doesn't already exist

# Define superuser credentials
SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-"admin@example.com"}
SUPERUSER_USERNAME=${DJANGO_SUPERUSER_USERNAME:-"admin"}
SUPERUSER_PASSWORD=${DJANGO_SUPERUSER_PASSWORD:-"adminpass123"}

# Navigate to the Django project directory (adjust path if necessary)
PROJECT_DIR="/path/to/your/django/project"
cd $PROJECT_DIR

# Activate your virtual environment (if applicable)
# Uncomment the line below if using a virtual environment
# source /path/to/your/virtualenv/bin/activate

# Check if the superuser exists
echo "Checking if superuser $SUPERUSER_USERNAME exists..."
EXISTS=$(echo "from django.contrib.auth.models import User; print(User.objects.filter(username='$SUPERUSER_USERNAME').exists())" | python manage.py shell)

if [ "$EXISTS" = "True" ]; then
    echo "Superuser $SUPERUSER_USERNAME already exists. No need to create."
else
    echo "Creating superuser $SUPERUSER_USERNAME..."

    # Create the superuser non-interactively using Django's manage.py
    python manage.py createsuperuser --noinput --email "$SUPERUSER_EMAIL" --username "$SUPERUSER_USERNAME"

    # Use the Django shell to set the password for the superuser
    echo "from django.contrib.auth.models import User; user = User.objects.get(username='$SUPERUSER_USERNAME'); user.set_password('$SUPERUSER_PASSWORD'); user.save();" | python manage.py shell

    echo "Superuser $SUPERUSER_USERNAME created successfully!"
fi

