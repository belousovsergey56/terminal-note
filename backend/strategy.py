from abc import ABC, abstractmethod

class HandlerStrategy(ABC):
    @abstractmethod
    def create(self, name):
        pass

    @abstractmethod
    def create_on_template(self, name):
        pass

    @abstractmethod
    def edit(self, name):
        pass

    @abstractmethod
    def delete(self, name):
        pass

    @abstractmethod
    def inline_note(self, text):
        pass

    @abstractmethod
    def read(self, name):
        pass

    @abstractmethod
    def show_tree(self):
        pass

class HandlerService:
    def __init__(self, strategy: HandlerStrategy):
        self._strategy = strategy

    def create(self, name):
        return self._strategy.create(name)

    def create_on_template(self, name):
        return self._strategy.create_on_template(name)

    def edit(self, name):
        return self._strategy.edit(name)

    def delete(self, name):
        return self._strategy.delete( name)

    def inline_note(self, text):
        return self._strategy.inline_note(text)

    def read(self, name):
        return self._strategy.read(name)

    def show_tree(self):
        return self._strategy.show_tree()
