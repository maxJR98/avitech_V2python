from app.models import GeneticLine, GrowthTable, FeedPhase

def calculate_feed_and_water(genetic_line_name, weeks, birds):
    line = GeneticLine.query.filter_by(name=genetic_line_name).first()
    if not line:
        return {'error': 'Línea genética no encontrada'}
    table = GrowthTable.query.filter_by(genetic_line_id=line.id, week=weeks).first()
    if not table:
        return {'error': 'Datos no disponibles para esa semana'}
    total_feed = table.daily_feed_grams * birds / 1000
    total_water = table.daily_water_ml * birds / 1000
    return {
        'genetic_line': genetic_line_name,
        'week': weeks,
        'birds': birds,
        'daily_feed_kg': round(total_feed, 2),
        'daily_water_l': round(total_water, 2),
        'weight_kg': table.weight_kg
    }

def get_feed_phase(weeks):
    phase = FeedPhase.query.filter(FeedPhase.min_week <= weeks, FeedPhase.max_week >= weeks).first()
    return phase.name if phase else None