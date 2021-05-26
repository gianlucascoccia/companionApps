var gplay = require('google-play-scraper');
var fs = require('fs')

var appId = process.argv[2].trim();
var page =  process.argv[3];
var input = {
              appId: appId,
              sort: gplay.sort.RATING,
              num: 100000000000
            };

gplay.reviews(input).then(function(apps){

  fs.writeFile("data/raw/reviews/" + appId + ".json", JSON.stringify(apps.data), (err)=>{
  if(err) {
      console.log(err)
      process.exit(1)
  }
   else {
      console.log(apps.data.length)
      process.exit()
   } 
})
  
}).catch(function(e){
  console.log('There was an error fetching the reviews!');
  console.log(e.message);
  process.exit(1)
});
