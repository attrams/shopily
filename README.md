# shopily

This e-commerce platform is a web application that allows users to browse products, add them to their cart, and make purchases. In addition to these standard e-commerce capabilities, this webapp includes a blog section with articles, guides, and news about our products and related topics.

## Features

- **Product Catalogue**: A wide range of products categorized for easy navigation.
- **Search and Filter**: Search and filter options to help users find their desired products.
- **User Authentication**: Secure signup/login processes for a personalized shopping experience.
- **Shopping Cart**: A user-friendly cart for managing selected products before purchase.
- **Checkout System**: An integrated checkout system with multiple payment options.
- **Blog Section**: A dedicated section for articles, guides, and news to engage users and provide value beyond shopping.

## Libraries

- [pillow](https://python-pillow.org/) - required since image field is used in the product model.
- [celery](https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html) - for sending email asynchronously when order is created.
- [flower](https://flower.readthedocs.io/en/latest/) - for monitoring asynchronous task instead of using rabbitmq management ui.
- [stripe](https://github.com/stripe/stripe-python) - for processing payment.
- [python-dotenv](https://github.com/theskumar/python-dotenv) - for loading configuration.
- [weasyprint](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html) - for generating order invoice pdf.
- [redis](https://github.com/redis/redis-py) - stores products for frequently bought together feature.
- [easy-thumbnails](https://github.com/SmileyChris/easy-thumbnails) - for rendering thumbnails.
- [django-taggit](https://github.com/jazzband/django-taggit) - for working with blog tags.
- [psycopg2-binary](https://pypi.org/project/psycopg2-binary/) - PostgreSQL adapter.
- [django-extensions](https://github.com/django-extensions/django-extensions) - this extension also includes the installation of:
  - [werkzeug](https://pypi.org/project/Werkzeug/) - which is required by RunServerPlus extension of Django extensions.
  - [pyOpenSSL](https://pypi.org/project/pyOpenSSL/) - which is required to use SSL/TLS functionality of RunServerPlus.
- [django-allauth](https://docs.allauth.org/en/latest/introduction/index.html) - for social authentication(login with google).
- [django-rosetta](https://django-rosetta.readthedocs.io/) - interface for translations.
- [django-parler](https://django-parler.readthedocs.io/en/stable/) - for translating models.
- [django-localflavor](https://django-localflavor.readthedocs.io/en/latest/) - for country specific localization format.

## Note

In case you want to try out or clone this project, you need to carry out the steps below. You can simply use the docker image if you want to skip the steps below.

- Run the `requirements.txt` file to install the packages. you can run this file using the command `pip install -r requirements.txt` if you are not using a [virtual environment](https://docs.python.org/3/library/venv.html) or `python -m pip install -r requirements.txt` if you are using one.

- This project uses [postgresql](https://www.postgresql.org/) so you need to install postgresql if you haven't already installed it.

- [redis](https://redis.io/) is also required since it is used to store recommended products.

- Remember to run the migrations. This can be done by using the command `python manage.py migrate`.

- [Celery](https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html) requires a [message broker](https://en.wikipedia.org/wiki/Message_broker). You can check this part of the [documentation](https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html#choosing-a-broker) on how to install and run it.

- Add `.env` file at the root of the project. The root of the project is the folder that contains files like `manage.py`, `.gitignore` and etc.

  - Add the stripe configuration.

    - `STRIPE_PUBLISHABLE_KEY`=`"your stripe publishable key"`
    - `STRIPE_SECRET_KEY`=`"your stripe secret key"`
    - `STRIPE_API_VERSION`=`"your api version"`
    - `STRIPE_WEBHOOK_SECRET`=`"your webhook secret"`

    To get the above values, you can follow the steps below:

    1.  Visit [stripe](https://dashboard.stripe.com/login).
    2.  Create an app. This can be located at the left top corner.
    3.  Access the [developers](https://dashboard.stripe.com/test/developers) page.
    4.  You can find the api version on this page.
    5.  Checkout the [API keys](https://dashboard.stripe.com/test/apikeys) tab for api keys.
    6.  Visit [webhooks](https://dashboard.stripe.com/test/webhooks/create?endpoint_location=local) for the stripe webhook secret.

    After getting these values set each variable in the `.env` file.

  - Along with the stripe configurations, you also need these:

    These for redis configuration.

    - `REDIS_HOST`= `"your redis host"`
    - `REDIS_PORT`= `"your redis port"`
    - `REDIS_DB`= `"your redis DB name"`

    These for DB configuration(postgres)

    - `DB_NAME`= `"your postgres database name"`
    - `DB_USERNAME`= `"your postgres database username"`
    - `DB_PASSWORD`= `"your postgres database password"`
    - `DB_HOST`= `"your postgres host"`
    - `DB_PORT`= `"your postgres port"`

    In case you want to check out social authentication with google, switch to the `social-auth` branch. These configurations will be needed for the google social authentication to work.

    - `GOOGLE_CLIENT_ID` = `"your google client id"`
    - `GOOGLE_SECRET` = `"your google secret"`
    - `GOOGLE_KEY` = `"your google key"`

    You can check these pages on how to get them.

    - [How to get Google Client ID and Client Secret?](https://www.balbooa.com/help/gridbox-documentation/integrations/other/google-client-id)
    - [Setting up OAuth 2.0](https://support.google.com/cloud/answer/6158849?hl=en)

- With your message broker running, Run [celery](https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html) with the command `celery -A myshop worker -l info`. You also have to run the [stripe webhook](https://dashboard.stripe.com/test/webhooks/create?endpoint_location=local) for the stripe webhook to automatically update order status. This can be done using the command `stripe listen --forward-to [your webhook path]`. For this project, the stripe webhooks will be forwarded to `localhost:8000/payment/webhook/` that is `stripe listen --forward-to localhost:8000/payment/webhook/`. Then you can run the django project. So in all four things must be running, your chosen message broker, [celery](https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html), [stripe webhook](https://dashboard.stripe.com/test/webhooks/create?endpoint_location=local) and the django project.

- You can check this page on stripe for [test cards](https://stripe.com/docs/testing) when you get to the payment page.
