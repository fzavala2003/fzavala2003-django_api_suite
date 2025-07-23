from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import uuid

# Simulación de base de datos local en memoria
data_list = []

# Añadiendo algunos datos de ejemplo para probar el GET
data_list.append({'id': str(uuid.uuid4()), 'name': 'User01', 'email': 'user01@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False}) # Ejemplo de item inactivo

class DemoRestApi(APIView):
    name = "Demo REST API"
    def get(self, request):

      # Filtra la lista para incluir solo los elementos donde 'is_active' es True
      active_items = [item for item in data_list if item.get('is_active', False)]
      return Response(active_items, status=status.HTTP_200_OK)

    def post(self, request):
      data = request.data

      # Validación mínima
      if 'name' not in data or 'email' not in data:
         return Response({'error': 'Faltan campos requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

      data['id'] = str(uuid.uuid4())
      data['is_active'] = True
      data_list.append(data)

      return Response({'message': 'Dato guardado exitosamente.', 'data': data}, status=status.HTTP_201_CREATED)
    


class DemoRestApiItem(APIView):
    def get_item_by_id(self, id):
        """Buscar un item por su ID."""
        return next((item for item in data_list if item['id'] == id), None)

    def put(self, request, id):
        """
        Reemplaza completamente los datos de un ítem (menos el ID).
        El campo 'id' es obligatorio y debe coincidir con la URL.
        """
        new_data = request.data
        if 'id' not in new_data or new_data['id'] != id:
            return Response({'error': 'El ID del cuerpo debe coincidir con el ID de la URL.'}, status=status.HTTP_400_BAD_REQUEST)

        item = self.get_item_by_id(id)
        if not item:
            return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        item.clear()
        item.update({
            'id': id,
            'name': new_data.get('name', ''),
            'email': new_data.get('email', ''),
            'is_active': new_data.get('is_active', False)
        })

        return Response(item, status=status.HTTP_200_OK)

    def patch(self, request, id):
        """
        Actualiza parcialmente los campos de un ítem.
        """
        item = self.get_item_by_id(id)
        if not item:
            return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        item.update({key: value for key, value in request.data.items() if key in item and key != 'id'})
        return Response(item, status=status.HTTP_200_OK)

    def delete(self, request, id):
        """
        Eliminación lógica: marca 'is_active' como False.
        """
        item = self.get_item_by_id(id)
        if not item:
            return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        item['is_active'] = False
        return Response({'mensaje': 'Elemento desactivado lógicamente.'}, status=status.HTTP_204_NO_CONTENT)
