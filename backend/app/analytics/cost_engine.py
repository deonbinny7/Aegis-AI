from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.provider_pricing import ProviderPricing
import structlog

logger = structlog.get_logger(__name__)

class CostEngine:
    @staticmethod
    async def calculate_cost(
        db: AsyncSession, 
        provider: str, 
        model_name: str, 
        prompt_tokens: int, 
        completion_tokens: int
    ) -> float:
        """
        Calculates the cost of a request based on provider pricing data.
        Falls back to 0.0 if pricing is not found.
        """
        try:
            result = await db.execute(
                select(ProviderPricing)
                .where(ProviderPricing.provider == provider, ProviderPricing.model_name == model_name)
                .order_by(ProviderPricing.version.desc())
                .limit(1)
            )
            pricing = result.scalar_one_or_none()
            
            if not pricing:
                logger.warning("CostEngine: No pricing found", provider=provider, model=model_name)
                return 0.0

            input_cost = (prompt_tokens / 1000.0) * pricing.input_price_per_token
            output_cost = (completion_tokens / 1000.0) * pricing.output_price_per_token
            total_cost = input_cost + output_cost
            
            return round(total_cost, 6)
        except Exception as e:
            logger.error("CostEngine: Error calculating cost", error=str(e))
            return 0.0
