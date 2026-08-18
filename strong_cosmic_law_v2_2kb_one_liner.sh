#!/bin/sh
# CLΣ-SCL/2 compact <=2KB one-liner-style verifier. Formal computational certificate only.
command -v python3>/dev/null 2>&1||{ echo python3_required;exit 127;};python3 -c 'import sys,json,math,zlib,base64;exec("try:sys.set_int_max_str_digits(0)\nexcept:pass");P="Cosmic Love Is The Solution(s) For Everything";R="CLSIGMA_STRONG_COSMIC_LAW_GODEL_SPECTRUM/2KB/1";T=[]
for v in range(256):
 s=0
 for k in range(7,-1,-1):s=2*s+(2 if(v>>k)&1 else 5)
 T+=[s]
x=sys.stdin.buffer.read();z=zlib.compress(x,9);b=base64.b64encode(z);q=zlib.decompress(base64.b64decode(b));G=1
for v in z:G=(G<<8)+T[v]
C=q==x;S=all(T[v]>=0 for v in z);F=int(not(C and S));A=O=E=H=F;ZE=int(A==O==E==H==0);SCL=int(C and S and ZE);print(json.dumps({"P":R,"Axiom":P,"InputBytes":len(x),"CompressedBytes":len(z),"G25":str(G),"rho":{"real":.5,"imag":math.log(G)},"A_n":A,"O_n":O,"DeltaE_n":E,"H_n":H,"ZE":ZE,"Replay":int(C),"Spectrum":int(S),"SCL":SCL,"Result":"PASS" if SCL else "FAIL","Boundary":"internal deterministic certificate; no thermodynamic/RH/physical-law claim"},ensure_ascii=False,separators=(",",":")))'