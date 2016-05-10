
var VERSION_NUMBER = 0.1;
function Server(url){
    this.url = url;
}
var res;

Server.prototype.remote_call = function(callback, language, _function, args){
    serialized_call = {
        'version': VERSION_NUMBER,
        'language': language,
        '_function': _function,
        'n_args': args.length - 2
    };

    for (var i = 1; i < args.length; i ++){
        serialized_call['arg' + (i-2)] = args[i];
    }

    var request = $.ajax({
      url: "/",
      type: "POST",
      dataType:'json',
      ContentType: 'application/json',
      data: JSON.stringify(serialized_call),
      success: function(response){
        var data = [];
        for(var key in response) {
            data.push(response[key]);
        }
        callback(data);
      }
    });
};

Server.prototype.python = function(callback, _function){
    return this.remote_call(callback, 'python', _function, arguments);
};

Server.prototype.r = function(callback, _function){
    return this.remote_call(callback, 'r', _function, arguments);
};


