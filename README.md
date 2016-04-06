# Revealer
Flask application to serve multiple [reveal.js](https://github.com/hakimel/reveal.js/releases) slideshows.

## Requirements
In order to run the application you must satisfy the server dependencies, so before run, execute the following:

```terminal
$ pip install -r requirements.txt
```

## Configuration
Before you can run the application properly you must configure it to satisfy your needs. Open `revealer/config.py` and follow the instructions to provide the correct values.

### Databse
Revealer uses `MySQL` as database handler. Set the values of the `MYSQL_*` variables in order to connect correctly with `MYSQL`.

Also, the database `DATABASE_NAME` must exist before the application could be executed.

When the values are correct, run:

```terminal
$ python manage.py upgrade
```

### Secret Key
You must define a secret key. You can configure one doing so:

```python
SECRET_KEY='s0m353cr3tK3y'
```

## Usage
Now you can run:

```terminal
$ python manage.py runserver
```

## Serving slideshows
Examine the file in `revealer/static/example.html`. You'll find something like this:

```html+jinja
{% block slides %}
    <section>
        <!-- ... -->
    </section>
{% endblock %}
```
> The `example.html` file is also accessible by going to the `Upload` link on the application and downloading it from the page

Inside this block you can put your slides to be shown. Please see the [revealjs documentation](https://github.com/hakimel/reveal.js/README.md) to learn how.

After this, you can upload the resulting file to the server. Going to `slideshows` link will list all slideshows on the server, from there you can present yours.

Anytime you start presenting a slideshow, an entry on the index page its added, from there, the clients can connect to your presentation.

### Adding Resources
Custom styles or images can be added for the slideshow to use. Just upload them together with the slideshow template. To refer any of them use the `/files/<name>` uri, where `name` is the name of the file you want to use

```html
<!-- Use an uploaded image -->
<img src="/files/picture.png" />
```
