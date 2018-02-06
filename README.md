# Detector de copias
Aplicación que permite comparar ficheros en código ASCII para buscar similitudes entre ellos, diseñado para localizar copias en ejercicios prácticos de programación.
## Ejecución
`> python [-s|n|p|lA|cA,B] {lista de ficheros}`
Opción | Significado
---| ---
`-s`    | No ignorar espacios
`-n`    | No ignorar saltos de linea
`-lA`   | Ignorar comentarios de linea que comiencen por `A`
`-cA,B` | Ignorar comentarios multilinea delimitados por `A` y `B`
La `lista de ficheros` requiere al menos dos ficheros para comparar. Se permite el uso de comodines.
### Ejemplos de ejecución
`> python detectorCopias.py -l// -c/*,*/ *.c *.h`
`> python detectorCopias.py -l// -c/*,*/ *.java otro/*.java`
`> python detectorCopias.py -l# -s -n ../otroFichero.py *.py`
