const { Console } = require('console');


var appId = process.argv[2].trim();

someFile = 'data/raw/reviews/' + appId + '.json'

var fs = require('fs')
fs.readFile(someFile, 'utf8', function (err,data) {
  if (err) {
    return console.log(err);
  }
  var result = data.split('][').join(',')
  console.log(result)

  fs.writeFile(someFile, result, 'utf8', function (err) {
     if (err) return console.log(err);
  });
});
