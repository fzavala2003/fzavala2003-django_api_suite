from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import firebase_admin
from firebase_admin import db
from datetime import datetime
import os

# Inicializar Firebase Admin (hazlo solo una vez)
if not firebase_admin._apps:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cred_path = os.path.join(BASE_DIR, "secrets", "landing-key.json")
    cred = firebase_admin.credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://TU-PROYECTO.firebaseio.com'  # Cambia esta URL por la tuya
    })


class LandingAPI(APIView):
    name = "Landing API"
    collection_name = "comentarios"  # Cambia este nombre según tu colección en Firebase

    def get(self, request):
        try:
            ref = db.reference(self.collection_name)
            data = ref.get()
            return Response({"data": data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            ref = db.reference(self.collection_name)
            payload = request.data
            # Agrega un timestamp
            payload['created_at'] = datetime.utcnow().isoformat()
            new_ref = ref.push(payload)
            return Response({"id": new_ref.key}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
