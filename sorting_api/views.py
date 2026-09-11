from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class BubbleSortView(APIView):
    def post(self, request):
        inputData = request.data["array"]
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