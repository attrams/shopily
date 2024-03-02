# shopily

This e-commerce platform is a full-featured web application that allows users to browse products, add them to their cart, and make purchases. In addition to these standard e-commerce capabilities, our platform includes a blog section where we publish articles, guides, and news about our products and related topics. This integration aims to enrich the customer's shopping experience, offering them a one-stop solution for both their shopping needs and their quest for information.

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
