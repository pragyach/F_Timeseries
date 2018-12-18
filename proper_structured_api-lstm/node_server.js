var expre = require('express')
var app = expre();
app.get('/',function(req,res){
	res.send('Pragya');

})
var server =  app.listen(8080, function(){
	console.log('server up')
})

app.get('/python', callName);
function callName(req,res)
{
	var spawn = require("child_process").spawn;
	var process = spawn('python',["./train_predict.py",req.query.firstname,req.query.lastn]);
	process.stdout.on('data',function(d){
		res.send(d.toString());
	})
}