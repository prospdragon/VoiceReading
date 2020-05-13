from flask_assets import Environment, Bundle


def compile_assets(app):
    """Configure logged-in asset bundles."""
    assets = Environment(app)
    Environment.auto_build = True
    Environment.debug = False

    # Stylesheets Bundle
    less_bundle = Bundle('src/less/style.less',
                         filters='less,cssmin',
                         output='dist/css/style.css',
                         extra={'rel': 'stylesheet/less'})

    # JavaScript Bundle
    js_bundle = Bundle('src/js/app.js',
                       filters='jsmin',
                       output='dist/js/app.min.js')

    # Register assets
    assets.register('less_all', less_bundle)
    assets.register('js_all', js_bundle)

    # Build assets in development mode
    if app.config['FLASK_ENV'] == 'development':
        less_bundle.build()
        js_bundle.build()
