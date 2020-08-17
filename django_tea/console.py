from typing import List, Union, Type

from rich.console import Console

from django_tea import serde
from django_tea.enums import ConsoleFormat
from django_tea.table import RichTableMixin


def output(
    fmt: ConsoleFormat,
    model: Type[RichTableMixin],
    objs: Union[List[RichTableMixin], RichTableMixin],
):
    console = Console()

    if fmt == ConsoleFormat.json:
        console.print(serde.json_dumps(objs))

    elif fmt == ConsoleFormat.text:
        if objs is None or (isinstance(objs, list) and len(objs) == 0):
            console.print(
                f"[cyan]No {model.__class__.__name__}s found.[/cyan]"
            )
            return

        if not isinstance(objs, list):
            objs = [objs]

        table = model.get_rich_table()
        for o in objs:
            table.add_row(*o.to_rich_row())

        console.print(table)
