

def abbreviation(a, b):
    if a == "" and b == "":
        return "YES"
    elif a == "" and b != "":
        return "NO"
    elif a != "" and b == "":
        return "YES"
    else:
        if a[-1] == b[-1]:
            return abbreviation(a[:-1], b[:-1])
        elif a[-1].upper() == b[-1]:
            return abbreviation(a[:-1], b[:-1]) or abbreviation(a[:-1], b)
        else:
            if a[-1].islower():
                return abbreviation(a[:-1], b)
            else:
                return "NO"


def abbreviation1(a, b):
    while a == "" and b == "":
        if a[-1] == b[-1]:
            a, b = a[:-1], b[:-1]
        elif a[-1].upper() == b[-1]:
            a, b = a[:-1], b[:-1]  # or abbreviation(a[:-1], b)
        else:
            a, b = a[:-1], b
    return "YES"


def abbreviation(a, b):
    m, n = len(a), len(b)
    dp = [[False]*(m+1) for _ in range(n+1)]
    dp[0][0] = True
    for i in range(n+1):
        for j in range(1, m+1):
            # if a[j-1] == b[i-1]:
            #     dp[i][j] = dp[i-1][j-1]
            if a[j-1].upper() == b[i-1]:
                dp[i][j] = dp[i-1][j-1] or dp[i][j-1]
            elif a[j-1].islower():
                dp[i][j] = dp[i][j-1]
    return "YES" if dp[n][m] else "NO"


# print(abbreviation1("daBcd", "ABC"))
print(abbreviation("daBcd", "ABC"))
# # print(abbreviation1("AbcdE", "AFDE"))
# print(abbreviation("AbcdE", "AFDE"))
print(abbreviation("XXVVnDEFYgYeMXzWINQYHAQKKOZEYgSRCzLZAmUYGUGILjMDET",
                   "XXVVDEFYYMXWINQYHAQKKOZEYSRCLZAUYGUGILMDETQVWU"))
print(abbreviation("PVJSNVBDXABZYYGIGFYDICWTFUEJMDXADhqcbzva",
                   "PVJSNVBDXABZYYGIGFYDICWTFUEJMDXAD"))
print(abbreviation("QOTLYiFECLAGIEWRQMWPSMWIOQSEBEOAuhuvo",
                   "QOTLYFECLAGIEWRQMWPSMWIOQSEBEOA"))
print(abbreviation("DRFNLZZVHLPZWIupjwdmqafmgkg",
                   "DRFNLZZVHLPZWI"))
print(abbreviation("SLIHGCUOXOPQYUNEPSYVDaEZKNEYZJUHFXUIL",
                   "SLIHCUOXOPQYNPSYVDEZKEZJUHFXUIHMGFP"))
print(abbreviation("RYASPJNZEFHEORROXWZFOVDWQCFGRZLWWXJVMTLGGnscruaa",
                   "RYASPJNZEFHEORROXWZFOVDWQCFGRZLWWXJVMTLGG"))
print(abbreviation("AVECtLVOXKPHIViTZViLKZCZAXZUZRYZDSTIHuCKNykdduywb",
                   "AVECLVOXKPHIVTZVLKZCZAXZUZRYZDSTIHCKN"))
print(abbreviation("wZPRSZwGIMUAKONSVAUBUgSVPBWRSTJZECxMTQXXA",
                   "ZPRSZGIMUAKONSVAUBUSVPBWRSTJZECMTQXXA"))
print(abbreviation("SYIHDDSMREKXOKRFDQAOZJQXRIDWXPYINFZCEFYyxu",
                   "SYIHDDSMREKXOKRFDQAOZJQXRIDWXPYINFZCEFY"))
print(abbreviation("EIZGAWWDCSJBBZPBYVNKRDEWVZnSSWZIw",
                   "EIZGAWWDCSJBBZPBYVNKRDEWVZSSWZI"))


'''
    
10
XXVVnDEFYgYeMXzWINQYHAQKKOZEYgSRCzLZAmUYGUGILjMDET
XXVVDEFYYMXWINQYHAQKKOZEYSRCLZAUYGUGILMDETQVWU
PVJSNVBDXABZYYGIGFYDICWTFUEJMDXADhqcbzva
PVJSNVBDXABZYYGIGFYDICWTFUEJMDXAD
QOTLYiFECLAGIEWRQMWPSMWIOQSEBEOAuhuvo
QOTLYFECLAGIEWRQMWPSMWIOQSEBEOA
DRFNLZZVHLPZWIupjwdmqafmgkg
DRFNLZZVHLPZWI
SLIHGCUOXOPQYUNEPSYVDaEZKNEYZJUHFXUIL
SLIHCUOXOPQYNPSYVDEZKEZJUHFXUIHMGFP
RYASPJNZEFHEORROXWZFOVDWQCFGRZLWWXJVMTLGGnscruaa
RYASPJNZEFHEORROXWZFOVDWQCFGRZLWWXJVMTLGG
AVECtLVOXKPHIViTZViLKZCZAXZUZRYZDSTIHuCKNykdduywb
AVECLVOXKPHIVTZVLKZCZAXZUZRYZDSTIHCKN
wZPRSZwGIMUAKONSVAUBUgSVPBWRSTJZECxMTQXXA
ZPRSZGIMUAKONSVAUBUSVPBWRSTJZECMTQXXA
SYIHDDSMREKXOKRFDQAOZJQXRIDWXPYINFZCEFYyxu
SYIHDDSMREKXOKRFDQAOZJQXRIDWXPYINFZCEFY
EIZGAWWDCSJBBZPBYVNKRDEWVZnSSWZIw
EIZGAWWDCSJBBZPBYVNKRDEWVZSSWZI

Expected Output
NO
YES
YES
YES
NO
YES
YES
YES
YES
YES
'''
