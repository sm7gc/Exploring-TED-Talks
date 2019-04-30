var width = 600,
    height = 600;

var pack = d3.pack()
    .size([width, height])
    .padding(10);

var color = d3.scaleSequential(d3.interpolateViridis);


var datajson, data, years, events, root, nodes;

function changeLabel(year_i) {
    if (year_i <= years.length) {
        $("#slider-label").html(years[year_i - 1]);
    } else {
        $("#slider-label").html("All");
    }
}

function getData(year_i = 0) {

    d3.json("ted-talks.json").then(function (d) {

        datajson = d;

        console.log(datajson);

        if (year_i > 0 && year_i <= years.length) {

            datajson = datajson.filter(function (d) {
                return d.year_filmed == years[year_i - 1];
            });

        } else {

            years = d3.map(datajson, function (d) {
                return d.year_filmed;
            }).keys().sort();

            $('#slider').prop({
                'min': 1,
                'max': years.length + 1,
                'step': 1
            });

            $.each(years, function (i, y) {
                $("#slider-vals").append($("<option>").attr('value', i).text(y));
            });

            $("#slider-vals").append($("<option>").attr('value', years.length).text("All"));

        }

        events = d3.map(datajson, function (d) {
            return d.event;
        }).keys();

        var nestedData = d3.nest()
            .key(function (d) {
                return d["event"];
            })
            .rollup(function (d) {
                return d3.sum(d, function (d) {
                    return 1;
                })
            })
            .entries(datajson);

        data = {
            "name": "ted-talks",
            "children": nestedData
        };

        packNodes();

        $("#dashboard").fadeIn("fast");
    });
}

function packNodes() {

    $("#chart").empty();

    root = d3.hierarchy(data)
        .sum(function (d) {
            return d.value
        });

    nodes = root.descendants();
    pack(root);

    drawNodes(nodes);
}

function drawNodes(nodes) {
    color.domain([0, events.length - 1]);

    var chart = d3.select("#chart")
        .attr("width", width)
        .attr("height", height);

    var node = chart.selectAll("g")
        .data(nodes);

    var g = node.enter()
        .append("g")
        .on("click", function (d, i) {
            expandEvent(d, i, d3.select(this));
        })
        .attr("transform", function (d) {
            return "translate(" + d.x + "," + d.y + ")";
        });

    g.append("circle")
        .on("mouseover", function (d, i) {
            if (i == 0) return;
            d3.selectAll("circle")
                .transition().duration(200)
                .attr("stroke", function (dat, ind) {
                    if (ind == i) {
                        return "black";
                    }
                })
                .style("opacity", function (dat, ind) {
                    if (ind == i) {
                        return 1;
                    } else {
                        return 0.5;
                    }
                });

            var event_desc = eventDetails(d.data.key);

            $("#event-title").text(d.data.key);
            $("#event-subtitle").text(event_desc.subtitle);
            $("#event-text").html(event_desc.text);


        })
        .on("mouseout", function (d, i) {
            d3.selectAll("circle")
                .transition().duration(200)
                .attr("stroke", "none")
                .style("opacity", 1);


            $("#event-title").text("Description");
            $("#event-subtitle").text("");
            $("#event-text").html("");
        })
        .attr('r', 0)
        .transition().duration(750)
        .attr("r", function (d) {
            return d.r;
        })
        .attr("fill", function (d) {
            if (d.data["key"] != null) {
                return color(events.indexOf(d.data["key"]));
            } else {
                return "white";
            }
        });

    g.append("text")
        .text(function (d) {
            if (d.r > 70) {
                if (d.data.key) {
                    if (d.data.key.length < 14) return d.data.key;
                }
            }
        })
        .attr("font-size", function (d) {
            return Math.min(Math.max(d.r, 10), 24);
        });
}

// Create HTML-formatted description of event
function eventDetails(event) {

    var sub = "";

    var eventjson = datajson.filter(function (d) {
        return d.event == event;
    });

    var talks = d3.map(eventjson, function (d) {
        return d.headline;
    }).keys();

    sub += talks.length + " talks";

    return {
        "subtitle": sub,
        "text": ""
    };

}

function expandEvent(d, i, clicked) {
    var event = d.data.key;

    //    d3.selectAll("g")
    //        .selectAll("circle")
    //        .style("visibility ", function (dat, ind) {
    //            return (dat == d) ? "visible" : "hidden";
    //        });
    //
    //    clicked
    //        .on("click", function (d, i) {})
    //        .transition().duration(750)
    //        .attr("transform", "translate(" + (width * 0.5) + "," + (height * 0.5) + ")");
    //
    //    clicked
    //        .select("circle")
    //        .on("click", function (d, i) {})
    //        .on("mouseover", function (d, i) {})
    //        .on("mouseout", function (d, i) {})
    //        .attr("r", d.r)
    //        .transition().duration(750)
    //        .attr("fill", "#f9f9f9")
    //        .attr("r", width * 0.5);
    //
    //    d3.selectAll("text").remove();

    var eventjson = datajson.filter(function (d) {
        return d.event == event;
    });

    var nestedData = d3.nest()
        .key(function (d) {
            return d["headline"];
        })
        .rollup(function (d) {
            return d3.sum(d, function (d) {
                return d["views"];
            })
        })
        .entries(datajson.filter(function (d) {
            return d.event == event;
        }));

    data = {
        "name": "ted-talks",
        "children": nestedData
    };

    $("#chart").empty();

    root = d3.hierarchy(data)
        .sum(function (d) {
            return d.value
        });

    nodes = root.descendants();
    pack(root);

    var views = d3.max(eventjson, function (d) {
        return d.views;
    });

    color.domain([0, views]);

    var chart = d3.select("#chart")
        .attr("width", width)
        .attr("height", height);

    var node = chart.selectAll("g")
        .data(nodes);

    var g = node.enter()
        .append("g")
        .on("click", function (d, i) {
            console.log(d.data.value);
        })
        .attr("transform", function (d) {
            return "translate(" + d.x + "," + d.y + ")";
        });

    g.append("circle")
        .on("mouseover", function (d, i) {
            if (i == 0) return;
            d3.selectAll("circle")
                .transition().duration(200)
                .attr("stroke", function (dat, ind) {
                    if (ind == i) {
                        return "black";
                    }
                })
                .style("opacity", function (dat, ind) {
                    if (ind == i) {
                        return 1;
                    } else {
                        return 0.5;
                    }
                });

            var headline = d.data.key;

            var talkjson = datajson.filter(function (d) {
                return d.headline == headline;
            })[0];

            var title = "<a href='" + talkjson.url + "' target='_blank'>" + headline + "</a>";

            $("#talk-title").html(title);
            $("#talk-subtitle").text("");
            $("#talk-text").html(talkjson.transcript);
        })
        .on("mouseout", function (d, i) {
            d3.selectAll("circle")
                .transition().duration(200)
                .attr("stroke", "none")
                .style("opacity", 1);

            //            $("#talk-title").text("Description ");
            //            $("#talk-subtitle").text("");
            //            $("#talk-text").html("");
        })
        .attr('r', 0)
        .transition().duration(750)
        .attr("r", function (d) {
            return d.r;
        })
        .attr("fill", function (d) {
            if (d.data["key"] != null) {
                return color(d.data["value"]);
            } else {
                return "white";
            }
        });

    g.append("text")
        .text(function (d) {
            if (d.r > 70) {
                if (d.data.key) {
                    if (d.data.key.length < 14) return d.data.key;
                }
            }
        })
        .attr("font-size", function (d) {
            return Math.min(Math.max(d.r, 10), 24);
        });
}
