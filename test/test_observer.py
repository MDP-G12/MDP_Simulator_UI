class Observable:
    def __init__(self):
        self.__observers = []

    def register_observer(self, observer):
        self.__observers.append(observer)

    def notify_observers(self, *args, **kwargs):
        for observer in self.__observers:
            observer(self, *args, **kwargs)


class Observer1:
    def __init__(self, observable):
        observable.register_observer(self.handler)

    def handler(self, observable, *args, **kwargs):
        print('Handler1: Got', args, kwargs, 'From', observable)

class Observer2:
    def __init__(self, observable):
        observable.register_observer(self.handler)

    def handler(self, observable, *args, **kwargs):
        print('Handler2: Got', args, kwargs, 'From', observable)


subject = Observable()
observer1 = Observer1(subject)
observer2 = Observer2(subject)
subject.notify_observers('test')
