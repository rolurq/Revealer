(function() {

	// Don't emit events from inside of notes windows
	if ( window.location.search.match( /receiver/gi ) ) { return; }

	var multiplex = Reveal.getConfig().multiplex;

	var socket = io.connect( multiplex.url );

	function post() {

		socket.emit( 'state', Reveal.getState() );

	};

	// Monitor events that trigger a change in state
	Reveal.addEventListener( 'slidechanged', post );
	Reveal.addEventListener( 'fragmentshown', post );
	Reveal.addEventListener( 'fragmenthidden', post );
	Reveal.addEventListener( 'overviewhidden', post );
	Reveal.addEventListener( 'overviewshown', post );
	Reveal.addEventListener( 'paused', post );
	Reveal.addEventListener( 'resumed', post );

}());
