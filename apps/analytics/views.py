from django.db.models import Count, Avg, Sum
from django.db.models.functions import TruncYear, TruncMonth
from django.utils import timezone
from datetime import timedelta

from rest_framework import viewsets
from .models import Metric
from .serializers import MetricSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.accidents.models import Accident
from apps.evacuations.models import Evacuation
from apps.fines.models import Fine
from apps.trafficlights.models import TrafficLight

import random, math


class MetricViewSet(viewsets.ModelViewSet):
    queryset = Metric.objects.all()
    serializer_class = MetricSerializer


# дистанция между двумя точками на карте
# нужна для районирования
def calculate_distance(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    R = 6371
    distance = R * c

    return distance


def find_closest_district(lat, lon):
    min_distance = float("inf")
    closest_district = None

    for dist in DISTRICTS:
        distance = calculate_distance(
            lat,
            lon,
            dist[0],
            dist[1],
        )

        if distance < min_distance:
            closest_district = dist
            min_distance = distance

    return closest_district


CHART_TYPES = ["bar", "area", "line"]
DISTRICTS = [
    (54.809566, 31.995314, "Заднепровский"),
    (54.765531, 32.019900, "Ленинский"),
    (54.773677, 32.089058, "Промышленный"),
]


class StatsViewSet(APIView):
    def get(self, request):
        result = []

        # FINES BLOCK
        fines = self._fines_stats()

        fines_data_map__total_count = {}
        fines_data_fields__total_count = set()
        for item in fines:
            year = item["year"] = item["year"].strftime("%Y")
            month = item["month"] = item["month"].strftime("%m")

            fines_data_fields__total_count.add(year)

            if month not in fines_data_map__total_count:
                fines_data_map__total_count[month] = {
                    "x": month,
                }

            fines_data_map__total_count[month][f"y_{year}"] = item["total_count"]

        fines_data_map__average_amount = {}
        fines_data_fields__average_amount = set()
        for item in fines:
            year = item["year"]
            month = item["month"]
            
            fines_data_fields__average_amount.add(year)

            if month not in fines_data_map__average_amount:
                fines_data_map__average_amount[month] = {
                    "x": month,
                }

            fines_data_map__average_amount[month][f"y_{year}"] = item["average_amount"]

        fines_data_map__total_amount = {}
        fines_data_fields__total_amount = set()
        for item in fines:
            year = item["year"] = item["year"]
            month = item["month"] = item["month"]

            fines_data_fields__total_amount.add(year)

            if month not in fines_data_map__total_amount:
                fines_data_map__total_amount[month] = {
                    "x": month,
                }

            fines_data_map__total_amount[month][f"y_{year}"] = item["total_amount"]

        result.append(
            {
                "name": "Штрафы (общая сумма)",
                "public": False,
                "type": "line",
                "fields": list(fines_data_fields__total_amount),
                "y_axis_name": "Сумма",
                "x_axis_name": "Месяц",
                "values": list(fines_data_map__total_amount.values()),
            }
        )
        result.append(
            {
                "name": "Штрафы (средняя сумма)",
                "public": "line",
                "type": "line",
                "fields": list(fines_data_fields__average_amount),
                "y_axis_name": "Сумма",
                "x_axis_name": "Месяц",
                "values": list(fines_data_map__average_amount.values()),
            }
        )
        result.append(
            {
                "name": "Штрафы (количество)",
                "public": "area",
                "type": random.choice(CHART_TYPES),
                "fields": list(fines_data_fields__total_count),
                "y_axis_name": "Количество",
                "x_axis_name": "Месяц",
                "values": list(fines_data_map__total_count.values()),
            }
        )

        # FINES BLOCK END

        # EVACUATIONS BLOCK
        evacuations = self._evacuation_stats()

        evacuations_data_map__total_count = {}
        evacuations_data_fields__total_count = set()
        for item in evacuations:
            year = item["year"] = item["year"].strftime("%Y")
            month = item["month"] = item["month"].strftime("%m")

            evacuations_data_fields__total_count.add(year)

            if month not in evacuations_data_map__total_count:
                evacuations_data_map__total_count[month] = {
                    "x": month,
                }

            evacuations_data_map__total_count[month][f"y_{year}"] = item["total_count"]

        result.append(
            {
                "name": "Эвакуации (количество)",
                "public": True,
                "type": "area",
                "fields": list(evacuations_data_fields__total_count),
                "y_axis_name": "Количество",
                "x_axis_name": "Месяц",
                "values": list(evacuations_data_map__total_count.values()),
            }
        )

        # EVACUATIONS BLOCK END

        # TRAFFIC LIGHTS BLOCK
        trafficlights = self._trafficlight_stats()

        trafficlights_data_map__total_count = {}
        trafficlights_data_fields__total_count = set()
        for item in trafficlights:
            year = item["year"] = item["year"].strftime("%Y")
            month = item["month"] = item["month"].strftime("%m")

            trafficlights_data_fields__total_count.add(year)

            if month not in trafficlights_data_map__total_count:
                trafficlights_data_map__total_count[month] = {
                    "x": month,
                }

            trafficlights_data_map__total_count[month][f"y_{year}"] = item[
                "total_count"
            ]

        trafficlights = self._trafficlight_stats_type()

        trafficlights_data_map__typed_count = {}
        trafficlights_data_fields__typed_count = set()
        for item in trafficlights:
            year = item["year"] = item["year"].strftime("%Y")
            type = item["type"]

            trafficlights_data_fields__typed_count.add(year)

            if type not in trafficlights_data_map__typed_count:
                trafficlights_data_map__typed_count[type] = {
                    "x": type,
                }

            trafficlights_data_map__typed_count[type][f"y_{year}"] = item["total_count"]

        trafficlights = self._trafficlights_stats_district()

        trafficlights_data_map__district = {}
        trafficlights_data_fields__district = set()
        for district, value in trafficlights.items():
            for year, count in value.items():
                trafficlights_data_fields__district.add(year)

                if district not in trafficlights_data_map__district:
                    trafficlights_data_map__district[district] = {"x": district}

                trafficlights_data_map__district[district][f"y_{year}"] = count

        result.append(
            {
                "name": "Светофоры (типы)",
                "public": True,
                "type": "bar",
                "fields": list(trafficlights_data_fields__typed_count),
                "y_axis_name": "Количество",
                "x_axis_name": "Тип",
                "values": list(trafficlights_data_map__typed_count.values()),
            }
        )

        result.append(
            {
                "name": "Светофоры (количество)",
                "public": True,
                "type": "area",
                "fields": list(trafficlights_data_fields__total_count),
                "y_axis_name": "Количество",
                "x_axis_name": "Месяц",
                "values": list(trafficlights_data_map__total_count.values()),
            }
        )

        result.append(
            {
                "name": "Светофоры (по районам)",
                "public": True,
                "type": "bar",
                "fields": list(trafficlights_data_fields__district),
                "y_axis_name": "Количество",
                "x_axis_name": "Район",
                "values": list(trafficlights_data_map__district.values()),
            }
        )

        # TRAFFIC LIGHTS BLOCK END

        # ACCIDENTS BLOCK

        accidents = self._accident_stats()

        accidents_data_map__total_count = {}
        accidents_data_fields__total_count = set()
        for item in accidents:
            year = item["year"] = item["year"].strftime("%Y")
            month = item["month"] = item["month"].strftime("%m")

            accidents_data_fields__total_count.add(year)

            if month not in accidents_data_map__total_count:
                accidents_data_map__total_count[month] = {
                    "x": month,
                }

            accidents_data_map__total_count[month][f"y_{year}"] = item["total_count"]
            
        accidents = self._accidents_stats_district()

        accidents_data_map__district = {}
        accidents_data_fields__district = set()
        for district, value in accidents.items():
            for year, count in value.items():
                accidents_data_fields__district.add(year)

                if district not in accidents_data_map__district:
                    accidents_data_map__district[district] = {"x": district}

                accidents_data_map__district[district][f"y_{year}"] = count
            
        result.append(
            {
                "name": "Аварии (количество)",
                "public": True,
                "type": random.choice(CHART_TYPES),
                "fields": list(accidents_data_fields__total_count),
                "y_axis_name": "Количество",
                "x_axis_name": "Месяц",
                "values": list(accidents_data_map__total_count.values()),
            }
        )
        
        result.append(
            {
                "name": "Аварии (по районам)",
                "public": True,
                "type": "bar",
                "fields": list(accidents_data_fields__district),
                "y_axis_name": "Количество",
                "x_axis_name": "Район",
                "values": list(accidents_data_map__district.values()),
            }
        )

        return Response(result)

    def _fines_stats(self):
        fines_stats = (
            Fine.objects.annotate(
                year=TruncYear("issued_at"),
                month=TruncMonth("issued_at"),
            )
            .values("year", "month")
            .annotate(
                total_count=Count("id"),
                average_amount=Avg("amount"),
                total_amount=Sum("amount"),
            )
            .order_by("year", "month")
        )

        return fines_stats

    def _evacuation_stats(self):
        evacuations_stats = (
            Evacuation.objects.annotate(
                year=TruncYear("requested_at"),
                month=TruncMonth("requested_at"),
            )
            .values("year", "month")
            .annotate(total_count=Count("id"))
            .order_by("year", "month")
        )

        return evacuations_stats

    def _trafficlight_stats(self):
        trafficlights_stats = (
            TrafficLight.objects.exclude(install_date__isnull=True)
            .annotate(year=TruncYear("install_date"), month=TruncMonth("install_date"))
            .values("year", "month")
            .annotate(total_count=Count("id"))
            .order_by("year", "month")
        )

        return trafficlights_stats

    def _trafficlight_stats_type(self):
        trafficlights_stats_type = (
            TrafficLight.objects.annotate(
                year=TruncYear("created_at"), month=TruncMonth("created_at")
            )
            .values("year", "month", "type")
            .annotate(total_count=Count("id"))
            .order_by("year", "month")
        )

        return trafficlights_stats_type

    def _trafficlights_stats_district(self):
        trafficlights = TrafficLight.objects.annotate(
            year=TruncYear("install_date"),
            year_2=TruncYear("created_at"),
        ).values("id", "latitude", "longitude", "year", "year_2")

        stats = {}
        for district in DISTRICTS:
            stats[district[2]] = {}

        for tf in trafficlights:
            closest = find_closest_district(
                tf["latitude"],
                tf["longitude"],
            )

            if closest:
                name = closest[2]
                keyname = (tf["year"] or tf["year_2"]).strftime("%Y")

                if keyname not in stats[name]:
                    stats[name][keyname] = 0

                stats[name][keyname] += 1

        return stats

    def _accident_stats(self):
        accidents_stats = (
            Accident.objects.annotate(
                year=TruncYear("reported_at"), month=TruncMonth("reported_at")
            )
            .values("year", "month")
            .annotate(total_count=Count("id"))
            .order_by("year", "month")
        )

        return accidents_stats

    def _accidents_stats_district(self):
        accidents = Accident.objects.annotate(
            year=TruncYear("reported_at"),
        ).values("id", "latitude", "longitude", "year")

        stats = {}
        for district in DISTRICTS:
            stats[district[2]] = {}

        for ac in accidents:
            closest = find_closest_district(
                ac["latitude"],
                ac["longitude"],
            )

            if closest:
                name = closest[2]
                keyname = ac["year"].strftime("%Y")

                if keyname not in stats[name]:
                    stats[name][keyname] = 0

                stats[name][keyname] += 1

        return stats
