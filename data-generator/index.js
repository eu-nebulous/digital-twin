const mqtt = require('mqtt')
require('dotenv').config();
const { v4: uuidv4 } = require('uuid');

const { generateCoords } = require('./randomCoords')

var isaac = require( 'isaac' );

if (process.env.RANDOM_SEED) {
  isaac.seed(process.env.RANDOM_SEED);
}

const mqtt_options = {
    host: process.env.MQTT_HOST,
    port: process.env.MQTT_PORT,
    username: process.env.MQTT_USER,
    password: process.env.MQTT_PASS
}

// generateCoords();
const data = require("./data.json")
let interval;

if(process.env.RANDOM_INTERVAL_MAX_MS) {
  interval = isaac.random() * process.env.RANDOM_INTERVAL_MAX_MS
} else {
  interval = process.env.INTERVAL
}

const mqttClient  = mqtt.connect(mqtt_options)

function upload(i) {
    process.stdout.clearLine(0);
    process.stdout.cursorTo(0);
    const text = "Progress: " + i + "/" + data[0].data.length + " // Last interval: " + interval + " ms"
    process.stdout.write(text); 

    for (let d of data) {
        if (d.data[i]){
            const ts = new Date().toISOString()
            let dp = {
                "@type": "type.googleapis.com/ttn.lorawan.v3.ApplicationUp",
                "end_device_ids": {
                  "device_id": d.id,
                  "application_ids": {
                    "application_id": "nebulous"
                  },
                  "dev_eui": "70B3D59930001032",
                  "join_eui": "70B3D5993FFFFFB7",
                  "dev_addr": "01684195"
                },
                "correlation_ids": [
                  "gs:uplink:01JA69V1WW63FH96AQHF1AM517",
                  "rpc:/ttn.lorawan.v3.GsNs/HandleUplink:01JA69V1WX00T0GJQDTHT8TQBM",
                  "rpc:/ttn.lorawan.v3.NsAs/HandleUplink:01JA69V23H93VBQAJVPNB9DC1P"
                ],
                "received_at": ts,
                "uplink_message": {
                  "session_key_id": "AY+hVJifpSkwvY5fY+N+TA==",
                  "f_port": 1,
                  "f_cnt": 40776,
                  "frm_payload": "EAD+Cwd4AAAAAD+A",
                  "decoded_payload": {
                    "batteryLevel": 254,
                    "containsGps": true,
                      "gps": {
                          "latitude": d.data[i][0],
                          "longitude": d.data[i][1],
                          "cog": 0,
                          "sog": 0
                      },
                    "containsOnboardSensors": true,
                    "containsSpecial": false,
                    "crc": 0,
                    "lightIntensity": 0,
                    "maxAccelerationHistory": 16.256,
                    "maxAccelerationNew": 0,
                    "sensorContent": {
                      "buttonEventInfo": false,
                      "containsAccelerometerCurrent": false,
                      "containsAccelerometerMax": true,
                      "containsBluetoothData": false,
                      "containsExternalSensors": false,
                      "containsLight": true,
                      "containsTemperature": true,
                      "containsWifiPositioningData": false
                    },
                    "temperature": 19.12,
                    "uplinkReasonButton": false,
                    "uplinkReasonGpio": false,
                    "uplinkReasonMovement": false
                  },
                  "rx_metadata": [
                    {
                      "gateway_ids": {
                        "gateway_id": "lora1",
                        "eui": "FCC23DFFFE0DB1E4"
                      },
                      "time": ts,
                      "timestamp": 1438395915,
                      "rssi": -82,
                      "channel_rssi": -82,
                      "snr": 6.75,
                      "uplink_token": "ChMKEQoFbG9yYTESCPzCPf/+DbHkEIvc8K0FGgsIs/C1uAYQrPvXLyD4tc+47qYB",
                      "received_at": ts
                    }
                  ],
                  "settings": {
                    "data_rate": {
                      "lora": {
                        "bandwidth": 125000,
                        "spreading_factor": 7,
                        "coding_rate": "4/5"
                      }
                    },
                    "frequency": "867100000",
                    "timestamp": 1438395915,
                    "time": ts
                  },
                  "received_at": ts,
                  "consumed_airtime": "0.061696s",
                  "version_ids": {
                    "brand_id": "iothings",
                    "model_id": "iotracker3",
                    "hardware_version": "3",
                    "firmware_version": "1.10",
                    "band_id": "EU_863_870"
                  },
                  "network_ids": {
                    "net_id": "000000"
                  }
                }
              }

            mqttClient.publish('nbls/lora/up', JSON.stringify(dp))
        }
    }
    if (data[0].data.length > i) {
      if(process.env.RANDOM_INTERVAL_MAX_MS) {
        interval = isaac.random() * process.env.RANDOM_INTERVAL_MAX_MS
      }
      setTimeout(upload, interval, i+1);
    } else {
        process.stdout.write("\n"); 
        console.log("Upload complete")
        process.exit()
    }
}

console.log("starting data upload at",interval,"ms interval for", data.length,"sensors with", data[0].data.length, "iterations.")
upload(0);
