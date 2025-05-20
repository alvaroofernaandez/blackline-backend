import mongoengine as me


class Participante(me.EmbeddedDocument):
    instagram_username = me.StringField(required=True, min_length=1)
    requirements = me.BooleanField(required=True)

    def clean(self):
        if not self.requirements:
            raise me.ValidationError(
                f"El participante @{self.instagram_username} no cumple los requisitos para participar en el sorteo."
            )
