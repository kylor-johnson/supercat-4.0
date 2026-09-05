"""Path -> iPad unit mapping for supercat_server spike/ecat-web files.

Shared by p3_spike.py (Phase 3 spike_status) and p6_calibration.py (Phase 6).
Ordered; first substring match wins. Every entry is a claim that can be checked
by opening the file.
"""

MAP = [
    ("ecat_customer_picker", "Customer"),
    ("ecat/customer_picker", "Customer"),
    ("ecat_order_process", "Order related"),
    ("ecat_saved_orders", "Order related"),
    ("ecat/park_cart_order", "Order related"),
    ("ecat/restore_saved_order", "Order related"),
    ("ecat_order_contextable", "Order related"),
    ("ecat/order_context", "Order related"),
    ("matrix_grid_presenter", "Kit/Options related"),
    ("_matrix_grid", "Kit/Options related"),
    ("kit_item_options_inline", "Kit/Options related"),
    ("kit_options_inline", "Kit/Options related"),
    ("product_options_inline", "Kit/Options related"),
    ("builds_unit_price", "Pricing"),
    ("product_price_labels", "Pricing"),
    ("pdp_presenter", "SingleItemView related"),
    ("pdp_detail_fields", "SingleItemView related"),
    ("pdp_product_card_collection", "SingleItemView related"),
    ("ecat_products/show", "SingleItemView related"),
    ("catalog_page_presenter", "Grid view related"),
    ("catalog_product_presenter", "Grid view related"),
    ("ecat_products", "Grid view related"),
    ("resolve_scan", "Scan Groups"),
    ("shell_browse_sections", "Left Nav"),
    ("shell_presenter", "Left Nav"),
    ("layouts/ecat", "Left Nav"),
    ("ecat_ui_switchable", "Left Nav"),
    ("ecat_online_controller", "Organization chooser"),
    ("vendor/design_system", "Custom UI controls"),
    ("ecat_ds.css", "Custom UI controls"),
    ("ecat_v2.css", "Custom UI controls"),
    ("postcss-ecat", "Custom UI controls"),
    ("app/components", "Custom UI controls"),
    ("app/javascript", "Custom UI controls"),
]

CATEGORY = [
    ("docs/design", "DESIGN_DOCS"),
    ("docs/superpowers", "DESIGN_DOCS"),
    ("test/", "TESTS"),
    ("db/", "SCHEMA"),
    ("config/", "CONFIG"),
    ("package", "BUILD"),
    ("yarn.lock", "BUILD"),
]
