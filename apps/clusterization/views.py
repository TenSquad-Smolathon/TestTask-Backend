from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.permissions import AllowAny
from collections import Counter, defaultdict
from pandas import read_excel, read_csv
import pandas as pd

COORDS = {
    "D1": [54.789358814745, 32.035550306418],
    "D2": [54.780969625604, 32.037309835532],
    "D3": [54.777677816468, 32.051729391196],
    "D4": [54.776984769882, 32.054647634604],
    "D5": [54.780103386015, 32.057694624045],
    "D6": [54.783371179261, 32.058335520619],
    "D7": [54.784310661667, 32.061857412436],
    "D8": [54.790472293085, 32.051600645163],
    "D9": [54.79042280581, 32.043918798545],
    "D10": [54.789804209761, 32.063273618796],
    "D11": [54.788690713022, 32.051986883261],
    "D12": [54.78127899239, 32.055892179587],
    "D13": [54.781105747281, 32.05248040972],
    "D14": [54.780685006071, 32.050270269492],
    "D15": [54.784620002897, 32.051536272147],
    "D16": [54.783432119671, 32.049133012869],
    "D17": [54.784026065645, 32.044841478446],
    "D18": [54.780116112768, 32.045275943653],
}


class ClustersViewSet(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        uploaded_file = request.FILES.get("file")

        if not uploaded_file:
            return Response({"error": "no file provided"}, status=HTTP_400_BAD_REQUEST)

        fname = uploaded_file.name
        dataframe = None

        if fname.endswith(".xlsx") or fname.endswith(".xls"):
            dataframe = read_excel(uploaded_file)
        elif fname.endswith(".csv"):
            dataframe = read_csv(uploaded_file)
        else:
            return Response(
                {
                    "error": f'bad file: expected xls/xlsx/csv, got {fname.split(".")[-1]}'
                },
                status=HTTP_400_BAD_REQUEST,
            )

        data = self.detect_groups(dataframe, COORDS, 3, 60, 30)

        return Response(data)

    # detects car groups and returns (groups, graph)
    def detect_groups(
        self,
        df: pd.DataFrame,
        coords: dict[str, list[float, float]],
        min_sequence_length: int = 3,
        max_time_gap: int = 60,
        n_most_used: int = 5,
    ) -> tuple[list, dict]:
        df = self.preprocess(df, coords)
        graph = self.build_graph(df)
        traj = self.build_trajectories(df)
        groups = self.build_simultaneous_groups(traj, max_time_gap, min_sequence_length)
        most_used = self.most_used_sections(
            traj, min_sequence_length, n_most_used, 1.7, 1.2
        )

        return {
            "groups": {k: v for k, v in zip(map(str, groups.keys()), groups.values())},
            "graph": graph,
            "most_used": most_used,
            "coords": coords,
        }

    # finds sections of road that are mostly used
    def most_used_sections(
        self,
        routes: list[list],
        min_sequence_length=3,
        n_top=5,
        alpha=1.7,  # coef of length
        beta=1.2,  # coef of frequency
    ):
        routes = [[x[1] for x in y] for y in routes.values()]
        sections = Counter()

        for route in routes:
            n = len(route)

            for length in range(min_sequence_length, n + 1):
                for i in range(n - length + 1):
                    section = tuple(route[i : i + length])
                    sections[section] += 1

        scored = [
            (sec, count, len(sec), (len(sec) ** alpha) * (count**beta))
            for sec, count in sections.items()
            if len(sec) >= min_sequence_length
        ]

        scored.sort(key=lambda x: x[3], reverse=True)

        top_sections = scored[:n_top]

        return top_sections

    # preprocess data for better perfomance
    def preprocess(
        self, df: pd.DataFrame, coords: dict[str, list[float, float]]
    ) -> pd.DataFrame:
        df = df.copy()
        df["Временная_метка"] = pd.to_datetime(df["Временная_метка"])
        df = df.sort_values(["Идентификатор_ТС", "Временная_метка"])

        df["lat"] = df["ID_детектора"].map(lambda x: coords.get(x, [None, None])[0])
        df["lon"] = df["ID_детектора"].map(lambda x: coords.get(x, [None, None])[0])

        return df

    # build graph of detectors
    def build_graph(self, df: pd.DataFrame) -> dict[str, list[str]]:
        graph = defaultdict(list)

        vehicle_detectors = df.groupby("Идентификатор_ТС")["ID_детектора"].apply(list)

        for detectors in vehicle_detectors:
            for i in range(len(detectors) - 1):
                current_det = detectors[i]
                next_det = detectors[i + 1]

                if next_det not in graph[current_det]:
                    graph[current_det].append(next_det)

        return dict(graph)

    # returns trajectories of cars
    def build_trajectories(self, df: pd.DataFrame):
        traj = {}

        grouped = df.groupby("Идентификатор_ТС")

        for ts_id, gdata in grouped:
            traj[ts_id] = list(
                zip(gdata["Временная_метка"].to_list(), gdata["ID_детектора"].to_list())
            )

        return traj

    # finds groups of cars that move simultaneously on some road segment
    def build_simultaneous_groups(self, traj: dict, time_threshhold=60, min_seq_len=2):
        traj_graph = list([x[1] for x in y] for y in traj.values())
        traj_time = list([x[0] for x in y] for y in traj.values())
        traj_keys = list(traj.keys())

        subseqs = {}

        for i, traj1 in enumerate(traj_graph):
            for j, traj2 in enumerate(traj_graph):
                if i == j or i < j:
                    continue

                common_subseq = self.longest_common_subsequence(traj1, traj2)

                if len(common_subseq) < min_seq_len:
                    continue

                start_diff = abs(
                    (
                        traj_time[i][traj1.index(common_subseq[0])]
                        - traj_time[j][traj2.index(common_subseq[0])]
                    ).total_seconds()
                )
                end_diff = abs(
                    (
                        traj_time[i][traj1[::-1].index(common_subseq[-1])]
                        - traj_time[j][traj2[::-1].index(common_subseq[-1])]
                    ).total_seconds()
                )

                if start_diff > time_threshhold or end_diff > time_threshhold:
                    continue

                subseqs[(traj_keys[i], traj_keys[j])] = list(set(common_subseq))

        return subseqs

    # LCS algo
    def longest_common_subsequence(self, list1: list, list2: list):
        n, m = len(list1), len(list2)
        dp = [[0] * (m + 1) for _ in range(n + 1)]

        for i in range(1, n + 1):
            for j in range(1, m + 1):
                if list1[i - 1] == list2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        lcs = []
        i, j = n, m
        while i > 0 and j > 0:
            if list1[i - 1] == list2[j - 1]:
                lcs.append(list1[i - 1])
                i -= 1
                j -= 1
            elif dp[i - 1][j] > dp[i][j - 1]:
                i -= 1
            else:
                j -= 1

        return lcs[::-1]
