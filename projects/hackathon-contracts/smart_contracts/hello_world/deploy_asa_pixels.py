import logging
from algokit_utils import AlgorandClient, AssetCreateParams
from pixel_grid import PixelGrid

# --- Configure logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# --- Config ---
GRID_WIDTH = 10   # number of columns
GRID_HEIGHT = 10  # number of rows


def create_pixel_assets(rows=GRID_HEIGHT, cols=GRID_WIDTH):
    """Create ASA assets for each pixel (x,y) on LocalNet."""
    algorand = AlgorandClient.from_environment()
    deployer = algorand.account.from_environment("DEPLOYER")

    logger.info(f"Using LocalNet deployer: {deployer.address}")
    created_assets = {}

    for row in range(rows):
        for col in range(cols):
            coord_name = f"{row}x{col}"
            unit_name = coord_name[:8]          # ≤8 chars
            asset_name = f"Pixel_{coord_name}"  # ≤32 chars

            params = AssetCreateParams(
                sender=deployer.address,
                total=1,
                decimals=0,
                default_frozen=False,
                unit_name=unit_name,
                asset_name=asset_name,
                url="http://localhost",
            )

            result = algorand.send.asset_create(params)
            asset_id = result["confirmation"]["asset-index"]
            created_assets[(row, col)] = asset_id
            logger.info(f"✅ Created ASA for pixel ({row},{col}) → Asset ID {asset_id}")

    logger.info(f"✅ Created {len(created_assets)} pixel ASAs successfully.")
    return created_assets


if __name__ == "__main__":
    logger.info("=== DEPLOYING PIXEL GRID ASAs ON LOCALNET ===")
    pixel_assets = create_pixel_assets()

    logger.info("=== LAUNCHING PIXEL GRID UI ===")
    app = PixelGrid(rows=GRID_HEIGHT, cols=GRID_WIDTH, pixel_size=25, pixel_assets=pixel_assets)
    app.mainloop()
