from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class BubbleSortView(APIView):
    def post(self, request):

        if "array" not in request.data:
            return Response(
                {"error": "Missing 'array' field."}, status = status.HTTP_400_BAD_REQUEST
            )
                
        inputData = request.data["array"]

        if not isinstance(inputData, list):
            return Response(
            {"error": "'array' must be a list."},
            status=status.HTTP_400_BAD_REQUEST
        )

        if not all(isinstance(value, (int, float)) for value in inputData):
            return Response(
            {"error": "'array' must contain only numbers."},
            status=status.HTTP_400_BAD_REQUEST
        )

        n = len(inputData)
        steps = []

        for i in range(n - 1):
            for j in range(n - i - 1):

                steps.append({
                    "type": "compare",
                    "indices": [j, j + 1]
                })
                

                if inputData[j] > inputData[j + 1]:
                    inputData[j], inputData[j + 1] =  inputData[j + 1], inputData[j]

                    steps.append({
                        "type": "swap",
                        "indices": [ j, j + 1]
                    })


        responseJson = {
            "sorted": inputData,
            "steps": steps
        }

        return Response(responseJson, status = status.HTTP_200_OK)