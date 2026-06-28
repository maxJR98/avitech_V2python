from app.models.modelos_db import TiposAve, ParametrosNutricionales

def calculate_feed_and_water(genetic_line_name, weeks, birds):
    # 1. Buscamos el ave
    tipo = TiposAve.query.filter(TiposAve.nombre_tipo.ilike(f'%{genetic_line_name}%')).first()
    
    if not tipo:
        return {'error': 'Ave no encontrada. Intenta con: Pollo de Engorde, Gallina Ponedora, etc.'}
    
    # 2. Intentamos buscar el dato EXACTO en la base de datos
    parametro_exacto = ParametrosNutricionales.query.filter_by(id_tipo_ave=tipo.id_tipo_ave, id_etapa=weeks).first()
    
    try:
        if parametro_exacto:
            # Si el dato existe, usamos la información real de la BD
            total_feed = float(parametro_exacto.consumo_alimento_gr_dia) * birds / 1000
            total_water = float(parametro_exacto.consumo_agua_ml_dia) * birds / 1000
            tipo_calculo = "Dato de tabla exacto"
            
        else:
            # 3. ¡LA CALCULADORA ENTRA EN ACCIÓN!
            # Buscamos el primer registro que exista de esta ave para usarlo como base
            parametro_base = ParametrosNutricionales.query.filter_by(id_tipo_ave=tipo.id_tipo_ave).order_by(ParametrosNutricionales.id_etapa.asc()).first()
            
            if not parametro_base:
                return {'error': 'No hay datos base registrados para crear un patrón.'}
                
            # PATRÓN MATEMÁTICO: Asumimos un crecimiento del 15% (0.15) de consumo por cada semana extra.
            # Puedes cambiar este 0.15 al porcentaje que creas más realista.
            semanas_diferencia = weeks - parametro_base.id_etapa
            factor_crecimiento = 1 + (0.15 * semanas_diferencia)
            
            consumo_alimento_estimado = float(parametro_base.consumo_alimento_gr_dia) * factor_crecimiento
            consumo_agua_estimado = float(parametro_base.consumo_agua_ml_dia) * factor_crecimiento
            
            total_feed = consumo_alimento_estimado * birds / 1000
            total_water = consumo_agua_estimado * birds / 1000
            tipo_calculo = "Cálculo automático por patrón"

    except Exception as e:
        return {'error': f'Error interno al calcular: {str(e)}'}

    return {
        'genetic_line': tipo.nombre_tipo,
        'week': weeks,
        'birds': birds,
        'daily_feed_kg': round(total_feed, 2),
        'daily_water_l': round(total_water, 2),
        'feed_phase': f'Etapa {weeks} ({tipo_calculo})' 
    }

def get_feed_phase(weeks):
    return None 