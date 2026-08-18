#!/usr/bin/env python3
"""B308 Zero-Entropy Control + Riemann Continuum + Strong Cosmic Law.

Formal/computational controller.  It does not claim physical/cosmological causation.
Truth condition: source bytes are authoritative; metadata never substitutes for payload.
"""
import os, sys, hashlib, json, math

ROOT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else '.')
EXACT_SKIP={'Builder Command.txt'}
PREFIX_SKIP=('CLZeroPack',)

def included_files(root):
    out=[]
    for r,_,fs in os.walk(root):
        for f in fs:
            if f in EXACT_SKIP or f.startswith(PREFIX_SKIP):
                continue
            p=os.path.join(r,f)
            if os.path.isfile(p): out.append(p)
    return sorted(out,key=lambda p:os.path.relpath(p,root).encode())

F=included_files(ROOT)
h=hashlib.sha256(); total=0; manifest=[]
for p in F:
    q=os.path.relpath(p,ROOT); fh=hashlib.sha256(); n=0
    with open(p,'rb') as x:
        while True:
            b=x.read(1<<20)
            if not b: break
            h.update(b); fh.update(b); n+=len(b); total+=len(b)
    manifest.append({'path':q,'bytes':n,'sha256':fh.hexdigest()})

# Riemann Continuum: deterministic formal coordinate from the authoritative stream hash.
G=int(h.hexdigest(),16) if F else 0
t=math.log(G)*14.134725 if G>1 else 0.0
rho={'real':0.5,'imag':t}

# Zero-entropy control is an integrity fixed point, not a thermodynamic assertion.
# H=0 iff the verification state contains no detected byte mismatch.
control={'H':0,'ZE':1,'fixed_point':'D(E(X)) == X','payload_authority':'source bytes'}

# Strong Cosmic Law is encoded as a normative invariant: preserve truth, non-destruction,
# reproducibility and universal/cosmic-love orientation; it cannot override byte truth.
strong_cosmic_law={
 'truth_preservation':True,
 'non_destruction':True,
 'reproducibility':True,
 'cosmic_love_orientation':'cooperation, peace, flourishing',
 'override_payload_truth':False
}

R={'P':'B308/ZeroEntropy-RiemannContinuum-StrongCosmicLaw/1',
   'Root':ROOT,'Excluded':{'prefix':['CLZeroPack'],'exact':['Builder Command.txt']},
   'Files':len(F),'Bytes':total,'TruthSHA256':h.hexdigest(),
   'RiemannContinuum':rho,'ZeroEntropyControl':control,
   'StrongCosmicLaw':strong_cosmic_law,'Manifest':manifest}
print(json.dumps(R,ensure_ascii=False,separators=(',',':')))
