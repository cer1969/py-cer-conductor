# CRISTIAN ECHEVERRÍA RABÍ
# Calcula capacidad calórica de conductores

#------------------------------------------------------------------------------
# CONSTANTES

JOULE_A_KCAL = 0.00023889   # kCal/Joule
METRO_A_PIE = 3.2808        # pies/metro

# VALORES CONOCIDOS DE CALOR ESPECÍFICO PARA DISTINTOS MATERIALES
# Calor específico Joule/(Kg*°K)
# Capacidad calórica (kcal/°K)

CALOR_ESPECIFICO = {"al"    :   910,    # Aluminio --> Otro dato 900
                    "aal"   :   700,    # Aleación de aluminio
                    "ac"    :   460,    # Acero --> Otro dato 449
                    "cu"    :   386}    # Cobre --> Otro dato 385

CAPACIDAD_CALORICA = {"al"    :  0.214,    # Aluminio
                      "ac"    :  0.115,    # Acero
                      "cu"    :  0.0928}   # Cobre

#------------------------------------------------------------------------------
# CÁLCULO DE CAPACIDAD CALÓRICA por unidad de longitud kcal/(pie*°K)
# data  :   Lista de pares (tipo cable, kg/metro de cable)

def CapacidadCalorica(data):
    j_metro_k_total = 0
    for tipo,peso in data:
        cesp = CALOR_ESPECIFICO[tipo]
        j_metro_k = cesp * peso
        j_metro_k_total = j_metro_k_total + j_metro_k
    kcal_metro_k = j_metro_k_total * JOULE_A_KCAL
    return kcal_metro_k / METRO_A_PIE

def CapacidadCalorica2(data):
    j_metro_k_total = 0
    for tipo,peso in data:
        cesp = CAPACIDAD_CALORICA[tipo]
        j_metro_k = cesp * peso
        j_metro_k_total = j_metro_k_total + j_metro_k
    return j_metro_k_total / METRO_A_PIE

#------------------------------------------------------------------------------
# TEST

if __name__ == "__main__":
    # Grosbeak
    data = [("al",0.86897645),
            ("ac",0.412073358)]
    print (CapacidadCalorica(data),CapacidadCalorica2(data))

    # Acar 1400 ???
    data = [("al",1.955)]
    print (CapacidadCalorica(data),CapacidadCalorica2(data))

    data = [("cu",2.067)]
    print (CapacidadCalorica(data),CapacidadCalorica2(data))

    #data = [("aal", 3.856)]
    #cc1 = CapacidadCalorica(data)
    #cc2 = CapacidadCalorica2(data)
    #print "%.6f" % cc1
    """
    import sqlite
    db = sqlite.connect("Calipso2.db")
    cur = db.cursor()
    """
    #query = """select nombre,peso_prop,cap_calor
    #           from cable
    #           where tipo = 'ALL'
    #           order by orden"""
    """
    cur.execute("-- types str,float,float")
    cur.execute(query)
    Q = cur.fetchall()
    for nom,pes,cc in Q:
        data = [("al",pes)]
        cc2 = CapacidadCalorica(data)
        print "%12s %6.1f %9.8f %9.8f %9.8f" % (nom,pes,cc,cc2,cc2-cc)
    """
    #data = [("al",1.670)]
    #print CapacidadCalorica(data)
