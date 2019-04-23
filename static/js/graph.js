d3.queue()
    .defer(d3.json, "/get_recipes")
    .await(makeGraphs);


function makeGraphs(error, recipeData) {
    var ndx = crossfilter(recipeData);
    console.log(recipeData);
    show_category_selector(ndx);
    show_category_graph(ndx);

    show_course_graph(ndx);
    show_cuisine_graph(ndx);
    show_author_graph(ndx);

    dc.renderAll();
}


function show_category_selector(ndx) {
    var categorySelectorDim = ndx.dimension(dc.pluck("category"));
    var categorySelectorSelect = categorySelectorDim.group();

    dc.selectMenu("#category-selector")
        .dimension(categorySelectorDim)
        .group(categorySelectorSelect);
}

function show_category_graph(ndx) {
    var categoryDim = ndx.dimension(dc.pluck("category"));
    var categoryMix = categoryDim.group();

    dc.barChart("#category-graph")
        .width(350)
        .height(250)
        .margins({top: 20, right: 20, bottom: 30, left: 10})
        .dimension(categoryDim)
        .group(categoryMix)
        .transitionDuration(500)
        .x(d3.scale.ordinal())
        .xUnits(dc.units.ordinal)
        .elasticY(true)
        .xAxisLabel("Category")
        .yAxis().tickFormat(d3.format("d"));

}

function show_cuisine_graph(ndx) {
    var cuisineDim = ndx.dimension(dc.pluck("cuisine"));
    var cuisineMix = cuisineDim.group();

    dc.rowChart("#cuisine-graph")
        .width(350)
        .height(250)
        .margins({top: 20, right: 20, bottom: 20, left: 10})
        .dimension(cuisineDim)
        .group(cuisineMix)
//        .transitionDuration(500)
        .rowsCap(20)
        .elasticX(true)
        .renderLabel(false)
        .renderTitleLabel(true)
        .titleLabelOffsetX(80)
        .xAxis().ticks(8);

}

function show_course_graph(ndx) {
    var courseDim = ndx.dimension(dc.pluck("course"));
    var courseMix = courseDim.group();

    var coursePieChart = dc.pieChart("#course-graph");

    coursePieChart
        .width(350)
        .height(250)
        .dimension(courseDim)
        .group(courseMix)
        .innerRadius(50)
        .transitionDuration(1500)
        .legend(dc.legend());
          // example of formatting the legend via svg
          // http://stackoverflow.com/questions/38430632/how-can-we-add-legends-value-beside-of-legend-with-proper-alignment
          coursePieChart.on('pretransition', function(coursePieChart) {
            coursePieChart.selectAll('.dc-legend-item text')
                  .text('')
                .append('tspan')
                  .text(function(d) { return d.name; })
                .append('tspan')
                  .attr('x', 100)
                  .attr('text-anchor', 'end')
                  .text(function(d) { return d.data; });
          });

}

function show_category_graph(ndx) {
    var categoryDim = ndx.dimension(dc.pluck("category"));
    var categoryMix = categoryDim.group();

    dc.barChart("#category-graph")
        .width(350)
        .height(250)
        .margins({top: 20, right: 20, bottom: 30, left: 10})
        .dimension(categoryDim)
        .group(categoryMix)
        .transitionDuration(500)
        .x(d3.scale.ordinal())
        .xUnits(dc.units.ordinal)
        .elasticY(true)
        .xAxisLabel("Category")
        .yAxis().tickFormat(d3.format("d"));

}function show_author_graph(ndx) {
    var authorDim = ndx.dimension(dc.pluck("author"));
    var authorMix = authorDim.group();

    dc.barChart("#author-graph")
        .width(400)
        .height(250)
        .margins({top: 20, right: 20, bottom: 30, left: 10})
        .dimension(authorDim)
        .group(authorMix)
        .transitionDuration(500)
        .x(d3.scale.ordinal())
        .xUnits(dc.units.ordinal)
        .elasticY(true)
        .xAxisLabel("Author")
        .yAxis().tickFormat(d3.format("d"));

}
