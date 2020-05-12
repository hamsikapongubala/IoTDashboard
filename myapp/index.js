const app = require('express')();
const bodyParser = require('body-parser');
const PORT = 3000;
const fetch = require('node-fetch');
const https = require('https');
const request = require('request');
var fs = require('fs');
let url = "";

let settings = { method: "Get" };
function saveImage(filename, data){
  var myBuffer = new Buffer(data.length);
  for (var i = 0; i < data.length; i++) {
      myBuffer[i] = data[i];
  }
  fs.writeFile(filename, myBuffer, function(err) {
      if(err) {
          console.log(err);
      } else {
          console.log("The file was saved!");
      }
  });
}

let options = {json: true};


request(url, options, (error, res, body) => {
    var jsonContent = JSON.parse(JSON.stringify(body));
    var data = jsonContent.Body.data;
    console.log(data);
    saveImage('doodle.png',data);
    if (error) {
        return  console.log(error)
    };

    if (!error && res.statusCode == 200) {
        // do something with JSON, using the 'body' variable
        console.log(error);
        
    };
});
// 




app.use(bodyParser.json());
const displayStatus = () => ({
  status: `OK`, });
app.get('/status', (req, res) => {
  res.status(200).send(displayStatus());
  //render(buff);
});
const server = app.listen(PORT, () =>
  console.log('Listening on ' +
    `http://localhost:${server.address().port}`));



