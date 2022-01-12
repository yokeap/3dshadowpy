var sliderObjH = document.getElementById('slider-h-obj')
    ,sliderObjS = document.getElementById('slider-s-obj')
    ,sliderObjV = document.getElementById('slider-v-obj')
    ,sliderShadowH = document.getElementById('slider-h-shadow')
    ,sliderShadowS = document.getElementById('slider-s-shadow')
    ,sliderShadowV = document.getElementById('slider-v-shadow');

const sliderConfig = {
    start: [0.2, 0.8],
    connect: true,
    range: {
        'min': 0,
        'max': 1
    }
}

// const sv_config = {
//     start: [20, 230],
//     connect: true,
//     range: {
//         'min': 0,
//         'max': 1
//     }
// }

noUiSlider.create(sliderObjH, sliderConfig);
noUiSlider.create(sliderObjS, sliderConfig);
noUiSlider.create(sliderObjV, sliderConfig);

noUiSlider.create(sliderShadowH, sliderConfig);
noUiSlider.create(sliderShadowS, sliderConfig);
noUiSlider.create(sliderShadowV, sliderConfig);

// sliderObjH.noUiSlider.on('update', function (values, handle) {
// //    console.log(values);
//     socket.emit('slider-obj-hsv', JSON.stringify({ objH : values }))
// });

// var slider_hsvs = document.querySelectorAll('[type=slider_hsv]');
// console.log(slider_hsvs);
document.querySelectorAll('[type=slider_hsv]').forEach(
    slider_hsv => slider_hsv.noUiSlider.on('update', function(data) {
        switch (slider_hsv.id) {
            case "slider-h-obj": 
                objHsvData.hue.min = data[0];
                objHsvData.hue.max = data[1];
                socket.emit('slider-obj-hsv', JSON.stringify(objHsvData));
                break;
            case "slider-s-obj": 
                objHsvData.saturation.min = data[0];
                objHsvData.saturation.max = data[1];
                socket.emit('slider-obj-hsv', JSON.stringify(objHsvData));
                break;
            case "slider-v-obj": 
                objHsvData.value.min = data[0];
                objHsvData.value.max = data[1];
                socket.emit('slider-obj-hsv', JSON.stringify(objHsvData));
                break;
            case "slider-h-shadow": 
                shadowHsvData.hue.min = data[0];
                shadowHsvData.hue.max = data[1];
                socket.emit('slider-shadow-hsv', JSON.stringify(shadowHsvData));
                break;
            case "slider-s-shadow": 
                shadowHsvData.saturation.min = data[0];
                shadowHsvData.saturation.max = data[1];
                socket.emit('slider-shadow-hsv', JSON.stringify(shadowHsvData));
                break;
            case "slider-v-shadow": 
                shadowHsvData.value.min = data[0];
                shadowHsvData.value.max = data[1];
                socket.emit('slider-shadow-hsv', JSON.stringify(shadowHsvData));
                break;
            default: ;
        }
    })
);

// bootstrap range
function updateSubtractTreshVal(data){
    subtractTreshVal.value = data;
    subtractTreshValText.value = data;
}

function updateImgAndBinTreshold(data){
    imgAndTreshVal.value = data;
    imgAndTreshValText.value = data;
}

function updateMedBlurVal(data){
    medBlurVal.value = data;
    medBlurValText.value = data;
}

function updateObjShadowTreshVal(data){
    objShadowTreshVal.value = data;
    objShadowTreshValText.value = data;
}