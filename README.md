# How to use "bower" in Django project on Mac

## Better Option

1. Install Anaconda and related pip packages to use Django (details omitted)
2. Create a project such as this 
    ```django-admin startproject demo```
3. install bower on your computer ```$ brew install bower```
```
$ cd demo; mkdir static; cd static;
$ bower init; cd ..
```

4 Edit file ```demo/settings.py``` and Add the following line
```
    $ vi demo/settings.py
          STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    $ python manage.py collectstatic 
```

```
$ cd static; bower install bootstrap --save
$ bower install jquery --save
$ ln -s bower_components bc
$ cd ..; python manage.py migrate; python manage.py runserver
```

4. Now you could use the javascripts from "/static/bower_components/

## Install Additional Components:
```
cd static
bower install highcharts w2ui highstock highmaps
```


## References:

* https://medium.com/@siddhism/using-bower-to-manage-static-files-with-django-8521331023af


## Github link

* This demo is available on github for cloning: "https://github.com/meyers007/django-demo.git"
