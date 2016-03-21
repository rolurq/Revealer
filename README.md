# Revealer
Flask application to serve multiple [reveal.js](https://github.com/hakimel/reveal.js/releases) slideshows.

## Configuration
Before you can run the application properly you must configure it to satisfy your needs. Open `revealer/config.py` and follow the instructions to provide the correct values.

### Secret Key
You must define a secret key. You can configure one doing so:
```terminal
$ export SECRET_KEY='s0m353cr3tK3y'
```

## Usage
In order to run the application you must satisfy the server dependencies, so before run, execute the following:

```terminal
$ pip install -r requirements.txt
```

Now you can run:
```terminal
$ python manage.py runserver
```

## Serving your presentation
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

After this, you should save the modified file with the name of your preference, lets say: `myslide.html`. Now you can acces your slide from http://&lt;application_addr&gt;/myslide
