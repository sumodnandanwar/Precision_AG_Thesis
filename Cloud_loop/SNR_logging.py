import logging
import csv
import routeros
import time
import datetime

logger = logging.getLogger('scope.name')
logger.setLevel('DEBUG')
curr_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')
file_log_handler = logging.FileHandler('logs/output_' + curr_time + '.log')
logger.addHandler(file_log_handler)
stdout_log_handler = logging.StreamHandler()
logger.addHandler(stdout_log_handler)
formatter = logging.Formatter('%(asctime)s - %(message)s')
file_log_handler.setFormatter(formatter)
stdout_log_handler.setFormatter(formatter)
csvfile = open(f"logs/SNR_log_{curr_time}.csv", 'w', newline='')
logwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
# logwriter.writerow(["Drone", "Latitude", "Longitude", "Relative Altitude", "Distance (from resupply point)","Signal Strength"])
accesspoint_ip  = "192.168.120.5"

try:
    accessPoint = routeros.RouterOS(accesspoint_ip, logger=logger)
    logger.info(accessPoint)
except Exception as e:
    accessPoint = None
    logger.info("WARNING: Access point not accessible, " + str(e))

printed = False

while True:
    if not printed:
        print("Logging in process")
        printed = True
    try:
        if accessPoint is not None:
            measurements = \
            accessPoint.getWiFiRegisteredClientsMeasurements()#filterByMac="48:8F:5A:E6:9A:DF"
            # print (measurements)
            if measurements is None:
                logwriter.writerow("No signal")


        if measurements is not None:
            device_measurement = measurements[0]
            signal_strength = device_measurement['=signal-strength']
            SNR_val = device_measurement['=signal-to-noise']
            curr_time = datetime.datetime.now().strftime('%H_%M_%S_%f')
            logwriter.writerow(curr_time +";"+ SNR_val + ";" + signal_strength )
            

        else:
            signal_strength = 'None'
    except Exception as e: 
        signal_strength = 'None'
    time.sleep(0.3)

# measurements return this
# {'=.id': '*4', '=interface': 'wlan2', '=mac-address': '14:AB:C5:C2:02:D1', '=ap': 'false', '=wds': 'false', '=bridge': 'false', '=rx-rate': '54Mbps',
#  '=tx-rate': '54Mbps', '=packets': '3031,3113', '=bytes': '200913,247415',
#  '=frames': '3031,3117', '=frame-bytes': '206971,229406', '=hw-frames': '3253,3294', '=hw-frame-bytes': '301909,358302', '=tx-frames-timed-out': '0',
#  '=uptime': '4m2s', '=last-activity': '0ms', '=signal-strength': '-43@6Mbps', '=signal-to-noise': '63', '=signal-strength-ch0': '-45',
#  '=signal-strength-ch1': '-51', '=strength-at-rates': '-35@1Mbps 1m41s900ms,
# -35@2Mbps 1m40s20ms,-35@5.5Mbps 1m40s130ms,-35@11Mbps 1m39s770ms,-43@6Mbps 550ms,-39@12Mbps 1m39s760ms,-37@18Mbps 1m39s760ms,
# -42@24Mbps 2s760ms,-41@36Mbps 2s780ms,-51@48Mbps 2s760ms,-58@54Mbps 0ms', '=tx-ccq': '100', '=p-throughput': '29718', '=distance': '44',
#  '=last-ip': '192.168.120.49', '=802.1x-port-enabled': 'true', '=authentication-type': 'wpa2-psk', '=encryption': 'aes-ccm', 
# '=group-encryption': 'aes-ccm', '=management-protection': 'false', '=wmm-enabled': 'false', '=tx-rate-set': 'CCK:1-11 OFDM:6-54'}