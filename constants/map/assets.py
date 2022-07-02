from constants.names import B_HOUSE, B_ROAD, B_VILLAGE, OG_AVARI, OG_KELGRAS, OG_LEVIATHAN, OG_THERON

MAP_OG_COLORS = {
    OG_AVARI: 'Yellow',
    OG_KELGRAS: 'Green',
    OG_LEVIATHAN: 'Blue',
    OG_THERON: 'Black'
}

def filename_gen(og):
    color = MAP_OG_COLORS[og]
    return {
        B_ROAD: color + 'Door.png',
        B_HOUSE: color + 'Flag.png',
        B_VILLAGE: color + 'Banner.png'
    }

MAP_ASSET_FILENAMES = {
    OG_AVARI: filename_gen(OG_AVARI),
    OG_KELGRAS: filename_gen(OG_KELGRAS),
    OG_LEVIATHAN: filename_gen(OG_LEVIATHAN),
    OG_THERON: filename_gen(OG_THERON)
}