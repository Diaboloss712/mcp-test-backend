import hashlib

def hash_problem_ids(problem_ids: list[int]) -> str:
    sorted_ids = sorted(problem_ids)
    id_string = ",".join(str(i) for i in sorted_ids)
    return hashlib.sha256(id_string.encode()).hexdigest()
