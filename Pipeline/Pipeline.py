from typing import Callable, Union
from requests import Session


class Pipeline(list[Callable]):
    session: Union[Session, None]
    pipe: list[Callable]
    kwargs: dict

    def __init__(self, *args: Callable, **kwargs):
        self.pipe = list(args)
        self.session = None
        self.kwargs = kwargs

    def run(self):
        if self.pipe[0].__annotations__.get("return", None) != Union[Session, None]:
            raise TypeError("The first function must return a Session object")

        self.session = self.pipe[0]()
        if not self.session:
            return None

        for function in self.pipe[1:]:
            self.kwargs.update({"session": self.session})
            print(f"Running \033[1m{function.__name__}\033[0m")
            

            retour = function(**{k: v for k, v in self.kwargs.items() if k in function.__annotations__})
            if not retour:
                return None
            
            if function.__code__.co_name.startswith("get_"):
                self.kwargs.update({function.__code__.co_name[4:]: retour})

        return None