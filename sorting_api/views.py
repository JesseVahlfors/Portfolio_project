from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .algorithms.bubble_sort import bubble_sort
from .algorithms.insertion_sort import insertion_sort
from .algorithms.merge_sort import merge_sort
from .algorithms.quick_sort import quick_sort
from .algorithms.selection_sort import selection_sort

SORTING_ALGORITHMS = {
    "bubble": bubble_sort,
    "selection": selection_sort,
    "insertion": insertion_sort,
    "merge": merge_sort,
    "quick": quick_sort,
}


class SortingView(APIView):
    def post(self, request):

        if "array" not in request.data:
            return Response(
                {"error": "Missing 'array' field."}, status=status.HTTP_400_BAD_REQUEST
            )

        if "algorithm" not in request.data:
            return Response(
                {"error": "Missing 'algorithm' field."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        input_data = request.data["array"]

        if not isinstance(input_data, list):
            return Response(
                {"error": "'array' must be a list."}, status=status.HTTP_400_BAD_REQUEST
            )

        if not all(isinstance(value, (int, float)) for value in input_data):
            return Response(
                {"error": "'array' must contain only numbers."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if len(input_data) == 0:
            return Response(
                {"error": "'array' must contain at least one number."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        input_algorithm = request.data["algorithm"]

        if not isinstance(input_algorithm, str):
            return Response(
                {"error": "'algorithm' must be a string."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if input_algorithm not in SORTING_ALGORITHMS:
            return Response(
                {
                    "error": f"'algorithm' needs to be one of the supported algorithms: {', '.join(SORTING_ALGORITHMS)} "
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        algorithm_function = SORTING_ALGORITHMS[input_algorithm]

        sorted_array, steps = algorithm_function(input_data)

        stats = {
            "comparisons": 0,
            "writes": 0,
            "swaps": 0,
            "moves": 0,
        }

        operation_mapping = {
            "compare": "comparisons",
            "write": "writes",
            "swap": "swaps",
            "move": "moves",
        }

        for step in steps:
            stats_key = operation_mapping.get(step["type"])

            if stats_key:
                stats[stats_key] += 1

        responseJson = {"sorted": sorted_array, "steps": steps, "stats": stats}

        return Response(responseJson, status=status.HTTP_200_OK)
