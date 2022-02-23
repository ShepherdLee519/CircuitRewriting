from match.match import match
from PatternMatching.check import reCheckM


def PatternMatching(data_path, pattern_path):
    mappingList = match(data_path, pattern_path)

    return reCheckM(mappingList, data_path, pattern_path)