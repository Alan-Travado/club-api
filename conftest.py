"""
Cuando realize por primevera vez el comando pytest me saltaron un monton de error y eso se debia a que pytest no estaba encontrando la carpeta raiz del proyecto.
Entoces debi crear un archivo llamado conftest.py en la carpeta raiz del proyecto para que pytest pueda encontrarla y no me de errores.

conftest.py es un archivo especial que pytest reconoce y busca automáticamente en la jerarquía de directorios.
es una convencion como .gitignore o requirements.txt. Cuando pytest arranca, busca ese archivo específico subiendo por las carpetas. 
En el momento en que lo encuentra, usa la ubicación de ese archivo como la carpeta de referencia real del proyecto, en vez de la carpeta de los tests.


O sea el archivo en sí no necesita codigo. Es como poner un cartelito que dice "acá empieza la raíz del proyecto".

"""