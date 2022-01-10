var sliderObjH = document.getElementById('slider-h-obj')
    ,sliderObjS = document.getElementById('slider-s-obj')
    ,sliderObjV = document.getElementById('slider-v-obj')
    ,sliderShadowH = document.getElementById('slider-h-shadow')
    ,sliderShadowS = document.getElementById('slider-s-shadow')
    ,sliderShadowV = document.getElementById('slider-v-shadow');

const h_config = {
    start: [20, 330],
    connect: true,
    range: {
        'min': 0,
        'max': 360
    }
}

const sv_config = {
    start: [20, 230],
    connect: true,
    range: {
        'min': 0,
        'max': 255
    }
}

noUiSlider.create(sliderObjH, h_config);
noUiSlider.create(sliderObjS, sv_config);
noUiSlider.create(sliderObjV, sv_config);

noUiSlider.create(sliderShadowH, h_config);
noUiSlider.create(sliderShadowS, sv_config);
noUiSlider.create(sliderShadowV, sv_config);

sliderObjH.noUiSlider.on('update', function (values, handle) {
//    console.log(values);
    socket.emit('slider-obj-hsv', JSON.stringify({ objH : values }))
});
