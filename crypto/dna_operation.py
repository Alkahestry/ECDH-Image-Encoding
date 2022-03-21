#DNA-Encoding RULE #1 A = 00, C=01, G=10, T=11
dna = {}
dna["00"] = "A"
dna["01"] = "C"
dna["10"] = "G"
dna["11"] = "T"
dna["A"] = "00"
dna["C"] = "01"
dna["G"] = "10"
dna["T"] = "11"
#DNA addition
dna["CT"]=dna["TC"]=dna["GG"]=dna["AA"]="A"
dna["AC"]=dna["CA"]=dna["TG"]=dna["GT"]="C"
dna["AG"]=dna["GA"]=dna["TT"]=dna["CC"]="G"
dna["AT"]=dna["TA"]=dna["CG"]=dna["GC"]="T"
#inverse shifting with shift sequence
dna_sub = {}
dna_sub["GG"]=dna_sub["CC"]=dna_sub["AA"]=dna_sub["TT"]="A"
dna_sub["AC"]=dna_sub["TA"]=dna_sub["CG"]=dna_sub["GT"]="C"
dna_sub["AG"]=dna_sub["TC"]=dna_sub["CT"]=dna_sub["GA"]="G"
dna_sub["AT"]=dna_sub["TG"]=dna_sub["CA"]=dna_sub["GC"]="T"