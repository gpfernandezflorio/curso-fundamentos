import sys
import os
import json

ENCODING = None # "utf-8"

def main():
  if len(sys.argv) < 2:
    print("Falta la ruta del archivo.")
    exit(0)

  rutaArchivo = sys.argv[1]
  if not os.path.isfile(rutaArchivo):
    print("El archivo " + rutaArchivo + " no existe.")
    exit(0)

  f = open(rutaArchivo, 'r', encoding=ENCODING)
  data = f.read()
  f.close()
  obj = json.loads(data)

  escribirArchivo("_original.json", obj)
  generarVersiones(obj)

def generarVersiones(obj):
  if not ("course" in obj):
    print("Archivo sin definición de curso.")
    exit(0)

  módulos = obj["modules"] if "modules" in obj else []
  actividades = obj["activities"] if "activities" in obj else []

  versiones = {
    "base":{},
    "full":{}
  }
  for alt in sinRepetidos(versionesDeclaradas(actividades)):
    versiones["alt_" + alt] = {}
  procesarCurso(obj["course"], versiones)

  procesarMódulos(módulos, versiones)

  procesarActividades(actividades, versiones)
  
  limpiarActividadesModulos(versiones)

  guardarArchivos(versiones)

def procesarCurso(definiciónCurso, versiones):
  for idVersión in versiones:
    versiones[idVersión]["course"] = copiaDeDatos(definiciónCurso)

def procesarMódulos(listaDeMódulos, versiones):
  for idVersión in versiones:
    versiones[idVersión]["modules"] = copiaDeDatos(listaDeMódulos)

def procesarActividades(listaDeActividades, versiones):
  for idVersión in versiones:
    versiones[idVersión]["activities"] = copiaDeDatos(actividadesDeVersión(listaDeActividades, idVersión))

def limpiarActividadesModulos(versiones):
  for idVersión in versiones:
    for módulo in versiones[idVersión]["modules"]:
      limpiarActividadesModulo(módulo, versiones[idVersión]["activities"])

def limpiarActividadesModulo(módulo, actividades):
  if "activities" in módulo and type(módulo["activities"]) == type([]):
    módulo["activities"] = filtroIds(módulo["activities"], idsDeActividades(actividades))

def copiaDeDatos(datosOriginales):
  if type(datosOriginales) == type([]):
    return copiaDeLista(datosOriginales)
  if type(datosOriginales) == type({}):
    return copiaDeObjeto(datosOriginales)
  if type(datosOriginales) == type(""):
    return datosOriginales
  if type(datosOriginales) == type(True):
    return datosOriginales
  if type(datosOriginales) == type(0):
    return datosOriginales
  if type(datosOriginales) == type(0.0):
    return datosOriginales
  print("Tipo de dato desconocido: " + str(datosOriginales))
  print(type(datosOriginales))
  exit(0)

def copiaDeObjeto(datosOriginales):
  copia = {}
  for k in datosOriginales:
    if k != "alts":
      copia[k] = copiaDeDatos(datosOriginales[k])
  return copia

def copiaDeLista(datosOriginales):
  copia = []
  for dato in datosOriginales:
    copia.append(copiaDeDatos(dato))
  return copia

def actividadesDeVersión(listaDeActividades, idVersión):
  filtrados = []
  for actividad in listaDeActividades:
    if pasaFiltro(actividad, idVersión):
      filtrados.append(actividad)
  return filtrados

def pasaFiltro(actividad, idVersión):
  return (idVersión == "full") or \
    (not ("alts" in actividad)) or \
    (idVersión[4:] in actividad["alts"])

def versionesDeclaradas(listaDeActividades):
  versiones = []
  for actividad in listaDeActividades:
    if "alts" in actividad:
      versiones = versiones + actividad["alts"]
  return versiones

def sinRepetidos(lista):
  unicos = []
  for elemento in lista:
    if not (elemento in unicos):
      unicos.append(elemento)
  return unicos

def guardarArchivos(versiones):
  for idVersión in versiones:
    escribirArchivo("_" + idVersión + ".json", versiones[idVersión])

def escribirArchivo(nombre, versión):
  data = json.dumps(versión, ensure_ascii=False, indent=2)
  f = open(nombre, 'w', encoding=ENCODING)
  f.write(data)
  f.close()

def filtroIds(idsOriginales, idsVálidos):
  ids = []
  for idActividad in idsOriginales:
    if idActividad in idsVálidos:
      ids.append(idActividad)
  return ids

def idsDeActividades(actividades):
  ids = []
  for actividad in actividades:
    if "reference_id" in actividad:
      ids.append(actividad["reference_id"])
  return ids

if __name__ == "__main__":
  main()