class NonPhysicalObjectError(Exception):
    def __init__(self):
        super(NonPhysicalObjectError, self).__init__("This is not an Matter.py physics object !")

class ObjectNotInWorld(Exception):
    def __init__(self):
        super(ObjectNotInWorld, self).__init__("This object is not in that world !")