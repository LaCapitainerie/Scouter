### README
## Scouter Interface
**Scouter Interface** allow you **deploy continuously**, scopes, assets and technologies
With only **few lines of codes**.
With it Pipeline system, no need to think how it works, put the stuff you want to add
And the **intelligent pipeline** with do the work for you.

> __Have 600 Assets you want to add but afraid to make an error ?__
The pipeline system have a **Plan mode** to allow you to control what changes will be done, without touching the remote data
```py
Pipeline(mode="Plan")
```

## Installation

To install Scouter Interface, fork the repo and write your code, no packages are needed, allowing you to use it very easily

```bash
git clone https://github.com/LaCapitainerie/Scouter.git
```

### Utilisation

Store **all the tasks** you want to **execute in a pipeline**, set the mode and execute it
Each part of Scouter has their own tasks, some are removed or added beside the others

> [!NOTE]
> Syntax is important, get_ function will create a variable in memory that will be usable, add_ will an in the memory, delete_ will delete, and add_mass_ won't pass a reference to avoid memory surcharge

**Every functions** return an **Error Code**, and the **corresponding result** to log every steps.

> [!TIP]
> Every Function is fully customisable, to use an argument from another function, just add it in the header of the function.

#### Client
```py
def get_client(name:str, data:Data) -> tuple[int, Union[str, None]]:
    """Get a client ref from the Scouter platform"""
```

#### Perimeters
```py
def get_perimeter(client:str, name:str, data:Data, nolog:bool) -> tuple[int, Union[Perimeter, None]]:
    """ Get the perimeters from the Scouter platform"""
```

```py
def add_perimeter(session:Session, client:str, name:str, data:Data, mode:Mode, nolog:bool) -> tuple[int, Union[Perimeter, None]]:
    """Add a perimeter to the Scouter platform"""
```

```py
def delete_perimeter(session:Session, client: str, name:str, data:Data, mode:Mode, nolog:bool, force:bool=False) -> tuple[int, Union[Perimeter, None]]:
    """Delete the perimeter from the Scouter platform"""
```

#### Assets
```py
def get_asset(perimeter:Perimeter, name:str) -> tuple[int, Union[Asset, None]]:
    """Get the assets from the Scouter platform"""
```

```py
def add_asset(session:Session, perimeter: Perimeter, name: str, description: str, mode:Mode, nolog:bool) -> tuple[int, Union[Asset, None]]:
    """Add an asset to the Scouter platform"""
```

```py
def add_mass_assets(session:Session, perimeter:Perimeter, column:Sequence[Any], mode:Mode, nolog:bool) -> tuple[int, tuple[int, Iterable[Asset], int]]:
    """Add multiple assets in one take to the Scouter platform"""
```

```py
def delete_asset(session:Session, perimeter:Perimeter, name:str, mode:Mode, nolog:bool) -> tuple[int, Union[Asset, None]]:
    """Delete an asset from the Scouter platform"""
```

#### Technos
```py
def get_techno(asset: Asset, name:str) -> tuple[int, Union[Techno, None]]:
    """ Get the technos from the Scouter platform"""
```

```py
def add_techno(session:Session, asset: Asset, name:str, description:str, vendor:str, version:str, mode:Mode, nolog:bool) -> tuple[int, Union[Techno, None]]:
    """Add a techno to the Scouter platform"""
```

```py
def add_mass_technos(session:Session, asset: Asset, technos: list[dict], mode:Mode, nolog:bool) -> tuple[int, tuple[int, int]]:
    """Add a list of technos to the Scouter platform"""
```

```py
def delete_techno(session:Session, asset: Asset, name:str, mode:Mode, nolog:bool) -> tuple[int, Union[Techno, None]]:
    """Delete the techno from the Scouter platform"""
```



## Contributing
If you accept contributions, explain how other developers can contribute to your project. For example:

**Fork the project :** 
Create your feature branch (git checkout -b feature/AmazingFeature)

**Commit your changes :**
(git commit -m 'Add some AmazingFeature')

**Push to the branch :**
(git push origin feature/AmazingFeature)

<img width="1239" alt="image" src="https://github.com/LaCapitainerie/Scouter/assets/66835496/6f2a780f-18cc-4860-9d55-5bb806851149">

**Fill The Pull Request Card**

<img width="356" alt="image" src="https://github.com/LaCapitainerie/Scouter/assets/66835496/ebed97f3-a9cb-49f4-985e-ff1730894815">

**And Open a Pull Request**

Contact
LaCapitainerie - hugo.antreassian@gmail.com - CNPP

Project Link: https://github.com/LaCapitainerie/Scouter.git