let turf = require('@turf/turf')
const fs = require('node:fs');
require('dotenv').config();
const { v4: uuidv4 } = require('uuid');

var isaac = require( 'isaac' );

if (process.env.COORD_SEED) {
  isaac.seed(process.env.COORD_SEED);
}

const startCoords = [53.1107071,8.8557395]

function getNextRandom(start) {
    // console.log("Start:", start)

    let startGeoJson = turf.point(start);

    let bearing = Math.floor(isaac.random() * 360)
    // console.log("Bearing:", bearing)
    
    let distance = Math.floor(isaac.random() * process.env.MAX_STEP)
    // console.log("Distance:", distance)

    return turf.transformTranslate(startGeoJson,distance,bearing,{units:'meters'})
}
 

function getRandomArray(start, length) {
    let array = []
    array.push(start)
    for (let i=0; i<length-1; i++) {
        array.push(getNextRandom(array[i]).geometry.coordinates)
    }
    return array
}

function swapLatLng(input) {
    let out = [input[1],input[0]]
    return out
}

function createDemoDataset(start, devices, points) {
    console.log('generating coords.',start,devices,points)
    let jsonOutput = []
    for (let i=0; i<devices; i++) {
        let deviceObj = {
            id: uuidv4(),
            data: getRandomArray(start, points)
        }
        jsonOutput.push(deviceObj)
    }
    fs.writeFileSync('./data.json', JSON.stringify(jsonOutput))
}

exports.generateCoords = createDemoDataset(startCoords, process.env.DEVICES , process.env.ITERATIONS)

// JSON.stringify(createDemoDataset(startCoords, process.env.DEVICES , process.env.ITERATIONS))