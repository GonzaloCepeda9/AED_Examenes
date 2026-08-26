class Superheroe:

    def __init__(
        self,
        name: str,
        alias: str,
        real_name: str,
        short_bio: str,
        first_appearance: int,
        is_villain: bool
    ):
        self.name = name
        self.alias = alias
        self.real_name = real_name
        self.short_bio = short_bio
        self.first_appearance = first_appearance
        self.is_villain = is_villain

    def __str__(self):
        return f'Nombre: {self.name} | Alias: {self.alias} | Nombre real: {self.real_name} | Biografía: {self.short_bio} | Primera aparición: {self.first_appearance} | Es villano: {self.is_villain}.'