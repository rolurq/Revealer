(function() {
	var multiplex = Reveal.getConfig().multiplex;
	var socketId = multiplex.id;
	var socket = io.connect(multiplex.url, function(state) {
        Reveal.setState(state);
    });

	socket.on('statechanged', function(state) {
		Reveal.setState(state);
	});
}());
