console.log("app included");
var _addEndpoints;
var instance;
var idCount=2;

function addNode(index){
    idCount = idCount+1;
    console.log($('#selector'+index).find(":selected").text());
    console.log("flowchartWindow"+idCount);
    var new_item = '<div class="window jtk-node" '
                    +'id="flowchartWindow'+idCount+'">'+
                    '<strong>'+$('#selector'+index).find(":selected").text()+'</strong><br>'
                    +'<label style="display: none;">'+idCount+'-'+index+'-'
                    +$('#selector'+index).find(":selected").val()+'</label></div>'
    $("#canvas").append(new_item);
    _addEndpoints("Window"+idCount);
    instance.draggable(document.querySelectorAll(".flowchart-demo .window"), { grid: [20, 10] })
}

jsPlumb.ready(function () {

    instance = window.jsp = jsPlumb.getInstance({
        // default drag options
        DragOptions: { cursor: 'pointer', zIndex: 2000 },
        // the overlays to decorate each connection with.  note that the label overlay uses a function to generate the label text; in this
        // case it returns the 'labelText' member that we set on each connection in the 'init' method below.
        ConnectionOverlays: [
            [ "Arrow", {
                location: 1,
                visible:true,
                id:"ARROW",
                events:{
                    click:function() { alert("you clicked on the arrow overlay")}
                }
            } ],
            [ "Label", {
                location: 0.1,
                id: "label",
                cssClass: "aLabel",
                events:{
                }
            }]
        ],
        Container: "canvas"
    });

    var basicType = {
        connector: "StateMachine",
        paintStyle: { strokeStyle: "red", lineWidth: 4 },
        hoverPaintStyle: { strokeStyle: "blue" },
        overlays: [
            "Arrow"
        ]
    };
    instance.registerConnectionType("basic", basicType);

    // this is the paint style for the connecting lines..
    var connectorPaintStyle = {
            lineWidth: 4,
            strokeStyle: "#61B7CF",
            joinstyle: "round",
            outlineColor: "white",
            outlineWidth: 2
        },
    // .. and this is the hover style.
        connectorHoverStyle = {
            lineWidth: 6,
            strokeStyle: "#216477",
            outlineWidth: 2,
            outlineColor: "white"
        },
        endpointHoverStyle = {
            fillStyle: "yellow",
            strokeStyle: "black"
        },
    // the definition of source endpoints (the small blue ones)
        sourceEndpoint = {
            endpoint: "Dot",
            paintStyle: {
                strokeStyle: "#7AB02C",
                fillStyle: "transparent",
                radius: 3,
                lineWidth: 3
            },
            isSource: true,
            connector: [ "Flowchart", { stub: [40, 60], gap: 10, cornerRadius: 5, alwaysRespectStubs: true } ],
            connectorStyle: connectorPaintStyle,
            hoverPaintStyle: endpointHoverStyle,
            connectorHoverStyle: connectorHoverStyle,
            dragOptions: {},
            overlays: [
                [ "Label", {
                    location: [0.5, 1.5],
                    label: "Drag",
                    cssClass: "endpointSourceLabel",
                    visible:false
                } ]
            ]
        },
    // the definition of target endpoints (will appear when the user drags a connection)
        targetEndpoint = {
            endpoint: "Dot",
            paintStyle: { fillStyle: "#7AB02C", radius: 4 },
            hoverPaintStyle: endpointHoverStyle,
            maxConnections: -1,
            dropOptions: { hoverClass: "hover", activeClass: "active" },
            isTarget: true,
            overlays: [
                [ "Label", { location: [0.5, -0.5], label: "Drop", cssClass: "endpointTargetLabel", visible:false } ]
            ]
        },
        init = function (connection) {
            connection.getOverlay("label").setLabel(connection.sourceId.substring(15) + "-" + connection.targetId.substring(15));
        };

    var sourceAnchors = ["TopRight","TopLeft","BottomCenter","BottomLeft","BottomRight","LeftMiddle", "RightMiddle"];
    var targetAnchors = ["TopCenter"];

    _addEndpoints = function (toId) {
        for (var i = 0; i < sourceAnchors.length; i++) {
            var sourceUUID = toId + sourceAnchors[i];
            instance.addEndpoint("flowchart" + toId, sourceEndpoint, {
                anchor: sourceAnchors[i], uuid: sourceUUID
            });
        }
        for (var j = 0; j < targetAnchors.length; j++) {
            var targetUUID = toId + targetAnchors[j];
            instance.addEndpoint("flowchart" + toId, targetEndpoint, {
                anchor: targetAnchors[j], uuid: targetUUID });
        }
    };

    // suspend drawing and initialise.
    instance.batch(function () {

        instance.addEndpoint("flowchartWindow1",sourceEndpoint, {
                anchor: "BottomCenter", uuid: "Window1BottomCenter"
        });
        instance.addEndpoint("flowchartWindow1",sourceEndpoint, {
                anchor: "BottomLeft", uuid: "Window1BottomLeft"
        });
        instance.addEndpoint("flowchartWindow1",sourceEndpoint, {
                anchor: "BottomRight", uuid: "Window1BottomRight"
        });
        instance.addEndpoint("flowchartWindow2",targetEndpoint, {
                anchor: "TopCenter", uuid: "Window2TopCenter"
        });
        instance.draggable(jsPlumb.getSelector(".flowchart-demo .window"), { grid: [20, 20] });

        // listen for new connections; initialise them the same way we initialise the connections at startup.
        instance.bind("connection", function (connInfo, originalEvent) {
            init(connInfo.connection);
        });

        // make all the window divs draggable
        instance.draggable(jsPlumb.getSelector(".flowchart-demo .window"), { grid: [20, 20] });

        // listen for clicks on connections, and offer to delete connections on click.
        instance.bind("click", function (conn, originalEvent) {
           // if (confirm("Delete connection from " + conn.sourceId + " to " + conn.targetId + "?"))
             //   instance.detach(conn);
            conn.toggleType("basic");
        });

        instance.bind("dblclick", function (conn, originalEvent) {
           // if (confirm("Delete connection from " + conn.sourceId + " to " + conn.targetId + "?"))
             //   instance.detach(conn);
            instance.detach(conn);
        });

        instance.bind("connectionDrag", function (connection) {
            console.log("connection " + connection.id + " is being dragged. suspendedElement is ", connection.suspendedElement, " of type ", connection.suspendedElementType);
        });

        instance.bind("connectionDragStop", function (connection) {
            console.log("connection " + connection.id + " was dragged");
        });

        instance.bind("connectionMoved", function (params) {
            console.log("connection " + params.connection.id + " was moved");
        });
    });

    jsPlumb.fire("jsPlumbDemoLoaded", instance);

});
