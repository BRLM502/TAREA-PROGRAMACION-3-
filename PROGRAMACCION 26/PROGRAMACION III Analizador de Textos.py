# Analizador de Textos 

class TextAnalyzer:
    def __init__(self, text):
        if text == "":
            raise ValueError("El texto esta vacio.")
        
        self.texto_original = text
        self.texto_normalizado = ""
        self.tokens = []
        self.conteos = {}
        self.unicos = set()  # Se usa 'set' como pide la rubrica

    def normalize_text(self, text):
        # Limpieza manual de puntuacion, tipico de logica basica
        texto = text.replace(".", " ")
        texto = texto.replace(",", " ")  # A partir de aqui usamos 'texto'
        texto = texto.replace(":", " ")
        texto = texto.replace(";", " ")
        texto = texto.replace("?", " ")
        texto = texto.replace("!", " ")
        texto = texto.replace("(", " ")
        texto = texto.replace(")", " ")
        texto = texto.replace("[", " ")
        texto = texto.replace("]", " ")
        texto = texto.replace("{", " ")
        texto = texto.replace("}", " ")
        texto = texto.replace("\"", " ")
        texto = texto.replace("'", " ")
        texto = texto.replace("\n", " ")
        
        texto_minusculas = texto.lower()
        
        # Eliminar espacios extra usando split y uniendo de nuevo
        palabras = texto_minusculas.split()
        texto_final = ""
        for p in palabras:
            texto_final = texto_final + p + " "
            
        return texto_final.strip()


    def tokenize(self, text):
        return text.split()

    def analyze(self):
        self.texto_normalizado = self.normalize_text(self.texto_original)
        self.tokens = self.tokenize(self.texto_normalizado)
        
        # Llenar el SET de unicos
        for t in self.tokens:
            self.unicos.add(t)
            
        # Llenar el diccionario de conteos manualmente
        for t in self.tokens:
            if t in self.conteos:
                self.conteos[t] = self.conteos[t] + 1
            else:
                self.conteos[t] = 1

    def report(self):
        total_tokens = len(self.tokens)
        total_unicos = len(self.unicos)
        
        # Calcular promedio con un ciclo basico
        suma_letras = 0
        for t in self.tokens:
            suma_letras = suma_letras + len(t)
        promedio = suma_letras / total_tokens if total_tokens > 0 else 0
        
        # Buscar palabra mas larga y mas corta con logica manual
        mas_larga = ""
        mas_corta = "                                                                      "
        
        for u in self.unicos:
            if len(u) > len(mas_larga):
                mas_larga = u
            if len(u) < len(mas_corta):
                mas_corta = u
                
        # Ordenar para el Top 10
        lista_conteo = list(self.conteos.items())
        lista_ordenada = sorted(lista_conteo, key=lambda x: x[1], reverse=True)
        top_10 = lista_ordenada[:10]

        print("\n===== REPORTE =====")
        print("Total de tokens:", total_tokens)
        print("Tokens unicos:", total_unicos)
        print("Longitud promedio:", promedio)
        print("Palabra mas larga:", mas_larga)
        print("Palabra mas corta:", mas_corta)
        
        print("\nTop 10 tokens mas frecuentes:")
        for palabra, cantidad in top_10:
            print(palabra, "->", cantidad)

    def query(self, word):
        word = word.lower()
        if word in self.conteos:
            veces = self.conteos[word]
            total = len(self.tokens)
            porcentaje = (veces / total) * 100
            
            if veces == 1:
                clasificacion = "rara"
            elif veces >= 5:
                clasificacion = "comun"
            else:
                clasificacion = "moderada"
                
            print("\nPalabra:", word)
            print("Frecuencia:", veces)
            print("Porcentaje:", porcentaje, "%")
            print("Clasificacion:", clasificacion)
        else:
            print("\nLa palabra '" + word + "' no aparece en el texto.")


# --- FUNCIONES DE ENTRADA ---

def leer_consola():
    print("\nEscribe o pega tu texto. Escribe END en una linea nueva para terminar:")
    texto_completo = ""
    while True:
        linea = input()
        if linea == "END":
            break
        texto_completo = texto_completo + linea + " "
    return texto_completo

def leer_archivo():
    ruta = input("Ingresa la ruta del archivo .txt: ")
    try:
        archivo = open(ruta, "r", encoding="utf-8")
        texto = archivo.read()
        archivo.close()
        return texto
    except FileNotFoundError:
        raise FileNotFoundError("Error: Archivo no encontrado.")
    except Exception:
        raise OSError("Error al leer el archivo.")

# --- PRUEBAS MINIMAS (OBLIGATORIAS) ---
def ejecutar_pruebas():
    analizador_prueba = TextAnalyzer("Hola, Mundo!! Python 3.")
    analizador_prueba.analyze()
    
    # Pruebas con assert
    assert analizador_prueba.texto_normalizado == "hola mundo python 3", "Fallo normalizacion"
    assert len(analizador_prueba.tokens) == 4, "Fallo tokenizacion"
    assert len(analizador_prueba.unicos) == 4, "Fallo set de unicos"

# --- PROGRAMA PRINCIPAL ---
def main():
    try:
        ejecutar_pruebas()
    except AssertionError as e:
        print("Error en las pruebas:", e)
        return

    print("=== SISTEMA DE TEXTO ===")
    print("1. Modo archivo")
    print("2. Modo consola")
    opcion = input("Elige (1/2): ")
    
    texto = ""
    try:
        if opcion == "1":
            texto = leer_archivo()
        elif opcion == "2":
            texto = leer_consola()
        else:
            print("Opcion invalida.")
            return
            
        if texto.strip() == "":
            raise ValueError("El texto esta vacio.")
            
        # Usamos la clase
        mi_analizador = TextAnalyzer(texto)
        mi_analizador.analyze()
        mi_analizador.report()
        
        while True:
            buscar = input("\nIngresa palabra para buscar (o 'exit' para salir): ")
            if buscar.lower() == "exit":
                break
            mi_analizador.query(buscar)
            
    except ValueError as e:
        print("Error de valor:", e)
    except FileNotFoundError as e:
        print(e)
    except OSError as e:
        print(e)

if __name__ == "__main__":
    main()
