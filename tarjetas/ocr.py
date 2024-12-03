# import cv2
# import pytesseract
# from PIL import Image

# class OCRExtractor:
#     def __init__(self, language="spa"):
#         """
#         Inicializa el extractor OCR.
#         :param language: Idioma para Tesseract OCR (por defecto, español: 'spa').
#         """
#         self.language = language
#         self.custom_config = r'--oem 3 --psm 6'  # Configuración básica de Tesseract

#     def preprocess_image(self, image_path, save_processed=False):
#         """
#         Preprocesa la imagen para mejorar la precisión del OCR.
#         :param image_path: Ruta de la imagen a procesar.
#         :param save_processed: Booleano, guarda la imagen preprocesada si es True.
#         :return: Imagen preprocesada (array de OpenCV).
#         """
#         # Cargar la imagen
#         image = cv2.imread(image_path)

#         # Convertir a escala de grises
#         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#         # Aplicar binarización
#         _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

#         # Guardar imagen procesada para debug (opcional)
#         if save_processed:
#             processed_path = "imagen_procesada.jpg"
#             cv2.imwrite(processed_path, binary)
#             print(f"Imagen preprocesada guardada en {processed_path}")

#         return binary

#     def extract_text(self, image_path, save_processed=False):
#         """
#         Extrae texto de una imagen usando Tesseract OCR.
#         :param image_path: Ruta de la imagen a procesar.
#         :param save_processed: Booleano, guarda la imagen preprocesada si es True.
#         :return: Texto extraído de la imagen.
#         """
#         # Preprocesar la imagen
#         preprocessed_image = self.preprocess_image(image_path, save_processed)

#         # Extraer texto usando Pytesseract
#         text = pytesseract.image_to_string(preprocessed_image, config=self.custom_config, lang=self.language)
#         return text

# # Ejemplo de uso
# if __name__ == "__main__":
#     ocr = OCRExtractor(language="spa")
#     image_path = "C:/Pablo/REPOSITORIO/IMV_T/reverso.jpg"  # Cambia esta ruta
#     extracted_text = ocr.extract_text(image_path, save_processed=True)
    
#     print("Texto extraído:")
#     print(extracted_text)


from PIL import Image
import pytesseract
import cv2
import numpy as np

# Ruta de la imagen
image_path = "C:/Pablo/REPOSITORIO/IMV_T/reverso.jpg"  # Cambia esto por la ruta real

# Cargar la imagen usando OpenCV
image = cv2.imread(image_path)

# Preprocesamiento: convertir a escala de grises
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Preprocesamiento: aplicar binarización (opcional)
_, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

# Guardar la imagen preprocesada (opcional, para debug)
cv2.imwrite("imagen_procesada.jpg", binary)

# Usar Pytesseract para extraer texto
custom_config = r'--oem 3 --psm 6'  # Configuración de Tesseract
extracted_text = pytesseract.image_to_string(binary, config=custom_config, lang="spa")

# Mostrar el texto extraído
print("Texto extraído:")
print(extracted_text)
