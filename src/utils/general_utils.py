import typer


class GeneralUtils:
    @staticmethod
    def sanitize_input(value):
        if len(value) > 50:
            raise typer.BadParameter("Too long")
        return value