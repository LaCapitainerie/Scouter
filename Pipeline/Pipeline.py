from collections import deque
from os import name
from typing import Any, Callable, Container, Type, TypeVar, Union
from requests import Session

from Global.Login import Login
from Global.Sync import get_data

PipelineFunctions = Union[Callable, tuple[Callable, dict[str, Any]]]

class Run:
    REMOVED = "red"
    ADDED = "green"
    WARNING = "yellow"
    INFO = "blue"
    STAY = "gray"


class Pipeline(list[Callable]):
    session: Union[Session, None]
    pipe: list[PipelineFunctions]
    kwargs: dict

    def __init__(self, *args: PipelineFunctions, **kwargs):
        self.pipe = list(args)
        self.session = None
        self.kwargs = kwargs
        self.log:deque[dict[str, str]] = deque([{Run.INFO: "Pipeline started"}])

    def run(self):

        if not self.pipe:
            raise ValueError("The pipeline is empty")
        
        if get_data not in self.pipe:
            print("Warning: Sync function not found in the pipeline")
            print("You run the risk of not having the necessary data to run the pipeline")

        if self.pipe[0].__annotations__.get("return", None) != Union[Session, None]:
            raise TypeError("The first function must return a Session object")

        if isinstance(self.pipe[0], Callable) and self.pipe[0] == Login:
            self.session = self.pipe[0]()
        
        if not self.session:
            return None

        for function in self.pipe[1:]:
            self.kwargs.update({"session": self.session})
            

            if isinstance(function, tuple):
                function, args = function
                if not isinstance(args, Container):
                    raise TypeError("The second element of the tuple must be a Container")
                
                self.kwargs.update(args)

            elif isinstance(function, Callable):
                ...

            else:
                raise TypeError("The function must be a Callable or a tuple")

                

            print(f"Running \033[1m{function.__name__}\033[0m")
            
            self.log.append({Run.INFO: f"Running {function.__name__}"})

            retour = function(**{k: v for k, v in self.kwargs.items() if k in function.__annotations__})


            name = f"'\033[1m{self.kwargs.get('name')}\033[0m'"
            func_name = function.__code__.co_name
            
            
            if func_name.startswith("get_"):
                print(f"Got \033[1m{func_name[4:]}\033[0m")
                self.kwargs.update({func_name[4:]: retour})

            
            if func_name.startswith("add_"):

                if not retour:
                    self.log.append({Run.STAY: f"{name} {func_name[4:]} already exists"})

                else:
                    self.log.append({Run.ADDED: f"Added {func_name[4:]}"})

            
            if func_name.startswith("delete_"):

                if not retour:
                    self.log.append({Run.WARNING: f"Failed to remove {name} {func_name[7:]}"})
                else:
                    self.log.append({Run.REMOVED: f"Removed {func_name[7:]} {name}"})

        self.log_output()

        return None
    
    def log_output(self):
        def icon_from_log(str):
            if str == Run.REMOVED:
                return "- [\033[31mx\033[0m]"
            elif str == Run.ADDED:
                return "- [\033[32m+\033[0m]"
            elif str == Run.WARNING:
                return "- [\033[33m!\033[0m]"
            elif str == Run.INFO:
                return "- [\033[34m-\033[0m]"
            elif str == Run.STAY:
                return "- [\033[37m=\033[0m]"
            else:
                return "- []"
            
        print("\n\n")
                
        for i in self.log:
            key, val = i.popitem()
            print(f"{icon_from_log(key)} {val}")