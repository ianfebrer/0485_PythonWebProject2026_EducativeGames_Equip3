class GeometricShape:
    def __init__(self, color, x=0, y=0):
        # Classe base per a totes les figures geomètriques amb color i posició
        self.color = color
        self.x = x
        self.y = y

    def calculate_area(self):
        # Mètode abstracte que han d'implementar les classes filles
        raise NotImplementedError("Aquest mètode s'ha de sobreescriure a les subclasses.")

class ComplexShape(GeometricShape):
    def __init__(self, color, name, sides):
        # Hereta de GeometricShape i afegeix atributs per a figures més complexes
        super().__init__(color)
        self.name = name
        self.sides = sides

    def calculate_area(self):
        # Lògica específica per calcular l'àrea d'una figura complexa
        return f"Calculant l'àrea per a un {self.name} amb {self.sides} costats."

    def to_dict(self):
        return {
            "name": self.name,
            "color": self.color,
            "sides": self.sides
        }

    def validate_drop(self, target_name):
        return self.name.lower() == target_name.lower()