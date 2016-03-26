var http = require('http');
var server = http.createServer().listen(8002);
var io = require('socket.io')(server);
var cookie_reader = require('cookie');
var querystring = require('querystring');
var redis = require('redis');

io.use(function(socket,accept){
    var data = socket.request;
    if(data.headers.cookie){
	data.cookie = cookie_reader.parse(data.headers.cookie);
	return accept(null, true);
    }
    return accept('error', false);
});

io.on('connection', function (socket) {

    // Redis client
    client = redis.createClient();

    // Subscribe to notification channel
    client.subscribe('notifications.' + socket.request.cookie['sessionid']);
    console.log('subscribed');
    
    //Grab message from Redis and send to client
    client.on('message', function(channel, message){
	console.log('on message', message);
        socket.send(message);
    });
    
    // Unsubscribe
    socket.on('disconnect', function() {
	client.unsubscribe('notifications.' + socket.request.cookie['sessionid']);
    });
});
