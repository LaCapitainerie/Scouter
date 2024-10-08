from collections import deque
from typing import Any, Callable, Container, Union
from requests import Session

from Global.Login import Login
from Global.Sync import get_data

PipelineFunctions = Union[Callable, tuple[Callable, dict[str, Any]]]

class Mode:
    PLAN = "Plan"
    EXECUTE = "Execute"

class Run:
    REMOVED = "- [\033[31mx\033[0m]"
    ADDED = "- [\033[32m+\033[0m]"
    WARNING = "- [\033[33m!\033[0m]"
    INFO = "- [\033[34m-\033[0m]"
    STAY = "- [\033[37m=\033[0m]"


class Pipeline(list[Callable]):
    session: Union[Session, None]
    pipe: list[PipelineFunctions]
    kwargs: dict

    def __init__(self, mode="Plan", nolog:bool=False, *args: PipelineFunctions, **kwargs):
        self.pipe = list(args)
        self.session = None
        self.kwargs = kwargs
        self.kwargs.update({"mode": mode, "nolog": nolog})
        self.log:deque[dict[str, str]] = deque([{Run.INFO: "Pipeline started"}])

    def run(self):

        if not self.pipe:
            raise ValueError("The pipeline is empty")
        
        if get_data not in self.pipe:
            self.log.append({Run.WARNING: "Warning: Sync function not found in the pipeline"})

        if self.kwargs.get("mode") == "Plan":
            self.session = Session()

        else:
            if self.pipe[0].__annotations__.get("return", None) != Union[Session, None]:
                raise TypeError("The first function must return a Session object")

            if isinstance(self.pipe[0], Callable) and self.pipe[0] == Login:
                self.session = self.pipe[0](nolog=self.kwargs.get("nolog"))
        
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

            if not self.kwargs.get("nolog"):print(f"Running \033[1m{function.__name__}\033[0m")
            
            # self.log.append({Run.INFO: f"Running {function.__name__}"})

            Rcode, retour = function(**{k: v for k, v in self.kwargs.items() if k in function.__annotations__})

            name = f"'\033[1m{self.kwargs.get('name')}\033[0m'"
            func_name = function.__code__.co_name

            fromW = self.fromW(func_name.split("_", maxsplit=1)[1])
            tmp = self.kwargs.get(fromW)
            Name:str = tmp if isinstance(tmp, str) else tmp['name'] if issubclass(type(tmp), dict) else '' # type: ignore
            Sup = f"'\033[1m{Name}\033[0m'"
            
            if func_name.startswith("get_"):
                if not self.kwargs.get("nolog"):print(f"Got \033[1m{func_name[4:]}\033[0m")
                self.kwargs.update({func_name[4:]: retour})
            
            if func_name.startswith("add_"):

                if func_name.startswith("add_mass_"):
                    # self.kwargs.update({func_name[9:]: retour})
                    if Rcode == 1:
                        Already, Added, Error = retour
                        lAdded = len(Added)
                        f"\033[1m{lAdded}\033[0m assets added, \033[1m{Already}\033[0m already existed, \033[1m{Error}\033[0m errors"
                        
                        self.log.append({Run.INFO: "Mass assets :"})
                        if lAdded > 0:self.log.append({"\t": f"{Run.ADDED} Added {lAdded} assets"})
                        if Already > 0:self.log.append({"\t": f"{Run.STAY} {Already} already existed"})
                        if Error > 0:self.log.append({"\t": f"{Run.WARNING} {Error} errors"})

                        if d := self.kwargs.get("data"):
                            for asset in Added:
                                for scope in d[self.kwargs.get("client")]["scopes"]:
                                    if scope["name"] == Name:
                                        scope["assets"].append(asset)
                                        break

                else:
                    self.kwargs.update({func_name[4:]: retour})

                    if Rcode == 0:
                        self.log.append({Run.STAY: f"{name} {func_name[4:]} already exists in {fromW} {Sup}"})

                    elif Rcode == 1:
                        self.log.append({Run.ADDED: f"Added {name} {func_name[4:]} in {fromW} {Sup}"})

                        # Update Data for the next function

                        if d := self.kwargs.get("data"):


                            if func_name[4:] == "perimeter":
                                d[Name]["scopes"].append(retour)

                            elif func_name[4:] == "asset":
                                for scope in d[self.kwargs.get("client")]["scopes"]:
                                    if scope["name"] == Name:
                                        scope["assets"].append(retour)
                                        break

                            elif func_name[4:] == "techno":
                                perim = self.kwargs.get("perimeter") or {}
                                for scope in d[self.kwargs.get("client")]["scopes"]:
                                    if scope["name"] == perim.get("name"):
                                        asset = self.kwargs.get("asset") or {}
                                        for asset in scope["assets"]:
                                            if asset["name"] == asset.get("name"):
                                                asset["technologies"].append(retour)
                                                break
                                        break


                            self.kwargs.update({"data": self.kwargs.get("data")})

                    else:
                        self.log.append({Run.REMOVED: f"Error when adding {name} {func_name[4:]} in {fromW} {Sup}"})

            
            if func_name.startswith("delete_"):

                if not retour:
                    self.log.append({Run.WARNING: f"Failed to remove {name} {func_name[7:]} from {fromW} {Sup}"})
                else:
                    self.log.append({Run.REMOVED: f"Removed {func_name[7:]} {name} from {fromW} {Sup}"})

                    if d := self.kwargs.get("data"):
                        
                        if func_name[7:] == "perimeter":
                            tmp = d[self.kwargs.get("client")]["scopes"][:]
                            for scope in tmp:
                                if scope["name"] == retour.get("name"):
                                    d[Name]["scopes"].remove(scope)
                            del tmp

                        elif func_name[7:] == "asset":
                            tmp = d[self.kwargs.get("client")]["scopes"][:]
                            perim = self.kwargs.get("perimeter") or {}
                            for spos, scope in enumerate(tmp):
                                if scope["name"] == perim.get("name"):
                                    asset_ = self.kwargs.get("asset") or {}
                                    for pos, asset in enumerate(scope["assets"]):
                                        if asset["name"] == asset_.get("name"):
                                            del d[self.kwargs.get("client")]["scopes"][spos]["assets"][pos]
                                            break
                                    break

                        elif func_name[7:] == "techno":
                            tmp = d[self.kwargs.get("client")]["scopes"][:]
                            perim = self.kwargs.get("perimeter") or {}
                            for spos, scope in enumerate(tmp):
                                if scope["name"] == perim.get("name"):
                                    asset_ = self.kwargs.get("asset") or {}
                                    for pos, asset in enumerate(scope["assets"]):
                                        if asset["name"] == asset_.get("name"):
                                            for tpos, techno in enumerate(asset["technologies"]):
                                                if techno.get("name") == retour.get("name"):
                                                    del d[self.kwargs.get("client")]["scopes"][spos]["assets"][pos]["technologies"][tpos]
                                                    break
                                            break
                                    break

                            # d[self.kwargs.get("client")]["scopes"][spos]["assets"][pos]["technologies"].remove(techno)

        self.log_output(self.kwargs.get("mode")) # type: ignore

        return [*map(lambda x: next(iter(dict.keys(x))), self.log)]
    
    def fromW(self, string:str):
        if string == "techno":
            return "asset"
        elif string == "asset" or string == "mass_assets":
            return "perimeter"
        elif string == "perimeter":
            return "client"
        return f"None ({string})"
        
    
    def log_output(self, mode:Mode):
            
        print("\n\n")
                
        for i in self.log:
            key, val = i.items().__iter__().__next__()
            print(f"{key} {val}")

        print("\n\n")

        print(f"\033[32mPipeline finished in mode {mode}")
        print("No changes were made\033[37m") if mode == Mode.PLAN else print("Pipeline finished successfully\033[37m")