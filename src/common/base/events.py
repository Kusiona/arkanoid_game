class EventHandlingMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for arg in args:
            main_app_class = arg
            if hasattr(arg, '__repr__') and arg.__repr__().endswith('Menu'):
                main_app_class = arg.main_app_class
        main_app_class.extra_event_handlers.append(self.handle_event)

    def handle_event(self, event):
        pass
