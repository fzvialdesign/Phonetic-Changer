from os import getcwd
from os import walk
from os import makedirs
from os import remove
from os import rmdir
from os import listdir

from os.path import join
from os.path import isdir
from os.path import isfile

import io

def change():
  # Initialize method-wide variables and reset output
  fpin = getcwd() + "\\Algorithms\\Evolution\\Sound Changer\\Input\\Data"
  fpout = getcwd() + "\\Algorithms\\Evolution\\Sound Changer\\Output"

  for root, dirs, files in walk(fpout):
    for file in files:
      remove(join(root, file))

    for dir in dirs:
      if not len(listdir(join(root, dir))):
        rmdir(join(root, dir))
  
  # Parse through input directory and generate for each file
  for root, dirs, files in walk(fpin):
    for file in files:
      src = root
      dest = fpout
    
      for subdir in src.replace(fpin, "").split("\\"):
        if not subdir:
          break
        
        dest = join(dest, subdir)
        
        if not isdir(dest):
          makedirs(dest)
          
      src = join(src, file)
      dest = join(dest, file)
        
      c_generate(src, dest)
      
def c_generate(src, dest):
    # Initialize method-wide variables
    fin = io.open(src, "r", encoding = "utf-16")
    fout = io.open(dest, "w", encoding = "utf-16")
    
    lines = fin.readlines()
    is_inflection = False
    
    # Write each (edited) line to the dest file
    for l in range(len(lines)):
      if not is_inflection:
        i_terms = ["Conjugation", "Declension"]
        
        is_inflection = lines[l].strip("• \n") in i_terms
        fout.write(lines[l])
        
        continue
        
      editable = lines[l]
      
      if "Pronunciation" in editable:
        editable = c_evolve(editable)
        
      fout.write(editable)
      
    # Close files
    fin.close()
    fout.close()
    
def c_evolve(fileline):
  # Decode change list
  fpref = getcwd() + "\\Algorithms\\Evolution\\Sound Changer\\Input\\Changes"
  
  if not isfile(join(fpref, "List.txt")):
    print("\nNO CHANGELIST FOUND")
    
    return
  
  fin = io.open(join(fpref, "List.txt"), "r", encoding = "utf-16")
  
  lines = fin.readlines()
  cstart = lines.index("• List\n") + 1
  changes = c_decode(lines[cstart : len(lines) - 1])
  
  fin.close()
  
  # Isolate the phonemes and apply ordered changes
  segments = fileline.split(" : ")
  segments[1] = c_apply(segments[1], changes)
  
  return " : ".join(segment for segment in segments)

def c_decode(changes):
  # Turn change list file into dict of changes
  decoded = {}
  
  cdef = ""
  specs = []
  
  for line in changes:
    cstripped = line.strip("‣⁃ \n")
    
    if line.startswith("  ‣ "):
      if cdef:
        decoded[cdef] = specs
      
      cdef = cstripped
      specs = []
      
      continue
    
    specs.append(cstripped.split(" : ")[1])
    
  return decoded

def c_apply(pstring, changes):
  # Initialize new pstring
  npstring = pstring
  
  npstring = npstring.replace("[", "[ # ,")
  npstring = npstring.replace("]\n", ", # ]")

  # Apply each change in the changes dict to the npstring
  for key in changes.keys():
    for change in changes[key]:
      print(npstring)
      dc = change
      
      dc = dc.replace("→", "$")
      dc = dc.replace("/", "$")
      dc = dc.replace("_", "$")

      dc = [elem.strip() for elem in dc.split("$")]
      
      before = " , ".join((dc[2], dc[0], dc[3])).replace("∅ , ", "")
      after = " , ".join((dc[2], dc[1], dc[3])).replace("∅ , ", "")
      
      print(before)
      print(after)
      
      npstring = npstring.replace(before, after)
    
  # Reformat the npstring
  npstring = npstring.replace("[ # ,", "[")
  npstring = npstring.replace(", # ]", "]\n")

  return npstring
  