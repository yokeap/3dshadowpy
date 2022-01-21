const {
    lightningChart,
    SolidFill,
    ColorRGBA,
    PointStyle3D,
    Themes
} = lcjs

const {
    createWaterDropDataGenerator
} = xydata

// // Create a XY Chart.
// const chart = lightningChart().ChartXY({
//     // Set the chart into a div with id, 'target'. 
//     // Chart's size will automatically adjust to div's size. 
//     container: '3dChart'
// })
//     .setTitle('My first chart') // Set chart title

// const data = [
//     { x: 0, y: 1.52 },
//     { x: 1, y: 1.56 },
//     { x: 2, y: 1.42 },
//     { x: 3, y: 1.85 },
//     { x: 4, y: 1.62 }
// ]

// // Add a line series.
// const lineSeries = chart.addLineSeries()
//     .setName('My data')
//     .add(data)

// Initiate chart
const chart3D = lightningChart().Chart3D({
    disableAnimations: true,
    container: '3dChart'
    // theme: Themes.darkGold
}).setBoundingBox({ x: 1.0, y: 0.5, z: 1.0}).setTitle('3D Scatter Chart')

// Set Axis titles
chart3D.getDefaultAxisX().setTitle('Axis X');
chart3D.getDefaultAxisY().setTitle('Axis Y');
chart3D.getDefaultAxisZ().setTitle('Axis Z');

const pointSeries3D = chart3D.addPointSeries()
    .setPointStyle(new PointStyle3D.Triangulated({
        fillStyle: new SolidFill({ color: ColorRGBA(224, 152, 0) }),
        size: 5,
        shape: 'sphere'
    }))
    .setName('3d-data')

socket.on('3d-data', function (data) {
    var JSON_received = JSON.parse(data);
    pointSeries3D.clear()
    // var test = [JSON_received.ptCloud.x[0], JSON_received.ptCloud.y[0], JSON_received.ptCloud.z[0]];
    // console.log(JSON_received);
    jsonData = 0;
    for (let i = 0; i < (JSON_received.ptCloud.x.length); i++){
        // pointSeries3D.add([JSON_received.ptCloud.x[i], JSON_received.ptCloud.y[i], JSON_received.ptCloud.z[i]]);
        jsonData = {
            x: JSON_received.ptCloud.x[i],
            z: JSON_received.ptCloud.y[i],
            y: JSON_received.ptCloud.z[i]
        } 
        pointSeries3D.add([jsonData]);
    }
    
    chart3D.setTitle("");
    chart3D.setTitle(chart3D.getTitle() + ` (${JSON_received.volume} cm^3)`);
        // Set explicit Y Axis interval.
    // chart3D.getDefaultAxisY().setInterval(0, 150, 2000, true)
});

// // Create Point Series for rendering max Y coords.
// const pointSeriesMaxCoords = chart3D.addPointSeries()
//     .setPointStyle(new PointStyle3D.Triangulated({
//         fillStyle: new SolidFill({ color: ColorRGBA(224, 152, 0) }),
//         size: 10,
//         shape: 'sphere'
//     }))
//     .setName('Max coords')

// // Create another Point Series for rendering other Y coords than Max.
// const pointSeriesOtherCoords = chart3D.addPointSeries()
//     .setPointStyle(new PointStyle3D.Triangulated({
//         fillStyle: new SolidFill({ color: ColorRGBA(255, 0, 0) }),
//         size: 5,
//         shape: 'cube'
//     }))
//     .setName('Below Max')

// // Add LegendBox to chart.
// chart3D.addLegendBox()
//     // Dispose example UI elements automatically if they take too much space. This is to avoid bad UI on mobile / etc. devices.
//     .setAutoDispose({
//         type: 'max-width',
//         maxWidth: 0.30,
//     })
//     .add(chart3D)

// // Generate heatmap data for depicting amount of scattered points along the XZ plane.
// let totalPointsAmount = 0
// const rows = 40
// const columns = 60




// createWaterDropDataGenerator()
//     .setRows( rows )
//     .setColumns( columns )
//     .generate()
//     .then( data => {
//         // 'data' is a number Matrix number[][], that can be read as data[row][column].
//         for ( let row = 0; row < rows; row ++ ) {
//             for ( let column = 0; column < columns; column ++ ) {
//                 const value = data[row][column]
//                 // Generate 'value' amount of points along this XZ coordinate,
//                 // with the Y coordinate range based on 'value'.
//                 const pointsAmount = Math.ceil( value / 100 )
//                 const yMin = 0
//                 const yMax = value
//                 for ( let iPoint = 0; iPoint < pointsAmount; iPoint ++ ) {
//                     const y = yMin + Math.random() * (yMax - yMin)
//                     pointSeriesOtherCoords.add({ x: row, z: column, y })
//                     totalPointsAmount ++
//                 }
//                 pointSeriesMaxCoords.add({ x: row, z: column, y: yMax })
//                 totalPointsAmount ++
//             }
//         }

//         chart3D.setTitle(chart3D.getTitle() + ` (${totalPointsAmount} data points)`)
//         // Set explicit Y Axis interval.
//         chart3D.getDefaultAxisY().setInterval(0, 150, 2000, true)
//     })
