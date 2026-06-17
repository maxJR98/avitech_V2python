from math import radians, sin, cos, sqrt, atan2
from app.models import Branch

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

def get_nearby_branches(lat, lon, limit=5):
    branches = Branch.query.filter_by(is_active=True).all()
    distances = []
    for branch in branches:
        dist = calculate_distance(lat, lon, branch.latitude, branch.longitude)
        distances.append((branch, dist))
    distances.sort(key=lambda x: x[1])
    return distances[:limit]