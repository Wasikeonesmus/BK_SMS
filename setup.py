from setuptools import setup, find_packages

setup(
    name="upendo-bakery",
    version="1.0.0",
    description="Upendo Bakery Management System",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "Django==5.2.1",
        "django-phonenumber-field==7.3.0",
        "phonenumbers==8.13.30",
        "Pillow==6.2.2",
        "python-decouple==3.8",
        "whitenoise==6.6.0",
        "crispy-forms==2.1",
        "crispy-bootstrap5==0.7",
        "dj-database-url==2.1.0",
        "psycopg2-binary==2.9.9",
        "boto3==1.34.69",
        "sentry-sdk==2.6.1",
        "gunicorn==21.2.0",
    ],
) 