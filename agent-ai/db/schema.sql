CREATE TABLE IF NOT EXISTS mobiles (
    id INTEGER,
    name TEXT,
    company TEXT,

    rear_camera_mp INTEGER,
    front_camera_mp INTEGER,

    storage_gb INTEGER,
    ram_gb INTEGER,

    battery_mah INTEGER,
    charging_watt INTEGER,
    charging_type TEXT,          -- USB-C, Lightning

    actual_price INTEGER,
    offer_price INTEGER,

    os TEXT,                     -- Android / iOS
    os_version TEXT,

    bluetooth_version TEXT,
    wifi_version TEXT,
    nfc BOOLEAN,

    display_size REAL,
    display_nits INTEGER,
    display_type TEXT,           -- Curved / Flat
    refresh_rate INTEGER,

    reverse_charging BOOLEAN,
    water_resistant BOOLEAN,

    battery_backup TEXT,         -- Poor / Average / Good / Excellent
    design_type TEXT,            -- Plastic / Metal / Glass / Aluminium

    stock INTEGER                -- random below 19
);
