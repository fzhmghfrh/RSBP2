var daikon = require('daikon');
var fs = require('fs');

var series = new daikon.Series();
// var files = fs.readdirSync('C:/Users/HP/Downloads/Daikon-master/Daikon-master/tests/data/volume/');
var files = fs.readdirSync('C:/Users/HP/Documents/kuliah/SEMESTER 5/RSBP/Asistensi/Tugas 1/Phantoms/Manekin-01/A/');
// var files = fs.readdirSync('C:/Users/HP/Documents/kuliah/SEMESTER 5/RSBP/Asistensi/Tugas 1/2_skull_ct/DICOM/');
// var files = fs.readdirSync('./DICOM/');
// var files = fs.readdirSync('./data/volume/');

function toArrayBuffer(buffer) {
    var arrayBuffer = new ArrayBuffer(buffer.length);
    var uint8Array = new Uint8Array(arrayBuffer);
    for (var i = 0; i < buffer.length; i++) {
        uint8Array[i] = buffer[i];
    }
    return arrayBuffer;
}

function applyWWWC(
    array,
    
    WWWC
) {
    
    const appliedArray = new Float32Array(512 * 512);
    const size = 512 * 512 ;
    
    for (let i = 0; i < size; i++) {
        const newValue = ((array[i] - (WWWC[1] - 0.5)) / WWWC[0] + 0.5) * 255;
        console.log(newValue);
        if (newValue > 255 || newValue < 0) appliedArray[i] = 0;
        else appliedArray[i] = newValue;
    }
    return appliedArray;
}

// terserah

for (var ctr in files) {
    // var name = 'C:/Users/HP/Downloads/Daikon-master/Daikon-master/tests/data/volume/' + files[ctr];
    var name = 'C:/Users/HP/Documents/kuliah/SEMESTER 5/RSBP/Asistensi/Tugas 1/Phantoms/Manekin-01/A/' + files[ctr];
    // var name = 'C:/Users/HP/Documents/kuliah/SEMESTER 5/RSBP/Asistensi/Tugas 1/2_skull_ct/DICOM/' + files[ctr];
    // var name = './DICOM/' + files[ctr];
    // var name = 'data/volume/' + files[ctr];
    var buf = fs.readFileSync(name);
    
    var image = daikon.Series.parseImage(new DataView(toArrayBuffer(buf)));

    if (image.getRows() != 512) continue

    if (image === null) {
        console.error(daikon.Series.parserError);
        console.log("Image loaded unsuccessfully from file: " + name);
    } else if (image.hasPixelData()) {
        if ((series.images.length === 0) || 
                (image.getSeriesId() === series.images[0].getSeriesId())) {
            series.addImage(image);
            console.log("------------------------");
            console.log("Image loaded successfully from file: " + name);
            console.log("Slice " + ctr + ":");
            console.log("Dimensions: " + image.getRows() + " x " + image.getCols());
            applyWWWC(image.getInterpretedData(), [500,1000]);
            console.log(image.getInterpretedData());
        }
    }
}

// order
series.buildSeries();

console.log("\n------------------------\n");
console.log("Number of images read is " + series.images.length);
// console.log("Each slice is " + series.images[0].getCols() + " x " + series.images[0].getRows());
// console.log("Each voxel is " + series.images[0].getBitsAllocated() + " bits, " + 
//     (series.images[0].littleEndian ? "little" : "big") + " endian");

// series.concatenateImageData(null, function (imageData) {
//     console.log("Total image data size is " + imageData.byteLength + " bytes");
// });