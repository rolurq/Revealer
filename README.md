# Reveal-Flask
Flask application to serve multiple [revealjs](https://github.com/hakimel/reveal.js/releases) slideshows.

## Usage
In order to run the application you must satisfy the server dependencies, so before run, execute the following:

```terminal
$ pip install -r requirements.txt
```

Now you can run:
```terminal
$ python manage.py runserver
```
In order for the application to work you must define a secret key. You can configure one doing so:
```terminal
$ export SECRET_KEY='s0m353cr3tK3y'
```

## Serving your presentation
Examine the file in `presentation/tenplates/example.html`. You'll find something like this:

```html+jinja
{% block slides %}
    <section>
        <!-- ... -->
    </section>
{% endblock %}
```
Inside this block you can put your slides to be shown. Please see the [revealjs documentation](https://github.com/hakimel/reveal.js/README.md) to learn how.

After this, you should save the modified file with the name of your preference, lets say: `myslide.html`. Now you can acces your slide from http://&lt;application_addr&gt;/myslide
