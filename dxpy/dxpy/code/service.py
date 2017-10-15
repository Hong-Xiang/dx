class SnippetMaker:
    from . import snippet

    @classmethod
    def service(cls, name, path='.'):
        pass

    @classmethod
    def component(cls, name, path='.'):
        cls.snippet.Component(name, path).make()
