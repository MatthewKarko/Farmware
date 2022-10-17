from rest_framework import status
from rest_framework.response import Response

class DefaultResponses:
    RESPONSE_FORBIDDEN = Response({'error': 'You do not have permission to do that.'}, status=status.HTTP_403_FORBIDDEN)
    def __init__(self, context: str) -> None:
        self.RESPONSE_CREATION_SUCCESS = Response(
            {'success': f'{context} created.'}, status=status.HTTP_201_CREATED
            )
        self.RESPONSE_DELETION_SUCCESS = Response(
            {'success': f'{context} deleted.'}, status=status.HTTP_200_OK
            )
        self.RESPONSE_DOES_NOT_EXIST = Response(
            {'error': f'{context} with the given id does not exist.'}, 
            status=status.HTTP_404_NOT_FOUND
            )