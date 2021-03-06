
def set_urls(handler, modules):
    for module_name in modules:
        try:
            module = __import__(module_name+'.urls')
            if getattr(getattr(module, 'urls'), 'urls', None):
                urls = getattr(module, 'urls').urls
                router = handler.get_router()
                for url in urls:
                    router.register(url[0], url[1])
            else:
                continue
        except ModuleNotFoundError:
            pass


def render():
    return
