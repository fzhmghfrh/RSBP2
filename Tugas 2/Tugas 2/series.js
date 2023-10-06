var daikon = require('daikon');
var fs = require('fs');

var series = new daikon.Series();
// var files = fs.readdirSync('./DICOM/');
var files = fs.readdirSync('./data/volume/');

function toArrayBuffer(buffer) {
    var arrayBuffer = new ArrayBuffer(buffer.length);
    var uint8Array = new Uint8Array(arrayBuffer);
    for (var i = 0; i < buffer.length; i++) {
        uint8Array[i] = buffer[i];
    }
    return arrayBuffer;
}

for (var ctr in files) {
    // var name = './DICOM/' + files[ctr];
    var name = 'data/volume/' + files[ctr];
    var buf = fs.readFileSync(name);
    
    var image = daikon.Series.parseImage(new DataView(toArrayBuffer(buf)));

    if (image === null) {
        console.error(daikon.Series.parserError);
    } else if (image.hasPixelData()) {
        if ((series.images.length === 0) || 
                (image.getSeriesId() === series.images[0].getSeriesId())) {
            series.addImage(image);
        }
    }
}

// order
series.buildSeries();

console.log("Number of images read is " + series.images.length);
console.log("Each slice is " + series.images[0].getCols() + " x " + series.images[0].getRows());
console.log("Each voxel is " + series.images[0].getBitsAllocated() + " bits, " + 
    (series.images[0].littleEndian ? "little" : "big") + " endian");

series.concatenateImageData(null, function (imageData) {
    console.log("Total image data size is " + imageData.byteLength + " bytes");
});