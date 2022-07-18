from constants.names import B_HOUSE, B_VILLAGE, B_ROAD, P_FLAG_STEAL, R_WATER, R_WOOD, R_MINERAL, R_WHEAT

def GET_B_TEMPLATE():
    return {
        B_HOUSE: [],
        B_VILLAGE: [],
        B_ROAD: []
    }

def GET_R_TEMPLATE(): 
    return {
        R_WATER: 0,
        R_WOOD: 0,
        R_MINERAL: 0,
        R_WHEAT: 0
    }

def GET_P_TEMPLATE():
    return {
        P_FLAG_STEAL: 0
    }
