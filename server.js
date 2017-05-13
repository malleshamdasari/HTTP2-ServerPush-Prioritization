var http2 = require('http2');
var fs = require('fs');
var path = require('path');
var _ = require('lodash');
var config = require('config');

//Utility Functions
function readFile(path) {
  try {
    return fs.readFileSync(path);
  } catch (err) {
    return undefined;
  }
}

//Push Policies
var pushPolicies = {
  pushNothing: null,
  pushEverything: function(req, resp, dependencyList, push) {
    for (var dependency in dependencyList){
      console.log('Current dependency:', dependency);
      //var dependencyObj = 
      var priority2 = serverOptions.prioritization ? dependencyList[dependency].priority : null;
      console.log('Obj', dependencyList[dependency], 'P:', priority2);
      push(dependency, path.join(__dirname, server_path, dependency), priority2, function(err, fileName2) {
        //var fileName2 = dependency;
        if (err) {
          console.log(fileName2, 'not pushed');
        } else {
          console.log(fileName2, 'pushed');
        }
      });
    };
  }
};

//Create Server
function pushManager(request, response, dependencies, cb) {
  function pushFile(fileName, filePath, priority, cb) {
    var options = {
      path: fileName,
      'status': 200
    };
    var push = response.push(options, priority);
    var file = readFile(filePath);
    var err = null;
    if (file) {
      push.write(file);
      if (priority)
      	push.stream._priority = priority;
      console.log('Push Stream ID:', push.stream.id, 'Priority:', push.stream._priority);
    } else {
      err = new Error('Unable to open file');
    }

    return push.end(function() {
      if (cb) {
        cb(err, fileName);
      }
    });
  }

  if (cb) {
    cb(request, response, dependencies, pushFile);
  }
}

function onRequest(req, resp, options) {
  console.log('Requested URL:', req.url);
  var fileURL, file, dependencies, priority;
  
  switch (req.url) {
    case '/':
       req.url = '/index.html';
       if (options.prioritization)
  	 priority = 1;
       dependencies = options.dependencies;
       break;
    default:
       dependencies = null;
       if (options.prioritization)
         priority = (options.dependencies[req.url] && options.dependencies[req.url].priority) || 20;
       else
         priority = null;
       break;
  }
  fileName = path.join(server_path, req.url);
  file = readFile(path.join(__dirname, fileName));

  if (file) {
    resp.write(file);
    if (priority)
      resp.stream._priority = priority;
    console.log('Response Stream ID:', resp.stream.id, 'Priority:', priority);
    if (options.pushCallback && dependencies) {
      console.log('Server Push is enabled');
      pushManager(req, resp, dependencies, options.pushCallback);
    }
  } else {
    console.log('Resource not found');
  }
  resp.end();
}


//Add dependencies information
var dependenciesInfo = {
  '/cat3.jpg': {
    priority: 10
  },
  '/dummy.js': {
    priority: 5
  },
  '/static/lib/css/bootstrap.min.css':{
    priority:10
  },
  '/static/lib/css/keen-dashboards.css':{
    priority:10
  },
  '/static/lib/css/dc.css':{
    priority:10
  },
  '/static/css/custom.css':{
    priority:10
  },
  '/static/images/ScreePlot.png':{
    priority:10
  },
  '/static/images/ScatterPlot_Random.png':{
    priority:10
  },
  '/static/lib/js/jquery.min.js':{
    priority:10
  },
  '/static/lib/js/bootstrap.min.js':{
    priority:10
  },
  '/static/lib/js/crossfilter.js':{
    priority:10
  },
  '/static/lib/js/d3.js':{
    priority:10
  },
  '/static/lib/js/dc.js':{
    priority:10
  },
  '/static/lib/js/queue.js':{
    priority:10
  },
  '/static/lib/js/keen.min.js':{
    priority:10
  },
  '/static/js/graphs.js':{
    priority:10
  }
};


var serverOptions = {
  key: fs.readFileSync(path.join(__dirname, '/server.key')),
  cert: fs.readFileSync(path.join(__dirname, '/server.crt')),
  prioritization: (config.has('prioritization') && config.get('prioritization')) || false,
  pushCallback: pushPolicies[(config.has('serverPush.policy') && config.get('serverPush.policy')) || 'pushNothing'],
  dependencies: dependenciesInfo,
  port: (config.has('port') && config.get('port')) || 8080
};

var server_path = './alok_server';
//var server_path = './public';

var server = http2.createServer(serverOptions, function(request, response) {
  console.log(config.get('serverPush.policy'));
  return onRequest(request, response, serverOptions);
});
server.listen(serverOptions.port);
