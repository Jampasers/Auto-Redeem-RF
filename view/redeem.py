import discord
import importlib
import pkgutil
import inspect
from pathlib import Path

class RedeemView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        package_name = "buttons.redeem"

        package = importlib.import_module(package_name)

        package_path = Path(package.__file__).parent

        for _, module_name, is_pkg in pkgutil.iter_modules([str(package_path)]):
            if is_pkg:
                continue 

            module = importlib.import_module(f"{package_name}.{module_name}")

            for _, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, discord.ui.Button) and obj is not discord.ui.Button:
                    self.add_item(obj())
