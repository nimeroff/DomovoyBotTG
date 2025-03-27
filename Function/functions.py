from ConfigData.config import podjezd

def existkv(vnkv: int, param: bool) -> dict | bool:
    nump: int = 0
    numf: int = 0
    for i in range(1, len(podjezd) + 1):
        if i == 8:
            jj = 2
        else:
            jj = 1
        for j in range(jj, len(podjezd[i]) + jj):
            if podjezd[i][j][0] <= vnkv and (podjezd[i][j][1]) >= vnkv:
                nump=i
                numf=j
    if nump != 0 and numf!=0:
        if param==True:
            return {1:nump,2:numf}
        else:
            return True
    else:
        if param == True:
            return {1:0,2:0}
        else:
            return False


def lowertext(txts:str) -> str:
    alf: dict [str,str] = {'А':'а','Б':'б','В':'в','Г':'г','Д':'д','Е':'е','Ё':'ё','Ж':'ж','З':'з','И':'и','Й':'й','К':'к','Л':'л','М':'м','Н':'н','О':'о',
                           'П':'п','Р':'р','С':'с','Т':'т','У':'у','Ф':'ф','Х':'х','Ц':'ц','Ч':'ч','Ш':'ш','Щ':'щ','Ъ':'ъ','Ы':'ы','Ь':'ь','Э':'э','Ю':'ю','Я':'я',
                           'A':'a','B':'b','C':'c','D':'d','E':'e','F':'f','G':'g','I':'i','H':'h','J':'j','K':'k','L':'l','M':'m','N':'n','O':'o','P':'p','Q':'q',
                           'R':'r','S':'s','T':'t','U':'u','V':'v','W':'w','X':'x','Y':'y','Z':'z',' ':''}

    alfRE: dict[str, str] = {'a':'а','b':'в','c':'с','e':'е','h':'н','k':'к','m':'м','o':'о','p':'р','r':'р','t':'т','x':'х','y':'у'}
    if txts != "нет авто":
        stroka = ""
        result = ""
        for i in range(0, len(txts)):
            smb = txts[i]
            try:
                keys = alf[smb.upper()] if not smb.isdigit() else smb
            except KeyError:
                keys = smb
            stroka = stroka + keys

        for i in range(0, len(stroka)):
            smb = stroka[i]
            try:
                keys = alfRE[smb]
            except KeyError:
                keys = smb
            result = result + keys
    else:
        result = ''
    return result