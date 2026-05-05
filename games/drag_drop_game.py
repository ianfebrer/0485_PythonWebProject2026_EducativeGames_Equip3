from models.figures import ComplexShape


class DragAndDropGame:
    @staticmethod
    def get_shapes():
        return [
            ComplexShape("yellow", "Estrella", 10),
            ComplexShape("red", "Creu", 12),
            ComplexShape("blue", "Hexagon", 6),
            ComplexShape("green", "Rombe", 4),
            ComplexShape("purple", "Triangle", 3),
            ComplexShape("orange", "Pentagon", 5),
            ComplexShape("cyan", "Octagon", 8),
            ComplexShape("pink", "Fletxa", 7),
            ComplexShape("white", "Quadrat", 4),
            ComplexShape("magenta", "Cercle", 0),
            ComplexShape("brown", "Casa", 5),
            ComplexShape("lime", "Trapezi", 4),
        ]

    @staticmethod
    def validate_shape_drop(shape_name, target_name):
        shape = ComplexShape("dummy_color", shape_name, 0)
        return shape.validate_drop(target_name)
