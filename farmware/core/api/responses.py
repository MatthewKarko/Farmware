from rest_framework import status
from rest_framework.response import Response
from django.forms.models import model_to_dict

class DefaultResponses:
    RESPONSE_FORBIDDEN = Response({'error': 'You do not have permission to do that.'}, status=status.HTTP_403_FORBIDDEN)
    def __init__(self, context: str) -> None:
        # Success
        self.SUCCESS = Response(
            status=status.HTTP_200_OK
        )

        self.CREATION_SUCCESS = Response(
            {'success': f'{context} created.'}, status=status.HTTP_201_CREATED
            )

        self.DELETION_SUCCESS = Response(
            {'success': f'{context} deleted.'}, status=status.HTTP_200_OK
            )

        # Fail
        self.DOES_NOT_EXIST = Response(
            {'error': f'{context} with the given id does not exist.'}, 
            status=status.HTTP_404_NOT_FOUND
            )

        self.ITEM_ALREADY_EXISTS = Response(
            {'error': f'{context} already exists.'}, 
            status=status.HTTP_404_NOT_FOUND
            )

        self.BAD_REQUEST = Response(
            {'error': f'Invalid request for {context}'}, 
            status=status.HTTP_400_BAD_REQUEST
            )

    def json(self, model):
        return Response(model_to_dict(model), status=status.HTTP_200_OK)
    
    def list_json(self, list):
        list = [model_to_dict(model) for model in list]
        return Response(list, status=status.HTTP_200_OK)