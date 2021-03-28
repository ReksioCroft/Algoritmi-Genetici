class Cromozom:
    def __init__( self, fin ):
        s = fin.readline().split()
        self.n = int( s[ -1 ] )
        s=fin.readline().split()
        self.domain=(int(s[-2]), int(s[-1]))
        s=fin.readline().split()
        self.function=(int(s[-3]),int(s[-2]), int(s[-1]))
        s=fin.readline().split()
        self.precisiton=int( s[ -1 ] )
        s = fin.readline().split()
        self.pRecombinare = float(s[-1])
        s = fin.readline().split()
        self.pMutatie = float(s[-1])
        s = fin.readline().split()
        self.nrEtape = int(s[-1])


fin = open( "date.in" )
cromozom = Cromozom( fin )
print(cromozom)