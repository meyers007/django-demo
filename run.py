#pipi Django
#pipi install djangorestframework
#pipi install markdown       # Markdown support for the browsable API.
#pipi install django-filter  # Filtering support
#pipi django-rest-framework
#python manage.py migrate
#
export HOSTNAME=`hostname`
echo $HOSTNAME

python3 manage.py runserver 0:8000
