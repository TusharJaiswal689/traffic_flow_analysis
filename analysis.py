
def traffic_delay_ratio(current_speed: float, free_flow_speed: float, road_closure: bool):
    if road_closure:
        return True
    delay_ratio = (current_speed/free_flow_speed).__round__(2)
    # print(f"Delay Ratio: {delay_ratio}")

    if delay_ratio >= 0.75:
        traffic = "Normal"
    elif delay_ratio < 0.75 and delay_ratio >= 0.40:
        traffic = "Slow"
    elif delay_ratio < 0.40 and delay_ratio >= 0.00:
        traffic = "Jam"
    else:
        print("Invalid Delay Ratio. Verify current_speed and free_flow_speed")
        return -1
    print(f"Delay Ratio: {delay_ratio}\nTraffic: {traffic}")
    return delay_ratio
