from constants.names import B_HOUSE, B_ROAD, B_VILLAGE

KEY_NAME = 'bName'
KEY_OWNER = 'bOwner'
KEY_C = 'bC'
KEY_CONNECTED = 'bConnected'

B_POINTS = {
    B_ROAD: 0,
    B_HOUSE: 1,
    B_VILLAGE: 2
}

#(own, [others])
B_RATIOS = {
    B_ROAD: (30, [10]),
    B_HOUSE: (40, [10, 10]),
    B_VILLAGE: (50, [20, 20, 10])
}