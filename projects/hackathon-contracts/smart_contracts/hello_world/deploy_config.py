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
GRID_WIDTH = 5   # number of columns
GRID_HEIGHT = 5  # number of rows


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
            asset_id = result.asset_id
            created_assets[(row, col)] = asset_id
            logger.info(f"Created ASA for pixel ({row},{col}) → Asset ID {asset_id}")

    logger.info(f"✅ Created {len(created_assets)} pixel ASAs successfully.")
    return created_assets


def deploy() -> None:
    """
    AlgoKit-compatible deploy function.
    Will be called automatically via `algokit project deploy`.
    """
    logger.info("=== DEPLOYING PIXEL GRID ASAs ON LOCALNET ===")
    pixel_assets = create_pixel_assets()

    logger.info("=== Deployment complete ===")


if __name__ == "__main__":
    deploy()
    # Launch UI separately when running directly
    app = PixelGrid(rows=GRID_HEIGHT, cols=GRID_WIDTH, pixel_size=25)
    app.mainloop()








# import logging

# import algokit_utils
# from algokit_utils import AlgorandClient

# logger = logging.getLogger(__name__)


# # define deployment behaviour based on supplied app spec
# def deploy() -> None:
#     from smart_contracts.artifacts.hello_world.hello_world_client import (
#         HelloArgs,
#         HelloWorldFactory,
#     )

#     algorand = algokit_utils.AlgorandClient.from_environment()
#     deployer_ = algorand.account.from_environment("DEPLOYER")

#     factory = algorand.client.get_typed_app_factory(
#         HelloWorldFactory, default_sender=deployer_.address
#     )

#     app_client, result = factory.deploy(
#         on_update=algokit_utils.OnUpdate.AppendApp,
#         on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
#     )

#     algorand_client = AlgorandClient.from_environment()
#     random_account = algorand_client.account.random()
#     print(random_account.private_key)

#     algorand.send.payment(
#         algokit_utils.PaymentParams(
#             amount=algokit_utils.AlgoAmount(algo=2),
#             # sender="C43XP3BDMGLHZHTNFJTKB7QCAX3JOX2XT5RFK2TGWPYAVZO3OA3ECZDWWE",
#             sender=deployer_.address,
#             receiver="KIJ4QO2B7IHFJXSBBN2VIALRLCA3XIOFQZZFAWL4H2B3GOAWJ52ENE7NTI"
#             # receiver=app_client.app_address,
#         )
#     )

#     if result.operation_performed in [
#         algokit_utils.OperationPerformed.Create,
#         algokit_utils.OperationPerformed.Replace,
#     ]:
#         algorand.send.payment(
#             algokit_utils.PaymentParams(
#                 amount=algokit_utils.AlgoAmount(algo=1),
#                 sender=deployer_.address,
#                 receiver=app_client.app_address,
#             )
#         )

#     name = "world"
#     response = app_client.send.hello(args=HelloArgs(name=name))
#     logger.info(
#         f"Called hello on {app_client.app_name} ({app_client.app_id}) "
#         f"with name={name}, received: {response.abi_return}"
#         f"app_address={app_client.app_address}"
#     )
