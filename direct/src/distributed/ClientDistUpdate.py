"""ClientDistUpdate module: contains the ClientDistUpdate class"""

import DirectNotifyGlobal

class ClientDistUpdate:
    notify = DirectNotifyGlobal.directNotify.newCategory("ClientDistUpdate")

    def __init__(self, dcField):
        self.number = dcField.getNumber()
        self.name = dcField.getName()
        self.types = self.deriveTypesFromParticle(dcField)
        return None

    def deriveTypesFromParticle(self, dcField):
        typeList=[]
        dcFieldAtomic = dcField.asAtomicField()
        dcFieldMolecular = dcField.asMolecularField()
        if dcFieldAtomic:
            for i in range(0, dcFieldAtomic.getNumElements()):
                typeList.append(dcFieldAtomic.getElementType(i))
        elif dcFieldMolecular:
            for i in range(0, dcFieldMolecular.getNumAtomics()):
                componentField = dcFieldMolecular.getAtomic(i)
                for j in range(0, componentField.getNumElements()):
                    typeList.append(componentField.getElementType(j))
        else:
            ClientDistUpdate.notify.error("field is neither atom nor molecule")
        return typeList

    def updateField(self, cdc, do, di):
        # Look up the class
        aClass = eval(cdc.name)
        # Look up the function
        assert(aClass.__dict__.has_key(self.name))
        func = aClass.__dict__[self.name]
        # Get the arguments into a list
        args = self.extractArgs(di)
        # Apply the function to the object with the arguments
        apply(func, [do] + args)
        return None

    def extractArgs(self, di):
        args = []
        for i in self.types:
            args.append(di.getArgs(i))
        return args

    def addArgs(self, datagram, args):
        # Add the args to the datagram
        numElems = len(args)
        assert (numElems == len(self.types))
        for i in range(0, numElems):
            datagram.addArg(args[i], self.types[i])
    
    def sendUpdate(self, do, args):
        datagram = Datagram()
        # Add message type
        datagram.addUint16(ALL_OBJECT_UPDATE_FIELD)
        # Add the DO id
        datagram.addUint32(do.doId)
        # Add the field id
        datagram.addUint8(self.number)
        # Add the arguments
        self.addArgs(datagram, args)
        # send the datagram

