import sys
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class Respondent:
    name: str
    age: int

    def __str__(self):
        return f"{self.name} ({self.age})"


class AgeGroup:
    def __init__(self, min_age: int, max_age: Optional[int], label: str):
        self.min_age = min_age
        self.max_age = max_age 
        self.label = label

    def contains(self, age: int) -> bool:
        if self.max_age is None:
            return age >= self.min_age
        return self.min_age <= age <= self.max_age


class SurveyProcessor:
    def __init__(self, boundaries: List[int]):
        self.boundaries = sorted(boundaries)
        self.groups = self._create_groups()

    def _create_groups(self) -> List[AgeGroup]:
        groups = []
        if self.boundaries:
            first = self.boundaries[0]
            groups.append(AgeGroup(0, first, f"0-{first}"))
        for i in range(len(self.boundaries) - 1):
            min_age = self.boundaries[i] + 1
            max_age = self.boundaries[i + 1]
            groups.append(AgeGroup(min_age, max_age, f"{min_age}-{max_age}"))
        if self.boundaries:
            last = self.boundaries[-1]
            groups.append(AgeGroup(last + 1, None, f"{last + 1}+"))
        return groups

    def process(self, input_stream) -> str:
        respondents = []
        for line in input_stream:
            line = line.strip()
            if line == "END":
                break
            if not line:
                continue
            parts = line.rsplit(',', 1)
            if len(parts) != 2:
                continue
            name = parts[0].strip()
            try:
                age = int(parts[1].strip())
            except ValueError:
                continue
            respondents.append(Respondent(name, age))

        grouped = {group: [] for group in self.groups}
        for resp in respondents:
            for group in self.groups:
                if group.contains(resp.age):
                    grouped[group].append(resp)
                    break

        output_lines = []
        for group in reversed(self.groups):
            resps = grouped[group]
            if not resps:
                continue
            resps.sort(key=lambda r: (-r.age, r.name))
            resps_str = ", ".join(str(r) for r in resps)
            output_lines.append(f"{group.label}: {resps_str}")
        return "\n\n".join(output_lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python survey.py <boundary1> <boundary2> ...", file=sys.stderr)
        sys.exit(1)
    try:
        boundaries = [int(x) for x in sys.argv[1:]]
    except ValueError:
        print("Boundaries must be integers", file=sys.stderr)
        sys.exit(1)

    processor = SurveyProcessor(boundaries)
    result = processor.process(sys.stdin)
    print(result)


if __name__ == '__main__':
    main()