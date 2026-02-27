"""
递归排序算法实现
包含：归并排序、快速排序、堆排序
"""


# ─────────────────────────────────────────────
# 归并排序 O(n log n)
# ─────────────────────────────────────────────
def merge_sort(arr: list) -> list:
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)


def _merge(left: list, right: list) -> list:
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# ─────────────────────────────────────────────
# 快速排序 O(n log n) 平均
# ─────────────────────────────────────────────
def quick_sort(arr: list, low: int = 0, high: int = None) -> list:
    if high is None:
        high = len(arr) - 1
    if low < high:
        pivot_idx = _partition(arr, low, high)
        quick_sort(arr, low, pivot_idx - 1)
        quick_sort(arr, pivot_idx + 1, high)
    return arr


def _partition(arr: list, low: int, high: int) -> int:
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


# ─────────────────────────────────────────────
# 堆排序 O(n log n)
# ─────────────────────────────────────────────
def heap_sort(arr: list) -> list:
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        _heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        _heapify(arr, i, 0)
    return arr


def _heapify(arr: list, n: int, i: int):
    largest = i
    left, right = 2 * i + 1, 2 * i + 2
    if left < n and arr[left] > arr[largest]:
        largest = left
    if right < n and arr[right] > arr[largest]:
        largest = right
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        _heapify(arr, n, largest)


# ─────────────────────────────────────────────
# 测试
# ─────────────────────────────────────────────
if __name__ == "__main__":
    import random

    data = random.sample(range(1, 101), 10)
    print(f"原始数据:   {data}")
    print(f"归并排序:   {merge_sort(data[:])}")
    print(f"快速排序:   {quick_sort(data[:])}")
    print(f"堆排序:     {heap_sort(data[:])}")
