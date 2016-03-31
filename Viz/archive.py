import json
import csv
from pprint import pprint
import string
import os

if __name__ == '__main__':

    with open('results\\results.metaresults.json') as data_file:    
        metaresults = json.load(data_file)
    
    plist = []
    mlist = []

    print "Available PET Datasets: "
    i = 0
    petDirs = []
    petDates = []
    select_list = []
    for rr in metaresults["Results"] :
        tmName= rr["Summary"]
        tmTime= rr["Time"]
        tmDesignID = rr["DesignID"]
        mdaoName = "results\\"+tmName.replace("testbench_manifest" , "mdao_config")
        
        try : 
            with open(mdaoName) as mdaoFile:    
                mdaoDescr = json.load(mdaoFile)
            petName= "["
            for cc in mdaoDescr["components"] : 
                #print cc
                petName = petName+cc+","
            #print "--"              
            print str(i)+":" + tmTime + " "+tmDesignID[1:8]+" "+petName[0:40]+"..."
            i = i + 1
            petDirs.append(mdaoName)
            petDates.append(tmTime)

        except :
            #print "Not a PET, No MDAO_config.json"
            petName = "NONE"
    
    select_str = raw_input("Select DOE set to archive (e.g. 1,3,4,6):")
    if select_str == "":
        select_str = "all 0"
    
    if select_str.find("all") != -1 :
        patidx = int(select_str[4:])
        targDate = petDates[patidx]
        iidx = 0
        for tt in petDates :
            if targDate == tt :
                select_list.append(iidx)
            iidx = iidx + 1
    else :
        select_list = [int(k) for k in select_str.split(',')]
        
    print "Datasets to archive: {}".format(select_list)
    
    # Get archive filename from user
    confirmed = False
    while not confirmed:
        file_str = raw_input("Filename: ")
        file_str = ''.join(ch for ch in file_str if ch.isalnum() or ch == ' ').replace(' ','_')
        
        file_path = os.path.join('archive',(file_str+'.csv'))
        # Add error checking for file existance
        n = 0
        while os.path.isfile(file_path):
            n = n + 1
            file_path = os.path.join('archive',file_str+str(n)+'.csv')
            
        print "New Filename: {}".format(os.path.basename(file_path))
        ans = raw_input("Is this filename ok? ([y]/n): ")
        if 'n' not in ans.lower():
            confirmed = True
    
    if not os.path.isdir("archive"):
        os.mkdir("archive")
    
    fmerge = open(file_path, 'wb')
    
    # Combine all the design space data
    firstDict = True
    headers = {}
    fullIn = {}
    for xx in select_list:
        csvName = petDirs[xx].replace("mdao_config.json","output.csv")
        print "Processing: "+csvName
        firstLine = True  
        with open(csvName) as csvfile:
            partIn = csv.DictReader(csvfile)
            if partIn.fieldnames is not None:
                if firstDict : 
                    partOut = csv.DictWriter(fmerge, delimiter=',', fieldnames=partIn.fieldnames,dialect=csv.excel)    
                    headers = dict( (n,n) for n in partIn.fieldnames )
                    partOut.writerow(headers)
                    firstDict = False
                
                for row in partIn :
                    partOut.writerow(row)
    
    fmerge.close()

    print "Done!"
    
    os.system("pause")


