from typing import List, Dict
from app.models.schemas import OEEInput, OEEResult, ProcessStep

class LeanCalculator:
    """
    Service for calculating Lean Manufacturing metrics
    """
    
    @staticmethod
    def calculate_oee(input: OEEInput) -> OEEResult:
        """
        Calculate Overall Equipment Effectiveness (OEE)
        
        OEE = Availability × Performance × Quality
        
        Args:
            input: OEEInput with availability, performance, quality percentages
            
        Returns:
            OEEResult with calculated OEE and recommendations
        """
        # Calculate OEE
        oee = (input.availability / 100) * \
              (input.performance / 100) * \
              (input.quality / 100) * 100
        
        # Analyze losses
        losses = {
            "availability_loss": round(100 - input.availability, 2),
            "performance_loss": round(100 - input.performance, 2),
            "quality_loss": round(100 - input.quality, 2),
            "total_loss": round(100 - oee, 2)
        }
        
        # Generate recommendations
        recommendations = []
        
        if input.availability < 90:
            recommendations.append(
                "🔧 Availability < 90%: Implementar TPM (Total Productive Maintenance) "
                "para reducir paradas no planificadas y tiempos de setup"
            )
        
        if input.performance < 95:
            recommendations.append(
                "⚡ Performance < 95%: Analizar cuellos de botella con Theory of Constraints "
                "y optimizar la velocidad de producción"
            )
        
        if input.quality < 99:
            recommendations.append(
                "✅ Quality < 99%: Implementar Poka-Yoke (error-proofing) y Jidoka "
                "para detectar defectos en origen"
            )
        
        if oee >= 85:
            recommendations.append(
                "🏆 ¡Felicitaciones! Tu OEE está en nivel World-Class (≥85%). "
                "Continúa con mejora continua (Kaizen)"
            )
        elif oee >= 60:
            recommendations.append(
                "📊 OEE Aceptable (60-85%). Enfócate en la pérdida mayor para "
                "alcanzar World-Class"
            )
        else:
            recommendations.append(
                "⚠️ OEE Bajo (<60%). Requiere atención urgente. "
                "Prioriza la dimensión con mayor pérdida"
            )
        
        return OEEResult(
            oee=round(oee, 2),
            world_class=oee >= 85,
            losses=losses,
            recommendations=recommendations
        )
    
    @staticmethod
    def calculate_takt_time(
        available_time_minutes: float,
        customer_demand_units: int
    ) -> Dict:
        """
        Calculate Takt Time
        
        Takt Time = Available Production Time / Customer Demand
        
        Args:
            available_time_minutes: Available production time in minutes
            customer_demand_units: Customer demand in units
            
        Returns:
            Dict with takt time in different units and interpretation
        """
        if customer_demand_units <= 0:
            raise ValueError("Customer demand must be greater than 0")
        
        takt_time_minutes = available_time_minutes / customer_demand_units
        takt_time_seconds = takt_time_minutes * 60
        
        return {
            "takt_time_minutes": round(takt_time_minutes, 2),
            "takt_time_seconds": round(takt_time_seconds, 2),
            "units_per_hour": round(60 / takt_time_minutes, 2),
            "units_per_day": round((available_time_minutes / takt_time_minutes) * (480 / available_time_minutes), 2),
            "interpretation": f"Cada {takt_time_minutes:.2f} minutos ({takt_time_seconds:.1f} segundos) debe completarse una unidad para cumplir con la demanda del cliente"
        }
    
    @staticmethod
    def calculate_lead_time(process_steps: List[dict]) -> Dict:
        """
        Calculate Lead Time from process steps
        
        Lead Time = Sum of all cycle times + wait times
        
        Args:
            process_steps: List of dicts with name, cycle_time, wait_time
            
        Returns:
            Dict with lead time analysis
        """
        total_cycle = sum(step.get("cycle_time", 0) for step in process_steps)
        total_wait = sum(step.get("wait_time", 0) for step in process_steps)
        total_lead = total_cycle + total_wait
        
        value_added_ratio = (total_cycle / total_lead * 100) if total_lead > 0 else 0
        
        # Generate recommendations
        recommendations = []
        if value_added_ratio < 50:
            recommendations.append(
                "⚠️ Menos del 50% del tiempo agrega valor. "
                "Implementar flujo continuo y eliminar esperas"
            )
            recommendations.append(
                "📦 Considerar reducir tamaños de lote para disminuir WIP"
            )
        elif value_added_ratio < 75:
            recommendations.append(
                "📈 Hay oportunidad de mejora. Analizar y reducir tiempos de espera"
            )
        else:
            recommendations.append(
                "✅ Buen flujo de valor. Continuar con Kaizen para optimizar"
            )
        
        # Identify bottleneck
        if process_steps:
            bottleneck = max(process_steps, key=lambda x: x.get("cycle_time", 0))
            recommendations.append(
                f"🎯 Cuello de botella: '{bottleneck['name']}' "
                f"({bottleneck.get('cycle_time', 0)} min)"
            )
        
        return {
            "total_lead_time_minutes": round(total_lead, 2),
            "total_lead_time_hours": round(total_lead / 60, 2),
            "total_cycle_time": round(total_cycle, 2),
            "total_wait_time": round(total_wait, 2),
            "value_added_ratio": round(value_added_ratio, 2),
            "waste_percentage": round(100 - value_added_ratio, 2),
            "process_efficiency": "High" if value_added_ratio >= 75 else "Medium" if value_added_ratio >= 50 else "Low",
            "recommendations": recommendations
        }
    
    @staticmethod
    def calculate_cycle_time_vs_takt(
        cycle_time_minutes: float,
        takt_time_minutes: float
    ) -> Dict:
        """
        Compare cycle time vs takt time
        
        Args:
            cycle_time_minutes: Actual process cycle time
            takt_time_minutes: Required takt time
            
        Returns:
            Analysis of capacity vs demand
        """
        ratio = cycle_time_minutes / takt_time_minutes
        
        if ratio < 1:
            status = "✅ Capacidad suficiente"
            interpretation = (
                f"El proceso es {((1 - ratio) * 100):.1f}% más rápido que el takt time. "
                "Hay capacidad para cumplir la demanda."
            )
        elif ratio == 1:
            status = "⚖️ Balanceado"
            interpretation = "Ciclo y takt time están perfectamente balanceados."
        else:
            status = "⚠️ Capacidad insuficiente"
            interpretation = (
                f"El proceso es {((ratio - 1) * 100):.1f}% más lento que el takt time. "
                "No hay capacidad suficiente para cumplir la demanda."
            )
        
        return {
            "cycle_time": cycle_time_minutes,
            "takt_time": takt_time_minutes,
            "ratio": round(ratio, 3),
            "status": status,
            "interpretation": interpretation,
            "recommendation": (
                "Reducir tiempo de ciclo o aumentar recursos" 
                if ratio >= 1 
                else "Mantener el proceso y considerar reducir inventario"
            )
        }
