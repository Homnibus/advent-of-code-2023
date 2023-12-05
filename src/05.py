from dataclasses import dataclass
from operator import attrgetter
import re
from utils.api import get_input


@dataclass
class CategoryInterval:
    start: int
    lenght: int

    @property
    def end(self) -> int:
        return self.start + self.lenght - 1


@dataclass
class ConversionInterval:
    destination_start: int
    source_start: int
    lenght: int

    @property
    def source_end(self) -> int:
        return self.source_start + self.lenght - 1

    @property
    def destination_end(self) -> int:
        return self.source_start + self.lenght - 1

    @property
    def shift(self) -> int:
        return self.destination_start - self.source_start


def aglomerate_category_intervals(seeds: list[list[int]]) -> list[list[int]]:
    working_list = seeds.copy()
    result_list: list[list[int]] = []
    while len(working_list) > 1:
        current_seed = working_list.pop(0)
        if (current_seed[0] + current_seed[1]) == (working_list[0][0]):
            next_seed = working_list.pop(0)
            new_seed = [current_seed[0], current_seed[1] + next_seed[1]]
            working_list.insert(0, new_seed)
        else:
            result_list.append(current_seed)
    if len(working_list) > 0:
        result_list.append(working_list[0])
    return result_list


def extract_conversion_table(
    split_inputs: list[str], rank: int
) -> list[ConversionInterval]:
    conversion_table: list[ConversionInterval] = []
    for line in split_inputs[rank].splitlines()[1:]:
        line_str_values = re.findall(r"([0-9]+)", line)
        line_values = list(map(lambda x: int(x), line_str_values))
        conversion_table.append(ConversionInterval(*line_values))
    # add end limit
    conversion_table.append(
        ConversionInterval(
            -1, 9999999999999999999999999999999999999999999999999999999999999999, 0
        )
    )
    conversion_table.sort(key=attrgetter("source_start"))
    return conversion_table


def extract_seeds(split_inputs: str) -> list[CategoryInterval]:
    seed_interval_list: list[CategoryInterval] = []
    line_payload = split_inputs.split(":")[1]
    line_intervals = re.findall(r"([0-9]+\s[0-9]+)", line_payload)
    for interval in line_intervals:
        interval_str_values = re.findall(r"([0-9]+)", interval)
        interval_values = list(map(lambda x: int(x), interval_str_values))
        seed_interval_list.append(CategoryInterval(*interval_values))
    seed_interval_list.sort(key=attrgetter("start"))
    return seed_interval_list


def aglomerate_category_intervals(
    category_intervals: list[CategoryInterval],
) -> list[CategoryInterval]:
    result_list: list[CategoryInterval] = []
    working_list = category_intervals.copy()
    while len(working_list) > 1:
        current_category_interval = working_list.pop(0)
        if (current_category_interval.end + 1) == (working_list[0].start):
            next_category_interval = working_list.pop(0)
            new_category_interval = CategoryInterval(
                current_category_interval.start,
                current_category_interval.lenght + next_category_interval.lenght,
            )
            working_list.insert(0, new_category_interval)
        else:
            result_list.append(current_category_interval)
    if len(working_list) > 0:
        result_list.append(working_list[0])
    return result_list


def translate(
    category_intervals: list[CategoryInterval],
    conversion_table: list[ConversionInterval],
) -> list[CategoryInterval]:
    translated_category_intervals: list[CategoryInterval] = []
    conversion_interval_index = 0
    while len(category_intervals) > 0:
        category_interval = category_intervals.pop(0)

        # make START of category interval <= END of conversion interval by finding the next matcing conversion interval
        while (
            category_interval.start
            > conversion_table[conversion_interval_index].source_end
        ):
            conversion_interval_index += 1
        conversion_interval = conversion_table[conversion_interval_index]

        # START of category interval < START of conversion interval
        if category_interval.start < conversion_interval.source_start:
            # END of category interval < START of conversion interval
            if category_interval.end < conversion_interval.source_start:
                translated_category_intervals.append(category_interval)
            # END of category interval >= START of conversion interval
            else:
                intersection_lenght = (
                    conversion_interval.source_start - category_interval.start
                )
                translated_category_intervals.append(
                    CategoryInterval(category_interval.start, intersection_lenght)
                )
                category_intervals.insert(
                    0,
                    CategoryInterval(
                        conversion_interval.source_start,
                        category_interval.lenght - intersection_lenght,
                    ),
                )
        # START category interval IN a conversion interval
        else:
            # END of category interval <= END of conversion interval
            if category_interval.end <= conversion_interval.source_end:
                translated_category_intervals.append(
                    CategoryInterval(
                        category_interval.start + conversion_interval.shift,
                        category_interval.lenght,
                    )
                )
            # END of category interval > END of conversion interval
            else:
                intersection_lenght = (
                    conversion_interval.source_end - category_interval.start + 1
                )
                translated_category_intervals.append(
                    CategoryInterval(
                        category_interval.start + conversion_interval.shift,
                        intersection_lenght,
                    )
                )
                category_intervals.insert(
                    0,
                    CategoryInterval(
                        conversion_interval.source_end + 1,
                        category_interval.lenght - intersection_lenght,
                    ),
                )
    translated_category_intervals.sort(key=attrgetter("start"))
    translated_category_intervals = aglomerate_category_intervals(
        translated_category_intervals
    )
    return translated_category_intervals


input_str = get_input(5)
splited_input = input_str.split("\n\n")
seeds = extract_seeds(splited_input[0])
conversion_tables = [extract_conversion_table(splited_input, i) for i in range(1, 8)]

current_category_intervals = seeds
for conversion_table in conversion_tables:
    current_category_intervals = translate(current_category_intervals, conversion_table)

print(current_category_intervals[0].start)
