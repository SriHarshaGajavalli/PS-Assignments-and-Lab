import cgitb
cgitb.enable()

print("Content-Type: text/html")
print()

class Family:
    Name, Gender, DOB, DOD, Relation, Relatedto = (0, 1, 2, 3, 4, 5)
    
    def __init__(self, filename):
        # Copying dataset.csv to dictionary self.dataset
        self.dataset = {}
        try:
            for line in open(filename):
                lst = line.strip('\n').split(';')
                if lst[0] == 'PKey': continue
                self.dataset[lst[0]] = lst[1:]
        except FileNotFoundError:
            print ('File "', filename, '" not found in working directory! Check the filename and path')
    
    def getrelatedname(self, id):
        # Finding first generation relationship person name
        rid = self.dataset[id][Family.Relatedto]
        if rid == 'Self':
            name = 'Self'
        else:
            name = self.dataset[rid][Family.Name]
        return name    
        
    def getid(self, name):
        # Finding Pkey by name
        for id in self.dataset:
            if self.dataset[id][Family.Name] == name: break
            id = 'no'
        return id
 
    def getfamilytree(self, id):
        # Returning family tree list for Pkey
        famtree = []
        rname = self.dataset[id][Family.Name]
        famtree.append(rname)
        while rname != 'Self':
            rid = self.getid(rname)
            rname = self.getrelatedname(rid)
            if self.dataset[rid][Family.Relation] == 'Spouse':
                famtree[len(famtree)-1] = rname
            else:
                if rname != 'Self': famtree.append(rname)
        return famtree
            
    
    def relation(self, id, index):
        relationlist = [('Mother', 'Father'),
                        ('Grand Mother', 'Grand Father'), 
                        ('Great Grand Mother', 'Great Grand Father'),
                        ('Great-Aunt', 'Great-Uncle'),
                        ('Aunt', 'Uncle'),
                        ('Cousin-Aunt', 'Cousin-Uncle')]
        if self.dataset[id][Family.Gender] == 'F':
            gender = 0
        else:
            gender = 1
        return relationlist[index][gender]
    
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
        
        # Checking first generation relationship
        rname1 = self.getrelatedname(id1)
        rname2 = self.getrelatedname(id2)
        if rname1 == rname2:
            if rname1 != 'Self':
                if self.dataset[id1][Family.Relation] == 'Child' and self.dataset[id2][Family.Relation] == 'Child': # We guess that person may have zero or one spouse
                    print(name1, 'and', name2, 'are the siblings')
                else:
                    if self.dataset[id1][Family.Relation] == 'Spouse':
                        print(name1, 'is a', self.relation(id1, 0), 'of', name2)
                    else:
                        print(name2, 'is a', self.relation(id2, 0), 'of', name1)
            else:
                print('There is no info about relationship between', name1, 'and', name2)
            return 0
        else:
            if rname1 == name2:
                if self.dataset[id1][Family.Relation] == 'Spouse':
                    print(name1, 'is a Spouse of', name2)
                else:
                    print(name2, 'is a', self.relation(id2, 0), 'of', name1)
                return 0
            elif rname2 == name1:
                if self.dataset[id2][Family.Relation] == 'Spouse':
                    print(name2, 'is a Spouse of', name1)
                else:
                    print(name1, 'is a', self.relation(id1, 0), 'of', name2)
                return 0
        
        
        # Checking 2-4 generation relationship or non-direct relationship
        famlist1 = self.getfamilytree(id1)
        famlist2 = self.getfamilytree(id2)
                
        length = min(len(famlist1), len(famlist2))
        if length < len(famlist1):
            famlist1 = famlist1[len(famlist1)-length:]
        if length < len(famlist2):
            famlist2 = famlist2[len(famlist2)-length:]
        
        id = -1
        for i in range(len(famlist1)):
            if famlist1[i] == famlist2[i]:
                id = i # Finding common ancestor in famlist
                break
        if id == -1:
            print('There is no info about relationship between', name1, 'and', name2)
            return 0
        
        commonancestor = famlist1[id]
        famlist1 = self.getfamilytree(id1)
        famlist2 = self.getfamilytree(id2)
        ancid1 = famlist1.index(commonancestor)
        ancid2 = famlist2.index(commonancestor)
            
        if ancid1 == ancid2:
            inlaw = ''
            if self.dataset[id1][Family.Relation] == 'Spouse' or self.dataset[id2][Family.Relation] == 'Spouse':
                inlaw = '-in-law'
            if ancid1 == 1:
                print(name1, 'and', name2, 'are the siblings'+inlaw)
            elif ancid1 == 2:
                print(name1, 'and', name2, 'are the cousins'+inlaw)
            elif ancid1 == 3:
                print(name1, 'and', name2, 'are the second cousins')
        else: # not siblings
            
            if ancid2 < ancid1:
                ancid1, ancid2 = ancid2, ancid1
                name1, name2 = name2, name1
                id1, id2 = id2, id1
                                
            inlaw = ''
            if self.dataset[id2][Family.Relation] == 'Spouse':
                inlaw = '-in-law'
                
            if ancid1 == 0 and ancid2 == 3: # Great Grand Parent
                print (name1, 'is a ', self.relation(id1, 2), ' of', name2)
            elif ancid1 == 0 and ancid2 == 2: # Grand Parent
                print (name1, 'is a ', self.relation(id1, 1)+inlaw, ' of', name2)
            elif ancid1 == 0 and ancid2 == 1: # Parent
                print (name1, 'is a ', self.relation(id1, 0)+inlaw, ' of', name2)
            elif ancid1 == 1 and ancid2 == 3: # Great-Aunt/Uncle
                print (name1, 'is a ', self.relation(id1, 3), ' of', name2)
            elif ancid1 == 1 and ancid2 == 2: # Aunt/Uncle
                print (name1, 'is a ', self.relation(id1, 4)+inlaw, ' of', name2)
            elif ancid1 == 2 and ancid2 == 3: # Cousin-Aunt/Uncle
                print (name1, 'is a ', self.relation(id1, 5), ' of', name2)
 
 
    def findspouseid(self, id):
        if self.dataset[id][Family.Relation] == 'Spouse':
            spouseid = self.dataset[id][Family.Relatedto]
        else:
            spouseid = -1
            for pkey in self.dataset:
                if self.dataset[pkey][Family.Relation] == 'Spouse' and self.dataset[pkey][Family.Relatedto] == id:
                    spouseid = pkey
                    break
        return spouseid
    
    
    def findparents(self, id):
        if self.dataset[id][Family.Relation] == 'Self':
            return ('Self', 'Self')
        
        if self.dataset[id][Family.Relation] == 'Spouse':
            spouseid = self.dataset[id][Family.Relatedto]
            parents = self.findparents(spouseid)
            return parents
            
        if self.dataset[id][Family.Relation] == 'Child':
            pid = self.dataset[id][Family.Relatedto]
            spouseid = self.findspouseid(pid)
            parents = (self.dataset[pid][Family.Name], self.dataset[spouseid][Family.Name])
            return parents
    
    
    def findgrandparents(self, id):
        p1, p2 = self.findparents(id)
        if p1 == 'Self' or p2 == 'Self':
            return ('Self', 'Self')
        id1 = self.getid(p1)
        id2 = self.getid(p2)
        pkey = id1
        if self.dataset[id1][Family.Relation] == 'Spouse':
            pkey = id2
        p1, p2 = self.findparents(pkey)
        return (p1, p2)
    
    def findgreatgrandparents(self, id):
        p1, p2 = self.findgrandparents(id)
        if p1 == 'Self' or p2 == 'Self':
            return ('Self', 'Self')
        id1 = self.getid(p1)
        id2 = self.getid(p2)
        pkey = id1
        if self.dataset[id1][Family.Relation] == 'Spouse':
            pkey = id2
        p1, p2 = self.findparents(pkey)
        return (p1, p2)
    
    
    def findchildren(self, id):
        spouseid = self.findspouseid(id)
        if spouseid == -1: return -1 # No spouse- no children
        children = []
        for pkey in self.dataset:
            if self.dataset[pkey][Family.Relation] == 'Child' and (self.dataset[pkey][Family.Relatedto] == id or self.dataset[pkey][Family.Relatedto] == spouseid):
                children.append(self.dataset[pkey][Family.Name])
        return children
    
    def findsiblings(self, id):
        p1, p2 = self.findparents(id)
        if p1 == 'Self' or p2 == 'Self': # No parents- no siblings
            return -1
            
        id1 = self.getid(p1)
        children = self.findchildren(id1)
        siblings = set(children) - set([self.dataset[id][Family.Name]])
        if not len(siblings): # One child of own parents
            return -1
        return list(siblings)
    
    def finduncles(self, id):
        p1, p2 = self.findparents(id)
        if p1 == 'Self' or p2 == 'Self': # No parents- no uncles
            return -1
            
        id1 = self.getid(p1)
        uncles = self.findsiblings(id1)
        if uncles == -1:
            return -1
        return uncles
        
    
    def findcousins(self, id):
        uncles = self.finduncles(id)
        if uncles == -1: # No uncles/aunts- no cousins
            return -1
        cousins = []
        for uncle in uncles:
            id1 = self.getid(uncle)
            children = self.findchildren(id1)
            if children == -1: continue
            cousins = cousins + children
        return cousins
            
    def findsecond(self):
        print ('\nFinding 2nd person name for an input of 1st person name and the relation')
        name = input('Input person name: ')
        id = self.getid(name)
        if id == 'no':
            print('There is no name"', name, '" in dataset')
            return 0
            
        search = [0, 'Parents', 'Grand parents', 'Great grand parents', 'Uncles/Aunts', 'Siblings', 'Cousins', 'Spouse', 'Children']
        action = '0'
        eight = ['1', '2', '3', '4', '5', '6', '7', '8'] 
        while action not in eight:
            print ('Input 1, 2, 3, ... for choosing relation')
            
            for i in range(1, 9):
                print(str(i)+'.', search[i])
                
            action = input('Your choice: ')
            if action == '1':
                p1, p2 = self.findparents(id)
            elif action == '2':
                p1, p2 = self.findgrandparents(id)
            elif action == '3':
                p1, p2 = self.findgreatgrandparents(id)
            elif action == '4':
                p1 = self.finduncles(id)
                if p1 == -1:
                    answer = 'There is no info about uncles/aunts of ' + name
                else:
                    answer = ' '.join(p1) + ' is(are) a uncles/aunts of ' + name
                break
            elif action == '5':
                p1 = self.findsiblings(id)
                if p1 == -1:
                    answer = 'There is no info about siblings of ' + name
                else:
                    answer = ' '.join(p1) + ' is(are) a sibling(s) of ' + name
                break
            elif action == '6':
                p1 = self.findcousins(id)
                if p1 == -1:
                    answer = 'There is no info about cousins of ' + name
                else:
                    answer = ' '.join(p1) + ' is(are) a cousin(s) of ' + name
                break
            elif action == '7':
                spouseid = self.findspouseid(id)
                if spouseid == -1:
                    answer = name+' has no spouse'
                else:
                    answer = self.dataset[spouseid][Family.Name] + ' is a spouse of ' + name
                break
            elif action == '8':
                p1 = self.findchildren(id)
                if p1 == -1:
                    answer = 'There is no info about children of ' + name
                else:
                    answer = ' '.join(p1) + ' is(are) a child(children) of ' + name
                break
            else:
                print('Input incorrect')
                
            if p1 == 'Self':
                answer = 'There is no info about ' + search[int(action)] + ' of ' + name + ' in dataset'
            else:
                answer = search[int(action)] + ' of ' + name + ' are ' + p1 + ' ' + p2
        
        print ('Searching', search[int(action)], 'of', name, '...')
        print (answer)
        #print ("Special function answer:" + len(p1) + "people satisfies the give relationship with the first person")
        
            
    
    def showmenu(self):
        if not self.dataset:
            return 111 # Exiting if *.csv not loaded to dataset dictionary
        while True:
            print ('\nInput 1, 2, 3 for action')
            print('1. Find relationship between two persons')
            print('2. Find 2nd person name for an input of 1st person name and the relation')
            print('3. Exit')
            action = input('Your choice: ')
            if action == '1':
                f.findrelationship()
            elif action == '2':
                f.findsecond()
            elif action =='3':
                break
            else:
                print('Input incorrect')
        

if __name__ == '__main__':
    f = Family('dataset.csv')
    f.showmenu()  
