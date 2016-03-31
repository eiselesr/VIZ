import json
import csv
from pprint import pprint
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--combine',
                       default="",
                       help='file to append')
    parser.add_argument('--calc',
                        default=False,
                        action='store_true',
                        help='Use surrogate CostWeightPOST')
                       

    args = parser.parse_args()

    with open('results\\results.metaresults.json') as data_file:    
        metaresults = json.load(data_file)
    
    plist =  []
    mlist = []

    fmerge = open('results\\mergedPET.csv', 'wb')
    
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
    
    select_str = raw_input("Select DOE set to visualize (e.g. 1,3,4,6):")
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
        
    print select_list
    
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




