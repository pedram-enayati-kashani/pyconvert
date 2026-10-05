from sorl.thumbnail.engines.pil_engine import Engine
from PIL import Image as PILImage
from Admin_panel.helpers.client.watermark import get_watermark


class WatermarkEngine(Engine):

    def create(self, image, geometry, options):

        image = super().create(image, geometry, options)

        if options.get('watermark'):
            image = self.add_watermark(image)

        return image

    def get_watermark_setting(self):
        return get_watermark()


    def add_watermark(self, image):

        if not isinstance(image, PILImage.Image):
            image = PILImage.open(image)

        image = image.convert("RGBA")

        watermark_setting = self.get_watermark_setting()

        if not watermark_setting or not watermark_setting.image:
            return image.convert("RGB")

        try:
            watermark = PILImage.open(
                watermark_setting.image.path
            ).convert("RGBA")
        except Exception:
            return image.convert("RGB")

        opacity = watermark_setting.opacity or 70
        padding = watermark_setting.padding or 10

        # ===== opacity =====
        alpha = watermark.getchannel("A")
        alpha = alpha.point(lambda p: int(p * (opacity / 100)))
        watermark.putalpha(alpha)

        # ===== size =====
        wm_width = watermark.width
        wm_height = watermark.height

        if watermark_setting.width_mode == "auto":
            percent = watermark_setting.width_percent or 20
            wm_width = int(image.width * percent / 100)
            ratio = wm_width / watermark.width
            wm_height = int(watermark.height * ratio)

        elif watermark_setting.width_mode == "manual" and watermark_setting.manual_width:
            wm_width = watermark_setting.manual_width
            ratio = wm_width / watermark.width
            wm_height = int(watermark.height * ratio)

        watermark = watermark.resize((wm_width, wm_height), PILImage.LANCZOS)

        # ===== position =====
        position_map = {
            "top-left": (padding, padding),
            "top-center": ((image.width - watermark.width) // 2, padding),
            "top-right": (image.width - watermark.width - padding, padding),

            "center-left": (
                padding,
                (image.height - watermark.height) // 2
            ),
            "center": (
                (image.width - watermark.width) // 2,
                (image.height - watermark.height) // 2
            ),
            "center-right": (
                image.width - watermark.width - padding,
                (image.height - watermark.height) // 2
            ),

            "bottom-left": (padding, image.height - watermark.height - padding),
            "bottom-center": ((image.width - watermark.width) // 2, image.height - watermark.height - padding),
            "bottom-right": (image.width - watermark.width - padding, image.height - watermark.height - padding),
        }

        position = position_map.get(
            watermark_setting.position,
            position_map["bottom-right"]
        )

        # Make sure the watermark position stays inside the image boundaries.
        x, y = position
        x = max(0, min(x, image.width - watermark.width))
        y = max(0, min(y, image.height - watermark.height))
        position = (x, y)

        transparent = PILImage.new('RGBA', image.size, (0, 0, 0, 0))
        transparent.paste(image, (0, 0))
        transparent.paste(watermark, position, mask=watermark)

        return transparent.convert("RGB")
