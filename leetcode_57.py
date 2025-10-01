class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        output = []

        newStart = newInterval[0]
        newEnd = newInterval[1]

        i = 0
        n = len(intervals)

        # Add all intervals that come before the new interval
        while i < n and newStart > intervals[i][0]:
            output.append(intervals[i])
            i += 1

        # Merge newInterval with the last interval in output if necessary
        if not output or output[-1][1] < newStart:
            output.append(newInterval)
        else:
            output[-1][1] = max(output[-1][1], newEnd)

        # Add remaining intervals, merging if necessary
        while i < n:
            start, end = intervals[i]

            if output[-1][1] < start:
                output.append([start, end])
            else:
                output[-1][1] = max(output[-1][1], end)
            i += 1

        return output
