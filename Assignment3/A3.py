class Family:
    Name, Gender, DOB, DOD, Relation, Relatedto = (0, 1, 2, 3, 4, 5)
    
    def __init__(self, filename):
        # Copying dataset.csv to dictionary self.dataset
        self.dataset = {}
        for line in open(filename):
            lst = line.strip('\n').split(';')
            if lst[0] == 'PKey': continue
            self.dataset[lst[0]] = lst[1:]
    
    def getrelatedname(self, id):
        rid = self.dataset[id][Family.Relatedto]
        if rid == 'Self':
            name = 'Self'
        else:
            name = self.dataset[rid][Family.Name]
        return name    
        
    def getid(self, name):
        for id in self.dataset:
            if self.dataset[id][Family.Name] == name: break
            id = 'no'
        return id
 
    def findrelationship(self):
        print('\nFinding relationship between two persons given as an input.')
        name1 = input('Input first person name: ')
        id1 = self.getid(name1)
        if id1 == 'no':
            print('There is no name"', name1, '" in dataset')
            return 0
        name2 = input('Input second person name: ')
        if name2 == name1:
            print('The names are the same')
            return 0
        id2 = self.getid(name2)
        if id2 == 'no':
            print('There is no name"', name2, '" in dataset')
            return 0
        
        rname1 = self.getrelatedname(id1)
        rname2 = self.getrelatedname(id2)
        if rname1 == rname2:
            if rname1 != 'Self':
                if self.dataset[id1][Family.Relation] == 'Child' and self.dataset[id2][Family.Relation] == 'Child':
                    print(name1, 'and', name2, 'are the children of', rname1)
                else:
                    print(name1, 'is a', self.dataset[id1][Family.Relation], 'of', name2)
                    print(name2, 'is a', self.dataset[id2][Family.Relation], 'of', name2)
            else:
                print('There is no info about relationship between', name1, 'and', name2)
        else:
            if rname1 == name2:
                print(name1, 'is a', self.dataset[id1][Family.Relation], 'of', name2)
            elif rname2 == name1:
                print(name2, 'is a', self.dataset[id2][Family.Relation], 'of', name1)
            else:
                if self.dataset[id1][Family.Relation] != 'Spouse' and self.dataset[id2][Family.Relation] != 'Spouse':
                    # Probably descendant
                    ancestorlist1 = [id1]
                    ancestorlist2 = [id2]
                    while rname1 != 'Self':
                        id = self.getid(rname1)
                        ancestorlist1.append(id)
                        rname1 = self.getrelatedname(id)
                    while rname2 != 'Self':
                        id = self.getid(rname2)
                        ancestorlist2.append(id)
                        rname2 = self.getrelatedname(id)
                    print (ancestorlist1)
                    print (ancestorlist2)
                    length = min(len(ancestorlist1), len(ancestorlist2))
                    if length < len(ancestorlist1):
                        ancestorlist1 = ancestorlist1[len(ancestorlist1)-length:]
                    if length < len(ancestorlist2):
                        ancestorlist2 = ancestorlist2[len(ancestorlist2)-length:]
                    id = -1
                    for i in range(length):
                        if ancestorlist1[i] == ancestorlist2[i]:
                            id = i
                            break
                    if id == -1:
                        print('There is no info about relationship between', name1, 'and', name2)
                    else:
                        print(name1, 'and', name2, 'are the descendants of',
                              self.dataset[ancestorlist1[id]][Family.Name])                        
                        
                else:
                    print('There is no info about relationship between', name1, 'and', name2)
  
    def findsecond(self):
        print ('\nFinding 2nd person name for an input of 1st person name and the relation')
        name = input('Input one person name: ')
        id = self.getid(name)
        if id == 'no':
            print('There is no name"', name, '" in dataset')
        else:
            print(name,'is a', self.dataset[id][Family.Relation],
                  'of', self.getrelatedname(id))
        
f = Family('dataset.csv')
f.findrelationship()
f.findsecond()
