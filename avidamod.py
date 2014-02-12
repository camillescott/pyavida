import numpy as np

class PhenotypeMap:

    def __init__(self, mapfile, verbosity=1):
        self.mapfile = mapfile
        self.verbosity = verbosity
    
        parser = [r for r in self.iter_mapfile(self.mapfile)]
        i, inst_letter, inst_name, update, tasks = parser[0]
        
        self.length = len(parser) - 1
        self.mapMat = np.zeros((len(tasks), self.length))
        print self.mapMat
        self.tasks = tasks
        
        self.update = update
        #self.taskMap = [[1] if c>0 else [0] for c in tasks]
        #self.taskCountMap = [[c] for c in tasks]
        
        if self.verbosity > 1:
            print "Debug data: init values for update, taskMap, taskCountMap, numMapped"
            print self.update, self.taskMap, self.taskCountMap, self.numMapped
            
        print "building map matrix for {}\n\theader:{}".format(self.mapfile, self.tasks)
        for i, inst_letter, inst_name, viable, tasks in parser[1:]:
            # we'll store the number of times an instruction contributes to a task: ie, absolute
            # value of the number times performed minus the number times performed afer knockout.
            # this way we're actually agnostic to the value in the header, and 0's are positions
            # that don't matter
            
            counts = []
            for j, t in enumerate(tasks):
                if self.tasks[j] > 0:
                    counts.append( abs(self.tasks[j] - t ) )
            #print i, inst_letter, inst_name, viable, tasks
            #print counts
            self.mapMat[0:len(counts),i-1] = np.array(counts)
    
    @staticmethod
    def buildModuleVector(mat):
        s = np.zeros( (len(mat.T)) )
        
        groups = {}
        for i, row in enumerate(mat.T):
            #print row
            _bin = np.array(row)
            _bin[_bin.nonzero()] = 1
            key = ''
            for b in _bin:
                key += str(int(b))
            
            #print key, '\n'
            # index with the binary vector of tasks performed
            # so we're agnostic to the number of tasks
            if key not in groups.viewkeys():
                if groups.viewkeys():
                    groups[key] = max(groups.viewvalues())+1
                else:
                    groups[key] = 1
            s[i] = groups[key]
        return s
    
    # build an adjacency matrix from the module assignment vector s
    @staticmethod
    def buildSimpleAdjMatrix(s):
        adjMat = np.zeros( (len(s), len(s)) )
        
        for i in range(len(s)):
            for j in range(len(s)):
                if s[i] == s[j] and i != j:
                    adjMat[i,j] = 1.0
        return adjMat
    
    @staticmethod
    def buildModularityMatrix(A):
        degrees = A.sum(axis=0)
        M = float(degrees.sum())/2
        
        B = A.copy()
        for i in range(len(degrees)):
            for j in range(len(degrees)):
                B[i,j] = A[i,j] - (degrees[i] * degrees[j])/M
        return B, degrees, M/2
    
    def getModularityMatrx(self):
        self.B, self.degrees, self.m = PhenotypeMap.buildModularityMatrix(self.A)
        return self.B
    
    # builds and returns the module vector and adj matrix for this map
    def getSimpleAdjMatrix(self):
        self.s = PhenotypeMap.buildModuleVector(self.mapMat)
        self.A = PhenotypeMap.buildSimpleAdjMatrix(self.s)
        
        return self.A, self.s
    
    def calcNewmanMod(self):
        accum = 0.0
        for i in range(len(self.s)):
            for j in range(i+1,len(self.s)):
                if self.s[i] == self.s[j] and i != j:
                    accum += self.B[i,j]
        M = 1.0 / (4.0 * self.m)
        self.Q = M * accum
        return self.Q
        
    def makeHeatMap(self):
    
    	self.heatMap = np.zeros(len(self))
    
        for i, row in enumerate(self.mapMat):
        	_bin = np.array(row)
        	_bin[_bin.nonzero()] = 1
        	
        	if _bin.sum() > 1:
        		self.heatMap[i] = _bin.sum() + len(_bin)
        	else:
        		self.heatMap[i] = np.where(_bin > 0).sum()
        		
    # iterator over a map file
    @staticmethod
    def iter_mapfile(mapFile):
        with open(mapFile, 'rb') as mapfp:
            for line in mapfp:
                c = line.split()
                i = int(c[0])
                inst_letter = c[1]
                inst_name = c[2]
                viable = int(c[3])
                ttasks = c[4:]
                tasks = [int(x) for x in ttasks]
                yield i, inst_letter, inst_name, viable, tasks
